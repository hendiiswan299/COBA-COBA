# app.py
import sys
import os

# Menambahkan direktori root proyek ke path Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# ---- Baru lakukan import modul Anda di bawahnya ----
import streamlit as st
from models.manajer_tugas import ManajerTugas
from models.tugas import Tugas, TugasPrioritas
import datetime

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Manajer Tugas Mahasiswa",
    page_icon="📚",
    layout="wide"
)

# --- Judul Aplikasi ---
st.title("📚 Manajemen Tugas Mahasiswa")
st.markdown("Aplikasi web sederhana untuk mengelola tugas kuliah Anda.")

# --- Manajemen State ---
# Menggunakan st.session_state untuk menyimpan instance ManajerTugas
# agar tidak dibuat ulang setiap kali ada interaksi.
if 'manajer' not in st.session_state:
    st.session_state.manajer = ManajerTugas(file_path='data/tugas.json')

manajer = st.session_state.manajer

# --- Sidebar untuk Menambah Tugas Baru ---
with st.sidebar:
    st.header("➕ Tambah Tugas Baru")
    with st.form("form_tambah_tugas", clear_on_submit=True):
        tipe_tugas = st.selectbox("Jenis Tugas", ["Tugas Biasa", "Tugas Prioritas"])
        judul = st.text_input("Judul Tugas")
        deskripsi = st.text_area("Deskripsi")
        # Menggunakan st.date_input untuk antarmuka kalender
        deadline = st.date_input("Deadline", min_value=datetime.date.today())
        
        prioritas = None
        if tipe_tugas == "Tugas Prioritas":
            prioritas = st.selectbox("Prioritas", ["Tinggi", "Sedang", "Rendah"])

        submitted = st.form_submit_button("Simpan Tugas")
        
        if submitted:
            if not judul:
                st.error("Judul tidak boleh kosong!")
            else:
                deadline_str = deadline.strftime("%d-%m-%Y")
                if tipe_tugas == "Tugas Prioritas":
                    tugas_baru = TugasPrioritas(judul, deskripsi, deadline_str, prioritas)
                else:
                    tugas_baru = Tugas(judul, deskripsi, deadline_str)
                
                manajer.tambah_tugas(tugas_baru)
                st.success("Tugas berhasil ditambahkan!")
                # Tidak perlu st.rerun() karena form_submit_button sudah memicu rerun

# --- Tampilan Daftar Tugas ---
st.header("📋 Daftar Tugas Anda")

if not manajer.daftar_tugas:
    st.info("Belum ada tugas yang tersimpan. Silakan tambahkan tugas baru melalui sidebar.")
else:
    # Mengurutkan tugas berdasarkan deadline terdekat
    manajer.daftar_tugas.sort(key=lambda x: x.deadline)
    
    for i, tugas in enumerate(manajer.daftar_tugas):
        status_emoji = "✅" if tugas.selesai else "⏳"
        
        with st.expander(f"{status_emoji} **{tugas.judul}** - Deadline: {tugas.deadline.strftime('%d %B %Y')}"):
            st.markdown(f"**Deskripsi:** {tugas.deskripsi}")
            
            # Menampilkan prioritas jika ada (memanfaatkan polimorfisme)
            if isinstance(tugas, TugasPrioritas):
                st.markdown(f"**Prioritas:** `{tugas.prioritas}`")
            
            # Kolom untuk tombol aksi
            col1, col2 = st.columns(2)

            with col1:
                # Tombol Selesai
                if not tugas.selesai:
                    if st.button("Tandai Selesai", key=f"selesai_{i}"):
                        manajer.tandai_tugas_selesai(i)
                        st.rerun() # Refresh halaman untuk update UI
            
            with col2:
                # Tombol Hapus
                if st.button("Hapus", key=f"hapus_{i}", type="primary"):
                    manajer.hapus_tugas(i)
                    st.rerun() # Refresh halaman untuk update UI
