from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List
from datetime import date

from skor_risiko import hitung_skor_risiko
from rekomendasi import tentukan_saran
from restock import hitung_restock
from riwayat import hitung_riwayat

# ── Inisialisasi aplikasi FastAPI ──────────────────────────────────────────
app = FastAPI(
    title="API Inventori Pintar UMKM",
    description="Menghitung skor risiko kedaluwarsa dan saran tindakan per batch.",
    version="1.0.0"
)

# ── CORS middleware ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Definisi bentuk data yang masuk (request) ──────────────────────────────
class BatchInput(BaseModel):
    batch_id             : str
    produk               : str
    sisa_stok            : float
    tanggal_kedaluwarsa  : str
    penjualan_14_hari    : List[float]

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


# ── Endpoint risiko ────────────────────────────────────────────────────────
@app.post("/risiko")
def hitung_risiko(data: BatchInput):
    hasil_skor = hitung_skor_risiko(
        sisa_stok           = data.sisa_stok,
        tanggal_kedaluwarsa = data.tanggal_kedaluwarsa,
        penjualan_14_hari   = data.penjualan_14_hari
    )
    hasil_saran = tentukan_saran(
        status      = hasil_skor["status"],
        sisa_hari   = hasil_skor["sisa_hari"],
        sisa_stok   = data.sisa_stok,
        nama_produk = data.produk
    )
    return {
        "batch_id"                     : data.batch_id,
        "produk"                       : data.produk,
        "skor_risiko"                  : hasil_skor["skor_risiko"],
        "status"                       : hasil_skor["status"],
        "perkiraan_terjual_sampai_exp" : hasil_skor["perkiraan_terjual"],
        "sisa_hari"                    : hasil_skor["sisa_hari"],
        "saran_tindakan"               : hasil_saran["saran"],
        "prioritas"                    : hasil_saran["prioritas"],
        "catatan"                      : hasil_skor.get("catatan", "")
    }


# ── Endpoint restock ───────────────────────────────────────────────────────
class RestockInput(BaseModel):
    produk            : str
    sisa_stok         : float
    penjualan_14_hari : List[float]
    hari_target       : int = 14

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
        if any(x < 0 for x in v):
            raise ValueError("Nilai penjualan tidak boleh negatif.")
        return v

    @field_validator("hari_target")
    @classmethod
    def hari_target_valid(cls, v):
        if v <= 0:
            raise ValueError("hari_target harus lebih dari 0.")
        return v


@app.post("/restock")
def prediksi_restock(data: RestockInput):
    hasil = hitung_restock(
        sisa_stok         = data.sisa_stok,
        penjualan_14_hari = data.penjualan_14_hari,
        hari_target       = data.hari_target
    )
    return {
        "produk"             : data.produk,
        "rata_rata_harian"   : hasil["rata_rata_harian"],
        "sisa_stok"          : data.sisa_stok,
        "estimasi_habis_hari": hasil["estimasi_habis_hari"],
        "saran_belanja"      : hasil["saran_belanja"],
        "catatan"            : hasil["catatan"]
    }


# ── Endpoint riwayat ───────────────────────────────────────────────────────
@app.get("/riwayat")
def get_riwayat(tahun: int = 2026):
    if tahun < 2000 or tahun > 2100:
        return {"error": "Tahun tidak valid."}
    return hitung_riwayat(tahun)


# ── Endpoint cek kesehatan ─────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "API berjalan", "versi": "1.0.0"}