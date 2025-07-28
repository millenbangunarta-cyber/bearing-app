# Mengimpor library yang diperlukan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone
import os
import io

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

# Judul Aplikasi
st.markdown("<h1 style='color: white;'>📈 Pencatatan Suhu Bearing</h1>", unsafe_allow_html=True)

# Input pengguna
nama_bearing = st.text_input('🔧 Nama Bearing')
suhu_bearing = st.number_input('🌡️ Suhu Bearing (°C)', min_value=-100, max_value=200)

# Tombol submit
if st.button('Submit'):
    if nama_bearing.strip() == "":
        st.warning("Nama bearing tidak boleh kosong.")
    else:
        result, chart = catat_data(nama_bearing, suhu_bearing)
        # result otomatis setelah submit
        st.success(result)
        st.image(chart)
        # Reset input otomatis setelah submit
        st.session_state.input_nama = ""
        st.session_state.input_suhu = 0

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
