# models/tugas.py

import datetime

class Tugas:
    """
    Class dasar untuk representasi sebuah tugas.
    """
    def __init__(self, judul, deskripsi, deadline_str):
        self.judul = judul
        self.deskripsi = deskripsi
        # Mengubah string 'DD-MM-YYYY' menjadi objek date
        self.deadline = datetime.datetime.strptime(deadline_str, "%d-%m-%Y").date()
        self.selesai = False

    def tandai_selesai(self):
        """Mengubah status tugas menjadi selesai."""
        self.selesai = True

    def tampilkan(self):
        """Menampilkan detail tugas."""
        status = "Selesai" if self.selesai else "Belum Selesai"
        return (f"Judul     : {self.judul}\n"
                f"Deadline  : {self.deadline.strftime('%d %B %Y')}\n"
                f"Status    : {status}\n"
                f"Deskripsi : {self.deskripsi}")

    def ke_dict(self):
        """Mengubah objek tugas menjadi dictionary untuk disimpan ke JSON."""
        return {
            "tipe": "Tugas",
            "judul": self.judul,
            "deskripsi": self.deskripsi,
            "deadline": self.deadline.strftime("%d-%m-%Y"),
            "selesai": self.selesai
        }


class TugasPrioritas(Tugas):
    """
    Class turunan untuk tugas yang memiliki tingkat prioritas.
    Ini adalah contoh dari INHERITANCE.
    """
    def __init__(self, judul, deskripsi, deadline_str, prioritas):
        super().__init__(judul, deskripsi, deadline_str)
        self.prioritas = prioritas  # Contoh: "Tinggi", "Sedang", "Rendah"

    # Contoh POLYMORPHISM (method overriding)
    def tampilkan(self):
        """Menampilkan detail tugas dengan tambahan prioritas."""
        detail_dasar = super().tampilkan()
        return f"{detail_dasar}\nPrioritas : {self.prioritas}"

    # Contoh POLYMORPHISM (method overriding)
    def ke_dict(self):
        """Menambah field prioritas saat konversi ke dictionary."""
        data = super().ke_dict()
        data["tipe"] = "TugasPrioritas"
        data["prioritas"] = self.prioritas
        return data