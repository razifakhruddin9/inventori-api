def tentukan_saran(status, sisa_hari, sisa_stok, nama_produk="produk ini"):
    """
    Menentukan saran tindakan berdasarkan status risiko.

    Parameter:
    - status      : str, "hijau" / "kuning" / "merah"
    - sisa_hari   : int, berapa hari sampai kedaluwarsa
    - sisa_stok   : float/int, jumlah stok yang masih ada
    - nama_produk : str, nama produk (opsional, untuk pesan yang lebih jelas)

    Mengembalikan:
    - dict berisi saran (str) dan prioritas (1=rendah, 2=sedang, 3=tinggi)
    """

    # ── Kasus ganjil ───────────────────────────────────────────────────────
    if sisa_stok <= 0:
        return {
            "saran"    : "Stok sudah habis. Tidak ada tindakan diperlukan.",
            "prioritas": 1
        }

    if sisa_hari <= 0:
        return {
            "saran"    : f"SEGERA: {nama_produk} sudah kedaluwarsa. Pisahkan dari stok aktif.",
            "prioritas": 3
        }

    # ── Hijau: aman ────────────────────────────────────────────────────────
    if status == "hijau":
        return {
            "saran"    : "Stok aman. Tidak ada tindakan khusus diperlukan.",
            "prioritas": 1
        }

    # ── Kuning: perlu perhatian ────────────────────────────────────────────
    if status == "kuning":
        if sisa_hari <= 3:
            return {
                "saran"    : f"Sisa {sisa_hari} hari. Pindahkan {nama_produk} ke posisi depan (FEFO) dan pertimbangkan diskon kecil.",
                "prioritas": 2
            }
        else:
            return {
                "saran"    : f"Pantau {nama_produk}. Pertimbangkan bundling dengan produk lain untuk mempercepat penjualan.",
                "prioritas": 2
            }

    # ── Merah: risiko tinggi ───────────────────────────────────────────────
    if status == "merah":
        if sisa_hari <= 2:
            return {
                "saran"    : f"DARURAT: Sisa {sisa_hari} hari. Donasikan atau buang {nama_produk} jika tidak laku hari ini.",
                "prioritas": 3
            }
        elif sisa_hari <= 7:
            return {
                "saran"    : f"Diskon segera untuk {nama_produk}. Jika tidak laku dalam 2 hari, pertimbangkan donasi.",
                "prioritas": 3
            }
        else:
            return {
                "saran"    : f"Buat promo bundling untuk {nama_produk} dan pindahkan ke lokasi yang lebih terlihat.",
                "prioritas": 3
            }

    # ── Fallback: status tidak dikenal ─────────────────────────────────────
    return {
        "saran"    : "Status tidak dikenal. Periksa data batch.",
        "prioritas": 1
    }


# ── Uji coba langsung ──────────────────────────────────────────────────────
if __name__ == "__main__":

    kasus = [
        ("hijau",  15, 80,  "Tahu Sumedang"),
        ("kuning", 5,  60,  "Tempe Goreng"),
        ("kuning", 2,  40,  "Roti Tawar"),
        ("merah",  1,  50,  "Susu UHT"),
        ("merah",  4,  90,  "Yogurt Stroberi"),
        ("merah",  10, 100, "Keju Slice"),
        ("hijau",  10, 0,   "Produk Kosong"),
        ("merah",  -1, 30,  "Produk Expired"),
    ]

    for status, sisa_hari, sisa_stok, nama in kasus:
        hasil = tentukan_saran(status, sisa_hari, sisa_stok, nama)
        print(f"[{status.upper():6} | {sisa_hari:3} hari | stok {sisa_stok:3}] "
              f"Prioritas {hasil['prioritas']} → {hasil['saran']}")