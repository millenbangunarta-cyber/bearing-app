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
def catat_data(nama_bearing, suhu_bearing):
    # Gunakan zona waktu Kalimantan Timur (WITA)
    tz = timezone('Asia/Makassar')
    waktu_input = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # Validasi suhu
    if suhu_bearing > 100:
        validasi_suhu = "Warning: Suhu terlalu tinggi!"
    else:
        validasi_suhu = "Suhu normal."
    
    # Simpan data ke DataFrame
    data = pd.DataFrame([[waktu_input, nama_bearing, suhu_bearing, validasi_suhu]],
                        columns=["Waktu", "Nama Bearing", "Suhu Bearing", "Status"])

    # Simpan ke file CSV
    if os.path.exists("data_bearing.csv"):
        data.to_csv("data_bearing.csv", mode='a', header=False, index=False)
    else:
        data.to_csv("data_bearing.csv", index=False)

    # Membuat grafik suhu
    fig, ax = plt.subplots()
    df = pd.read_csv("data_bearing.csv")
    
    # Filter grafik berdasarkan nama bearing yang sama
    df = df[df["Nama Bearing"] == nama_bearing]
    
    ax.plot(pd.to_datetime(df["Waktu"]), df["Suhu Bearing"], marker='o', color='b', label="Suhu Bearing")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Suhu (°C)")
    ax.set_title(f"Tren Suhu Bearing: {nama_bearing}")
    ax.legend()

    # Simpan grafik ke BytesIO
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    
    return f"Data berhasil disimpan!\nWaktu: {waktu_input}\nBearing: {nama_bearing}\nSuhu: {suhu_bearing}°C\nStatus: {validasi_suhu}", buf

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
if "nama_bearing" not in st.session_state:
    st.session_state.nama_bearing = ""
if "suhu_bearing" not in st.session_state:
    st.session_state.suhu_bearing = 0
if "submit_result" not in st.session_state:
    st.session_state.submit_result = None
if "submit_chart" not in st.session_state:
    st.session_state.submit_chart = None
    
    
# Judul Aplikasi
st.markdown("<h1 style='color: white;'>📈 Pencatatan Suhu Bearing</h1>", unsafe_allow_html=True)

# Ambil daftar bearing untuk auto-complete
bearing_list = []
if os.path.exists("data_bearing.csv"):
    df_existing = pd.read_csv("data_bearing.csv")
    bearing_list = sorted(df_existing["Nama Bearing"].dropna().unique().tolist())

# Input nama bearing dengan selectbox + text_input
nama_terpilih = st.selectbox("🔧 Pilih Nama Bearing (Opsional)", options=[""] + bearing_list)
nama_manual = st.text_input("📝 Atau Tulis Nama Bearing Baru", value=st.session_state.nama_bearing)

# Final nama bearing yang akan digunakan
nama_bearing = nama_manual.strip() if nama_manual.strip() else nama_terpilih

# Auto-koreksi jika tidak persis dan mirip dengan data sebelumnya
if nama_bearing and nama_bearing not in bearing_list:
    terdekat = difflib.get_close_matches(nama_bearing, bearing_list, n=1)
    if terdekat:
        st.info(f"🔄 Koreksi otomatis: '{nama_bearing}' → '{terdekat[0]}'")
        nama_bearing = terdekat[0]


# Input pengguna
suhu_bearing = st.number_input('🌡️ Suhu Bearing (°C)', min_value=-100, max_value=200, value=st.session_state.suhu_bearing, key="suhu_bearing")

# Fungsi ketika tombol submit ditekan
def submit_callback():
    if st.session_state.nama_bearing.strip() == "":
        st.session_state.submit_result = "warning"
        st.session_state.submit_chart = None
    else:
        result, chart = catat_data(
            st.session_state.nama_bearing,
            st.session_state.suhu_bearing
        )
        st.session_state.submit_result = result
        st.session_state.submit_chart = chart

        # Reset input
        st.session_state.nama_bearing = ""
        st.session_state.suhu_bearing = 0

# Tombol submit
st.button("Submit", on_click=submit_callback)

# Tampilkan hasil jika ada
if st.session_state.submit_result:
    if st.session_state.submit_result == "warning":
        st.warning("Nama bearing tidak boleh kosong.")
    else:
        st.success(st.session_state.submit_result)
        if st.session_state.submit_chart:
            st.image(st.session_state.submit_chart)

# Tombol download CSV
if os.path.exists("data_bearing.csv"):
    with open("data_bearing.csv", "rb") as file:
        st.download_button(label="📥 Unduh Data CSV", data=file, file_name="data_bearing.csv")

# Footer / Copyright
st.markdown(
    """
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <div style="text-align: center; color: gray; font-size: small;">
        &copy; 2025 Aplikasi Pencatatan Suhu Bearing - Made with ❤️ by millen as a planner BEP
    </div>
    """,
    unsafe_allow_html=True
)
