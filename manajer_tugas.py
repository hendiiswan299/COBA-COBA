# models/manajer_tugas.py

import json
import os
from .tugas import Tugas, TugasPrioritas

class ManajerTugas:
    """
    Class untuk mengelola semua tugas, termasuk penyimpanan dan pemuatan data.
    """
    def __init__(self, file_path='data/tugas.json'):
        self.file_path = file_path
        self.daftar_tugas = []
        self._pastikan_direktori_data_ada()
        self.muat_tugas()

    def _pastikan_direktori_data_ada(self):
        """Memastikan direktori 'data' ada sebelum menulis file."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def tambah_tugas(self, tugas):
        """Menambahkan objek tugas baru ke dalam daftar."""
        self.daftar_tugas.append(tugas)
        self.simpan_tugas()
        print("\n✅ Tugas berhasil ditambahkan!")

    def lihat_semua_tugas(self):
        """Menampilkan semua tugas yang ada di daftar."""
        if not self.daftar_tugas:
            print("\nℹ️  Belum ada tugas yang tersimpan.")
            return

        # Mengurutkan tugas berdasarkan deadline
        self.daftar_tugas.sort(key=lambda x: x.deadline)
        
        print("\n--- Daftar Tugas Mahasiswa ---")
        for i, tugas in enumerate(self.daftar_tugas):
            print(f"\n--- TUGAS #{i+1} ---")
            # Ini adalah contoh polymorphism saat runtime.
            # Python secara otomatis akan memanggil method .tampilkan()
            # dari class yang sesuai (Tugas atau TugasPrioritas).
            print(tugas.tampilkan())
        print("\n------------------------------")

    def tandai_tugas_selesai(self, indeks):
        """Menandai tugas pada indeks tertentu sebagai selesai."""
        if 0 <= indeks < len(self.daftar_tugas):
            self.daftar_tugas[indeks].tandai_selesai()
            self.simpan_tugas()
            print(f"\n✅ Tugas #{indeks+1} telah ditandai selesai.")
        else:
            print("\n❌ Indeks tidak valid.")

    def hapus_tugas(self, indeks):
        """Menghapus tugas dari daftar berdasarkan indeks."""
        if 0 <= indeks < len(self.daftar_tugas):
            tugas_dihapus = self.daftar_tugas.pop(indeks)
            self.simpan_tugas()
            print(f"\n🗑️  Tugas '{tugas_dihapus.judul}' berhasil dihapus.")
        else:
            print("\n❌ Indeks tidak valid.")

    def simpan_tugas(self):
        """Menyimpan seluruh daftar tugas ke dalam file JSON."""
        # Mengubah setiap objek tugas menjadi dictionary
        data_untuk_disimpan = [tugas.ke_dict() for tugas in self.daftar_tugas]
        with open(self.file_path, 'w') as f:
            json.dump(data_untuk_disimpan, f, indent=4)

    def muat_tugas(self):
        """Memuat tugas dari file JSON saat aplikasi dimulai."""
        try:
            with open(self.file_path, 'r') as f:
                data_tugas = json.load(f)
                for item in data_tugas:
                    # Membuat objek yang sesuai berdasarkan 'tipe'
                    if item['tipe'] == 'TugasPrioritas':
                        tugas = TugasPrioritas(item['judul'], item['deskripsi'], item['deadline'], item['prioritas'])
                    else: # Default ke Tugas biasa
                        tugas = Tugas(item['judul'], item['deskripsi'], item['deadline'])
                    
                    if item['selesai']:
                        tugas.tandai_selesai()
                    self.daftar_tugas.append(tugas)
        except (FileNotFoundError, json.JSONDecodeError):
            # Jika file tidak ada atau kosong, mulai dengan daftar kosong
            self.daftar_tugas = []