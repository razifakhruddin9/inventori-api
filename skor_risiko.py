from datetime import date

def hitung_skor_risiko(sisa_stok, tanggal_kedaluwarsa, penjualan_14_hari):
    """
    Menghitung skor risiko kedaluwarsa untuk satu batch produk.

    Parameter:
    - sisa_stok           : int/float, jumlah stok yang masih ada
    - tanggal_kedaluwarsa : str, format "YYYY-MM-DD"
    - penjualan_14_hari   : list of float/int, angka penjualan 14 hari terakhir

    Mengembalikan:
    - dict berisi skor_risiko, status, perkiraan_terjual, sisa_hari
    """

    # ── 1. Hitung sisa hari sampai kedaluwarsa ──────────────────────────────
    hari_ini = date.today()
    tgl_exp  = date.fromisoformat(tanggal_kedaluwarsa)   # ubah string ke objek tanggal
    sisa_hari = (tgl_exp - hari_ini).days                # bisa negatif jika sudah lewat

    # ── 2. Kasus ganjil: produk sudah kedaluwarsa ──────────────────────────
    if sisa_hari <= 0:
        return {
            "skor_risiko"  : 100,
            "status"       : "merah",
            "perkiraan_terjual" : 0,
            "sisa_hari"    : sisa_hari,
            "catatan"      : "Produk sudah kedaluwarsa"
        }

    # ── 3. Kasus ganjil: stok kosong ───────────────────────────────────────
    if sisa_stok <= 0:
        return {
            "skor_risiko"  : 0,
            "status"       : "hijau",
            "perkiraan_terjual" : 0,
            "sisa_hari"    : sisa_hari,
            "catatan"      : "Stok sudah habis, tidak ada risiko terbuang."
        }

    # ── 4. Hitung rata-rata penjualan harian ───────────────────────────────
    if len(penjualan_14_hari) == 0 or sum(penjualan_14_hari) == 0:
        rata_rata_harian = 0.0
    else:
        rata_rata_harian = sum(penjualan_14_hari) / len(penjualan_14_hari)

    # ── 5. Perkiraan terjual sampai kedaluwarsa ─────────────────────────────
    perkiraan_terjual = rata_rata_harian * sisa_hari

    # ── 6. Hitung rasio risiko ──────────────────────────────────────────────
    # Rasio = berapa persen stok yang TIDAK akan terjual sebelum kedaluwarsa
    # Rasio 0   → semua stok diperkirakan terjual   → aman
    # Rasio 1   → tidak ada yang terjual sama sekali → sangat berbahaya
    stok_tidak_terjual = max(0, sisa_stok - perkiraan_terjual)
    rasio_risiko = stok_tidak_terjual / sisa_stok   # nilai antara 0.0 dan 1.0

    # ── 7. Ubah rasio menjadi skor 0-100 ───────────────────────────────────
    skor = round(rasio_risiko * 100)

    # ── 8. Tentukan status berdasarkan skor ────────────────────────────────
    if skor <= 30:
        status = "hijau"    # aman, tidak perlu tindakan
    elif skor <= 69:
        status = "kuning"   # perlu perhatian
    else:
        status = "merah"    # risiko tinggi, perlu tindakan segera

    return {
        "skor_risiko"       : skor,
        "status"            : status,
        "perkiraan_terjual" : round(perkiraan_terjual, 2),
        "sisa_hari"         : sisa_hari,
        "catatan"           : ""
    }


# ── Uji coba langsung ──────────────────────────────────────────────────────
if __name__ == "__main__":

    # Kasus 1: Normal, produk masih laku
    hasil = hitung_skor_risiko(
        sisa_stok=100,
        tanggal_kedaluwarsa="2026-11-20",
        penjualan_14_hari=[8, 7, 9, 6, 8, 7, 5, 8, 9, 7, 6, 8, 7, 8]
    )
    print("Kasus 1 (normal):", hasil)

    # Kasus 2: Produk hampir tidak laku
    hasil = hitung_skor_risiko(
        sisa_stok=100,
        tanggal_kedaluwarsa="2026-11-20",
        penjualan_14_hari=[1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
    )
    print("Kasus 2 (laku sedikit):", hasil)

    # Kasus 3: Produk sudah kedaluwarsa
    hasil = hitung_skor_risiko(
        sisa_stok=50,
        tanggal_kedaluwarsa="2026-10-01",
        penjualan_14_hari=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    )
    print("Kasus 3 (sudah exp):", hasil)

    # Kasus 4: Stok kosong
    hasil = hitung_skor_risiko(
        sisa_stok=0,
        tanggal_kedaluwarsa="2026-11-20",
        penjualan_14_hari=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    )
    print("Kasus 4 (stok kosong):", hasil)

    # Kasus 5: Penjualan semua nol
    hasil = hitung_skor_risiko(
        sisa_stok=80,
        tanggal_kedaluwarsa="2026-11-20",
        penjualan_14_hari=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    print("Kasus 5 (penjualan 0):", hasil)