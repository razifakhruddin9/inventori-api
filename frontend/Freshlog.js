/* ========================================== */
/* 1. NAVIGASI HALAMAN (SINGLE PAGE APP)      */
/* ========================================== */
document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-menu a");
  const sections = document.querySelectorAll(".main-content .section");

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      // Ambil ID target dari atribut href (contoh: #produk -> produk)
      const targetId = this.getAttribute("href").substring(1);

      // Sembunyikan semua section
      sections.forEach((section) => {
        section.style.display = "none";
      });

      // Tampilkan section yang dipilih
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.style.display = "block";
        
        // JIKA USER MEMBUKA HALAMAN INVENTARIS, OTOMATIS AMBIL DATA DARI BACKEND PYTHON
        if (targetId === "inventaris" || targetId === "produk") {
            loadInventarisDariServer();
        }
      }

      // Perbarui status kelas active pada menu navigasi
      navLinks.forEach((nav) => nav.classList.remove("active"));
      this.classList.add("active");

      // Otomatis tutup sidebar jika berada di layar seluler (HP)
      const sidebar = document.getElementById("sidebar");
      if (sidebar.classList.contains("active")) {
        sidebar.classList.remove("active");
      }
    });
  });

  // Secara default, tampilkan section Dashboard saja saat pertama kali dimuat
  sections.forEach((section) => (section.style.display = "none"));
  const defaultDashboard = document.getElementById("dashboard");
  if (defaultDashboard) {
    defaultDashboard.style.display = "block";
  }
  
  // Panggil data pertama kali saat web dibuka
  loadInventarisDariServer();
});

/* ========================================== */
/* 2. MENU HAMBURGER (RESPONSIF HP)           */
/* ========================================== */
const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");

if (menuToggle && sidebar) {
menuToggle.addEventListener("click", function () {
  sidebar.classList.toggle("active");
});
}

/* ========================================== */
/* 3. POP-UP MODAL (OPEN & CLOSE)             */
/* ========================================== */
function openModal(modalId) {
const modal = document.getElementById(modalId);
if (modal) {
  modal.style.display = "flex";
}
}

function closeModal(modalId) {
const modal = document.getElementById(modalId);
if (modal) {
  modal.style.display = "none";
}
}

// Tutup modal jika pengguna mengklik area luar kotak modal
window.addEventListener("click", function (event) {
const modals = document.querySelectorAll(".modal");
modals.forEach((modal) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});
});

/* ========================================== */
/* 4. SIMULASI KASIR (AUTOMATIC SCANNING)     */
/* ========================================== */
const barcodeInput = document.getElementById("barcode-scanner");
const cartItemsTable = document.getElementById("cart-items");

if (barcodeInput && cartItemsTable) {
// Simulasi database produk dummy
const productDatabase = {
  "899123456789": { name: "Susu UHT 1L", price: 18000 },
  "899999900001": { name: "Roti Tawar Daging", price: 12500 },
};

barcodeInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    const code = this.value.trim();

    if (productDatabase[code]) {
      const item = productDatabase[code];

      // Tambah baris baru ke tabel keranjang belanja
      const newRow = document.createElement("tr");
      newRow.innerHTML = `
        <td>${item.name}</td>
        <td>1</td>
        <td>Rp ${item.price.toLocaleString("id-ID")}</td>
        <td>Rp ${item.price.toLocaleString("id-ID")}</td>
        <td><button class="btn btn-sm btn-delete" onclick="removeItem(this)">✕</button></td>
      `;
      cartItemsTable.appendChild(newRow);

      // Bersihkan kolom input scanner setelah berhasil discan
      this.value = "";
    } else if (code !== "") {
      alert("Barcode produk tidak ditemukan dalam database!");
      this.value = "";
    }
  }
});
}

// Fungsi menghapus item dari keranjang kasir
function removeItem(button) {
const row = button.closest("tr");
if (row) {
  row.remove();
}
}

/* ========================================== */
/* 5. KONEKSI KONTROLER BACKEND PYTHON        */
/* ========================================== */
function loadInventarisDariServer() {
// Arahkan ke URL port Python Flask Anda (misal http://localhost:5000) jika berbeda port
fetch('http://localhost:5000/api/inventaris')
    .then(response => {
        if (!response.ok) throw new Error("Gagal mengambil data dari server");
        return response.json();
    })
    .then(data => {
        const tbody = document.querySelector("#table-inventaris tbody");
        if (tbody) {
            tbody.innerHTML = "";
            data.forEach(batch => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${batch.code}</strong></td>
                    <td>${batch.name}</td>
                    <td>${batch.category}</td>
                    <td>${batch.stock} Pcs</td>
                    <td>${batch.expiry_date}</td>
                    <td><span class="status-badge ${batch.risiko.color}">${batch.risiko.status}</span></td>
                    <td><select class="form-select"><option>${batch.risiko.saran}</option></select></td>
                    <td><button class="btn btn-sm btn-primary">Ubah</button></td>
                `;
                tbody.appendChild(tr);
            });
        }
    })
    .catch(error => console.error("Error koneksi Python:", error));
}
