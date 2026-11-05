# API Inventori Pintar UMKM

API untuk menghitung skor risiko kedaluwarsa dan saran tindakan per batch produk.

## Endpoint

### POST /risiko
Input:
- batch_id, produk, sisa_stok, tanggal_kedaluwarsa, penjualan_14_hari

Output:
- skor_risiko (0-100), status (hijau/kuning/merah), perkiraan_terjual_sampai_exp, saran_tindakan, prioritas

## Asumsi
- Rata-rata penjualan dihitung dari data 14 hari terakhir
- Batas status: hijau ≤ 30, kuning 31-69, merah ≥ 70
- Batas saran kuning mendesak: sisa hari ≤ 3
- Batas saran merah darurat: sisa hari ≤ 2

## Catatan Data
Semua data yang digunakan untuk pengujian dan demonstrasi adalah DATA SIMULASI,
bukan data transaksi nyata.