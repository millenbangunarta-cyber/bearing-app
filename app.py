# Mengimpor library yang diperlukan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
from datetime import datetime
from pytz import timezone

# Fungsi untuk mencatat data bearing dan suhu, serta membuat grafik
def catat_data(nama_bearing, suhu_bearing):
    tz = timezone('Asia/Makassar')
    waktu_input = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # Validasi suhu (misalnya suhu tinggi lebih dari 100 derajat dianggap warning)
    if suhu_bearing > 60:
        validasi_suhu = "Warning: Suhu terlalu tinggi!"
    else:
        validasi_suhu = "Suhu normal."
    
    # Simpan data ke dalam DataFrame
    data = pd.DataFrame([[waktu_input, nama_bearing, suhu_bearing, validasi_suhu]], columns=["Waktu", "Nama Bearing", "Suhu Bearing", "Status"])

    # Jika file CSV sudah ada, tambahkan data baru, jika belum buat file baru
    if os.path.exists("data_bearing.csv"):
        data.to_csv("data_bearing.csv", mode='a', header=False, index=False)
    else:
        data.to_csv("data_bearing.csv", index=False)

    # Membuat grafik suhu
    fig, ax = plt.subplots()
    df = pd.read_csv("data_bearing.csv")
    ax.plot(pd.to_datetime(df["Waktu"]), df["Suhu Bearing"], marker='o', color='b', label="Suhu Bearing")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Suhu (°C)")
    ax.set_title(f"Tren Suhu Bearing {nama_bearing}")
    ax.legend()

    # Simpan grafik ke dalam format BytesIO untuk ditampilkan di Streamlit
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    
    return f"Data berhasil disimpan! Waktu: {waktu_input}, Bearing: {nama_bearing}, Suhu: {suhu_bearing}, Status: {validasi_suhu}", buf

# Streamlit App
st.title('Pencatatan Suhu Bearing')  # Judul Aplikasi

# Input untuk Nama Bearing dan Suhu Bearing
nama_bearing = st.text_input('Nama Bearing')  # Input untuk nama bearing
suhu_bearing = st.number_input('Suhu Bearing (°C)', min_value=-100, max_value=200)  # Input untuk suhu

# Tombol untuk mengirim data
if st.button('Submit'):
    result, chart = catat_data(nama_bearing, suhu_bearing)
    st.write(result)  # Menampilkan hasil input
    st.image(chart)  # Menampilkan grafik suhu

# Tombol untuk mengunduh Data CSV
if st.button('Unduh Data CSV'):
    with open("data_bearing.csv", "rb") as file:
        st.download_button(label="Download CSV", data=file, file_name="data_bearing.csv")


