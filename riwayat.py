def hitung_riwayat(tahun):
    """
    Menghasilkan data pembelian dan penjualan per bulan.
    Sumber: DATA SIMULASI

    Parameter:
    - tahun: int, tahun yang ingin ditampilkan

    Mengembalikan:
    - dict berisi data per bulan
    """

    import random
    random.seed(tahun)

    NAMA_BULAN = [
        "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
        "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
    ]

    data = []
    for i, bulan in enumerate(NAMA_BULAN):

        # Simulasi pembelian antara 300-500 unit per bulan
        pembelian = random.randint(300, 500)

        # Penjualan selalu sedikit lebih kecil dari pembelian
        # karena ada sisa stok yang tidak terjual
        penjualan = int(pembelian * random.uniform(0.80, 0.95))

        data.append({
            "bulan"    : bulan,
            "pembelian": pembelian,
            "penjualan": penjualan
        })

    return {
        "tahun"  : tahun,
        "data"   : data,
        "catatan": "DATA SIMULASI"
    }


# ── Uji coba langsung ──────────────────────────────────────────────────────
if __name__ == "__main__":
    hasil = hitung_riwayat(2026)
    print(f"Tahun: {hasil['tahun']}")
    print(f"Catatan: {hasil['catatan']}")
    print()
    for baris in hasil["data"]:
        print(f"{baris['bulan']}: pembelian {baris['pembelian']:4} | penjualan {baris['penjualan']:4}")