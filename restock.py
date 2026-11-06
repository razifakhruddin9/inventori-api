def hitung_restock(sisa_stok, penjualan_14_hari, hari_target=14):
    """
    Menghitung kebutuhan restock berdasarkan pola penjualan.

    Parameter:
    - sisa_stok        : float/int, stok yang masih ada sekarang
    - penjualan_14_hari: list of float/int, penjualan 14 hari terakhir
    - hari_target      : int, berapa hari ke depan yang ingin dicukupi (default 14)

    Mengembalikan:
    - dict berisi rata_rata_harian, estimasi_habis_hari, saran_belanja
    """

    # ── Kasus ganjil: stok kosong ──────────────────────────────────────────
    if sisa_stok < 0:
        sisa_stok = 0

    # ── Kasus ganjil: penjualan kosong atau semua nol ─────────────────────
    if len(penjualan_14_hari) == 0 or sum(penjualan_14_hari) == 0:
        return {
            "rata_rata_harian"   : 0.0,
            "estimasi_habis_hari": None,
            "saran_belanja"      : hari_target,
            "catatan"            : "Tidak ada data penjualan. Saran belanja = kebutuhan penuh."
        }

    # ── Hitung rata-rata harian ────────────────────────────────────────────
    rata_rata_harian = sum(penjualan_14_hari) / len(penjualan_14_hari)

    # ── Estimasi berapa hari stok sekarang bertahan ────────────────────────
    estimasi_habis_hari = round(sisa_stok / rata_rata_harian, 1)

    # ── Hitung kebutuhan dan saran belanja ─────────────────────────────────
    kebutuhan     = rata_rata_harian * hari_target
    saran_belanja = max(0, round(kebutuhan - sisa_stok))

    # ── Kasus: stok masih cukup ────────────────────────────────────────────
    if saran_belanja == 0:
        catatan = "Stok masih cukup untuk periode target."
    else:
        catatan = ""

    return {
        "rata_rata_harian"   : round(rata_rata_harian, 1),
        "estimasi_habis_hari": estimasi_habis_hari,
        "saran_belanja"      : saran_belanja,
        "catatan"            : catatan
    }


# ── Uji coba langsung ──────────────────────────────────────────────────────
if __name__ == "__main__":

    # Kasus 1: Normal, stok hampir habis (kasus Susu UHT dari tampilan Orang B)
    hasil = hitung_restock(
        sisa_stok=10,
        penjualan_14_hari=[15,15,14,16,15,15,14,15,16,15,14,15,15,16],
        hari_target=14
    )
    print("Kasus 1 (hampir habis):", hasil)

    # Kasus 2: Stok masih banyak, tidak perlu beli
    hasil = hitung_restock(
        sisa_stok=500,
        penjualan_14_hari=[8,7,9,6,8,7,5,8,9,7,6,8,7,8],
        hari_target=14
    )
    print("Kasus 2 (stok cukup):", hasil)

    # Kasus 3: Penjualan semua nol
    hasil = hitung_restock(
        sisa_stok=50,
        penjualan_14_hari=[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        hari_target=14
    )
    print("Kasus 3 (penjualan nol):", hasil)

    # Kasus 4: Stok nol
    hasil = hitung_restock(
        sisa_stok=0,
        penjualan_14_hari=[10,10,10,10,10,10,10,10,10,10,10,10,10,10],
        hari_target=14
    )
    print("Kasus 4 (stok nol):", hasil)