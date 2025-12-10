import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date, datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from io import BytesIO
import base64

# === FIX: Fungsi rerun kompatibel untuk semua versi ===
def main():
    """Reruns the current Streamlit app."""
    pass
if hasattr(st, "rerun"):
st.rerun()
else:
st.experimental_rerun()

# ===================== LOGIN MANUAL (Menggunakan Secrets) =====================

# Ambil kredensial dari secrets.toml
try:
USER_CREDENTIALS = st.secrets["credentials"]
except KeyError:
st.error("❌ Konfigurasi Error: File .streamlit/secrets.toml tidak ditemukan atau kredensial kosong.")
st.stop()
except Exception:
USER_CREDENTIALS = {}

# Initialize session state
if "logged_in" not in st.session_state:
st.session_state.logged_in = False
if "username" not in st.session_state:
st.session_state.username = ""
if "menu_choice" not in st.session_state:
st.session_state.menu_choice = "📊 Keuangan" 
if "submenu_choice" not in st.session_state:
st.session_state.submenu_choice = "📝 Tambah Data Siswa"
if "submenu_guru_choice" not in st.session_state:
st.session_state.submenu_guru_choice = "👨‍🏫 Tambah Data Guru & Karyawan"

if not st.session_state.logged_in:
st.title("🔐 Login Aplikasi")
st.markdown("Gunakan username developer_keuangan dan password pass123")

with st.form("login_form"):
username = st.text_input("👤 Username")
password = st.text_input("🔑 Password", type="password")
login_btn = st.form_submit_button("Login")

if login_btn:
if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
st.session_state.logged_in = True
st.session_state.username = username
st.success("✅ Login berhasil!")
rerun()
else:
st.error("❌ Username atau password salah.")
else:
# ===================== APLIKASI UTAMA =====================
with st.sidebar:
st.markdown(f"👋 Halo, *{st.session_state.username}*")
st.divider() 

# Menu utama - gunakan callback untuk update session state
def update_menu_choice():
st.session_state.menu_choice = st.session_state.sidebar_menu_widget

pilihan = st.radio(
"Pilih Menu:", 
["📊 Keuangan", "🎓 Data Siswa", "👨‍🏫 Data Guru & Karyawan"], 
key="sidebar_menu_widget",
on_change=update_menu_choice
)

# Submenu untuk Data Siswa
if pilihan == "🎓 Data Siswa":
st.divider()
st.markdown("📚 Kelola Data Siswa:")

def update_submenu_choice():
st.session_state.submenu_choice = st.session_state.submenu_widget

submenu = st.radio(
"Pilih Submenu:",
["📝 Tambah Data Siswa", "🎨 Data TK", "📚 Data SD", "🎓 Data SMP", "👥 Semua Siswa", "📄 Cetak Laporan"],
key="submenu_widget",
on_change=update_submenu_choice
)

# Submenu untuk Data Guru & Karyawan
elif pilihan == "👨‍🏫 Data Guru & Karyawan":
st.divider()
st.markdown("👨‍🏫 Kelola Data Guru & Karyawan:")

def update_submenu_guru_choice():
st.session_state.submenu_guru_choice = st.session_state.submenu_guru_widget

submenu_guru = st.radio(
"Pilih Submenu:",
["👨‍🏫 Tambah Data Guru & Karyawan", "📋 Data Guru", "👨‍💼 Data Karyawan", "👥 Semua Data"],
key="submenu_guru_widget",
on_change=update_submenu_guru_choice
)

st.divider()

if st.button("🚪 Keluar", type="primary", use_container_width=True):
st.session_state.logged_in = False
st.session_state.username = ""
st.session_state.menu_choice = "📊 Keuangan" 
st.session_state.submenu_choice = "📝 Tambah Data Siswa"
st.session_state.submenu_guru_choice = "👨‍🏫 Tambah Data Guru & Karyawan"
rerun()

st.title("📚 Aplikasi Manajemen Data & Keuangan")

pilihan_aktif = st.session_state.menu_choice 

# ==================== MENU KEUANGAN (MODIFIKASI) ====================
if pilihan_aktif == "📊 Keuangan":
# File paths
FILE_PATH = "transaksi_keuangan.xlsx"
FILE_SISWA = "data_siswa.xlsx"
FILE_SPP = "pembayaran_spp.xlsx"

# Load data functions
@st.cache_data
def load_data():
if os.path.exists(FILE_PATH):
df = pd.read_excel(FILE_PATH)
df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date
return df
else:
return pd.DataFrame(columns=["Tanggal", "Kategori", "Jumlah", "Jenis", "Deskripsi", "Tipe_Keuangan"])

@st.cache_data
def load_siswa():
if os.path.exists(FILE_SISWA):
df = pd.read_excel(FILE_SISWA)
return df
else:
columns = [
"Nama Lengkap", "Tempat Lahir", "Tanggal Lahir", "Jenis Kelamin", "Jenjang Sekolah", 
"Kelas", "NIS", "NISN", "Golongan Darah", "Agama", "No HP/WA", "Sosial Media", 
"Alamat Domisili", "Alamat KTP", "NIK", "Tanggal Terdaftar", "Sekolah Asal", "Foto",
"Nama Ayah", "Tempat Lahir Ayah", "Tanggal Lahir Ayah", "Agama Ayah", "Pekerjaan Ayah",
"Golongan Darah Ayah", "No HP/WA Ayah", "Sosial Media Ayah", "Alamat Domisili Ayah",
"Alamat KTP Ayah", "NIK Ayah", "No KK Ayah",
"Nama Ibu", "Tempat Lahir Ibu", "Tanggal Lahir Ibu", "Agama Ibu", "Pekerjaan Ibu",
"Golongan Darah Ibu", "No HP/WA Ibu", "Sosial Media Ibu", "Alamat Domisili Ibu",
"Alamat KTP Ibu", "NIK Ibu", "No KK Ibu",
"Nama Wali", "Tempat Lahir Wali", "Tanggal Lahir Wali", "Agama Wali", "Pekerjaan Wali",
"Golongan Darah Wali", "No HP/WA Wali", "Sosial Media Wali", "Alamat Domisili Wali",
"Alamat KTP Wali", "NIK Wali", "No KK Wali"
]
return pd.DataFrame(columns=columns)

@st.cache_data
def load_spp():
if os.path.exists(FILE_SPP):
df = pd.read_excel(FILE_SPP)
df['Tanggal_Bayar'] = pd.to_datetime(df['Tanggal_Bayar']).dt.date
df['Bulan_Tagihan'] = pd.to_datetime(df['Bulan_Tagihan']).dt.date
return df
else:
return pd.DataFrame(columns=["NISN", "Nama", "Kelas", "Bulan_Tagihan", "Jumlah", "Tanggal_Bayar", "Status", "Keterangan"])

def save_data(df):
df.to_excel(FILE_PATH, index=False)
st.cache_data.clear()

def save_spp(df):
df.to_excel(FILE_SPP, index=False)
st.cache_data.clear()

def add_transaction(df, tanggal, kategori, jumlah, jenis, deskripsi, tipe_keuangan):
new_data = {
"Tanggal": tanggal,
"Kategori": kategori,
"Jumlah": float(jumlah),
"Jenis": jenis,
"Deskripsi": deskripsi,
"Tipe_Keuangan": tipe_keuangan
}
df_new = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
save_data(df_new)
return df_new

def add_pembayaran_spp(df_spp, nisn, nama, kelas, bulan_tagihan, jumlah, tanggal_bayar, keterangan):
new_data = {
"NISN": nisn,
"Nama": nama,
"Kelas": kelas,
"Bulan_Tagihan": bulan_tagihan,
"Jumlah": float(jumlah),
"Tanggal_Bayar": tanggal_bayar,
"Status": "Lunas",
"Keterangan": keterangan
}
df_new = pd.concat([df_spp, pd.DataFrame([new_data])], ignore_index=True)
save_spp(df_new)
return df_new

def calculate_summary(df):
pemasukan = df[df["Jenis"] == "Pemasukan"]["Jumlah"].sum()
pengeluaran = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
saldo = pemasukan - pengeluaran
return saldo, pemasukan, pengeluaran

# --- FUNGSI CETAK LAPORAN KEUANGAN DENGAN FILTER KATEGORI ---
def export_laporan_keuangan_filtered_pdf(df, periode_type, periode_value, kategori_filter=None):
"""Generates PDF financial report dengan filter kategori"""
try:
buffer = BytesIO()
c = canvas.Canvas(buffer, pagesize=A4)
width, height = A4

# Judul berdasarkan periode dan kategori
if periode_type == "Harian":
judul = f"LAPORAN KEUANGAN HARIAN"
subjudul = f"Tanggal: {periode_value.strftime('%d %B %Y')}"
if kategori_filter and kategori_filter != "Semua Kategori":
    subjudul += f" | Kategori: {kategori_filter}"
filename = f"laporan_keuangan_harian_{periode_value.strftime('%Y%m%d')}"
if kategori_filter and kategori_filter != "Semua Kategori":
    filename += f"{kategori_filter.replace(' ', '')}"
filename += ".pdf"
elif periode_type == "Bulanan":
judul = f"LAPORAN KEUANGAN BULANAN"
subjudul = f"Periode: {periode_value.strftime('%B %Y')}"
if kategori_filter and kategori_filter != "Semua Kategori":
    subjudul += f" | Kategori: {kategori_filter}"
filename = f"laporan_keuangan_bulanan_{periode_value.strftime('%Y%m')}"
if kategori_filter and kategori_filter != "Semua Kategori":
    filename += f"{kategori_filter.replace(' ', '')}"
filename += ".pdf"
else:  # Tahunan
judul = f"LAPORAN KEUANGAN TAHUNAN"
subjudul = f"Tahun: {periode_value}"
if kategori_filter and kategori_filter != "Semua Kategori":
    subjudul += f" | Kategori: {kategori_filter}"
filename = f"laporan_keuangan_tahunan_{periode_value}"
if kategori_filter and kategori_filter != "Semua Kategori":
    filename += f"{kategori_filter.replace(' ', '')}"
filename += ".pdf"

# Header
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(width/2, height - 50, judul)
c.setFont("Helvetica-Bold", 12)
c.drawCentredString(width/2, height - 70, subjudul)
c.setFont("Helvetica", 10)
c.drawCentredString(width/2, height - 85, "=" * 60)

# Jika tidak ada data
if df.empty:
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(width/2, height - 120, "TIDAK ADA DATA TRANSAKSI")
c.setFont("Helvetica", 12)
c.drawCentredString(width/2, height - 140, "Tidak ditemukan transaksi untuk periode ini")

