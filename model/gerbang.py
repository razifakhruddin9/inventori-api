from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List
from datetime import date

# ── IMPORT MODUL PYTHON ANDA ───────────────────────────────────────────────
# Pastikan ke-4 file ini berada dalam folder yang sama dengan main.py
try:
    from skor_risiko import hitung_skor_risiko
    from rekomendasi import tentukan_saran
    from restock import hitung_restock
    from riwayat import hitung_riwayat
except ImportError as e:
    # Fallback / Placeholder jika file modul belum Anda buat agar server tidak crash
    print(f"Peringatan: {e}. Menggunakan fungsi simulasi internal.")
    def hitung_skor_risiko(**kwargs): 
        return {"skor_risiko": 45, "status": "hitam", "perkiraan_terjual": 12, "sisa_hari": 12, "catatan": "Simulasi"}
    def tentukan_saran(**kwargs): 
        return {"saran": "Diskon 50% / Segera Salurkan Donasi", "prioritas": 3}
    def hitung_restock(**kwargs): 
        return {"rata_rata_harian": 4.5, "estimasi_habis_hari": 5, "saran_belanja": 35, "catatan": "Simulasi"}
    def hitung_riwayat(tahun): 
        return {"pembelian":, "penjualan":}

# ── INISIALISASI FASTAPI ───────────────────────────────────────────────────
app = FastAPI(
    title="API Inventori Pintar FreshLog",
    description="Backend Python penghubung modul analisis FEFO & Restock",
    version="1.0.0"
)

# ── KONFIGURASI MENDESAK: CORS MIDDLEWARE (AGAR BISA DITEMBAK OLEH JS) ──────
# Ini yang membuat JavaScript browser diizinkan mengakses data dari server Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua domain/browser mengakses API
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# ── MODEL DATA INPUT (SKEMA PYDANTIC) ──────────────────────────────────────

class BatchInput(BaseModel):
    batch_id: str
    produk: str
    sisa_stok: float
    tanggal_kedaluwarsa: str
    penjualan_14_hari: List[float]

    @field_validator("sisa_stok")
    @classmethod
    def stok_tidak_negatif(cls, v):
        if v < 0:
            raise ValueError("sisa_stok tidak boleh negatif.")
        return v

    @field_validator("tanggal_kedaluwarsa")
    @classmethod
    def format_tanggal_valid(cls, v):
        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError("tanggal_kedaluwarsa harus format YYYY-MM-DD")
        return v

    @field_validator("penjualan_14_hari")
    @classmethod
    def penjualan_tidak_kosong(cls, v):
        if len(v) == 0:
            raise ValueError("penjualan_14_hari tidak boleh daftar kosong.")
        if any(x < 0 for x in v):
            raise ValueError("Nilai penjualan tidak boleh negatif.")
        return v

class RestockInput(BaseModel):
    produk: str
    sisa_stok: float
    penjualan_14_hari: List[float]
    hari_target: int = 14

    @field_validator("sisa_stok")
    @classmethod
    def stok_tidak_negatif(cls, v):
        if v < 0:
            raise ValueError("sisa_stok tidak boleh negatif.")
        return v

    @field_validator("penjualan_14_hari")
    @classmethod
    def penjualan_tidak_kosong(cls, v):
        if len(v) == 0:
            raise ValueError("penjualan_14_hari tidak boleh daftar kosong.")
        return v

# ── ENDPOINTS API YANG MENYAMBUNG LANGSUNG KE JAVASCRIPT ─────────────────────

@app.get("/")
def root():
    return {"status": "API FreshLog Berjalan Lancar", "versi": "1.0.0"}

# 1. MENYAMBUNG KE: loadInventarisDariServer() di JS
@app.post("/risiko")
def api_hitung_risiko(data: BatchInput):
    # Memanggil logika dari skor_risiko.py
    hasil_skor = hitung_skor_risiko(
        sisa_stok=data.sisa_stok,
        tanggal_kedaluwarsa=data.tanggal_kedaluwarsa,
        penjualan_14_hari=data.penjualan_14_hari
    )

    # Memanggil logika dari rekomendasi.py
    hasil_saran = tentukan_saran(
        status=hasil_skor["status"],
        sisa_hari=hasil_skor["sisa_hari"],
        sisa_stok=data.sisa_stok,
        nama_produk=data.produk
    )

    return {
        "batch_id": data.batch_id,
        "produk": data.produk,
        "skor_risiko": hasil_skor["skor_risiko"],
        "status": hasil_skor["status"],
        "perkiraan_terjual_sampai_exp": hasil_skor["perkiraan_terjual"],
        "sisa_hari": hasil_skor["sisa_hari"],
        "saran_tindakan": hasil_saran["saran"],
        "prioritas": hasil_saran["prioritas"],
        "catatan": hasil_skor.get("catatan", "")
    }

# 2. MENYAMBUNG KE: loadPrediksiRestockDariServer() di JS
@app.post("/restock")
def api_prediksi_restock(data: RestockInput):
    # Memanggil logika dari restock.py
    hasil = hitung_restock(
        sisa_stok=data.sisa_stok,
        penjualan_14_hari=data.penjualan_14_hari,
        hari_target=data.hari_target
    )

    return {
        "produk": data.produk,
        "rata_rata_harian": hasil["rata_rata_harian"],
        "sisa_stok": data.sisa_stok,
        "estimasi_habis_hari": hasil["estimasi_habis_hari"],
        "saran_belanja": hasil["saran_belanja"],
        "catatan": hasil["catatan"]
    }

# 3. MENYAMBUNG KE: loadRiwayatGrafikDariServer() di JS
@app.get("/riwayat")
def api_get_riwayat(tahun: int = 2026):
    if tahun < 2000 or tahun > 2100:
        raise HTTPException(status_code=400, detail="Tahun tidak valid.")
        
    # Memanggil logika dari riwayat.py untuk grafik Chart.js
    hasil = hitung_riwayat(tahun)
    return hasil

# ── CARA MENJALANKANNYA ──────────────────────────────────────────────────────
# Tulis perintah berikut di terminal komputer Anda:
# pip install fastapi uvicorn
# uvicorn main:app --reload --port 8000
