# Mengimpor library yang diperlukan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone
import os
import io
import difflib

# Fungsi untuk mencatat data bearing dan suhu, serta membuat grafik
def catat_data(nama_part, suhu_part):
    # Gunakan zona waktu Kalimantan Timur (WITA)
    tz = timezone('Asia/Makassar')
    waktu_input = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # Validasi suhu
    if suhu_part > 100:
        validasi_suhu = "Warning: Suhu terlalu tinggi!"
    else:
        validasi_suhu = "Suhu normal."
    
    # Simpan data ke DataFrame
    data = pd.DataFrame([[waktu_input, nama_part, suhu_part, validasi_suhu]],
                        columns=["Waktu", "Nama part", "Suhu part", "Status"])

    # Simpan ke file CSV
    if os.path.exists("data_suhu.csv"):
        data.to_csv("data_part.csv", mode='a', header=False, index=False)
    else:
        data.to_csv("data_part.csv", index=False)

    # Membuat grafik suhu
    fig, ax = plt.subplots()
    df = pd.read_csv("data_part.csv")
    
    # Filter grafik berdasarkan nama bearing yang sama
    df = df[df["Nama Part"] == nama_part]
    
    ax.plot(pd.to_datetime(df["Waktu"]), df["Suhu Part"], marker='o', color='b', label="Suhu Part")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Suhu (°C)")
    ax.set_title(f"Tren Suhu Part: {nama_part}")
    ax.legend()

    # Simpan grafik ke BytesIO
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    
    return f"Data berhasil disimpan!\nWaktu: {waktu_input}\nPart: {nama_part}\nSuhu: {suhu_part}°C\nStatus: {validasi_suhu}", buf

# --- Streamlit App ---

# Tambahkan styling background
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
            url("https://raw.githubusercontent.com/millenbangunarta-cyber/bearing-app/main/IMG_1714.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
       label {
        color: white !important;  /* Ganti warna teks input di sini */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --- INISIALISASI SESSION STATE ---
if "nama_part" not in st.session_state:
    st.session_state.nama_part = ""
if "suhu_part" not in st.session_state:
    st.session_state.suhu_part = 0
if "submit_result" not in st.session_state:
    st.session_state.submit_result = None
if "submit_chart" not in st.session_state:
    st.session_state.submit_chart = None
    
    
# Judul Aplikasi
st.markdown("<h1 style='color: white;'>📈 Pencatatan Suhu Part</h1>", unsafe_allow_html=True)

# Ambil daftar nama bearing dari file CSV (jika ada)
bearing_list = []
if os.path.exists("data_part.csv"):
    df_all = pd.read_csv("data_part.csv")
    part_list = sorted(df_all["Nama Part"].dropna().unique().tolist())

# Input manual dari pengguna
input_nama_part = st.text_input('🔧 Nama Part', value=st.session_state.nama_part, key="nama_part")

# Koreksi ejaan otomatis
nama_part = input_nama_part.strip()
nama_part_final = nama_part  # default tanpa koreksi

if nama_part:
    match = difflib.get_close_matches(nama_part, part_list, n=1, cutoff=0.8)
    if match:
        corrected = match[0]
        if corrected.lower() != nama_part.lower():
            st.info(f"Nama part dikoreksi menjadi: **{corrected}**")
            nama_part_final = corrected

# Input pengguna
suhu_part = st.number_input('🌡️ Suhu Part (°C)', min_value=-100, max_value=200, value=st.session_state.suhu_part, key="suhu_part")

# Fungsi ketika tombol submit ditekan
def submit_callback():
    if st.session_state.nama_part.strip() == "":
        st.session_state.submit_result = "warning"
        st.session_state.submit_chart = None
    else:
        result, chart = catat_data(
        nama_part_final,
        st.session_state.suhu_part
        )

        st.session_state.submit_result = result
        st.session_state.submit_chart = chart

        # Reset input
        st.session_state.nama_part = ""
        st.session_state.suhu_part = 0

# Tombol submit
st.button("Submit", on_click=submit_callback)

# Tampilkan hasil jika ada
if st.session_state.submit_result:
    if st.session_state.submit_result == "warning":
        st.warning("Nama part tidak boleh kosong.")
    else:
        st.success(st.session_state.submit_result)
        if st.session_state.submit_chart:
            st.image(st.session_state.submit_chart)

# Tombol download CSV
if os.path.exists("data_part.csv"):
    with open("data_part.csv", "rb") as file:
        st.download_button(label="📥 Unduh Data CSV", data=file, file_name="data_part.csv")

# Footer / Copyright
st.markdown(
    """
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <div style="text-align: center; color: gray; font-size: small;">
        &copy; 2025 Aplikasi Pencatatan Suhu Part - Made with ❤️ by millen as a planner BEP
    </div>
    """,
    unsafe_allow_html=True
)
