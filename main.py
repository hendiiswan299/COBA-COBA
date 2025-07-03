# main.py

from models.manajer_tugas import ManajerTugas
from models.tugas import Tugas, TugasPrioritas

def tampilkan_menu():
    """Menampilkan menu utama aplikasi."""
    print("\n===== APLIKASI MANAJEMEN TUGAS MAHASISWA =====")
    print("1. Tambah Tugas Biasa")
    print("2. Tambah Tugas Prioritas")
    print("3. Lihat Semua Tugas")
    print("4. Tandai Tugas Selesai")
    print("5. Hapus Tugas")
    print("6. Keluar")
    print("==============================================")
    return input("Pilih menu (1-6): ")

def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    manajer = ManajerTugas()

    while True:
        pilihan = tampilkan_menu()

        if pilihan == '1':
            print("\n--- Menambah Tugas Biasa ---")
            judul = input("Judul Tugas: ")
            deskripsi = input("Deskripsi: ")
            deadline = input("Deadline (DD-MM-YYYY): ")
            tugas_baru = Tugas(judul, deskripsi, deadline)
            manajer.tambah_tugas(tugas_baru)

        elif pilihan == '2':
            print("\n--- Menambah Tugas Prioritas ---")
            judul = input("Judul Tugas: ")
            deskripsi = input("Deskripsi: ")
            deadline = input("Deadline (DD-MM-YYYY): ")
            prioritas = input("Prioritas (Tinggi/Sedang/Rendah): ")
            tugas_baru = TugasPrioritas(judul, deskripsi, deadline, prioritas)
            manajer.tambah_tugas(tugas_baru)

        elif pilihan == '3':
            manajer.lihat_semua_tugas()

        elif pilihan == '4':
            manajer.lihat_semua_tugas()
            try:
                indeks = int(input("\nMasukkan nomor tugas yang ingin ditandai selesai: ")) - 1
                manajer.tandai_tugas_selesai(indeks)
            except ValueError:
                print("❌ Input harus berupa angka.")


        elif pilihan == '5':
            manajer.lihat_semua_tugas()
            try:
                indeks = int(input("\nMasukkan nomor tugas yang ingin dihapus: ")) - 1
                manajer.hapus_tugas(indeks)
            except ValueError:
                print("❌ Input harus berupa angka.")

        elif pilihan == '6':
            print("\nTerima kasih telah menggunakan aplikasi. Data tersimpan.")
            break

        else:
            print("\n❌ Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()