# Footer
c.setFont("Helvetica-Oblique", 8)
c.drawString(50, 30, f"Dicetak pada: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
c.drawString(width-150, 30, f"Total Transaksi: 0")

c.showPage()
c.save()
buffer.seek(0)
return buffer, filename

# Ringkasan Keuangan
y = height - 110
line_height = 22

# Hitung ringkasan untuk periode yang dipilih
pemasukan_periode = df[df["Jenis"] == "Pemasukan"]["Jumlah"].sum()
pengeluaran_periode = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
saldo_periode = pemasukan_periode - pengeluaran_periode

# Format Rupiah
format_rupiah = lambda x: f"Rp {x:,.0f}".replace(",", "").replace(".", ",").replace("", ".")

c.setFont("Helvetica-Bold", 14)
c.drawString(50, y, "RINGKASAN KEUANGAN")
y -= 30

def draw_financial_field(label, value, y_pos):
c.setFont("Helvetica-Bold", 12)
c.drawString(50, y_pos, f"{label}:")
c.setFont("Helvetica", 12)
value_str = format_rupiah(value)
value_width = c.stringWidth(value_str, "Helvetica", 12)
c.drawString(width - 50 - value_width, y_pos, value_str)
return y_pos - line_height

y = draw_financial_field("Total Pemasukan", pemasukan_periode, y)
y = draw_financial_field("Total Pengeluaran", pengeluaran_periode, y)
y = draw_financial_field("Saldo", saldo_periode, y)

# Statistik per Kategori
y -= 15
c.setFont("Helvetica-Bold", 14)
c.drawString(50, y, "STATISTIK PER KATEGORI")
y -= 30

# Group by Kategori dan hitung pemasukan/pengeluaran
kategori_stats = []
for kategori in df['Kategori'].unique():
if pd.isna(kategori):
    kategori_display = "Lainnya"
else:
    kategori_display = str(kategori)
    
df_kategori = df[df['Kategori'] == kategori]
pemasukan_kategori = df_kategori[df_kategori["Jenis"] == "Pemasukan"]["Jumlah"].sum()
pengeluaran_kategori = df_kategori[df_kategori["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
total_kategori = pemasukan_kategori + pengeluaran_kategori

if total_kategori > 0:  # Hanya tampilkan kategori dengan transaksi
    kategori_stats.append((kategori_display, pemasukan_kategori, pengeluaran_kategori, total_kategori))

# Urutkan berdasarkan total tertinggi
kategori_stats.sort(key=lambda x: x[3], reverse=True)

for kategori_display, pemasukan_kategori, pengeluaran_kategori, total_kategori in kategori_stats:
if y < 100:
    c.showPage()
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "STATISTIK PER KATEGORI (Lanjutan)")
    y -= 30

c.setFont("Helvetica-Bold", 11)
kategori_line = f"{kategori_display}:"
if len(kategori_line) > 30:
    kategori_line = kategori_line[:30] + "..."
c.drawString(50, y, kategori_line)

c.setFont("Helvetica", 11)
pemasukan_str = f"Pemasukan: {format_rupiah(pemasukan_kategori)}"
pengeluaran_str = f"Pengeluaran: {format_rupiah(pengeluaran_kategori)}"

c.drawString(180, y, pemasukan_str)
c.drawString(350, y, pengeluaran_str)
y -= 18

y -= 10

# Detail Transaksi
if y < 150:
c.showPage()
y = height - 50

c.setFont("Helvetica-Bold", 14)
c.drawString(50, y, "DETAIL TRANSAKSI")
y -= 30

# Header tabel
c.setFont("Helvetica-Bold", 9)
col_positions = [50, 100, 180, 280, 350, 430]

c.drawString(col_positions[0], y, "Tanggal")
c.drawString(col_positions[1], y, "Jenis")
c.drawString(col_positions[2], y, "Kategori")
c.drawString(col_positions[3], y, "Tipe")
c.drawString(col_positions[4], y, "Jumlah")
c.drawString(col_positions[5], y, "Deskripsi")

c.line(50, y-5, width-50, y-5)
y -= 20

# Data transaksi
c.setFont("Helvetica", 8)
for _, transaksi in df.iterrows():
if y < 60:
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height-50, "DETAIL TRANSAKSI (Lanjutan)")
    c.setFont("Helvetica-Bold", 9)
    y = height - 80
    
    c.drawString(col_positions[0], y, "Tanggal")
    c.drawString(col_positions[1], y, "Jenis")
    c.drawString(col_positions[2], y, "Kategori")
    c.drawString(col_positions[3], y, "Tipe")
    c.drawString(col_positions[4], y, "Jumlah")
    c.drawString(col_positions[5], y, "Deskripsi")
    c.line(50, y-5, width-50, y-5)
    y -= 20
    c.setFont("Helvetica", 8)

# Data row
tanggal = str(transaksi['Tanggal'])
jenis = str(transaksi['Jenis'])
kategori = str(transaksi['Kategori'])
tipe = str(transaksi['Tipe_Keuangan']) if pd.notna(transaksi['Tipe_Keuangan']) else "Lainnya"
jumlah = format_rupiah(transaksi['Jumlah'])
deskripsi = str(transaksi['Deskripsi']) if pd.notna(transaksi['Deskripsi']) else "-"

# Potong teks yang terlalu panjang
if len(tanggal) > 10:
    tanggal = tanggal[:10]
if len(jenis) > 8:
    jenis = jenis[:8]
if len(kategori) > 15:
    kategori = kategori[:15] + "..."
if len(tipe) > 10:
    tipe = tipe[:10]
if len(deskripsi) > 20:
    deskripsi = deskripsi[:20] + "..."

# Draw data
c.drawString(col_positions[0], y, tanggal)
c.drawString(col_positions[1], y, jenis)
c.drawString(col_positions[2], y, kategori)
c.drawString(col_positions[3], y, tipe)
c.drawString(col_positions[4], y, jumlah)
c.drawString(col_positions[5], y, deskripsi)

y -= 15

# Footer
c.setFont("Helvetica-Oblique", 8)
c.drawString(50, 30, f"Dicetak pada: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
c.drawString(width-150, 30, f"Total Transaksi: {len(df)}")

c.showPage()
c.save()
buffer.seek(0)

return buffer, filename

except Exception as e:
st.error(f"Error generating financial report: {str(e)}")
import traceback
st.error(f"Traceback: {traceback.format_exc()}")
return None, None

# Load all data
df = load_data()
df_siswa = load_siswa()
df_spp = load_spp()
saldo, pemasukan, pengeluaran = calculate_summary(df)

# Ringkasan Keuangan
st.subheader("📊 Ringkasan Keuangan")
col1, col2, col3 = st.columns(3)
format_rupiah = lambda x: f"Rp {x:,.0f}".replace(",", "").replace(".", ",").replace("", ".")
col1.metric("💵 Saldo", format_rupiah(saldo))
col2.metric("⬆ Pemasukan", format_rupiah(pemasukan))
col3.metric("⬇ Pengeluaran", format_rupiah(pengeluaran))

# ========== TAB KEUANGAN YANG DIMODIFIKASI ==========
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
"💰 Pemasukan", "💸 Pengeluaran", "💳 Pembayaran SPP", 
"📋 Riwayat Transaksi", "🔍 Filter Transaksi", "🖨 Cetak Laporan"
])

with tab1:
st.subheader("💰 Input Pemasukan")

with st.form("form_pemasukan"):
colA, colB = st.columns(2)
tanggal = colA.date_input("📅 Tanggal", value=date.today(), key="pemasukan_tanggal")
kategori = colB.selectbox("Kategori Pemasukan*", [
"Uang Pendaftaran",
"Uang Pangkal (UP)", 
"Uang Sumbangan Pendidikan (SPP)",
"Uang Buku",
"Sumbangan Sukarela / Hibah",
"Iuran Kegiatan Siswa",
"Uang Iuran Ekskul",
"Uang Seragam",
"Catering Siswa",
"Jemputan Siswa",
"Tasyakuran",
"Sewa Kantin",
"Fee Jemputan",
"Fee Catering",
"Fee Ekskul",
"Lainnya Pemasukan"
], key="pemasukan_kategori")

colC, colD = st.columns(2)
jumlah = colC.number_input("Jumlah (Rp)*", min_value=1.0, step=1000.0, key="pemasukan_jumlah")
deskripsi = colD.text_input("Deskripsi (Opsional)", key="pemasukan_deskripsi")

simpan = st.form_submit_button("💾 Simpan Pemasukan")
if simpan:
if jumlah >= 1.0:
    df = add_transaction(df, tanggal, kategori, jumlah, "Pemasukan", deskripsi, "Pemasukan")
    st.success("✅ Data pemasukan berhasil ditambahkan!")
    rerun()
else:
    st.error("Jumlah harus lebih besar dari Rp 0.")

with tab2:
st.subheader("💸 Input Pengeluaran")

with st.form("form_pengeluaran"):
colA, colB = st.columns(2)
tanggal = colA.date_input("📅 Tanggal", value=date.today(), key="pengeluaran_tanggal")
kategori = colB.selectbox("Kategori Pengeluaran*", [
"Gaji Guru & Karyawan",
"THR Guru & Yayasan",
"Transport Yayasan",
"THR Yayasan", 
"Transport Pejabat Dinas",
"Transportasi Dinas Guru & Karyawan",
"Konsumsi Internal Sekolah",
"Entertain Tamu",
"Iuran ke Dinas Pendidikan",
"Training Guru dan Karyawan",
"Dana Sosial",
"CSR",
"Listrik",
"Internet dan Data",
"Kegiatan Renang TK",
"Kegiatan Renang SD", 
"Kegiatan Renang SMP",
"Cookery TK",
"Cookery SD",
"Cookery SMP",
"Media Pembelajaran",
"Pengadaan Inventaris",
"Alat dan Bahan Kebersihan",
"Maintenance Gedung",
"Maintenance Peralatan",
"ATK Office",
"Pajak Bumi dan Bangunan",
"Operasional BOS",
"Operasional Office",
"Marketing",
"Cicilan Hutang",
"Riset R&D",
"Honor Pelatih Ekskul",
"Catering Siswa",
"Jemputan Siswa",
"Kegiatan dan Kunjungan Siswa",
"Pinjaman Guru & Karyawan",
"Lainnya Pengeluaran"
], key="pengeluaran_kategori")

colC, colD = st.columns(2)
jumlah = colC.number_input("Jumlah (Rp)*", min_value=1.0, step=1000.0, key="pengeluaran_jumlah")
deskripsi = colD.text_input("Deskripsi (Opsional)", key="pengeluaran_deskripsi")

simpan = st.form_submit_button("💾 Simpan Pengeluaran")
if simpan:
if jumlah >= 1.0:
    df = add_transaction(df, tanggal, kategori, jumlah, "Pengeluaran", deskripsi, "Pengeluaran")
    st.success("✅ Data pengeluaran berhasil ditambahkan!")
    rerun()
else:
    st.error("Jumlah harus lebih besar dari Rp 0.")

with tab3:
st.subheader("💳 Pembayaran SPP")

if not df_siswa.empty:
# Pencarian siswa
col_search1, col_search2 = st.columns([2, 1])
with col_search1:
pencarian = st.text_input("🔍 Cari Siswa (NISN atau Nama)", key="pencarian_spp")

# Filter siswa berdasarkan pencarian
if pencarian:
filtered_siswa = df_siswa[
    df_siswa['NISN'].astype(str).str.contains(pencarian, case=False) |
    df_siswa['Nama Lengkap'].str.contains(pencarian, case=False)
]
else:
filtered_siswa = df_siswa

if not filtered_siswa.empty:
with col_search2:
    selected_index = st.selectbox(
        "Pilih Siswa",
        options=range(len(filtered_siswa)),
        format_func=lambda x: f"{filtered_siswa.iloc[x]['NISN']} - {filtered_siswa.iloc[x]['Nama Lengkap']} - {filtered_siswa.iloc[x]['Kelas']} ({filtered_siswa.iloc[x]['Jenjang Sekolah']})",
        key="select_siswa_spp"
    )

selected_siswa = filtered_siswa.iloc[selected_index]

# Tampilkan data siswa yang dipilih
st.info(f"*Siswa Terpilih:* {selected_siswa['Nama Lengkap']} (NISN: {selected_siswa['NISN']}, Kelas: {selected_siswa['Kelas']}, Jenjang: {selected_siswa['Jenjang Sekolah']})")

# Form pembayaran SPP
with st.form("form_spp"):
    colA, colB = st.columns(2)
    bulan_tagihan = colA.date_input("Bulan Tagihan", value=date.today().replace(day=1), key="bulan_tagihan")
    
    # Tentukan jumlah SPP berdasarkan jenjang
    if selected_siswa['Jenjang Sekolah'] == "TK":
        jumlah_default = 300000.0
    elif selected_siswa['Jenjang Sekolah'] == "SD":
        jumlah_default = 400000.0
    else:  # SMP
        jumlah_default = 500000.0
        
    jumlah_spp = colB.number_input("Jumlah SPP (Rp)", min_value=1000.0, value=jumlah_default, step=50000.0, key="jumlah_spp")
    
    colC, colD = st.columns(2)
    tanggal_bayar = colC.date_input("Tanggal Bayar", value=date.today(), key="tanggal_bayar_spp")
    keterangan = colD.text_input("Keterangan (Opsional)", key="keterangan_spp")
    
    bayar_spp = st.form_submit_button("💳 Bayar SPP")
    
    if bayar_spp:
        # Cek apakah sudah bayar untuk bulan yang sama
        existing_payment = df_spp[
            (df_spp['NISN'] == selected_siswa['NISN']) & 
            (df_spp['Bulan_Tagihan'] == bulan_tagihan)
        ]
        
        if not existing_payment.empty:
            st.error(f"❌ Siswa sudah membayar SPP untuk bulan {bulan_tagihan.strftime('%B %Y')}")
        else:
            # Tambah ke pembayaran SPP
            df_spp = add_pembayaran_spp(
                df_spp, 
                selected_siswa['NISN'],
                selected_siswa['Nama Lengkap'],
                selected_siswa['Kelas'],
                bulan_tagihan,
                jumlah_spp,
                tanggal_bayar,
                keterangan
            )
            
            # Tambah ke transaksi keuangan umum
            df = add_transaction(
                df,
                tanggal_bayar,
                "Uang Sumbangan Pendidikan (SPP)",
                jumlah_spp,
                "Pemasukan",
                f"SPP {selected_siswa['Nama Lengkap']} - {selected_siswa['Jenjang Sekolah']} - {bulan_tagihan.strftime('%B %Y')}",
                "SPP"
            )
            
            st.success("✅ Pembayaran SPP berhasil dicatat!")
            rerun()

else:
st.warning("❌ Tidak ada siswa yang sesuai dengan pencarian")
else:
st.warning("❌ Belum ada data siswa. Silakan tambah data siswa terlebih dahulu di menu Data Siswa.")

# Riwayat Pembayaran SPP
st.subheader("📋 Riwayat Pembayaran SPP")
if not df_spp.empty:
st.dataframe(df_spp.sort_values(by="Tanggal_Bayar", ascending=False), use_container_width=True)

# Statistik SPP
col_spp1, col_spp2, col_spp3 = st.columns(3)
total_spp = df_spp['Jumlah'].sum()
total_siswa = df_spp['NISN'].nunique()
bulan_ini = date.today().replace(day=1)
spp_bulan_ini = df_spp[df_spp['Bulan_Tagihan'] == bulan_ini]['Jumlah'].sum()

col_spp1.metric("💰 Total SPP Tertagih", format_rupiah(total_spp))
col_spp2.metric("👥 Total Siswa Bayar", total_siswa)
col_spp3.metric("📅 SPP Bulan Ini", format_rupiah(spp_bulan_ini))
else:
st.info("Belum ada pembayaran SPP")

with tab4:
st.subheader("📋 Riwayat Transaksi Lengkap")

if not df.empty:
st.dataframe(df.sort_values(by="Tanggal", ascending=False), use_container_width=True)

# Summary semua data
col_sum1, col_sum2, col_sum3 = st.columns(3)
col_sum1.metric("Total Pemasukan", format_rupiah(pemasukan))
col_sum2.metric("Total Pengeluaran", format_rupiah(pengeluaran))
col_sum3.metric("Saldo Akhir", format_rupiah(saldo))
else:
st.info("Belum ada transaksi yang dicatat")

# ========== TAB BARU: FILTER TRANSAKSI ==========
with tab5:
st.subheader("🔍 Filter dan Analisis Transaksi")

if not df.empty:
# Filter options
col_filter1, col_filter2, col_filter3 = st.columns(3)

with col_filter1:
jenis_filter = st.selectbox(
    "Filter Jenis Transaksi",
    options=["Semua", "Pemasukan", "Pengeluaran"],
    key="filter_jenis_analisis"
)

with col_filter2:
# Get unique categories
all_categories = ["Semua Kategori"] + sorted(df['Kategori'].unique().tolist())
kategori_filter = st.selectbox(
    "Filter Kategori",
    options=all_categories,
    key="filter_kategori_analisis"
)

with col_filter3:
tanggal_mulai = st.date_input("Dari Tanggal", 
                            value=date.today().replace(day=1),
                            key="filter_mulai_analisis")
tanggal_akhir = st.date_input("Sampai Tanggal", 
                            value=date.today(),
                            key="filter_akhir_analisis")

# Apply filters
df_filtered = df.copy()

if jenis_filter != "Semua":
df_filtered = df_filtered[df_filtered['Jenis'] == jenis_filter]

if kategori_filter != "Semua Kategori":
df_filtered = df_filtered[df_filtered['Kategori'] == kategori_filter]

df_filtered = df_filtered[
(df_filtered['Tanggal'] >= tanggal_mulai) & 
(df_filtered['Tanggal'] <= tanggal_akhir)
]

if not df_filtered.empty:
# Summary filtered
pemasukan_filtered = df_filtered[df_filtered['Jenis'] == "Pemasukan"]['Jumlah'].sum()
pengeluaran_filtered = df_filtered[df_filtered['Jenis'] == "Pengeluaran"]['Jumlah'].sum()
saldo_filtered = pemasukan_filtered - pengeluaran_filtered

st.subheader("📊 Ringkasan Hasil Filter")
col_sum1, col_sum2, col_sum3 = st.columns(3)
col_sum1.metric("Pemasukan (Filter)", format_rupiah(pemasukan_filtered))
col_sum2.metric("Pengeluaran (Filter)", format_rupiah(pengeluaran_filtered))
col_sum3.metric("Saldo (Filter)", format_rupiah(saldo_filtered))

# Tampilkan data
st.subheader("📋 Data Transaksi Hasil Filter")
st.dataframe(df_filtered.sort_values(by="Tanggal", ascending=False), use_container_width=True)

# Chart
st.subheader("📈 Grafik Analisis")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Pie chart untuk jenis transaksi
    if len(df_filtered) > 0:
        jenis_counts = df_filtered['Jenis'].value_counts()
        fig_pie = px.pie(
            values=jenis_counts.values,
            names=jenis_counts.index,
            title='Distribusi Jenis Transaksi'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    # Bar chart untuk kategori
    if len(df_filtered) > 0:
        kategori_sum = df_filtered.groupby(['Kategori', 'Jenis'])['Jumlah'].sum().reset_index()
        fig_bar = px.bar(
            kategori_sum,
            x='Kategori',
            y='Jumlah',
            color='Jenis',
            title='Total per Kategori',
            barmode='group'
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

# Trend bulanan
st.subheader("📅 Trend Bulanan")
df_monthly = df_filtered.copy()
df_monthly['Bulan'] = pd.to_datetime(df_monthly['Tanggal']).dt.to_period('M')
monthly_sum = df_monthly.groupby(['Bulan', 'Jenis'])['Jumlah'].sum().reset_index()
monthly_sum['Bulan'] = monthly_sum['Bulan'].astype(str)

if len(monthly_sum) > 0:
    fig_trend = px.line(
        monthly_sum,
        x='Bulan',
        y='Jumlah',
        color='Jenis',
        title='Trend Bulanan',
        markers=True
    )
    st.plotly_chart(fig_trend, use_container_width=True)

else:
st.info("❌ Tidak ada transaksi yang sesuai dengan filter yang dipilih.")
else:
st.info("Belum ada transaksi yang dicatat.")

# ========== TAB BARU: CETAK LAPORAN DENGAN FILTER KATEGORI ==========
with tab6:
st.subheader("🖨 Cetak Laporan Keuangan")

# Pilihan periode
col_periode1, col_periode2, col_periode3 = st.columns(3)

with col_periode1:
st.write("📅 Laporan Harian**")
tanggal_harian = st.date_input("Pilih Tanggal", value=date.today(), key="harian_cetak")

# Get categories for daily report
df_harian = df[df['Tanggal'] == tanggal_harian]
kategori_harian = ["Semua Kategori"] + sorted(df_harian['Kategori'].unique().tolist())
kategori_harian_pilih = st.selectbox(
"Filter Kategori Harian",
options=kategori_harian,
key="kategori_harian"
)

# Apply category filter for daily
if kategori_harian_pilih != "Semua Kategori":
df_harian = df_harian[df_harian['Kategori'] == kategori_harian_pilih]

st.write(f"*Data ditemukan:* {len(df_harian)} transaksi")

if st.button("📄 Generate Laporan Harian", use_container_width=True, key="btn_harian_cetak"):
if not df_harian.empty:
    with st.spinner("Membuat laporan harian..."):
        pdf_buffer, filename = export_laporan_keuangan_filtered_pdf(
            df_harian, "Harian", tanggal_harian, kategori_harian_pilih
        )
        if pdf_buffer and filename:
            st.success("✅ Laporan harian berhasil dibuat!")
            st.download_button(
                label="⬇ Download Laporan Harian",
                data=pdf_buffer,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                key="dl_harian_cetak"
            )
else:
    st.warning("⚠ Tidak ada transaksi pada tanggal tersebut")

with col_periode2:
st.write("📊 Laporan Bulanan**")
bulan_tahun = st.date_input("Pilih Bulan", value=date.today(), key="bulanan_cetak")

# Get categories for monthly report
tahun = bulan_tahun.year
bulan = bulan_tahun.month
df_bulanan = df[(df['Tanggal'].apply(lambda x: x.year) == tahun) & 
            (df['Tanggal'].apply(lambda x: x.month) == bulan)]
kategori_bulanan = ["Semua Kategori"] + sorted(df_bulanan['Kategori'].unique().tolist())
kategori_bulanan_pilih = st.selectbox(
"Filter Kategori Bulanan",
options=kategori_bulanan,
key="kategori_bulanan"
)

# Apply category filter for monthly
if kategori_bulanan_pilih != "Semua Kategori":
df_bulanan = df_bulanan[df_bulanan['Kategori'] == kategori_bulanan_pilih]

st.write(f"*Data ditemukan:* {len(df_bulanan)} transaksi")

if st.button("📄 Generate Laporan Bulanan", use_container_width=True, key="btn_bulanan_cetak"):
if not df_bulanan.empty:
    with st.spinner("Membuat laporan bulanan..."):
        pdf_buffer, filename = export_laporan_keuangan_filtered_pdf(
            df_bulanan, "Bulanan", bulan_tahun, kategori_bulanan_pilih
        )
        if pdf_buffer and filename:
            st.success("✅ Laporan bulanan berhasil dibuat!")
            st.download_button(
                label="⬇ Download Laporan Bulanan",
                data=pdf_buffer,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                key="dl_bulanan_cetak"
            )
else:
    st.warning("⚠ Tidak ada transaksi pada bulan tersebut")

with col_periode3:
st.write("📈 Laporan Tahunan**")
tahun = st.number_input("Pilih Tahun", min_value=2000, max_value=2100, 
                    value=date.today().year, key="tahunan_cetak")

# Get categories for yearly report
df_tahunan = df[df['Tanggal'].apply(lambda x: x.year) == tahun]
kategori_tahunan = ["Semua Kategori"] + sorted(df_tahunan['Kategori'].unique().tolist())
kategori_tahunan_pilih = st.selectbox(
"Filter Kategori Tahunan",
options=kategori_tahunan,
key="kategori_tahunan"
)

# Apply category filter for yearly
if kategori_tahunan_pilih != "Semua Kategori":
df_tahunan = df_tahunan[df_tahunan['Kategori'] == kategori_tahunan_pilih]

st.write(f"*Data ditemukan:* {len(df_tahunan)} transaksi")

if st.button("📄 Generate Laporan Tahunan", use_container_width=True, key="btn_tahunan_cetak"):
if not df_tahunan.empty:
    with st.spinner("Membuat laporan tahunan..."):
        pdf_buffer, filename = export_laporan_keuangan_filtered_pdf(
            df_tahunan, "Tahunan", tahun, kategori_tahunan_pilih
        )
        if pdf_buffer and filename:
            st.success("✅ Laporan tahunan berhasil dibuat!")
            st.download_button(
                label="⬇ Download Laporan Tahunan",
                data=pdf_buffer,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                key="dl_tahunan_cetak"
            )
else:
    st.warning("⚠ Tidak ada transaksi pada tahun tersebut")

# Laporan Multi-Bulan (Maksimal 3 bulan)
st.divider()
st.subheader("📑 Laporan Multi-Bulan (Maksimal 3 Bulan)")

col_multi1, col_multi2 = st.columns(2)

with col_multi1:
bulan_mulai = st.date_input("Bulan Mulai", 
                        value=date.today().replace(day=1) - timedelta(days=60),
                        key="multi_mulai")
bulan_akhir = st.date_input("Bulan Akhir", 
                        value=date.today().replace(day=1),
                        key="multi_akhir")

with col_multi2:
# Validasi maksimal 3 bulan
bulan_diff = (bulan_akhir.year - bulan_mulai.year) * 12 + (bulan_akhir.month - bulan_mulai.month)
if bulan_diff > 2:  # Maksimal 3 bulan (0,1,2 difference)
st.error("❌ Maksimal 3 bulan untuk laporan multi-bulan")
bulan_akhir = bulan_mulai.replace(month=bulan_mulai.month + 2)
st.info(f"Diubah menjadi: {bulan_mulai.strftime('%B %Y')} - {bulan_akhir.strftime('%B %Y')}")

# Get categories for multi-month report
df_multi = df[
(df['Tanggal'] >= bulan_mulai.replace(day=1)) & 
(df['Tanggal'] <= bulan_akhir.replace(day=28))
]
kategori_multi = ["Semua Kategori"] + sorted(df_multi['Kategori'].unique().tolist())
kategori_multi_pilih = st.selectbox(
"Filter Kategori Multi-Bulan",
options=kategori_multi,
key="kategori_multi"
)

# Apply category filter for multi-month
if kategori_multi_pilih != "Semua Kategori":
df_multi = df_multi[df_multi['Kategori'] == kategori_multi_pilih]

st.write(f"*Data ditemukan:* {len(df_multi)} transaksi")

if st.button("📄 Generate Laporan Multi-Bulan", use_container_width=True, key="btn_multi_cetak"):
if not df_multi.empty:
with st.spinner("Membuat laporan multi-bulan..."):
    # Custom title for multi-month
    judul_periode = f"{bulan_mulai.strftime('%B %Y')} - {bulan_akhir.strftime('%B %Y')}"
    pdf_buffer, filename = export_laporan_keuangan_filtered_pdf(
        df_multi, "Bulanan", bulan_mulai, kategori_multi_pilih
    )
    if pdf_buffer and filename:
        # Rename filename for multi-month
        filename = f"laporan_keuangan_multibulan_{bulan_mulai.strftime('%Y%m')}_{bulan_akhir.strftime('%Y%m')}"
        if kategori_multi_pilih != "Semua Kategori":
            filename += f"{kategori_multi_pilih.replace(' ', '')}"
        filename += ".pdf"
        
        st.success("✅ Laporan multi-bulan berhasil dibuat!")
        st.download_button(
            label="⬇ Download Laporan Multi-Bulan",
            data=pdf_buffer,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
            key="dl_multi_cetak"
        )
else:
st.warning("⚠ Tidak ada transaksi pada periode tersebut")

# Laporan All Time dengan Filter Kategori
st.divider()
st.write("📚 Laporan Semua Data**")

# Get categories for all data
kategori_all = ["Semua Kategori"] + sorted(df['Kategori'].unique().tolist())
kategori_all_pilih = st.selectbox(
"Filter Kategori Semua Data",
options=kategori_all,
key="kategori_all"
)

# Apply category filter for all data
df_all = df.copy()
if kategori_all_pilih != "Semua Kategori":
df_all = df_all[df_all['Kategori'] == kategori_all_pilih]

st.write(f"*Total data:* {len(df_all)} transaksi")

if st.button("📄 Generate Laporan Semua Data", use_container_width=True, key="btn_all_cetak"):
if not df_all.empty:
with st.spinner("Membuat laporan semua data..."):
    pdf_buffer, filename = export_laporan_keuangan_filtered_pdf(
        df_all, "Semua Data", "All Time", kategori_all_pilih
    )
    if pdf_buffer and filename:
        st.success("✅ Laporan semua data berhasil dibuat!")
        st.download_button(
            label="⬇ Download Laporan Semua Data",
            data=pdf_buffer,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
            key="dl_all_cetak"
        )
else:
st.warning("⚠ Tidak ada data transaksi")

# ==================== MENU DATA SISWA (MODIFIKASI) ====================
elif pilihan_aktif == "🎓 Data Siswa":
FILE_SISWA = "data_siswa.xlsx"
FILE_SPP = "pembayaran_spp.xlsx"

@st.cache_data
def load_siswa():
if os.path.exists(FILE_SISWA):
df = pd.read_excel(FILE_SISWA)
return df
else:
columns = [
# DATA SISWA
"Nama Lengkap", "Tempat Lahir", "Tanggal Lahir", "Jenis Kelamin", "Jenjang Sekolah", 
"Kelas", "NIS", "NISN", "Golongan Darah", "Agama", "No HP/WA", "Sosial Media", 
"Alamat Domisili", "Alamat KTP", "NIK", "Tanggal Terdaftar", "Sekolah Asal", "Foto",
# DATA ORANG TUA
"Nama Ayah", "Pekerjaan Ayah", "No HP/WA Ayah", "NIK Ayah",
"Nama Ibu", "Pekerjaan Ibu", "No HP/WA Ibu", "NIK Ibu",
"Nama Wali", "Pekerjaan Wali", "No HP/WA Wali", "NIK Wali",
"Alamat Orang Tua"
]
return pd.DataFrame(columns=columns)

@st.cache_data
def load_spp():
if os.path.exists(FILE_SPP):
df = pd.read_excel(FILE_SPP)
df['Tanggal_Bayar'] = pd.to_datetime(df['Tanggal_Bayar']).dt.date
df['Bulan_Tagihan'] = pd.to_datetime(df['Bulan_Tagihan']).dt.date
return df
else:
return pd.DataFrame(columns=["NISN", "Nama", "Kelas", "Bulan_Tagihan", "Jumlah", "Tanggal_Bayar", "Status", "Keterangan"])

def save_siswa(df):
df.to_excel(FILE_SISWA, index=False)
st.cache_data.clear()

def add_siswa(df, data_siswa):
if str(data_siswa['NISN']) in df['NISN'].astype(str).values:
st.error(f"❌ NISN *{data_siswa['NISN']}* sudah terdaftar. Data tidak ditambahkan.")
return df, False

new_data = data_siswa
df_new = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
save_siswa(df_new)
return df_new, True

# Load data
df_siswa = load_siswa()
df_spp = load_spp()

# Initialize session state untuk form data siswa
if 'form_siswa_data' not in st.session_state:
st.session_state.form_siswa_data = {
# Data Siswa
'nama_lengkap': '', 'tempat_lahir': '', 'tanggal_lahir': date.today().replace(year=date.today().year-10),
'jenis_kelamin': 'Laki-laki', 'jenjang_sekolah': 'TK', 'kelas': '', 'nis': '', 'nisn': '',
'golongan_darah': 'A', 'agama': 'Islam', 'no_hp': '', 'sosial_media': '',
'alamat_domisili': '', 'alamat_ktp': '', 'nik': '', 'tanggal_terdaftar': date.today(),
'sekolah_asal': '', 'foto': None,
# Data Orang Tua
'nama_ayah': '', 'pekerjaan_ayah': '', 'no_hp_ayah': '', 'nik_ayah': '',
'nama_ibu': '', 'pekerjaan_ibu': '', 'no_hp_ibu': '', 'nik_ibu': '',
'nama_wali': '', 'pekerjaan_wali': '', 'no_hp_wali': '', 'nik_wali': '',
'alamat_orang_tua': ''
}

# Tampilkan konten berdasarkan submenu yang dipilih
submenu_aktif = st.session_state.submenu_choice

if submenu_aktif == "📝 Tambah Data Siswa":
st.subheader("📝 Tambah Data Siswa")

with st.form("form_siswa"):
st.markdown("### 📋 DATA SISWA")

# Tab untuk organisasi yang lebih baik
tab1, tab2, tab3 = st.tabs(["Data Pribadi", "Data Kontak & Alamat", "Data Orang Tua"])

with tab1:
col1, col2 = st.columns(2)
with col1:
    # Data wajib - bagian kiri
    st.session_state.form_siswa_data['nama_lengkap'] = st.text_input(
        "Nama Lengkap*", 
        value=st.session_state.form_siswa_data['nama_lengkap'],
        placeholder="Contoh: Ahmad Budiman"
    )
    st.session_state.form_siswa_data['tempat_lahir'] = st.text_input(
        "Tempat Lahir*", 
        value=st.session_state.form_siswa_data['tempat_lahir'],
        placeholder="Contoh: Jakarta"
    )
    st.session_state.form_siswa_data['tanggal_lahir'] = st.date_input(
        "Tanggal Lahir*", 
        value=st.session_state.form_siswa_data['tanggal_lahir']
    )
    st.session_state.form_siswa_data['jenis_kelamin'] = st.selectbox(
        "Jenis Kelamin*", 
        ["Laki-laki", "Perempuan"],
        index=0 if st.session_state.form_siswa_data['jenis_kelamin'] == 'Laki-laki' else 1
    )
    st.session_state.form_siswa_data['jenjang_sekolah'] = st.selectbox(
        "Jenjang Sekolah*", 
        ["TK", "SD", "SMP"],
        index=["TK", "SD", "SMP"].index(st.session_state.form_siswa_data['jenjang_sekolah'])
    )
    
with col2:
    # Data wajib - bagian kanan
    st.session_state.form_siswa_data['kelas'] = st.text_input(
        "Kelas (Rombongan Belajar)*", 
        value=st.session_state.form_siswa_data['kelas'],
        placeholder="Contoh: TK-A, 1A, 7A"
    )
    st.session_state.form_siswa_data['nis'] = st.text_input(
        "Nomor Induk Siswa (NIS)*", 
        value=st.session_state.form_siswa_data['nis'],
        placeholder="Contoh: 2024001"
    )
    st.session_state.form_siswa_data['nisn'] = st.text_input(
        "Nomor Induk Siswa Nasional (NISN)*", 
        value=st.session_state.form_siswa_data['nisn'],
        placeholder="Contoh: 0023456789"
    )
    st.session_state.form_siswa_data['agama'] = st.selectbox(
        "Agama*", 
        ["Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Konghucu"],
        index=["Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Konghucu"].index(st.session_state.form_siswa_data['agama'])
    )
    st.session_state.form_siswa_data['golongan_darah'] = st.selectbox(
        "Golongan Darah", 
        ["A", "B", "AB", "O", "Tidak Tahu"],
        index=["A", "B", "AB", "O", "Tidak Tahu"].index(st.session_state.form_siswa_data['golongan_darah'])
    )

with tab2:
col3, col4 = st.columns(2)
with col3:
    # Data kontak dan alamat
    st.session_state.form_siswa_data['no_hp'] = st.text_input(
        "No HP/WA*", 
        value=st.session_state.form_siswa_data['no_hp'],
        placeholder="Contoh: 081234567890"
    )
    st.session_state.form_siswa_data['sosial_media'] = st.text_input(
        "Sosial Media (IG, FB, Tiktok dll)", 
        value=st.session_state.form_siswa_data['sosial_media'],
        placeholder="Contoh: @username"
    )
    st.session_state.form_siswa_data['nik'] = st.text_input(
        "Nomor Induk Kependudukan (NIK)*", 
        value=st.session_state.form_siswa_data['nik'],
        placeholder="16 digit NIK"
    )
    
with col4:
    st.session_state.form_siswa_data['alamat_domisili'] = st.text_area(
        "Alamat Domisili*", 
        value=st.session_state.form_siswa_data['alamat_domisili'],
        placeholder="Alamat tempat tinggal saat ini",
        height=80
    )
    st.session_state.form_siswa_data['alamat_ktp'] = st.text_area(
        "Alamat Berdasarkan KTP*", 
        value=st.session_state.form_siswa_data['alamat_ktp'],
        placeholder="Alamat sesuai KTP (jika berbeda)",
        height=80
    )

col5, col6 = st.columns(2)
with col5:
    st.session_state.form_siswa_data['tanggal_terdaftar'] = st.date_input(
        "Tanggal Terdaftar di Sekolah*", 
        value=st.session_state.form_siswa_data['tanggal_terdaftar']
    )
with col6:
    st.session_state.form_siswa_data['sekolah_asal'] = st.text_input(
        "Sekolah Asal", 
        value=st.session_state.form_siswa_data['sekolah_asal'],
        placeholder="Nama sekolah sebelumnya"
    )

# Upload foto
uploaded_foto = st.file_uploader("Upload Foto Siswa", type=['jpg', 'jpeg', 'png'], key="foto_upload")
if uploaded_foto:
    st.session_state.form_siswa_data['foto'] = uploaded_foto
    st.image(uploaded_foto, width=150, caption="Preview Foto")
elif st.session_state.form_siswa_data['foto'] and hasattr(st.session_state.form_siswa_data['foto'], 'getvalue'):
    st.image(st.session_state.form_siswa_data['foto'], width=150, caption="Foto yang akan diupload")

with tab3:
st.markdown("#### 👨 Data Ayah")
col7, col8 = st.columns(2)
with col7:
    st.session_state.form_siswa_data['nama_ayah'] = st.text_input(
        "Nama Lengkap Ayah", 
        value=st.session_state.form_siswa_data['nama_ayah'],
        placeholder="Nama lengkap ayah"
    )
    st.session_state.form_siswa_data['pekerjaan_ayah'] = st.text_input(
        "Pekerjaan Ayah", 
        value=st.session_state.form_siswa_data['pekerjaan_ayah'],
        placeholder="Pekerjaan ayah"
    )
with col8:
    st.session_state.form_siswa_data['no_hp_ayah'] = st.text_input(
        "No HP/WA Ayah", 
        value=st.session_state.form_siswa_data['no_hp_ayah'],
        placeholder="Nomor telepon ayah"
    )
    st.session_state.form_siswa_data['nik_ayah'] = st.text_input(
        "NIK Ayah", 
        value=st.session_state.form_siswa_data['nik_ayah'],
        placeholder="NIK ayah"
    )

st.markdown("#### 👩 Data Ibu")
col9, col10 = st.columns(2)
with col9:
    st.session_state.form_siswa_data['nama_ibu'] = st.text_input(
        "Nama Lengkap Ibu", 
        value=st.session_state.form_siswa_data['nama_ibu'],
        placeholder="Nama lengkap ibu"
    )
    st.session_state.form_siswa_data['pekerjaan_ibu'] = st.text_input(
        "Pekerjaan Ibu", 
        value=st.session_state.form_siswa_data['pekerjaan_ibu'],
        placeholder="Pekerjaan ibu"
    )
with col10:
    st.session_state.form_siswa_data['no_hp_ibu'] = st.text_input(
        "No HP/WA Ibu", 
        value=st.session_state.form_siswa_data['no_hp_ibu'],
        placeholder="Nomor telepon ibu"
    )
    st.session_state.form_siswa_data['nik_ibu'] = st.text_input(
        "NIK Ibu", 
        value=st.session_state.form_siswa_data['nik_ibu'],
        placeholder="NIK ibu"
    )

st.markdown("#### 👨‍💼 Data Wali (Jika berbeda dengan orang tua)")
col11, col12 = st.columns(2)
with col11:
    st.session_state.form_siswa_data['nama_wali'] = st.text_input(
        "Nama Lengkap Wali", 
        value=st.session_state.form_siswa_data['nama_wali'],
        placeholder="Nama lengkap wali"
    )
    st.session_state.form_siswa_data['pekerjaan_wali'] = st.text_input(
        "Pekerjaan Wali", 
        value=st.session_state.form_siswa_data['pekerjaan_wali'],
        placeholder="Pekerjaan wali"
    )

with col12:
    st.session_state.form_siswa_data['no_hp_wali'] = st.text_input(
        "No HP/WA Wali", 
        value=st.session_state.form_siswa_data['no_hp_wali'],
        placeholder="Nomor telepon wali"
    )
    st.session_state.form_siswa_data['nik_wali'] = st.text_input(
        "NIK Wali", 
        value=st.session_state.form_siswa_data['nik_wali'],
        placeholder="NIK wali"
    )

st.session_state.form_siswa_data['alamat_orang_tua'] = st.text_area(
    "Alamat Orang Tua/Wali", 
    value=st.session_state.form_siswa_data['alamat_orang_tua'],
    placeholder="Alamat orang tua/wali",
    height=60
)
                
                st.markdown("*Keterangan:* * = Wajib diisi")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    simpan_siswa = st.form_submit_button("💾 Simpan Data Siswa", use_container_width=True)
                with col_btn2:
                    reset_form = st.form_submit_button("🔄 Reset Form", use_container_width=True)
                
                if reset_form:
                    # Reset form data
                    st.session_state.form_siswa_data = {
                        'nama_lengkap': '', 'tempat_lahir': '', 'tanggal_lahir': date.today().replace(year=date.today().year-10),
                        'jenis_kelamin': 'Laki-laki', 'jenjang_sekolah': 'TK', 'kelas': '', 'nis': '', 'nisn': '',
                        'golongan_darah': 'A', 'agama': 'Islam', 'no_hp': '', 'sosial_media': '',
                        'alamat_domisili': '', 'alamat_ktp': '', 'nik': '', 'tanggal_terdaftar': date.today(),
                        'sekolah_asal': '', 'foto': None,
                        'nama_ayah': '', 'pekerjaan_ayah': '', 'no_hp_ayah': '', 'nik_ayah': '',
                        'nama_ibu': '', 'pekerjaan_ibu': '', 'no_hp_ibu': '', 'nik_ibu': '',
                        'nama_wali': '', 'pekerjaan_wali': '', 'no_hp_wali': '', 'nik_wali': '',
                        'alamat_orang_tua': ''
                    }
                    st.success("Form berhasil direset!")
                    rerun()
                
                if simpan_siswa:
                    # Validasi data wajib
                    data = st.session_state.form_siswa_data
                    wajib_diisi = [
                        data['nama_lengkap'], data['tempat_lahir'], data['jenis_kelamin'], 
                        data['jenjang_sekolah'], data['kelas'], data['nis'], data['nisn'], 
                        data['agama'], data['no_hp'], data['alamat_domisili'], data['alamat_ktp'], data['nik']
                    ]
                    
                    if all(wajib_diisi):
                        # Validasi NISN unik
                        if str(data['nisn']) in df_siswa['NISN'].astype(str).values:
                            st.error(f"❌ NISN *{data['nisn']}* sudah terdaftar. Gunakan NISN yang berbeda.")
                        else:
                            # Konversi foto ke base64 jika ada
                            foto_base64 = None
                            if data['foto'] and hasattr(data['foto'], 'getvalue'):
                                foto_bytes = data['foto'].getvalue()
                                foto_base64 = base64.b64encode(foto_bytes).decode()
                            
                            data_siswa = {
                                # Data Siswa
                                "Nama Lengkap": data['nama_lengkap'],
                                "Tempat Lahir": data['tempat_lahir'],
                                "Tanggal Lahir": data['tanggal_lahir'],
                                "Jenis Kelamin": data['jenis_kelamin'],
                                "Jenjang Sekolah": data['jenjang_sekolah'],
                                "Kelas": data['kelas'],
                                "NIS": data['nis'],
                                "NISN": data['nisn'],
                                "Golongan Darah": data['golongan_darah'],
                                "Agama": data['agama'],
                                "No HP/WA": data['no_hp'],
                                "Sosial Media": data['sosial_media'],
                                "Alamat Domisili": data['alamat_domisili'],
                                "Alamat KTP": data['alamat_ktp'],
                                "NIK": data['nik'],
                                "Tanggal Terdaftar": data['tanggal_terdaftar'],
                                "Sekolah Asal": data['sekolah_asal'],
                                "Foto": foto_base64,
                                # Data Orang Tua
                                "Nama Ayah": data['nama_ayah'],
                                "Pekerjaan Ayah": data['pekerjaan_ayah'],
                                "No HP/WA Ayah": data['no_hp_ayah'],
                                "NIK Ayah": data['nik_ayah'],
                                "Nama Ibu": data['nama_ibu'],
                                "Pekerjaan Ibu": data['pekerjaan_ibu'],
                                "No HP/WA Ibu": data['no_hp_ibu'],
                                "NIK Ibu": data['nik_ibu'],
                                "Nama Wali": data['nama_wali'],
                                "Pekerjaan Wali": data['pekerjaan_wali'],
                                "No HP/WA Wali": data['no_hp_wali'],
                                "NIK Wali": data['nik_wali'],
                                "Alamat Orang Tua": data['alamat_orang_tua']
                            }
                            
                            df_siswa_new, success = add_siswa(df_siswa, data_siswa)
                            
                            if success:
                                st.success("✅ Data siswa berhasil disimpan!")
                                # Reset form setelah berhasil disimpan
                                st.session_state.form_siswa_data = {
                                    'nama_lengkap': '', 'tempat_lahir': '', 'tanggal_lahir': date.today().replace(year=date.today().year-10),
                                    'jenis_kelamin': 'Laki-laki', 'jenjang_sekolah': 'TK', 'kelas': '', 'nis': '', 'nisn': '',
                                    'golongan_darah': 'A', 'agama': 'Islam', 'no_hp': '', 'sosial_media': '',
                                    'alamat_domisili': '', 'alamat_ktp': '', 'nik': '', 'tanggal_terdaftar': date.today(),
                                    'sekolah_asal': '', 'foto': None,
                                    'nama_ayah': '', 'pekerjaan_ayah': '', 'no_hp_ayah': '', 'nik_ayah': '',
                                    'nama_ibu': '', 'pekerjaan_ibu': '', 'no_hp_ibu': '', 'nik_ibu': '',
                                    'nama_wali': '', 'pekerjaan_wali': '', 'no_hp_wali': '', 'nik_wali': '',
                                    'alamat_orang_tua': ''
                                }
                                df_siswa = df_siswa_new
                                rerun()
                    else:
                        st.error("❌ Semua field yang bertanda * wajib diisi!")
                        # Tampilkan field yang masih kosong
                        fields_kosong = []
                        if not data['nama_lengkap']: fields_kosong.append("Nama Lengkap")
                        if not data['tempat_lahir']: fields_kosong.append("Tempat Lahir")
                        if not data['kelas']: fields_kosong.append("Kelas")
                        if not data['nis']: fields_kosong.append("NIS")
                        if not data['nisn']: fields_kosong.append("NISN")
                        if not data['no_hp']: fields_kosong.append("No HP/WA")
                        if not data['alamat_domisili']: fields_kosong.append("Alamat Domisili")
                        if not data['alamat_ktp']: fields_kosong.append("Alamat KTP")
                        if not data['nik']: fields_kosong.append("NIK")
                        
                        if fields_kosong:
                            st.warning(f"Field berikut masih kosong: {', '.join(fields_kosong)}")

            # Preview Data yang Akan Disimpan
            st.divider()
            st.subheader("👁 Preview Data")
            
            if st.session_state.form_siswa_data['nama_lengkap']:
                col_preview1, col_preview2 = st.columns(2)
                with col_preview1:
                    st.write("*Data Pribadi:*")
                    st.write(f"*Nama:* {st.session_state.form_siswa_data['nama_lengkap']}")
                    st.write(f"*TTL:* {st.session_state.form_siswa_data['tempat_lahir']}, {st.session_state.form_siswa_data['tanggal_lahir']}")
                    st.write(f"*Jenjang:* {st.session_state.form_siswa_data['jenjang_sekolah']} - {st.session_state.form_siswa_data['kelas']}")
                    st.write(f"*NIS/NISN:* {st.session_state.form_siswa_data['nis']} / {st.session_state.form_siswa_data['nisn']}")
                
                with col_preview2:
                    st.write("*Kontak:*")
                    st.write(f"*No HP:* {st.session_state.form_siswa_data['no_hp']}")
                    if st.session_state.form_siswa_data['nama_ayah']:
                        st.write(f"*Ayah:* {st.session_state.form_siswa_data['nama_ayah']}")
                    if st.session_state.form_siswa_data['nama_ibu']:
                        st.write(f"*Ibu:* {st.session_state.form_siswa_data['nama_ibu']}")
            else:
                st.info("Isi form di atas untuk melihat preview data")

        elif submenu_aktif == "📄 Cetak Laporan":
            st.subheader("📄 Cetak Laporan Data Siswa")
            
            if not df_siswa.empty:
                st.info("Fitur cetak laporan data siswa")
                # Implementasi cetak laporan data siswa bisa ditambahkan di sini
            else:
                st.warning("❌ Belum ada data siswa. Silakan tambah data siswa terlebih dahulu.")

        else:
            # Fungsi untuk menampilkan data siswa per jenjang
            def tampilkan_data_siswa(jenjang_filter=None):
                if jenjang_filter == "🎨 Data TK":
                    jenjang_value = "TK"
                    judul = "Data Siswa TK"
                elif jenjang_filter == "📚 Data SD":
                    jenjang_value = "SD"
                    judul = "Data Siswa SD"
                elif jenjang_filter == "🎓 Data SMP":
                    jenjang_value = "SMP"
                    judul = "Data Siswa SMP"
                else:  # Semua Siswa
                    jenjang_value = None
                    judul = "Semua Data Siswa"
                
                if jenjang_value:
                    df_filtered = df_siswa[df_siswa['Jenjang Sekolah'] == jenjang_value]
                else:
                    df_filtered = df_siswa
                
                st.subheader(judul)
                
                if not df_filtered.empty:
                    st.dataframe(df_filtered[['Nama Lengkap', 'NISN', 'Kelas', 'Jenjang Sekolah', 'No HP/WA']], 
                            use_container_width=True)
                else:
                    st.info(f"Belum ada data siswa {jenjang_value if jenjang_value else ''} yang dicatat.")
            
            # Tampilkan data berdasarkan submenu
            if submenu_aktif in ["🎨 Data TK", "📚 Data SD", "🎓 Data SMP", "👥 Semua Siswa"]:
                tampilkan_data_siswa(submenu_aktif)

    # ==================== MENU DATA GURU & KARYAWAN (MODIFIKASI LENGKAP) ====================
    elif pilihan_aktif == "👨‍🏫 Data Guru & Karyawan":
        FILE_GURU = "data_guru_karyawan.xlsx"

        @st.cache_data
        def load_guru():
            if os.path.exists(FILE_GURU):
                df = pd.read_excel(FILE_GURU)
                return df
            else:
                columns = [
                    # DATA PRIBADI
                    "Nama Lengkap", "Tempat Lahir", "Tanggal Lahir", "Jenis Kelamin", 
                    "No Induk Pegawai", "NUPTK", "Email", "Status Pernikahan", "Status Kepegawaian",
                    "Jabatan Terakhir", "Golongan Darah", "Nomor HP/WA", "Nomor HP/WA Pasangan",
                    "Sosial Media", "Alamat Domisili", "Alamat KTP", "Mulai Bekerja", "Masa Kerja",
                    "SK Pengangkatan Karyawan Tetap", "SK Pengangkatan Karyawan Tidak Tetap", 
                    "SK Pengangkatan Jabatan", "Foto",
                    
                    # DATA KELUARGA & DARURAT
                    "Nama Pasangan", "Jumlah Anak", "Nama Anak 1", "Nama Anak 2", "Nama Anak 3",
                    "Kontak Darurat Nama", "Kontak Darurat Hubungan", "Kontak Darurat No HP",
                    
                    # DATA BANK
                    "Nama Bank", "Nomor Rekening", "Atas Nama Rekening",
                    
                    # DATA PENDIDIKAN
                    "Pendidikan Terakhir", "Jurusan", "Nama Sekolah/Universitas", "Tahun Lulus"
                ]
                return pd.DataFrame(columns=columns)

        def save_guru(df):
            df.to_excel(FILE_GURU, index=False)
            st.cache_data.clear()

        def add_guru(df, data_guru):
            if str(data_guru['No Induk Pegawai']) in df['No Induk Pegawai'].astype(str).values:
                st.error(f"❌ No Induk Pegawai *{data_guru['No Induk Pegawai']}* sudah terdaftar. Data tidak ditambahkan.")
                return df, False

            new_data = data_guru
            df_new = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_guru(df_new)
            return df_new, True

        # Load data
        df_guru = load_guru()

        # Initialize session state untuk form data guru
        if 'form_guru_data' not in st.session_state:
            st.session_state.form_guru_data = {
                # Data Pribadi
                'nama_lengkap': '', 'tempat_lahir': '', 'tanggal_lahir': date.today().replace(year=date.today().year-30),
                'jenis_kelamin': 'Laki-laki', 'no_induk_pegawai': '', 'nuptk': '', 'email': '',
                'status_pernikahan': 'Belum Menikah', 'status_kepegawaian': 'GTY', 
                'jabatan_terakhir': 'Guru', 'golongan_darah': 'A', 'no_hp': '', 'no_hp_pasangan': '',
                'sosial_media': '', 'alamat_domisili': '', 'alamat_ktp': '', 
                'mulai_bekerja': date.today(), 'masa_kerja': '', 
                'sk_pengangkatan_tetap': '', 'sk_pengangkatan_tidak_tetap': '', 'sk_pengangkatan_jabatan': '',
                'foto': None,
                
                # Data Keluarga
                'nama_pasangan': '', 'jumlah_anak': 0, 'nama_anak1': '', 'nama_anak2': '', 'nama_anak3': '',
                'kontak_darurat_nama': '', 'kontak_darurat_hubungan': '', 'kontak_darurat_no': '',
                
                # Data Bank
                'nama_bank': '', 'no_rekening': '', 'atas_nama_rekening': '',
                
                # Data Pendidikan
                'pendidikan_terakhir': 'S1', 'jurusan': '', 'nama_sekolah': '', 'tahun_lulus': date.today().year
            }

        # Tampilkan konten berdasarkan submenu yang dipilih
        submenu_guru_aktif = st.session_state.submenu_guru_choice

        if submenu_guru_aktif == "👨‍🏫 Tambah Data Guru & Karyawan":
            st.subheader("👨‍🏫 Tambah Data Guru & Karyawan")
            
            with st.form("form_guru"):
                st.markdown("### 📋 DATA PRIBADI")
                
                # Tab untuk organisasi yang lebih baik
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "Data Pribadi", "Data Kontak & Alamat", "Data Kepegawaian", 
                    "Data Keluarga & Pendidikan", "Data Bank"
                ])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        # Data dasar
                        st.session_state.form_guru_data['nama_lengkap'] = st.text_input(
                            "Nama Lengkap*", 
                            value=st.session_state.form_guru_data['nama_lengkap'],
                            placeholder="Contoh: Dr. Ahmad Budiman, M.Pd"
                        )
                        st.session_state.form_guru_data['tempat_lahir'] = st.text_input(
                            "Tempat Lahir*", 
                            value=st.session_state.form_guru_data['tempat_lahir'],
                            placeholder="Contoh: Jakarta"
                        )
                        st.session_state.form_guru_data['tanggal_lahir'] = st.date_input(
                            "Tanggal Lahir*", 
                            value=st.session_state.form_guru_data['tanggal_lahir']
                        )
                        st.session_state.form_guru_data['jenis_kelamin'] = st.selectbox(
                            "Jenis Kelamin*", 
                            ["Laki-laki", "Perempuan"],
                            index=0 if st.session_state.form_guru_data['jenis_kelamin'] == 'Laki-laki' else 1
                        )
                        st.session_state.form_guru_data['golongan_darah'] = st.selectbox(
                            "Golongan Darah", 
                            ["A", "B", "AB", "O", "Tidak Tahu"],
                            index=["A", "B", "AB", "O", "Tidak Tahu"].index(st.session_state.form_guru_data['golongan_darah'])
                        )
                        
                    with col2:
                        # Data identitas
                        st.session_state.form_guru_data['no_induk_pegawai'] = st.text_input(
                            "No Induk Pegawai*", 
                            value=st.session_state.form_guru_data['no_induk_pegawai'],
                            placeholder="Contoh: PGW2024001"
                        )
                        st.session_state.form_guru_data['nuptk'] = st.text_input(
                            "NUPTK", 
                            value=st.session_state.form_guru_data['nuptk'],
                            placeholder="Nomor Unik Pendidik dan Tenaga Kependidikan"
                        )
                        st.session_state.form_guru_data['email'] = st.text_input(
                            "E-Mail", 
                            value=st.session_state.form_guru_data['email'],
                            placeholder="contoh@email.com"
                        )
                        st.session_state.form_guru_data['status_pernikahan'] = st.selectbox(
                            "Status Pernikahan", 
                            ["Belum Menikah", "Menikah", "Cerai"],
                            index=["Belum Menikah", "Menikah", "Cerai"].index(st.session_state.form_guru_data['status_pernikahan'])
                        )
                
                with tab2:
                    col3, col4 = st.columns(2)
                    with col3:
                        # Data kontak
                        st.session_state.form_guru_data['no_hp'] = st.text_input(
                            "Nomor HP/WA*", 
                            value=st.session_state.form_guru_data['no_hp'],
                            placeholder="Contoh: 081234567890"
                        )
                        st.session_state.form_guru_data['no_hp_pasangan'] = st.text_input(
                            "Nomor HP/WA Pasangan", 
                            value=st.session_state.form_guru_data['no_hp_pasangan'],
                            placeholder="Nomor telepon pasangan"
                        )
                        st.session_state.form_guru_data['sosial_media'] = st.text_input(
                            "Sosial Media (IG, FB, Tiktok dll)", 
                            value=st.session_state.form_guru_data['sosial_media'],
                            placeholder="Contoh: @username"
                        )
                        
                    with col4:
                        # Data alamat
                        st.session_state.form_guru_data['alamat_domisili'] = st.text_area(
                            "Alamat Domisili*", 
                            value=st.session_state.form_guru_data['alamat_domisili'],
                            placeholder="Alamat tempat tinggal saat ini",
                            height=80
                        )
                        st.session_state.form_guru_data['alamat_ktp'] = st.text_area(
                            "Alamat Berdasarkan KTP*", 
                            value=st.session_state.form_guru_data['alamat_ktp'],
                            placeholder="Alamat sesuai KTP (jika berbeda)",
                            height=80
                        )
                
                with tab3:
                    col5, col6 = st.columns(2)
                    with col5:
                        # Data kepegawaian
                        st.session_state.form_guru_data['status_kepegawaian'] = st.selectbox(
                            "Status Kepegawaian*", 
                            ["GTY", "GTTY", "Honorer"],
                            index=["GTY", "GTTY", "Honorer"].index(st.session_state.form_guru_data['status_kepegawaian'])
                        )
                        st.session_state.form_guru_data['jabatan_terakhir'] = st.selectbox(
                            "Jabatan Terakhir*", 
                            [
                                "Kepala Sekolah", "Wakil Kepala Sekolah", "Koordinator Agama", 
                                "Marketing", "HRD", "R&D", "Operator Dapodik", "Kepala Finance", 
                                "Staff Finance", "Guru", "Support Team"
                            ],
                            index=[
                                "Kepala Sekolah", "Wakil Kepala Sekolah", "Koordinator Agama", 
                                "Marketing", "HRD", "R&D", "Operator Dapodik", "Kepala Finance", 
                                "Staff Finance", "Guru", "Support Team"
                            ].index(st.session_state.form_guru_data['jabatan_terakhir'])
                        )
                        st.session_state.form_guru_data['mulai_bekerja'] = st.date_input(
                            "Mulai Bekerja di Pelita Insani*", 
                            value=st.session_state.form_guru_data['mulai_bekerja']
                        )
                        
                    with col6:
                        # Data SK
                        st.session_state.form_guru_data['sk_pengangkatan_tetap'] = st.text_input(
                            "SK Pengangkatan Karyawan Tetap", 
                            value=st.session_state.form_guru_data['sk_pengangkatan_tetap'],
                            placeholder="Nomor SK"
                        )
                        st.session_state.form_guru_data['sk_pengangkatan_tidak_tetap'] = st.text_input(
                            "SK Pengangkatan Karyawan Tidak Tetap", 
                            value=st.session_state.form_guru_data['sk_pengangkatan_tidak_tetap'],
                            placeholder="Nomor SK"
                        )
                        st.session_state.form_guru_data['sk_pengangkatan_jabatan'] = st.text_input(
                            "SK Pengangkatan Jabatan", 
                            value=st.session_state.form_guru_data['sk_pengangkatan_jabatan'],
                            placeholder="Nomor SK"
                        )
                    
                    # Upload foto
                    uploaded_foto = st.file_uploader("Upload Foto", type=['jpg', 'jpeg', 'png'], key="foto_guru")
                    if uploaded_foto:
                        st.session_state.form_guru_data['foto'] = uploaded_foto
                        st.image(uploaded_foto, width=150, caption="Preview Foto")
                    elif st.session_state.form_guru_data['foto'] and hasattr(st.session_state.form_guru_data['foto'], 'getvalue'):
                        st.image(st.session_state.form_guru_data['foto'], width=150, caption="Foto yang akan diupload")
                
                with tab4:
                    col7, col8 = st.columns(2)
                    with col7:
                        # Data keluarga
                        st.session_state.form_guru_data['nama_pasangan'] = st.text_input(
                            "Nama Pasangan", 
                            value=st.session_state.form_guru_data['nama_pasangan'],
                            placeholder="Nama lengkap pasangan"
                        )
                        st.session_state.form_guru_data['jumlah_anak'] = st.number_input(
                            "Jumlah Anak", 
                            min_value=0, max_value=10, 
                            value=st.session_state.form_guru_data['jumlah_anak']
                        )
                        if st.session_state.form_guru_data['jumlah_anak'] >= 1:
                            st.session_state.form_guru_data['nama_anak1'] = st.text_input(
                                "Nama Anak 1", 
                                value=st.session_state.form_guru_data['nama_anak1']
                            )
                        if st.session_state.form_guru_data['jumlah_anak'] >= 2:
                            st.session_state.form_guru_data['nama_anak2'] = st.text_input(
                                "Nama Anak 2", 
                                value=st.session_state.form_guru_data['nama_anak2']
                            )
                        if st.session_state.form_guru_data['jumlah_anak'] >= 3:
                            st.session_state.form_guru_data['nama_anak3'] = st.text_input(
                                "Nama Anak 3", 
                                value=st.session_state.form_guru_data['nama_anak3']
                            )
                        
                        # Kontak darurat
                        st.markdown("#### 📞 Kontak Darurat")
                        st.session_state.form_guru_data['kontak_darurat_nama'] = st.text_input(
                            "Nama Kontak Darurat", 
                            value=st.session_state.form_guru_data['kontak_darurat_nama']
                        )
                        st.session_state.form_guru_data['kontak_darurat_hubungan'] = st.text_input(
                            "Hubungan", 
                            value=st.session_state.form_guru_data['kontak_darurat_hubungan']
                        )
                        st.session_state.form_guru_data['kontak_darurat_no'] = st.text_input(
                            "No HP Darurat", 
                            value=st.session_state.form_guru_data['kontak_darurat_no']
                        )
                    
                    with col8:
                        # Data pendidikan
                        st.markdown("#### 🎓 Data Pendidikan")
                        st.session_state.form_guru_data['pendidikan_terakhir'] = st.selectbox(
                            "Pendidikan Terakhir", 
                            ["SMA/Sederajat", "D3", "S1", "S2", "S3"],
                            index=["SMA/Sederajat", "D3", "S1", "S2", "S3"].index(st.session_state.form_guru_data['pendidikan_terakhir'])
                        )
                        st.session_state.form_guru_data['jurusan'] = st.text_input(
                            "Jurusan", 
                            value=st.session_state.form_guru_data['jurusan'],
                            placeholder="Contoh: Pendidikan Matematika"
                        )
                        st.session_state.form_guru_data['nama_sekolah'] = st.text_input(
                            "Nama Sekolah/Universitas", 
                            value=st.session_state.form_guru_data['nama_sekolah'],
                            placeholder="Nama institusi pendidikan"
                        )
                        st.session_state.form_guru_data['tahun_lulus'] = st.number_input(
                            "Tahun Lulus", 
                            min_value=1950, max_value=date.today().year,
                            value=st.session_state.form_guru_data['tahun_lulus']
                        )
                
                with tab5:
                    st.markdown("#### 💳 Data Bank")
                    col9, col10 = st.columns(2)
                    with col9:
                        st.session_state.form_guru_data['nama_bank'] = st.text_input(
                            "Nama Bank", 
                            value=st.session_state.form_guru_data['nama_bank'],
                            placeholder="Contoh: BCA, Mandiri, BNI"
                        )
                        st.session_state.form_guru_data['no_rekening'] = st.text_input(
                            "Nomor Rekening", 
                            value=st.session_state.form_guru_data['no_rekening'],
                            placeholder="Nomor rekening bank"
                        )
                    with col10:
                        st.session_state.form_guru_data['atas_nama_rekening'] = st.text_input(
                            "Atas Nama Rekening", 
                            value=st.session_state.form_guru_data['atas_nama_rekening'],
                            placeholder="Nama pemilik rekening"
                        )
                
                st.markdown("*Keterangan:* * = Wajib diisi")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    simpan_guru = st.form_submit_button("💾 Simpan Data Guru/Karyawan", use_container_width=True)
                with col_btn2:
                    reset_form = st.form_submit_button("🔄 Reset Form", use_container_width=True)
                
                if reset_form:
                    # Reset form data
                    st.session_state.form_guru_data = {
                        'nama_lengkap': '', 'tempat_lahir': '', 'tanggal_lahir': date.today().replace(year=date.today().year-30),
                        'jenis_kelamin': 'Laki-laki', 'no_induk_pegawai': '', 'nuptk': '', 'email': '',
                        'status_pernikahan': 'Belum Menikah', 'status_kepegawaian': 'GTY', 
                        'jabatan_terakhir': 'Guru', 'golongan_darah': 'A', 'no_hp': '', 'no_hp_pasangan': '',
                        'sosial_media': '', 'alamat_domisili': '', 'alamat_ktp': '', 
                        'mulai_bekerja': date.today(), 'masa_kerja': '', 
                        'sk_pengangkatan_tetap': '', 'sk_pengangkatan_tidak_tetap': '', 'sk_pengangkatan_jabatan': '',
                        'foto': None,
                        'nama_pasangan': '', 'jumlah_anak': 0, 'nama_anak1': '', 'nama_anak2': '', 'nama_anak3': '',
                        'kontak_darurat_nama': '', 'kontak_darurat_hubungan': '', 'kontak_darurat_no': '',
                        'nama_bank': '', 'no_rekening': '', 'atas_nama_rekening': '',
                        'pendidikan_terakhir': 'S1', 'jurusan': '', 'nama_sekolah': '', 'tahun_lulus': date.today().year
                    }
                    st.success("Form berhasil direset!")
                    rerun()
                
                if simpan_guru:
                    # Validasi data wajib
                    data = st.session_state.form_guru_data
                    wajib_diisi = [
                        data['nama_lengkap'], data['tempat_lahir'], data['jenis_kelamin'],
                        data['no_induk_pegawai'], data['status_kepegawaian'], data['jabatan_terakhir'],
                        data['no_hp'], data['alamat_domisili'], data['alamat_ktp'], data['mulai_bekerja']
                    ]
                    
                    if all(wajib_diisi):
                        # Validasi No Induk Pegawai unik
                        if str(data['no_induk_pegawai']) in df_guru['No Induk Pegawai'].astype(str).values:
                            st.error(f"❌ No Induk Pegawai *{data['no_induk_pegawai']}* sudah terdaftar. Gunakan No Induk Pegawai yang berbeda.")
                        else:
                            # Konversi foto ke base64 jika ada
                            foto_base64 = None
                            if data['foto'] and hasattr(data['foto'], 'getvalue'):
                                foto_bytes = data['foto'].getvalue()
                                foto_base64 = base64.b64encode(foto_bytes).decode()
                            
                            # Hitung masa kerja
                            masa_kerja_timedelta = date.today() - data['mulai_bekerja']
                            masa_kerja_tahun = masa_kerja_timedelta.days // 365
                            masa_kerja_bulan = (masa_kerja_timedelta.days % 365) // 30
                            masa_kerja = f"{masa_kerja_tahun} tahun {masa_kerja_bulan} bulan"
                            
                            data_guru = {
                                # Data Pribadi
                                "Nama Lengkap": data['nama_lengkap'],
                                "Tempat Lahir": data['tempat_lahir'],
                                "Tanggal Lahir": data['tanggal_lahir'],
                                "Jenis Kelamin": data['jenis_kelamin'],
                                "No Induk Pegawai": data['no_induk_pegawai'],
                                "NUPTK": data['nuptk'],
                                "Email": data['email'],
                                "Status Pernikahan": data['status_pernikahan'],
                                "Status Kepegawaian": data['status_kepegawaian'],
                                "Jabatan Terakhir": data['jabatan_terakhir'],
                                "Golongan Darah": data['golongan_darah'],
                                "Nomor HP/WA": data['no_hp'],
                                "Nomor HP/WA Pasangan": data['no_hp_pasangan'],
                                "Sosial Media": data['sosial_media'],
                                "Alamat Domisili": data['alamat_domisili'],
                                "Alamat KTP": data['alamat_ktp'],
                                "Mulai Bekerja": data['mulai_bekerja'],
                                "Masa Kerja": masa_kerja,
                                "SK Pengangkatan Karyawan Tetap": data['sk_pengangkatan_tetap'],
                                "SK Pengangkatan Karyawan Tidak Tetap": data['sk_pengangkatan_tidak_tetap'],
                                "SK Pengangkatan Jabatan": data['sk_pengangkatan_jabatan'],
                                "Foto": foto_base64,
                                
                                # Data Keluarga
                                "Nama Pasangan": data['nama_pasangan'],
                                "Jumlah Anak": data['jumlah_anak'],
                                "Nama Anak 1": data['nama_anak1'],
                                "Nama Anak 2": data['nama_anak2'],
                                "Nama Anak 3": data['nama_anak3'],
                                "Kontak Darurat Nama": data['kontak_darurat_nama'],
                                "Kontak Darurat Hubungan": data['kontak_darurat_hubungan'],
                                "Kontak Darurat No HP": data['kontak_darurat_no'],
                                
                                # Data Bank
                                "Nama Bank": data['nama_bank'],
                                "Nomor Rekening": data['no_rekening'],
                                "Atas Nama Rekening": data['atas_nama_rekening'],
                                
                                # Data Pendidikan
                                "Pendidikan Terakhir": data['pendidikan_terakhir'],
                                "Jurusan": data['jurusan'],
                                "Nama Sekolah/Universitas": data['nama_sekolah'],
                                "Tahun Lulus": data['tahun_lulus']
                            }
                            
                            df_guru_new, success = add_guru(df_guru, data_guru)
                            
                            if success:
                                st.success("✅ Data guru/karyawan berhasil disimpan!")
                                # Reset form setelah berhasil disimpan
                                st.session_state.form_guru_data = {
                                    'nama_lengkap': '', 'tempat_lahir': '', 'tanggal_lahir': date.today().replace(year=date.today().year-30),
                                    'jenis_kelamin': 'Laki-laki', 'no_induk_pegawai': '', 'nuptk': '', 'email': '',
                                    'status_pernikahan': 'Belum Menikah', 'status_kepegawaian': 'GTY', 
                                    'jabatan_terakhir': 'Guru', 'golongan_darah': 'A', 'no_hp': '', 'no_hp_pasangan': '',
                                    'sosial_media': '', 'alamat_domisili': '', 'alamat_ktp': '', 
                                    'mulai_bekerja': date.today(), 'masa_kerja': '', 
                                    'sk_pengangkatan_tetap': '', 'sk_pengangkatan_tidak_tetap': '', 'sk_pengangkatan_jabatan': '',
                                    'foto': None,
                                    'nama_pasangan': '', 'jumlah_anak': 0, 'nama_anak1': '', 'nama_anak2': '', 'nama_anak3': '',
                                    'kontak_darurat_nama': '', 'kontak_darurat_hubungan': '', 'kontak_darurat_no': '',
                                    'nama_bank': '', 'no_rekening': '', 'atas_nama_rekening': '',
                                    'pendidikan_terakhir': 'S1', 'jurusan': '', 'nama_sekolah': '', 'tahun_lulus': date.today().year
                                }
                                df_guru = df_guru_new
                                rerun()
                    else:
                        st.error("❌ Semua field yang bertanda * wajib diisi!")
                        # Tampilkan field yang masih kosong
                        fields_kosong = []
                        if not data['nama_lengkap']: fields_kosong.append("Nama Lengkap")
                        if not data['tempat_lahir']: fields_kosong.append("Tempat Lahir")
                        if not data['no_induk_pegawai']: fields_kosong.append("No Induk Pegawai")
                        if not data['status_kepegawaian']: fields_kosong.append("Status Kepegawaian")
                        if not data['jabatan_terakhir']: fields_kosong.append("Jabatan Terakhir")
                        if not data['no_hp']: fields_kosong.append("Nomor HP/WA")
                        if not data['alamat_domisili']: fields_kosong.append("Alamat Domisili")
                        if not data['alamat_ktp']: fields_kosong.append("Alamat KTP")
                        if not data['mulai_bekerja']: fields_kosong.append("Mulai Bekerja")
                        
                        if fields_kosong:
                            st.warning(f"Field berikut masih kosong: {', '.join(fields_kosong)}")

            # Preview Data yang Akan Disimpan
            st.divider()
            st.subheader("👁 Preview Data")
            
            if st.session_state.form_guru_data['nama_lengkap']:
                col_preview1, col_preview2 = st.columns(2)
                with col_preview1:
                    st.write("*Data Pribadi:*")
                    st.write(f"*Nama:* {st.session_state.form_guru_data['nama_lengkap']}")
                    st.write(f"*TTL:* {st.session_state.form_guru_data['tempat_lahir']}, {st.session_state.form_guru_data['tanggal_lahir']}")
                    st.write(f"*Jabatan:* {st.session_state.form_guru_data['jabatan_terakhir']}")
                    st.write(f"*Status:* {st.session_state.form_guru_data['status_kepegawaian']}")
                
                with col_preview2:
                    st.write("*Kontak:*")
                    st.write(f"*No HP:* {st.session_state.form_guru_data['no_hp']}")
                    st.write(f"*Mulai Bekerja:* {st.session_state.form_guru_data['mulai_bekerja']}")
                    if st.session_state.form_guru_data['nama_pasangan']:
                        st.write(f"*Pasangan:* {st.session_state.form_guru_data['nama_pasangan']}")
            else:
                st.info("Isi form di atas untuk melihat preview data")

        else:
            # Fungsi untuk menampilkan data guru/karyawan
            def tampilkan_data_guru(jenis_filter=None):
                if jenis_filter == "📋 Data Guru":
                    df_filtered = df_guru[df_guru['Jabatan Terakhir'].str.contains('Guru|Kepala Sekolah|Wakil|Koordinator', na=False)]
                    judul = "Data Guru"
                elif jenis_filter == "👨‍💼 Data Karyawan":
                    df_filtered = df_guru[~df_guru['Jabatan Terakhir'].str.contains('Guru|Kepala Sekolah|Wakil|Koordinator', na=False)]
                    judul = "Data Karyawan"
                else:  # Semua Data
                    df_filtered = df_guru
                    judul = "Semua Data Guru & Karyawan"
                
                st.subheader(judul)
                
                if not df_filtered.empty:
                    st.dataframe(df_filtered[['Nama Lengkap', 'No Induk Pegawai', 'Jabatan Terakhir', 'Status Kepegawaian', 'Nomor HP/WA']], 
                            use_container_width=True)
                else:
                    st.info(f"Belum ada data {judul.lower()} yang dicatat.")
            
            # Tampilkan data berdasarkan submenu
            if submenu_guru_aktif in ["📋 Data Guru", "👨‍💼 Data Karyawan", "👥 Semua Data"]:
                tampilkan_data_guru(submenu_guru_aktif)

    else:
        st.info("Pilih menu dari sidebar untuk mulai menggunakan aplikasi.")

