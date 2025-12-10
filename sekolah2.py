import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date, datetime, timedelta
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from io import BytesIO
import base64

# ==================== KONFIGURASI FULL SCREEN ====================
st.set_page_config(
    page_title="Aplikasi Manajemen Sekolah",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== KONFIGURASI STYLING FULL SCREEN ====================
# DISABLE DULU UNTUK DEBUG
# st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
# st.markdown("""<script> ... </script>""", unsafe_allow_html=True)
# st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

/* Reset dasar untuk full width */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #f9fafb !important;
    color: #1e293b !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* Container utama full width */
[data-testid="stAppViewContainer"] { 
    background-color: #f9fafb !important;
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}

/* Main content area */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 100% !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0;
    box-shadow: 2px 0 6px rgba(0,0,0,0.04);
    min-width: 280px !important;
}

/* Header styling */
h1, h2, h3, h4 {
    color: #1d4ed8 !important;
    font-weight: 600;
}

/* Container blocks */
div[data-testid="stVerticalBlock"] {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
    width: 100% !important;
}

/* PERBAIKAN UTAMA: Metrics styling yang lebih baik untuk angka panjang */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    padding: 1.2rem !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    border: 1px solid #e2e8f0 !important;
    width: 100% !important;
    min-height: 100px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    text-align: center !important;
}

[data-testid="stMetricLabel"] { 
    color: #475569 !important; 
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.3rem !important;
    line-height: 1.2 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    max-width: 100% !important;
}

[data-testid="stMetricValue"] { 
    color: #0f172a !important; 
    font-weight: 700 !important;
    font-size: 1.6rem !important;
    line-height: 1.1 !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: unset !important;
    max-width: 100% !important;
    word-wrap: normal !important;
    letter-spacing: -0.5px !important;
}

[data-testid="stMetricDelta"] {
    font-size: 0.9rem !important;
    white-space: nowrap !important;
}

/* Custom metric container untuk angka yang panjang - PERBAIKAN LAYOUT */
.metric-container {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    text-align: center;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.metric-label {
    color: #475569;
    font-size: 0.95rem;
    font-weight: 500;
    margin-bottom: 0.3rem;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}

.metric-value {
    color: #0f172a;
    font-weight: 700;
    font-size: 1.6rem;
    line-height: 1.1;
    white-space: nowrap;
    overflow: visible;
    text-overflow: unset;
    max-width: 100%;
    word-wrap: normal;
    letter-spacing: -0.5px;
}

/* Button styling */
button[kind="primary"], .stButton>button {
    background-color: #0078d4 !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 500 !important;
    width: 100% !important;
}

/* Tabs styling */
div[data-baseweb="tab-list"] {
    background-color: #e0f2fe;
    border-radius: 10px;
    padding: 6px;
    width: 100% !important;
}

div[data-baseweb="tab"] {
    color: #0369a1 !important;
    font-weight: 500;
    border-radius: 8px;
    padding: 0.8rem 1.2rem !important;
    flex: 1 !important;
}

div[data-baseweb="tab"][aria-selected="true"] {
    background-color: #0369a1 !important;
    color: white !important;
}

/* Form elements */
input, select, textarea {
    border-radius: 6px !important;
    border: 1px solid #cbd5e1 !important;
    width: 100% !important;
}

/* Dataframe styling */
.stDataFrame {
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    width: 100% !important;
}

/* Column spacing */
[data-testid="column"] {
    padding: 0.5rem !important;
    gap: 0.5rem !important;
}

/* Remove default padding and margins */
[data-testid="stHeader"] { 
    background: none !important; 
    padding: 0 !important;
}

/* Full width for all containers */
.css-1r6slb0, .css-12oz5g7, .css-1v0mbdj, .css-1wrcr25 {
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Responsive adjustments for mobile */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    [data-testid="column"] {
        width: 100% !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
    
    .metric-value {
        font-size: 1.4rem !important;
    }
    
    [data-testid="stMetric"] {
        min-height: 90px !important;
        padding: 1rem !important;
    }
    
    .metric-container {
        min-height: 90px !important;
        padding: 1rem !important;
    }
}

/* Custom full-width classes */
.full-width {
    width: 100% !important;
    max-width: 100% !important;
}

.container-fluid {
    width: 100% !important;
    padding-right: 15px !important;
    padding-left: 15px !important;
    margin-right: auto !important;
    margin-left: auto !important;
}

/* Streamlit specific full-width fixes */
.st-emotion-cache-1jicfl2 {
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* Remove any max-width restrictions */
.st-emotion-cache-1wrcr25 {
    max-width: none !important;
}

/* Expand dataframe to full width */
.dataframe {
    width: 100% !important;
}

/* Make sure all content containers are full width */
.element-container {
    width: 100% !important;
    max-width: 100% !important;
}

/* Fix for metric containers */
[data-testid="metric-container"] {
    width: 100% !important;
}

/* Full width form containers */
.stForm {
    width: 100% !important;
}

/* Radio button groups full width */
.stRadio > div {
    width: 100% !important;
}

.stRadio > div > label {
    width: 100% !important;
    justify-content: flex-start !important;
}

/* Selectbox full width */
.stSelectbox {
    width: 100% !important;
}

/* Date input full width */
.stDateInput {
    width: 100% !important;
}

/* Number input full width */
.stNumberInput {
    width: 100% !important;
}

/* Text input full width */
.stTextInput {
    width: 100% !important;
}

/* Text area full width */
.stTextArea {
    width: 100% !important;
}

/* File uploader full width */
.stFileUploader {
    width: 100% !important;
}

/* Download button full width */
.stDownloadButton {
    width: 100% !important;
}

.stDownloadButton button {
    width: 100% !important;
}

/* Custom styling untuk angka yang panjang */
.large-number {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    line-height: 1.1 !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

.compact-metric {
    min-height: 100px !important;
    padding: 1.2rem !important;
}

/* PERBAIKAN: Layout khusus untuk ringkasan keuangan */
.keuangan-summary {
    display: flex !important;
    justify-content: space-between !important;
    gap: 1rem !important;
    width: 100% !important;
}

.keuangan-card {
    flex: 1 !important;
    min-width: 0 !important;
}

/* PERBAIKAN: Placeholder selectbox kosong */
.stSelectbox > div > div > div {
    color: #64748b !important;
}

</style>
""", unsafe_allow_html=True)

# JavaScript untuk full screen behavior
st.markdown("""
<script>
// Function to ensure full width behavior
function enforceFullWidth() {
    // Remove any max-width constraints
    const containers = document.querySelectorAll('[class*="container"]');
    containers.forEach(container => {
        container.style.maxWidth = '100%';
        container.style.width = '100%';
    });
    
    // Ensure main content area is full width
    const mainContainer = document.querySelector('.main .block-container');
    if (mainContainer) {
        mainContainer.style.maxWidth = '100%';
        mainContainer.style.paddingLeft = '3rem';
        mainContainer.style.paddingRight = '3rem';
    }
    
    // Ensure metric values are properly displayed
    const metricValues = document.querySelectorAll('[data-testid="stMetricValue"]');
    metricValues.forEach(value => {
        value.style.whiteSpace = 'nowrap';
        value.style.overflow = 'visible';
        value.style.textOverflow = unset;
    });
}

// Run on page load and when DOM changes
document.addEventListener('DOMContentLoaded', enforceFullWidth);
window.addEventListener('load', enforceFullWidth);

// Observe DOM changes for dynamic content
const observer = new MutationObserver(enforceFullWidth);
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# === FIX: Fungsi rerun kompatibel untuk semua versi ===
def rerun():
    """Reruns the current Streamlit app."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# ==================== FUNGSI FORMAT RUPIAH YANG DIPERBAIKI ====================
def format_rupiah(x):
    """Format angka menjadi format Rupiah lengkap"""
    if pd.isna(x) or x == 0:
        return "Rp 0"
    
    # Format lengkap tanpa singkatan
    return f"Rp {x:,.0f}".replace(",", "_").replace(".", ",").replace("_", ".")

def format_rupiah_detailed(x):
    """Format angka menjadi format Rupiah lengkap untuk tabel"""
    if pd.isna(x) or x == 0:
        return "Rp 0"
    return f"Rp {x:,.0f}".replace(",", "_").replace(".", ",").replace("_", ".")

# ==================== FUNGSI CUSTOM METRIC YANG DIPERBAIKI ====================
def display_metric_custom(label, value, delta=None, help_text=None):
    """Menampilkan metric dengan custom styling untuk angka yang panjang"""
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {f'<div style="color: #16a34a; font-size: 0.9rem; margin-top: 0.3rem;">{delta}</div>' if delta else ''}
        {f'<div style="color: #64748b; font-size: 0.8rem; margin-top: 0.3rem;">{help_text}</div>' if help_text else ''}
    </div>
    """, unsafe_allow_html=True)

# ==================== FUNGSI BARU UNTUK MANAJEMEN KELAS ====================

FILE_RIWAYAT_KELAS = "riwayat_kelas.xlsx"

@st.cache_data
def load_riwayat_kelas():
    """Load riwayat perpindahan kelas"""
    if os.path.exists(FILE_RIWAYAT_KELAS):
        df = pd.read_excel(FILE_RIWAYAT_KELAS)
        if 'Tanggal' in df.columns:
            df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date
        return df
    else:
        return pd.DataFrame(columns=[
            'NISN', 'Nama', 'Jenjang', 'Kelas_Lama', 'Kelas_Baru', 
            'Tahun_Ajaran', 'Tanggal', 'Jenis', 'Keterangan'
        ])

def save_riwayat_kelas(riwayat_data):
    """Simpan riwayat perpindahan kelas"""
    df_riwayat = load_riwayat_kelas()
    
    # Jika riwayat_data adalah dict (single record)
    if isinstance(riwayat_data, dict):
        df_new = pd.concat([df_riwayat, pd.DataFrame([riwayat_data])], ignore_index=True)
    # Jika riwayat_data adalah list of dict (multiple records)
    elif isinstance(riwayat_data, list):
        df_new = pd.concat([df_riwayat, pd.DataFrame(riwayat_data)], ignore_index=True)
    else:
        st.error("Format data riwayat tidak valid")
        return
    
    df_new.to_excel(FILE_RIWAYAT_KELAS, index=False)
    st.cache_data.clear()

def get_next_class(jenjang, kelas_sekarang):
    """Mendapatkan kelas berikutnya berdasarkan jenjang dan kelas sekarang"""
    mapping_kelas = {
        "TK": {
            "PLAYGROUP": "TK A",
            "TK A": "TK B", 
            "TK B": "LULUS"
        },
        "SD": {
            "1": "2",
            "2": "3", 
            "3": "4",
            "4": "5",
            "5": "6",
            "6": "LULUS"
        },
        "SMP": {
            "1": "2",
            "2": "3", 
            "3": "LULUS"
        }
    }
    
    return mapping_kelas.get(jenjang, {}).get(kelas_sekarang, kelas_sekarang)

def bulk_update_classes(df_siswa, jenjang, kelas, tahun_ajaran):
    """Update kelas massal untuk semua siswa di jenjang dan kelas tertentu"""
    updated_count = 0
    riwayat_list = []
    
    # Filter siswa berdasarkan jenjang dan kelas yang dipilih
    siswa_filtered = df_siswa[
        (df_siswa['Jenjang Sekolah'] == jenjang) & 
        (df_siswa['Kelas'] == kelas)
    ]
    
    for _, siswa in siswa_filtered.iterrows():
        kelas_sekarang = siswa['Kelas']
        kelas_baru = get_next_class(jenjang, kelas_sekarang)
        
        if kelas_baru != kelas_sekarang:
            # Update kelas di dataframe
            df_siswa.loc[df_siswa['NISN'] == siswa['NISN'], 'Kelas'] = kelas_baru
            
            # Catat riwayat
            riwayat_data = {
                'NISN': siswa['NISN'],
                'Nama': siswa['Nama Lengkap'],
                'Jenjang': jenjang,
                'Kelas_Lama': kelas_sekarang,
                'Kelas_Baru': kelas_baru,
                'Tahun_Ajaran': tahun_ajaran,
                'Tanggal': datetime.now().date(),
                'Jenis': 'KENAIKAN',
                'Keterangan': f'Kenaikan kelas otomatis {tahun_ajaran}'
            }
            riwayat_list.append(riwayat_data)
            updated_count += 1
    
    return df_siswa, riwayat_list, updated_count

def generate_kelas_pdf_report(df_riwayat):
    """Generate PDF report untuk riwayat kelas"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Buat style untuk wrap text
    wrap_style = ParagraphStyle(
        'WrapStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=9,
        wordWrap='CJK'  # Untuk wrap text
    )
    
    wrap_style_bold = ParagraphStyle(
        'WrapStyleBold',
        parent=styles['Normal'],
        fontSize=8,
        leading=9,
        wordWrap='CJK',
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Header
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=12,
        alignment=1,
        textColor=colors.black
    )
    
    story.append(Paragraph("LAPORAN RIWAYAT PERPINDAHAN KELAS", title_style))
    story.append(Paragraph(f"Periode: {datetime.now().strftime('%d %B %Y')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    if not df_riwayat.empty:
        # Siapkan data tabel dengan Paragraph untuk wrap text
        header_data = [
            Paragraph("No", wrap_style_bold),
            Paragraph("Tanggal", wrap_style_bold),
            Paragraph("NISN", wrap_style_bold),
            Paragraph("Nama", wrap_style_bold),
            Paragraph("Jenjang", wrap_style_bold),
            Paragraph("Kelas Lama", wrap_style_bold),
            Paragraph("Kelas Baru", wrap_style_bold),
            Paragraph("Jenis", wrap_style_bold),
            Paragraph("Keterangan", wrap_style_bold)
        ]
        
        table_data = [header_data]
        for i, (_, row) in enumerate(df_riwayat.iterrows(), 1):
            # Gunakan Paragraph untuk semua sel agar text wrap bekerja
            keterangan = str(row['Keterangan'])
            if len(keterangan) > 30:
                keterangan = keterangan[:27] + "..."
            
            table_data.append([
                Paragraph(str(i), wrap_style),
                Paragraph(row['Tanggal'].strftime('%d/%m/%Y') if hasattr(row['Tanggal'], 'strftime') else str(row['Tanggal']), wrap_style),
                Paragraph(str(row['NISN']), wrap_style),
                Paragraph(str(row['Nama']), wrap_style),
                Paragraph(str(row['Jenjang']), wrap_style),
                Paragraph(str(row['Kelas_Lama']), wrap_style),
                Paragraph(str(row['Kelas_Baru']), wrap_style),
                Paragraph(str(row['Jenis']), wrap_style),
                Paragraph(keterangan, wrap_style)
            ])
        
        # Buat tabel dengan lebar kolom yang lebih fleksibel
        col_widths = [25, 50, 60, 100, 40, 50, 50, 50, 100]  # Lebar kolom diperbesar
        riwayat_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Style untuk tabel dengan wrap
        riwayat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Vertical align top untuk wrap text
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(riwayat_table)
    else:
        story.append(Paragraph("Tidak ada data riwayat", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ===================== LOGIN MANUAL =====================

# Opsi 1: Coba dari secrets.toml (untuk production)
try:
    USER_CREDENTIALS = st.secrets["credentials"]
    st.success("✅ Login menggunakan secrets.toml")
except:
    # Opsi 2: Fallback langsung (untuk development/error)
    USER_CREDENTIALS = {
        "developer_keuangan": "pass123",
        "admin1": "admin1",
        "admin2": "admin2",
        "admin3": "admin3"
    }
    st.warning("⚠️ Menggunakan kredensial default. File secrets.toml tidak ditemukan.")

# HAPUS error message lama
# st.error("Konfigurasi Error: File .streamlit/secrets.toml tidak ditemukan...")
# st.stop()  # JANGAN stop aplikasi!

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "menu_choice" not in st.session_state:
    st.session_state.menu_choice = "Keuangan"
if "submenu_choice" not in st.session_state:
    st.session_state.submenu_choice = "Tambah Data Siswa"
if "keuangan_submenu" not in st.session_state:
    st.session_state.keuangan_submenu = "Pemasukan"
if "kas_harian_submenu" not in st.session_state:
    st.session_state.kas_harian_submenu = "Riwayat Harian"

# Tampilan Login
if not st.session_state.logged_in:
    # Container untuk login form di tengah
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='container-fluid'>", unsafe_allow_html=True)
        st.title("Login Aplikasi")
        st.markdown("Gunakan username `developer_keuangan` dan password `pass123`")

        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.form_submit_button("Login", use_container_width=True)

            if submit_button:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login berhasil!")
                    rerun()
                else:
                    st.error("Username atau password salah.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # ===================== APLIKASI UTAMA =====================
    
    # Container utama dengan full width
    st.markdown("<div class='container-fluid'>", unsafe_allow_html=True)
    
    # Header dengan informasi user
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.title("Aplikasi Manajemen Data & Keuangan")
    with col_header2:
        st.success(f"Selamat datang, **{st.session_state.username}**")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### Halo, **{st.session_state.username}**")
        st.divider() 

        # Menu utama - gunakan callback untuk update session state
        def update_menu_choice():
            st.session_state.menu_choice = st.session_state.sidebar_menu_widget

        pilihan = st.radio(
            "Pilih Menu:", 
            ["Keuangan", "Data Siswa", "Laporan"], 
            key="sidebar_menu_widget",
            on_change=update_menu_choice
        )

        # Submenu untuk Data Siswa
        if pilihan == "Data Siswa":
            st.divider()
            st.markdown("**Kelola Data Siswa:**")
            
            def update_submenu_choice():
                st.session_state.submenu_choice = st.session_state.submenu_widget
            
            submenu = st.radio(
                "Pilih Submenu:",
                ["Tambah Data Siswa", "Kenaikan Kelas", "Data TK", "Data SD", "Data SMP", "Semua Siswa"],
                key="submenu_widget",
                on_change=update_submenu_choice
            )

        # Submenu untuk Keuangan
        elif pilihan == "Keuangan":
            st.divider()
            st.markdown("**Kelola Keuangan:**")
            
            def update_keuangan_submenu():
                st.session_state.keuangan_submenu = st.session_state.keuangan_submenu_widget
            
            keuangan_submenu = st.radio(
                "Pilih Submenu:",
                ["Pemasukan", "Pengeluaran", "Kas Harian"],
                key="keuangan_submenu_widget",
                on_change=update_keuangan_submenu
            )

        # Submenu untuk Laporan
        elif pilihan == "Laporan":
            st.divider()
            st.markdown("**Cetak Laporan:**")
            
            def update_laporan_submenu():
                st.session_state.laporan_submenu = st.session_state.laporan_submenu_widget
            
            laporan_submenu = st.radio(
                "Pilih Laporan:",
                ["Buku Kas Harian", "Laporan Keuangan", "Jurnal Per Siswa", 
                 "Rekap Individual", "Rekap Per Unit", "Rekap Per Kelas"],
                key="laporan_submenu_widget",
                on_change=update_laporan_submenu
            )

        st.divider()

        if st.button("Keluar", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.menu_choice = "Keuangan" 
            st.session_state.submenu_choice = "Tambah Data Siswa"
            st.session_state.keuangan_submenu = "Pemasukan"
            st.session_state.kas_harian_submenu = "Riwayat Harian"
            rerun()

    # Konten utama berdasarkan pilihan menu
    pilihan_aktif = st.session_state.menu_choice 

    # ==================== MENU KEUANGAN ====================
    if pilihan_aktif == "Keuangan":
        # File paths
        FILE_PATH = "transaksi_keuangan.xlsx"
        FILE_SISWA = "data_siswa.xlsx"
        FILE_SPP = "pembayaran_spp.xlsx"
        FILE_KAS_HARIAN = "kas_harian.xlsx"

        # Load data functions
        @st.cache_data
        def load_data():
            if os.path.exists(FILE_PATH):
                df = pd.read_excel(FILE_PATH)
                df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date
                return df
            else:
                return pd.DataFrame(columns=["Tanggal", "Kategori", "Jumlah", "Jenis", "Deskripsi", "Tipe_Keuangan", "NISN"])

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

        @st.cache_data
        def load_kas_harian():
            if os.path.exists(FILE_KAS_HARIAN):
                df = pd.read_excel(FILE_KAS_HARIAN)
                df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date
                return df
            else:
                return pd.DataFrame(columns=["Tanggal", "Kategori", "Jumlah", "Jenis", "Deskripsi"])

        def save_data(df):
            df.to_excel(FILE_PATH, index=False)
            st.cache_data.clear()

        def save_spp(df):
            df.to_excel(FILE_SPP, index=False)
            st.cache_data.clear()

        def save_kas_harian(df):
            df.to_excel(FILE_KAS_HARIAN, index=False)
            st.cache_data.clear()

        def add_transaction(df, tanggal, kategori, jumlah, jenis, deskripsi, tipe_keuangan, nisn=None):
            # PERBAIKAN: Hilangkan template otomatis untuk deskripsi
            # Jika deskripsi kosong atau masih berisi template, ganti dengan kategori saja
            if not deskripsi or deskripsi.strip() == "":
                deskripsi = kategori
            elif "-" in deskripsi and deskripsi.strip().startswith(kategori):
                # Jika ada template otomatis, ambil hanya bagian setelah tanda strip pertama
                parts = deskripsi.split("-", 1)
                if len(parts) > 1:
                    deskripsi = parts[1].strip()
                else:
                    deskripsi = kategori
            
            new_data = {
                "Tanggal": tanggal,
                "Kategori": kategori,
                "Jumlah": float(jumlah),
                "Jenis": jenis,
                "Deskripsi": deskripsi,
                "Tipe_Keuangan": tipe_keuangan,
                "NISN": nisn
            }
            df_new = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df_new)
            return df_new

        def add_kas_harian(df_kas, tanggal, kategori, jumlah, jenis, deskripsi):
            # PERBAIKAN: Hilangkan template otomatis untuk deskripsi
            # Jika deskripsi kosong atau masih berisi template, ganti dengan kategori saja
            if not deskripsi or deskripsi.strip() == "":
                deskripsi = kategori
            elif "-" in deskripsi and deskripsi.strip().startswith(kategori):
                # Jika ada template otomatis, ambil hanya bagian setelah tanda strip pertama
                parts = deskripsi.split("-", 1)
                if len(parts) > 1:
                    deskripsi = parts[1].strip()
                else:
                    deskripsi = kategori
            
            new_data = {
                "Tanggal": tanggal,
                "Kategori": kategori,
                "Jumlah": float(jumlah),
                "Jenis": jenis,
                "Deskripsi": deskripsi
            }
            df_new = pd.concat([df_kas, pd.DataFrame([new_data])], ignore_index=True)
            save_kas_harian(df_new)
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

        # Load all data
        df = load_data()
        df_siswa = load_siswa()
        df_spp = load_spp()
        df_kas_harian = load_kas_harian()
        saldo, pemasukan, pengeluaran = calculate_summary(df)

        # PERBAIKAN UTAMA: Ringkasan Keuangan dengan layout yang lebih baik
        st.subheader("Ringkasan Keuangan")
        
        # Gunakan columns dengan proporsi yang lebih baik
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Gunakan st.metric dengan styling yang sudah diperbaiki
            st.metric(
                label="Saldo", 
                value=format_rupiah(saldo),
                help="Total saldo saat ini"
            )
        
        with col2:
            st.metric(
                label="Total Pemasukan", 
                value=format_rupiah(pemasukan),
                help="Total semua pemasukan"
            )
        
        with col3:
            st.metric(
                label="Total Pengeluaran", 
                value=format_rupiah(pengeluaran),
                help="Total semua pengeluaran"
            )

        # ========== SUBMENU KEUANGAN ==========
        keuangan_submenu_aktif = st.session_state.keuangan_submenu

        # ==================== SUBMENU PEMASUKAN ====================
        if keuangan_submenu_aktif == "Pemasukan":
            st.subheader("Pemasukan")
            
            # Container untuk form pemasukan
            with st.container():
                kategori_pemasukan = st.selectbox(
                    "Pilih Kategori Pemasukan:",
                    [
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
                        "Administrasi Kelulusan",  # Kategori baru ditambahkan
                        "Fieldtrip"  # Kategori baru ditambahkan
                    ]
                )
                
                if kategori_pemasukan == "Uang Sumbangan Pendidikan (SPP)":
                    st.subheader("Pembayaran SPP")
                    
                    if not df_siswa.empty:
                        col_search1, col_search2 = st.columns([2, 1])
                        with col_search1:
                            pencarian = st.text_input("Cari Siswa (NISN atau Nama)", key="pencarian_spp")
                        
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
                            
                            st.info(f"Siswa Terpilih: {selected_siswa['Nama Lengkap']} (NISN: {selected_siswa['NISN']}, Kelas: {selected_siswa['Kelas']}, Jenjang: {selected_siswa['Jenjang Sekolah']})")
                            
                            riwayat_spp = df_spp[df_spp['NISN'] == selected_siswa['NISN']]
                            if not riwayat_spp.empty:
                                st.subheader("Riwayat Pembayaran SPP")
                                # Format angka dalam dataframe
                                riwayat_spp_display = riwayat_spp.copy()
                                riwayat_spp_display['Jumlah'] = riwayat_spp_display['Jumlah'].apply(format_rupiah_detailed)
                                st.dataframe(riwayat_spp_display.sort_values(by="Bulan_Tagihan", ascending=False), use_container_width=True)
                            
                            with st.form("form_spp"):
                                colA, colB = st.columns(2)
                                bulan_tagihan = colA.date_input("Bulan Tagihan", value=date.today().replace(day=1), key="bulan_tagihan")
                                
                                if selected_siswa['Jenjang Sekolah'] == "TK":
                                    jumlah_default = 300000.0
                                elif selected_siswa['Jenjang Sekolah'] == "SD":
                                    jumlah_default = 400000.0
                                else:
                                    jumlah_default = 500000.0
                                    
                                jumlah_spp = colB.number_input("Jumlah SPP (Rp)", min_value=1000.0, value=jumlah_default, step=50000.0, key="jumlah_spp")
                                
                                colC, colD = st.columns(2)
                                tanggal_bayar = colC.date_input("Tanggal Bayar", value=date.today(), key="tanggal_bayar_spp")
                                keterangan = colD.text_input("Keterangan (Opsional)", key="keterangan_spp")
                                
                                submit_button = st.form_submit_button("Bayar SPP", use_container_width=True)
                                
                                if submit_button:
                                    existing_payment = df_spp[
                                        (df_spp['NISN'] == selected_siswa['NISN']) & 
                                        (df_spp['Bulan_Tagihan'] == bulan_tagihan)
                                    ]
                                    
                                    if not existing_payment.empty:
                                        st.error(f"Siswa sudah membayar SPP untuk bulan {bulan_tagihan.strftime('%B %Y')}")
                                    else:
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
                                        
                                        df = add_transaction(
                                            df,
                                            tanggal_bayar,
                                            "Uang Sumbangan Pendidikan (SPP)",
                                            jumlah_spp,
                                            "Pemasukan",
                                            f"SPP {selected_siswa['Nama Lengkap']} - {bulan_tagihan.strftime('%B %Y')}",
                                            "SPP",
                                            selected_siswa['NISN']
                                        )
                                        
                                        df_kas_harian = add_kas_harian(
                                            df_kas_harian,
                                            tanggal_bayar,
                                            "Uang Sumbangan Pendidikan (SPP)",
                                            jumlah_spp,
                                            "Pemasukan",
                                            f"SPP {selected_siswa['Nama Lengkap']} - {bulan_tagihan.strftime('%B %Y')}"
                                        )
                                        
                                        st.success("Pembayaran SPP berhasil dicatat!")
                                        rerun()
                        
                        else:
                            st.warning("Tidak ada siswa yang sesuai dengan pencarian")
                    else:
                        st.warning("Belum ada data siswa. Silakan tambah data siswa terlebih dahulu di menu Data Siswa.")
                
                else:
                    with st.form("form_pemasukan"):
                        colA, colB = st.columns(2)
                        tanggal = colA.date_input("Tanggal", value=date.today(), key="pemasukan_tanggal")
                        
                        nisn_pemasukan = None
                        deskripsi_default = ""  # PERBAIKAN: Kosongkan deskripsi default
                        
                        # PERBAIKAN: Hilangkan template otomatis di deskripsi
                        if kategori_pemasukan in ["Uang Pendaftaran", "Uang Pangkal (UP)", "Uang Buku", 
                                               "Uang Seragam", "Catering Siswa", "Jemputan Siswa",
                                               "Administrasi Kelulusan", "Fieldtrip"]:
                            if not df_siswa.empty:
                                selected_index_siswa = colB.selectbox(
                                    "Pilih Siswa",
                                    options=range(len(df_siswa)),
                                    format_func=lambda x: f"{df_siswa.iloc[x]['NISN']} - {df_siswa.iloc[x]['Nama Lengkap']}",
                                    key="select_siswa_pemasukan"
                                )
                                selected_siswa = df_siswa.iloc[selected_index_siswa]
                                nisn_pemasukan = selected_siswa['NISN']
                                # PERBAIKAN: Tidak ada template otomatis, kosongkan saja
                                deskripsi_default = ""
                            else:
                                st.warning("Belum ada data siswa")
                                deskripsi_default = ""
                        else:
                            # Untuk kategori seperti sumbangan sukarela, isi manual
                            deskripsi_default = ""
                        
                        colC, colD = st.columns(2)
                        jumlah = colC.number_input("Jumlah (Rp)", min_value=1000.0, value=100000.0, step=50000.0, key="pemasukan_jumlah")
                        deskripsi = colD.text_input("Deskripsi*", value=deskripsi_default, key="pemasukan_deskripsi", 
                                                   help="Wajib diisi. Contoh: 'Pembayaran uang pangkal', 'Sumbangan dari orang tua', dll")
                        
                        submit_button = st.form_submit_button("Tambah Pemasukan", use_container_width=True)
                        
                        if submit_button:
                            # PERBAIKAN: Validasi deskripsi tidak boleh kosong
                            if not deskripsi or deskripsi.strip() == "":
                                st.error("Deskripsi wajib diisi!")
                            else:
                                df = add_transaction(
                                    df,
                                    tanggal,
                                    kategori_pemasukan,
                                    jumlah,
                                    "Pemasukan",
                                    deskripsi,
                                    "Pemasukan",
                                    nisn_pemasukan
                                )
                                
                                df_kas_harian = add_kas_harian(
                                    df_kas_harian,
                                    tanggal,
                                    kategori_pemasukan,
                                    jumlah,
                                    "Pemasukan",
                                    deskripsi
                                )
                                
                                st.success("Data pemasukan berhasil ditambahkan!")
                                rerun()

        # ==================== SUBMENU PENGELUARAN ====================
        elif keuangan_submenu_aktif == "Pengeluaran":
            st.subheader("Pengeluaran")
            
            with st.container():
                kategori_pengeluaran = st.selectbox(
                    "Pilih Kategori Pengeluaran:",
                    [
                        "Gaji Karyawan",  # Kategori baru ditambahkan
                        "Cookery",  # Kategori baru ditambahkan
                        "Renang",  # Kategori baru ditambahkan
                        "Honor Yayasan",  # Kategori baru ditambahkan
                        "Administrasi Kelulusan",  # Kategori baru ditambahkan
                        "Fieldtrip",  # Kategori baru ditambahkan
                        "Media Pembelajaran",  # Kategori baru ditambahkan
                        "Operasional Yayasan",  # Kategori baru ditambahkan
                        "Biaya Riset & Pengembangan",  # Kategori baru ditambahkan
                        "Tunjangan Kesehatan",  # Kategori baru ditambahkan
                        "BPJS Ketenagakerjaan",  # Kategori baru ditambahkan
                        "Apresiasi Pegawai",  # Kategori baru ditambahkan
                        "Dana Sosial",  # Kategori baru ditambahkan
                        "PMB",  # Kategori baru ditambahkan
                        "Inventaris",  # Kategori baru ditambahkan
                        "Biaya Listrik, Air, dan Telepon",
                        "Biaya ATK",
                        "Biaya Perbaikan dan Pemeliharaan",
                        "Biaya Transportasi dan Perjalanan Dinas",
                        "Biaya Konsumsi dan Akomodasi",
                        "Biaya Rapat dan Rapat Kerja",
                        "Biaya Pelatihan dan Pengembangan",
                        "Biaya Iuran dan Sumbangan",
                        "Biaya Pajak",
                        "Biaya Asuransi",
                        "Biaya Sewa",
                        "Biaya Pembelian Peralatan",
                        "Biaya Pembangunan dan Renovasi"
                    ]
                )
                
                with st.form("form_pengeluaran"):
                    colA, colB = st.columns(2)
                    tanggal = colA.date_input("Tanggal", value=date.today(), key="pengeluaran_tanggal")
                    jumlah = colB.number_input("Jumlah (Rp)", min_value=1000.0, value=100000.0, step=50000.0, key="pengeluaran_jumlah")
                    
                    deskripsi = st.text_input("Deskripsi*", key="pengeluaran_deskripsi", 
                                             help="Wajib diisi. Contoh: 'Gaji guru bulan Mei', 'Pembelian ATK', dll")
                    
                    submit_button = st.form_submit_button("Tambah Pengeluaran", use_container_width=True)
                    
                    if submit_button:
                        # PERBAIKAN: Validasi deskripsi tidak boleh kosong
                        if not deskripsi or deskripsi.strip() == "":
                            st.error("Deskripsi wajib diisi!")
                        else:
                            df = add_transaction(
                                df,
                                tanggal,
                                kategori_pengeluaran,
                                jumlah,
                                "Pengeluaran",
                                deskripsi,
                                "Pengeluaran"
                            )
                            
                            df_kas_harian = add_kas_harian(
                                df_kas_harian,
                                tanggal,
                                kategori_pengeluaran,
                                jumlah,
                                "Pengeluaran",
                                deskripsi
                            )
                            
                            st.success("Data pengeluaran berhasil ditambahkan!")
                            rerun()

        # ==================== SUBMENU KAS HARIAN ====================
        elif keuangan_submenu_aktif == "Kas Harian":
            st.subheader("Kas Harian - Riwayat Transaksi")
            
            with st.container():
                kas_harian_submenu = st.radio(
                    "Pilih Periode:",
                    ["Riwayat Harian", "Riwayat Bulanan", "Riwayat Tahunan"],
                    key="kas_harian_submenu_widget"
                )
                
                if kas_harian_submenu == "Riwayat Harian":
                    st.subheader("Riwayat Transaksi Harian")
                    
                    selected_date = st.date_input("Pilih Tanggal", value=date.today())
                    
                    filtered_kas = df_kas_harian[df_kas_harian['Tanggal'] == selected_date]
                    
                    if not filtered_kas.empty:
                        total_pemasukan = filtered_kas[filtered_kas['Jenis'] == 'Pemasukan']['Jumlah'].sum()
                        total_pengeluaran = filtered_kas[filtered_kas['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
                        saldo_harian = total_pemasukan - total_pengeluaran
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Pemasukan", format_rupiah(total_pemasukan))
                        col2.metric("Total Pengeluaran", format_rupiah(total_pengeluaran))
                        col3.metric("Saldo Harian", format_rupiah(saldo_harian))
                        
                        # Format angka dalam dataframe
                        filtered_kas_display = filtered_kas.copy()
                        filtered_kas_display['Jumlah'] = filtered_kas_display['Jumlah'].apply(format_rupiah_detailed)
                        
                        st.dataframe(
                            filtered_kas_display[['Tanggal', 'Kategori', 'Jenis', 'Jumlah', 'Deskripsi']].sort_values('Jenis', ascending=False),
                            use_container_width=True
                        )
                    else:
                        st.info("Tidak ada transaksi pada tanggal yang dipilih")
                
                elif kas_harian_submenu == "Riwayat Bulanan":
                    st.subheader("Riwayat Transaksi Bulanan")
                    
                    col_bulan1, col_bulan2 = st.columns(2)
                    with col_bulan1:
                        selected_month = st.selectbox(
                            "Pilih Bulan:",
                            range(1, 13),
                            format_func=lambda x: date(2023, x, 1).strftime('%B'),
                            index=date.today().month - 1
                        )
                    with col_bulan2:
                        selected_year = st.selectbox(
                            "Pilih Tahun:",
                            range(2020, date.today().year + 2),
                            index=date.today().year - 2020
                        )
                    
                    df_kas_copy = df_kas_harian.copy()
                    df_kas_copy['Tanggal'] = pd.to_datetime(df_kas_copy['Tanggal'])
                    filtered_kas = df_kas_copy[
                        (df_kas_copy['Tanggal'].dt.year == selected_year) & 
                        (df_kas_copy['Tanggal'].dt.month == selected_month)
                    ]
                    
                    if not filtered_kas.empty:
                        total_pemasukan = filtered_kas[filtered_kas['Jenis'] == 'Pemasukan']['Jumlah'].sum()
                        total_pengeluaran = filtered_kas[filtered_kas['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
                        saldo_bulanan = total_pemasukan - total_pengeluaran
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Pemasukan", format_rupiah(total_pemasukan))
                        col2.metric("Total Pengeluaran", format_rupiah(total_pengeluaran))
                        col3.metric("Saldo Bulanan", format_rupiah(saldo_bulanan))
                        
                        # Format angka dalam dataframe
                        filtered_kas_display = filtered_kas.copy()
                        filtered_kas_display['Jumlah'] = filtered_kas_display['Jumlah'].apply(format_rupiah_detailed)
                        
                        st.dataframe(
                            filtered_kas_display[['Tanggal', 'Kategori', 'Jenis', 'Jumlah', 'Deskripsi']].sort_values(['Tanggal', 'Jenis'], ascending=[True, False]),
                            use_container_width=True
                        )
                    else:
                        st.info("Tidak ada transaksi pada bulan yang dipilih")
                
                elif kas_harian_submenu == "Riwayat Tahunan":
                    st.subheader("Riwayat Transaksi Tahunan")
                    
                    selected_year = st.selectbox(
                        "Pilih Tahun:",
                        range(2020, date.today().year + 2),
                        index=date.today().year - 2020,
                        key="select_year_annual"
                    )
                    
                    df_kas_copy = df_kas_harian.copy()
                    df_kas_copy['Tanggal'] = pd.to_datetime(df_kas_copy['Tanggal'])
                    filtered_kas = df_kas_copy[df_kas_copy['Tanggal'].dt.year == selected_year]
                    
                    if not filtered_kas.empty:
                        total_pemasukan = filtered_kas[filtered_kas['Jenis'] == 'Pemasukan']['Jumlah'].sum()
                        total_pengeluaran = filtered_kas[filtered_kas['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
                        saldo_tahunan = total_pemasukan - total_pengeluaran
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Pemasukan", format_rupiah(total_pemasukan))
                        col2.metric("Total Pengeluaran", format_rupiah(total_pengeluaran))
                        col3.metric("Saldo Tahunan", format_rupiah(saldo_tahunan))
                        
                        st.subheader("Ringkasan per Kategori")
                        category_summary = filtered_kas.groupby(['Kategori', 'Jenis'])['Jumlah'].sum().reset_index()
                        
                        # Format angka dalam summary
                        category_summary_display = category_summary.copy()
                        category_summary_display['Jumlah'] = category_summary_display['Jumlah'].apply(format_rupiah_detailed)
                        
                        st.dataframe(
                            category_summary_display.pivot_table(index='Kategori', columns='Jenis', values='Jumlah', aggfunc='sum').fillna(0),
                            use_container_width=True
                        )
                    else:
                        st.info("Tidak ada transaksi pada tahun yang dipilih")

    # ==================== MENU DATA SISWA ====================
    elif pilihan_aktif == "Data Siswa":
        # File paths
        FILE_SISWA = "data_siswa.xlsx"
        FILE_SPP = "pembayaran_spp.xlsx"

        # Load data functions
        @st.cache_data
        def load_data_siswa():
            if os.path.exists(FILE_SISWA):
                df = pd.read_excel(FILE_SISWA)
                return df
            else:
                columns = [
                    "Nama Lengkap", "Tempat Lahir", "Tanggal Lahir", "Jenis Kelamin", "Jenjang Sekolah", 
                    "Kelas", "NIS", "NISN", "Golongan Darah", "Agama", "No HP/WA", "Sosial Media", 
                    "Alamat Domisili", "Alamat KTP", "NIK", "Tanggal Terdaftar", "Sekolah Asal", "Foto",
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

        def save_data_siswa(df):
            df.to_excel(FILE_SISWA, index=False)
            st.cache_data.clear()

        def save_spp(df):
            df.to_excel(FILE_SPP, index=False)
            st.cache_data.clear()

        def add_siswa(df, data_siswa):
            df_new = pd.concat([df, pd.DataFrame([data_siswa])], ignore_index=True)
            save_data_siswa(df_new)
            return df_new

        # Load data
        df_siswa = load_data_siswa()
        df_spp = load_spp()

        # Submenu Data Siswa
        submenu_aktif = st.session_state.submenu_choice

        # ==================== TAMBAH DATA SISWA ====================
        if submenu_aktif == "Tambah Data Siswa":
            st.subheader("Tambah Data Siswa Baru")
            
            with st.container():
                with st.form("form_tambah_siswa"):
                    st.markdown("**Data Pribadi Siswa**")
                    col1, col2 = st.columns(2)
                    
                    nama_lengkap = col1.text_input("Nama Lengkap*")
                    tempat_lahir = col2.text_input("Tempat Lahir*")
                    tanggal_lahir = col1.date_input("Tanggal Lahir*", value=date(2015, 1, 1))
                    jenis_kelamin = col2.selectbox("Jenis Kelamin*", ["Laki-laki", "Perempuan"])
                    jenjang_sekolah = col1.selectbox("Jenjang Sekolah*", ["TK", "SD", "SMP"])
                    
                    # Pilihan kelas berdasarkan jenjang
                    if jenjang_sekolah == "TK":
                        kelas_options = ["PLAYGROUP", "TK A", "TK B"]
                    elif jenjang_sekolah == "SD":
                        kelas_options = ["1", "2", "3", "4", "5", "6"]
                    else:  # SMP
                        kelas_options = ["1", "2", "3"]
                    
                    kelas = col2.selectbox("Kelas*", kelas_options)
                    
                    nis = col1.text_input("NIS*")
                    nisn = col2.text_input("NISN*")
                    golongan_darah = col1.selectbox("Golongan Darah", ["A", "B", "AB", "O", "Tidak Tahu"])
                    agama = col2.selectbox("Agama*", ["Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Konghucu"])
                    no_hp = col1.text_input("No HP/WA*")
                    sosial_media = col2.text_input("Sosial Media (Opsional)")
                    alamat_domisili = st.text_area("Alamat Domisili*")
                    alamat_ktp = st.text_area("Alamat KTP*")
                    nik = st.text_input("NIK*")
                    tanggal_terdaftar = st.date_input("Tanggal Terdaftar*", value=date.today())
                    sekolah_asal = st.text_input("Sekolah Asal (Opsional)")
                    
                    st.divider()
                    st.markdown("**Data Orang Tua**")
                    col_ortu1, col_ortu2 = st.columns(2)
                    
                    nama_ayah = col_ortu1.text_input("Nama Ayah*")
                    pekerjaan_ayah = col_ortu2.text_input("Pekerjaan Ayah*")
                    no_hp_ayah = col_ortu1.text_input("No HP/WA Ayah*")
                    nik_ayah = col_ortu2.text_input("NIK Ayah*")
                    
                    nama_ibu = col_ortu1.text_input("Nama Ibu*")
                    pekerjaan_ibu = col_ortu2.text_input("Pekerjaan Ibu*")
                    no_hp_ibu = col_ortu1.text_input("No HP/WA Ibu*")
                    nik_ibu = col_ortu2.text_input("NIK Ibu*")
                    
                    st.divider()
                    st.markdown("**Data Wali (Opsional)**")
                    col_wali1, col_wali2 = st.columns(2)
                    
                    nama_wali = col_wali1.text_input("Nama Wali")
                    pekerjaan_wali = col_wali2.text_input("Pekerjaan Wali")
                    no_hp_wali = col_wali1.text_input("No HP/WA Wali")
                    nik_wali = col_wali2.text_input("NIK Wali")
                    
                    alamat_orang_tua = st.text_area("Alamat Orang Tua*")
                    
                    submit_button = st.form_submit_button("Simpan Data Siswa", use_container_width=True)
                    
                    if submit_button:
                        wajib_fields = {
                            "Nama Lengkap": nama_lengkap,
                            "Tempat Lahir": tempat_lahir,
                            "NIS": nis,
                            "NISN": nisn,
                            "No HP/WA": no_hp,
                            "Alamat Domisili": alamat_domisili,
                            "Alamat KTP": alamat_ktp,
                            "NIK": nik,
                            "Nama Ayah": nama_ayah,
                            "Pekerjaan Ayah": pekerjaan_ayah,
                            "No HP/WA Ayah": no_hp_ayah,
                            "NIK Ayah": nik_ayah,
                            "Nama Ibu": nama_ibu,
                            "Pekerjaan Ibu": pekerjaan_ibu,
                            "No HP/WA Ibu": no_hp_ibu,
                            "NIK Ibu": nik_ibu,
                            "Alamat Orang Tua": alamat_orang_tua
                        }
                        
                        missing_fields = [field for field, value in wajib_fields.items() if not value]
                        
                        if missing_fields:
                            st.error(f"Field berikut wajib diisi: {', '.join(missing_fields)}")
                        else:
                            if not df_siswa.empty and nisn in df_siswa['NISN'].values:
                                st.error(f"NISN {nisn} sudah terdaftar. Gunakan NISN yang berbeda.")
                            else:
                                data_siswa_baru = {
                                    "Nama Lengkap": nama_lengkap,
                                    "Tempat Lahir": tempat_lahir,
                                    "Tanggal Lahir": tanggal_lahir,
                                    "Jenis Kelamin": jenis_kelamin,
                                    "Jenjang Sekolah": jenjang_sekolah,
                                    "Kelas": kelas,
                                    "NIS": nis,
                                    "NISN": nisn,
                                    "Golongan Darah": golongan_darah,
                                    "Agama": agama,
                                    "No HP/WA": no_hp,
                                    "Sosial Media": sosial_media,
                                    "Alamat Domisili": alamat_domisili,
                                    "Alamat KTP": alamat_ktp,
                                    "NIK": nik,
                                    "Tanggal Terdaftar": tanggal_terdaftar,
                                    "Sekolah Asal": sekolah_asal,
                                    "Foto": "",
                                    "Nama Ayah": nama_ayah,
                                    "Pekerjaan Ayah": pekerjaan_ayah,
                                    "No HP/WA Ayah": no_hp_ayah,
                                    "NIK Ayah": nik_ayah,
                                    "Nama Ibu": nama_ibu,
                                    "Pekerjaan Ibu": pekerjaan_ibu,
                                    "No HP/WA Ibu": no_hp_ibu,
                                    "NIK Ibu": nik_ibu,
                                    "Nama Wali": nama_wali,
                                    "Pekerjaan Wali": pekerjaan_wali,
                                    "No HP/WA Wali": no_hp_wali,
                                    "NIK Wali": nik_wali,
                                    "Alamat Orang Tua": alamat_orang_tua
                                }
                                
                                df_siswa = add_siswa(df_siswa, data_siswa_baru)
                                st.success(f"Data siswa {nama_lengkap} berhasil disimpan!")
                                rerun()

        # ==================== KENAIKAN KELAS ====================
        elif submenu_aktif == "Kenaikan Kelas":
            st.subheader("🔄 Sistem Kenaikan Kelas Massal")
            
            tab1, tab2, tab3 = st.tabs(["Kenaikan Kelas Massal", "Tinggal Kelas", "Riwayat Perpindahan Kelas"])
            
            with tab1:
                st.markdown("### Kenaikan Kelas Massal")
                
                # Pilih jenjang, kelas, dan tahun ajaran
                col1, col2, col3 = st.columns(3)
                with col1:
                    jenjang = st.selectbox(
                        "Pilih Jenjang:",
                        ["TK", "SD", "SMP"],
                        key="kenaikan_jenjang"
                    )
                
                with col2:
                    # Pilihan kelas berdasarkan jenjang
                    if jenjang == "TK":
                        kelas_options = ["PLAYGROUP", "TK A", "TK B"]
                    elif jenjang == "SD":
                        kelas_options = ["1", "2", "3", "4", "5", "6"]
                    else:  # SMP
                        kelas_options = ["1", "2", "3"]
                    
                    kelas = st.selectbox(
                        "Pilih Kelas:",
                        kelas_options,
                        key="kenaikan_kelas"
                    )
                
                with col3:
                    tahun_ajaran = st.selectbox(
                        "Tahun Ajaran:",
                        [f"{year}/{year+1}" for year in range(2020, 2030)],
                        index=5,  # Default ke tahun berjalan
                        key="tahun_ajaran"
                    )
                
                # Tampilkan siswa berdasarkan jenjang dan kelas yang dipilih
                siswa_filtered = df_siswa[
                    (df_siswa['Jenjang Sekolah'] == jenjang) & 
                    (df_siswa['Kelas'] == kelas)
                ]
                
                if not siswa_filtered.empty:
                    # PERBAIKAN: Mapping kenaikan kelas dengan penanganan KELULUSAN
                    mapping_kelas = {
                        "TK": {
                            "PLAYGROUP": "TK A",
                            "TK A": "TK B", 
                            "TK B": "LULUS"  # TK B akan lulus, bukan naik kelas
                        },
                        "SD": {
                            "1": "2",
                            "2": "3", 
                            "3": "4",
                            "4": "5",
                            "5": "6",
                            "6": "LULUS"  # SD kelas 6 akan lulus
                        },
                        "SMP": {
                            "1": "2",
                            "2": "3", 
                            "3": "LULUS"  # SMP kelas 3 akan lulus
                        }
                    }
                    
                    # Tampilkan preview kenaikan kelas
                    st.markdown("### Preview Kenaikan Kelas")
                    
                    preview_data = []
                    siswa_akan_lulus = 0
                    siswa_akan_naik = 0
                    siswa_tetap = 0
                    
                    for _, siswa in siswa_filtered.iterrows():
                        kelas_sekarang = siswa['Kelas']
                        kelas_baru = mapping_kelas[jenjang].get(kelas_sekarang, kelas_sekarang)
                        
                        status = 'Tetap'
                        if kelas_baru != kelas_sekarang:
                            if kelas_baru == 'LULUS':
                                status = 'Akan LULUS'
                                siswa_akan_lulus += 1
                            else:
                                status = 'Akan Naik'
                                siswa_akan_naik += 1
                        else:
                            siswa_tetap += 1
                        
                        preview_data.append({
                            'NISN': siswa['NISN'],
                            'Nama': siswa['Nama Lengkap'],
                            'Kelas Sekarang': kelas_sekarang,
                            'Kelas Baru': kelas_baru,
                            'Status': status
                        })
                    
                    df_preview = pd.DataFrame(preview_data)
                    st.dataframe(df_preview, use_container_width=True)
                    
                    # Statistik kenaikan kelas
                    st.markdown("### 📊 Statistik Kenaikan Kelas")
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    col_stat1.metric("Akan Naik Kelas", siswa_akan_naik)
                    col_stat2.metric("Akan LULUS", siswa_akan_lulus)
                    col_stat3.metric("Tetap", siswa_tetap)
                    
                    # Konfirmasi kenaikan kelas
                    st.markdown("### Konfirmasi Kenaikan Kelas")
                    
                    if siswa_akan_lulus > 0:
                        st.warning(f"⚠️ **PERHATIAN KHUSUS**: {siswa_akan_lulus} siswa akan dinyatakan **LULUS** dan tidak akan muncul di data siswa aktif!")
                    
                    st.warning("⚠️ **PERHATIAN**: Tindakan ini akan mengubah data kelas semua siswa yang terpilih!")
                    
                    if st.button("🚀 Eksekusi Kenaikan Kelas Massal", type="primary", use_container_width=True):
                        # Backup data sebelum perubahan
                        backup_data = df_siswa.copy()
                        
                        try:
                            updated_count = 0
                            lulus_count = 0
                            riwayat_list = []
                            
                            for _, siswa in siswa_filtered.iterrows():
                                kelas_sekarang = siswa['Kelas']
                                kelas_baru = mapping_kelas[jenjang].get(kelas_sekarang, kelas_sekarang)
                                
                                if kelas_baru != kelas_sekarang:
                                    if kelas_baru == 'LULUS':
                                        # Untuk siswa yang lulus, hapus dari data siswa aktif
                                        df_siswa = df_siswa[df_siswa['NISN'] != siswa['NISN']]
                                        lulus_count += 1
                                        jenis_riwayat = 'LULUS'
                                        keterangan = f'Kelulusan {tahun_ajaran}'
                                    else:
                                        # Update kelas di dataframe untuk kenaikan kelas biasa
                                        df_siswa.loc[df_siswa['NISN'] == siswa['NISN'], 'Kelas'] = kelas_baru
                                        updated_count += 1
                                        jenis_riwayat = 'KENAIKAN'
                                        keterangan = f'Kenaikan kelas otomatis {tahun_ajaran}'
                                    
                                    # Catat riwayat
                                    riwayat_data = {
                                        'NISN': siswa['NISN'],
                                        'Nama': siswa['Nama Lengkap'],
                                        'Jenjang': jenjang,
                                        'Kelas_Lama': kelas_sekarang,
                                        'Kelas_Baru': kelas_baru,
                                        'Tahun_Ajaran': tahun_ajaran,
                                        'Tanggal': datetime.now().date(),
                                        'Jenis': jenis_riwayat,
                                        'Keterangan': keterangan
                                    }
                                    riwayat_list.append(riwayat_data)
                            
                            # Simpan perubahan
                            save_data_siswa(df_siswa)
                            
                            # Simpan riwayat
                            if riwayat_list:
                                save_riwayat_kelas(riwayat_list)
                            
                            # Tampilkan hasil
                            if updated_count > 0 and lulus_count > 0:
                                st.success(f"✅ **Berhasil!** {updated_count} siswa telah dinaikkan kelas dan {lulus_count} siswa telah LULUS!")
                            elif updated_count > 0:
                                st.success(f"✅ **Berhasil!** {updated_count} siswa telah dinaikkan kelas!")
                            elif lulus_count > 0:
                                st.success(f"✅ **Berhasil!** {lulus_count} siswa telah LULUS!")
                            else:
                                st.info("Tidak ada perubahan yang dilakukan.")
                            
                            st.balloons()
                            
                        except Exception as e:
                            # Rollback jika error
                            df_siswa = backup_data
                            save_data_siswa(df_siswa)
                            st.error(f"❌ Gagal melakukan kenaikan kelas: {str(e)}")
                
                else:
                    st.info(f"Tidak ada data siswa untuk jenjang {jenjang} kelas {kelas}")

            with tab2:
                st.markdown("### 🎯 Pengaturan Tinggal Kelas")
                
                # Pilih siswa untuk tinggal kelas
                if not df_siswa.empty:
                    col_search1, col_search2 = st.columns([2, 1])
                    with col_search1:
                        pencarian = st.text_input("Cari Siswa (NISN atau Nama)", key="pencarian_tinggal")
                    
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
                                "Pilih Siswa:",
                                options=range(len(filtered_siswa)),
                                format_func=lambda x: f"{filtered_siswa.iloc[x]['NISN']} - {filtered_siswa.iloc[x]['Nama Lengkap']} - {filtered_siswa.iloc[x]['Kelas']}",
                                key="select_siswa_tinggal"
                            )
                        
                        selected_siswa = filtered_siswa.iloc[selected_index]
                        
                        st.info(f"**Siswa Terpilih:** {selected_siswa['Nama Lengkap']} (Kelas: {selected_siswa['Kelas']})")
                        
                        # Form tinggal kelas
                        with st.form("form_tinggal_kelas"):
                            colA, colB = st.columns(2)
                            
                            dengan_catatan = colA.checkbox("Tinggal Kelas dengan Catatan", value=True)
                            tahun_ajaran_tinggal = colB.selectbox(
                                "Tahun Ajaran:",
                                [f"{year}/{year+1}" for year in range(2020, 2030)],
                                index=5,
                                key="tahun_ajaran_tinggal"
                            )
                            
                            keterangan = st.text_area("Keterangan/Alasan Tinggal Kelas", 
                                                    value="Tidak memenuhi syarat kenaikan kelas")
                            
                            submit_tinggal = st.form_submit_button("💾 Set Tinggal Kelas", 
                                                                 type="secondary", 
                                                                 use_container_width=True)
                            
                            if submit_tinggal:
                                # Logika untuk tinggal kelas (kelas tetap sama)
                                riwayat_data = {
                                    'NISN': selected_siswa['NISN'],
                                    'Nama': selected_siswa['Nama Lengkap'],
                                    'Jenjang': selected_siswa['Jenjang Sekolah'],
                                    'Kelas_Lama': selected_siswa['Kelas'],
                                    'Kelas_Baru': selected_siswa['Kelas'],  # Tetap di kelas yang sama
                                    'Tahun_Ajaran': tahun_ajaran_tinggal,
                                    'Tanggal': datetime.now().date(),
                                    'Jenis': 'TINGGAL',
                                    'Keterangan': keterangan
                                }
                                
                                # Simpan riwayat
                                save_riwayat_kelas(riwayat_data)
                                
                                st.success(f"✅ **Siswa {selected_siswa['Nama Lengkap']} ditetapkan tinggal kelas!**")
                    
                    else:
                        st.warning("Tidak ada siswa yang sesuai dengan pencarian")
                else:
                    st.info("Belum ada data siswa")
            
            with tab3:
                st.markdown("### 📊 Riwayat Perpindahan Kelas")
                
                # Load dan tampilkan riwayat
                df_riwayat = load_riwayat_kelas()
                
                if not df_riwayat.empty:
                    # Filter options
                    col_filter1, col_filter2, col_filter3 = st.columns(3)
                    with col_filter1:
                        filter_jenis = st.selectbox(
                            "Filter Jenis:",
                            ["SEMUA", "KENAIKAN", "TINGGAL", "LULUS"],
                            key="filter_jenis_riwayat"
                        )
                    
                    with col_filter2:
                        filter_jenjang = st.selectbox(
                            "Filter Jenjang:",
                            ["SEMUA", "TK", "SD", "SMP"],
                            key="filter_jenjang_riwayat"
                        )
                    
                    with col_filter3:
                        filter_tahun = st.selectbox(
                            "Filter Tahun Ajaran:",
                            ["SEMUA"] + [f"{year}/{year+1}" for year in range(2020, 2030)],
                            key="filter_tahun_riwayat"
                        )
                    
                    # Apply filters
                    filtered_riwayat = df_riwayat.copy()
                    if filter_jenis != "SEMUA":
                        filtered_riwayat = filtered_riwayat[filtered_riwayat['Jenis'] == filter_jenis]
                    if filter_jenjang != "SEMUA":
                        filtered_riwayat = filtered_riwayat[filtered_riwayat['Jenjang'] == filter_jenjang]
                    if filter_tahun != "SEMUA":
                        filtered_riwayat = filtered_riwayat[filtered_riwayat['Tahun_Ajaran'] == filter_tahun]
                    
                    st.dataframe(
                        filtered_riwayat[['Tanggal', 'NISN', 'Nama', 'Jenjang', 'Kelas_Lama', 'Kelas_Baru', 'Jenis', 'Keterangan']],
                        use_container_width=True
                    )
                    
                    # Statistik
                    st.markdown("#### 📈 Statistik Perpindahan Kelas")
                    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                    
                    total_kenaikan = len(filtered_riwayat[filtered_riwayat['Jenis'] == 'KENAIKAN'])
                    total_tinggal = len(filtered_riwayat[filtered_riwayat['Jenis'] == 'TINGGAL'])
                    total_lulus = len(filtered_riwayat[filtered_riwayat['Jenis'] == 'LULUS'])
                    total_riwayat = len(filtered_riwayat)
                    
                    col_stat1.metric("Total Kenaikan", total_kenaikan)
                    col_stat2.metric("Total Tinggal", total_tinggal)
                    col_stat3.metric("Total LULUS", total_lulus)
                    col_stat4.metric("Total Riwayat", total_riwayat)
                    
                    # Tombol ekspor
                    col_export1, col_export2 = st.columns(2)
                    
                    with col_export1:
                        if st.button("📊 Ekspor Laporan Excel", use_container_width=True):
                            # Buat file Excel
                            output = BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                filtered_riwayat.to_excel(writer, sheet_name='Riwayat_Kelas', index=False)
                                
                                # Buat sheet summary
                                summary_data = filtered_riwayat.groupby(['Jenis', 'Jenjang']).size().reset_index(name='Jumlah')
                                summary_data.to_excel(writer, sheet_name='Summary', index=False)
                            
                            output.seek(0)
                            
                            st.download_button(
                                label="📥 Download Laporan Excel",
                                data=output,
                                file_name=f"laporan_kenaikan_kelas_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                    
                    with col_export2:
                        if st.button("🖨️ Cetak Laporan PDF", use_container_width=True):
                            # Fungsi untuk generate PDF report
                            pdf_buffer = generate_kelas_pdf_report(filtered_riwayat)
                            
                            st.download_button(
                                label="📄 Download Laporan PDF",
                                data=pdf_buffer,
                                file_name=f"laporan_kelas_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                    
                else:
                    st.info("Belum ada riwayat perpindahan kelas")

        # ==================== DATA PER JENJANG ====================
        elif submenu_aktif in ["Data TK", "Data SD", "Data SMP", "Semua Siswa"]:
            if submenu_aktif == "Data TK":
                st.subheader("Data Siswa TK")
                filtered_siswa = df_siswa[df_siswa['Jenjang Sekolah'] == "TK"]
            elif submenu_aktif == "Data SD":
                st.subheader("Data Siswa SD")
                filtered_siswa = df_siswa[df_siswa['Jenjang Sekolah'] == "SD"]
            elif submenu_aktif == "Data SMP":
                st.subheader("Data Siswa SMP")
                filtered_siswa = df_siswa[df_siswa['Jenjang Sekolah'] == "SMP"]
            else:
                st.subheader("Semua Data Siswa")
                filtered_siswa = df_siswa
            
            with st.container():
                if not filtered_siswa.empty:
                    col_search1, col_search2 = st.columns([3, 1])
                    with col_search1:
                        pencarian = st.text_input("Cari Siswa (Nama, NIS, NISN, Kelas)")
                    
                    if pencarian:
                        filtered_siswa = filtered_siswa[
                            filtered_siswa['Nama Lengkap'].str.contains(pencarian, case=False, na=False) |
                            filtered_siswa['NIS'].astype(str).str.contains(pencarian, case=False, na=False) |
                            filtered_siswa['NISN'].astype(str).str.contains(pencarian, case=False, na=False) |
                            filtered_siswa['Kelas'].str.contains(pencarian, case=False, na=False)
                        ]
                    
                    with col_search2:
                        st.metric("Jumlah Siswa", len(filtered_siswa))
                    
                    st.dataframe(
                        filtered_siswa[['Nama Lengkap', 'Kelas', 'NIS', 'NISN', 'Jenis Kelamin', 'Tanggal Terdaftar']],
                        use_container_width=True
                    )
                    
                    if not filtered_siswa.empty:
                        st.subheader("Kelola Data Siswa")
                        
                        selected_index = st.selectbox(
                            "Pilih Siswa untuk Edit/Hapus:",
                            options=range(len(filtered_siswa)),
                            format_func=lambda x: f"{filtered_siswa.iloc[x]['NISN']} - {filtered_siswa.iloc[x]['Nama Lengkap']} - {filtered_siswa.iloc[x]['Kelas']}"
                        )
                        
                        selected_siswa = filtered_siswa.iloc[selected_index]
                        
                        col_edit1, col_edit2 = st.columns(2)
                        
                        with col_edit1:
                            if st.button("Edit Data Siswa", use_container_width=True):
                                st.session_state.editing_siswa = selected_siswa['NISN']
                                st.info("Fitur edit akan segera tersedia")
                        
                        with col_edit2:
                            if st.button("Hapus Data Siswa", type="secondary", use_container_width=True):
                                df_siswa = df_siswa[df_siswa['NISN'] != selected_siswa['NISN']]
                                save_data_siswa(df_siswa)
                                
                                df_spp = df_spp[df_spp['NISN'] != selected_siswa['NISN']]
                                save_spp(df_spp)
                                
                                st.success(f"Data siswa {selected_siswa['Nama Lengkap']} berhasil dihapus!")
                                rerun()
                else:
                    st.info(f"Belum ada data siswa untuk {submenu_aktif}")

    # ==================== MENU LAPORAN ====================
    elif pilihan_aktif == "Laporan":
        # File paths
        FILE_PATH = "transaksi_keuangan.xlsx"
        FILE_SISWA = "data_siswa.xlsx"
        FILE_SPP = "pembayaran_spp.xlsx"
        FILE_KAS_HARIAN = "kas_harian.xlsx"

        # Load data functions
        @st.cache_data
        def load_data():
            if os.path.exists(FILE_PATH):
                df = pd.read_excel(FILE_PATH)
                df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date
                return df
            else:
                return pd.DataFrame(columns=["Tanggal", "Kategori", "Jumlah", "Jenis", "Deskripsi", "Tipe_Keuangan", "NISN"])

        @st.cache_data
        def load_siswa():
            if os.path.exists(FILE_SISWA):
                df = pd.read_excel(FILE_SISWA)
                return df
            else:
                return pd.DataFrame()

        @st.cache_data
        def load_spp():
            if os.path.exists(FILE_SPP):
                df = pd.read_excel(FILE_SPP)
                df['Tanggal_Bayar'] = pd.to_datetime(df['Tanggal_Bayar']).dt.date
                df['Bulan_Tagihan'] = pd.to_datetime(df['Bulan_Tagihan']).dt.date
                return df
            else:
                return pd.DataFrame(columns=["NISN", "Nama", "Kelas", "Bulan_Tagihan", "Jumlah", "Tanggal_Bayar", "Status", "Keterangan"])

        @st.cache_data
        def load_kas_harian():
            if os.path.exists(FILE_KAS_HARIAN):
                df = pd.read_excel(FILE_KAS_HARIAN)
                df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date
                return df
            else:
                return pd.DataFrame(columns=["Tanggal", "Kategori", "Jumlah", "Jenis", "Deskripsi"])

        # Load data
        df = load_data()
        df_siswa = load_siswa()
        df_spp = load_spp()
        df_kas_harian = load_kas_harian()

        # ==================== FUNGSI LAPORAN PDF YANG DIPERBAIKI DENGAN TEXT WRAP ====================
        def create_laporan_keuangan_periode_pdf(df_transaksi, tanggal_awal, tanggal_akhir):
            """Membuat laporan keuangan dengan tanggal dan deskripsi lengkap dengan text wrap"""
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
            styles = getSampleStyleSheet()
            
            # Buat style untuk wrap text
            wrap_style = ParagraphStyle(
                'WrapStyle',
                parent=styles['Normal'],
                fontSize=8,
                leading=9,
                wordWrap='CJK'  # Untuk wrap text
            )
            
            wrap_style_bold = ParagraphStyle(
                'WrapStyleBold',
                parent=styles['Normal'],
                fontSize=8,
                leading=9,
                wordWrap='CJK',
                fontName='Helvetica-Bold'
            )
            
            wrap_style_header = ParagraphStyle(
                'WrapStyleHeader',
                parent=styles['Normal'],
                fontSize=8,
                leading=9,
                wordWrap='CJK',
                fontName='Helvetica-Bold',
                textColor=colors.whitesmoke
            )
            
            story = []
            
            # Header
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=14,
                spaceAfter=6,
                alignment=1,
                textColor=colors.black
            )
            
            story.append(Paragraph("YAYASAN PENDIDIKAN PELITA INSANI TELAGA KAHURIPAN", title_style))
            story.append(Paragraph("SEKOLAH PELITA INSANI", title_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph("LAPORAN KEUANGAN DETAIL", styles['Heading2']))
            story.append(Paragraph(f"PERIODE: {tanggal_awal.strftime('%d %B %Y')} s/d {tanggal_akhir.strftime('%d %B %Y')}", styles['Heading3']))
            story.append(Spacer(1, 15))
            
            # Filter data berdasarkan periode
            df_transaksi_copy = df_transaksi.copy()
            df_transaksi_copy['Tanggal'] = pd.to_datetime(df_transaksi_copy['Tanggal'])
            transaksi_periode = df_transaksi_copy[
                (df_transaksi_copy['Tanggal'] >= pd.Timestamp(tanggal_awal)) & 
                (df_transaksi_copy['Tanggal'] <= pd.Timestamp(tanggal_akhir))
            ]
            
            # Inisialisasi variabel dengan nilai default
            total_pemasukan = 0
            total_pengeluaran = 0
            
            if not transaksi_periode.empty:
                # Pisahkan pemasukan dan pengeluaran
                pemasukan_data = transaksi_periode[transaksi_periode['Jenis'] == 'Pemasukan']
                pengeluaran_data = transaksi_periode[transaksi_periode['Jenis'] == 'Pengeluaran']
                
                # Siapkan data tabel untuk pemasukan
                story.append(Paragraph("PEMASUKAN", styles['Heading3']))
                story.append(Spacer(1, 10))
                
                if not pemasukan_data.empty:
                    # Header dengan Paragraph untuk wrap text
                    header_pemasukan = [
                        Paragraph("No", wrap_style_header),
                        Paragraph("Tanggal", wrap_style_header),
                        Paragraph("Kategori", wrap_style_header),
                        Paragraph("Deskripsi", wrap_style_header),
                        Paragraph("Jumlah", wrap_style_header)
                    ]
                    
                    table_data_pemasukan = [header_pemasukan]
                    no = 1
                    
                    for _, row in pemasukan_data.sort_values('Tanggal').iterrows():
                        deskripsi = str(row['Deskripsi']).strip()
                        if not deskripsi or deskripsi == "nan":
                            deskripsi = str(row['Kategori'])
                        
                        # Gunakan Paragraph untuk semua sel agar text wrap bekerja
                        table_data_pemasukan.append([
                            Paragraph(str(no), wrap_style),
                            Paragraph(row['Tanggal'].strftime('%d/%m/%Y'), wrap_style),
                            Paragraph(row['Kategori'], wrap_style),
                            Paragraph(deskripsi, wrap_style),
                            Paragraph(f"{row['Jumlah']:,.0f}", wrap_style)
                        ])
                        
                        total_pemasukan += row['Jumlah']
                        no += 1
                    
                    # Tambah baris total pemasukan
                    table_data_pemasukan.append([
                        Paragraph("", wrap_style),
                        Paragraph("", wrap_style),
                        Paragraph("", wrap_style),
                        Paragraph("Total Pemasukan", wrap_style_bold),
                        Paragraph(f"{total_pemasukan:,.0f}", wrap_style_bold)
                    ])
                    
                    # Buat tabel pemasukan dengan kolom lebih lebar
                    col_widths_pemasukan = [25, 60, 120, 200, 100]
                    pemasukan_table = Table(table_data_pemasukan, colWidths=col_widths_pemasukan, repeatRows=1)
                    pemasukan_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (3, 0), (3, -2), 'LEFT'),
                        ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Vertical align top untuk wrap text
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),
                        ('LEFTPADDING', (0, 0), (-1, -1), 2),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                        ('GRID', (0, 0), (-1, -2), 1, colors.black),
                        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                    ]))
                    
                    story.append(pemasukan_table)
                else:
                    story.append(Paragraph("Tidak ada data pemasukan", styles['Normal']))
                
                story.append(Spacer(1, 20))
                
                # Siapkan data tabel untuk pengeluaran
                story.append(Paragraph("PENGELUARAN", styles['Heading3']))
                story.append(Spacer(1, 10))
                
                if not pengeluaran_data.empty:
                    # Header dengan Paragraph untuk wrap text
                    header_pengeluaran = [
                        Paragraph("No", wrap_style_header),
                        Paragraph("Tanggal", wrap_style_header),
                        Paragraph("Kategori", wrap_style_header),
                        Paragraph("Deskripsi", wrap_style_header),
                        Paragraph("Jumlah", wrap_style_header)
                    ]
                    
                    table_data_pengeluaran = [header_pengeluaran]
                    no = 1
                    
                    for _, row in pengeluaran_data.sort_values('Tanggal').iterrows():
                        deskripsi = str(row['Deskripsi']).strip()
                        if not deskripsi or deskripsi == "nan":
                            deskripsi = str(row['Kategori'])
                        
                        # Gunakan Paragraph untuk semua sel agar text wrap bekerja
                        table_data_pengeluaran.append([
                            Paragraph(str(no), wrap_style),
                            Paragraph(row['Tanggal'].strftime('%d/%m/%Y'), wrap_style),
                            Paragraph(row['Kategori'], wrap_style),
                            Paragraph(deskripsi, wrap_style),
                            Paragraph(f"{row['Jumlah']:,.0f}", wrap_style)
                        ])
                        
                        total_pengeluaran += row['Jumlah']
                        no += 1
                    
                    # Tambah baris total pengeluaran
                    table_data_pengeluaran.append([
                        Paragraph("", wrap_style),
                        Paragraph("", wrap_style),
                        Paragraph("", wrap_style),
                        Paragraph("Total Pengeluaran", wrap_style_bold),
                        Paragraph(f"{total_pengeluaran:,.0f}", wrap_style_bold)
                    ])
                    
                    # Buat tabel pengeluaran dengan kolom lebih lebar
                    col_widths_pengeluaran = [25, 60, 120, 200, 100]
                    pengeluaran_table = Table(table_data_pengeluaran, colWidths=col_widths_pengeluaran, repeatRows=1)
                    pengeluaran_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (3, 0), (3, -2), 'LEFT'),
                        ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Vertical align top untuk wrap text
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),
                        ('LEFTPADDING', (0, 0), (-1, -1), 2),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                        ('GRID', (0, 0), (-1, -2), 1, colors.black),
                        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                    ]))
                    
                    story.append(pengeluaran_table)
                else:
                    story.append(Paragraph("Tidak ada data pengeluaran", styles['Normal']))
                
                story.append(Spacer(1, 20))
                
                # Ringkasan akhir
                story.append(Paragraph("RINGKASAN KEUANGAN", styles['Heading3']))
                story.append(Spacer(1, 10))
                
                saldo = total_pemasukan - total_pengeluaran
                
                # Gunakan Paragraph untuk summary juga
                summary_data = [
                    [Paragraph("Total Pemasukan", wrap_style_bold), Paragraph(f"{total_pemasukan:,.0f}", wrap_style_bold)],
                    [Paragraph("Total Pengeluaran", wrap_style_bold), Paragraph(f"{total_pengeluaran:,.0f}", wrap_style_bold)],
                    [Paragraph("Saldo (Pemasukan - Pengeluaran)", wrap_style_bold), Paragraph(f"{saldo:,.0f}", wrap_style_bold)]
                ]
                
                summary_table = Table(summary_data, colWidths=[250, 150])
                summary_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                story.append(summary_table)
                story.append(Spacer(1, 30))
                
                # Tanda tangan di kanan bawah
                tanda_tangan_style = ParagraphStyle(
                    'RightAlign',
                    parent=styles['Normal'],
                    alignment=2,
                    fontSize=10
                )
                
                story.append(Paragraph("Bogor, ..........................", tanda_tangan_style))
                story.append(Spacer(1, 20))
                story.append(Paragraph("WAHYU HANDAYANI", tanda_tangan_style))
                story.append(Paragraph("FINANCE", tanda_tangan_style))
                
            else:
                story.append(Paragraph("Tidak ada data transaksi untuk periode ini.", styles['Normal']))
                story.append(Spacer(1, 20))
                
                # Ringkasan kosong
                story.append(Paragraph("RINGKASAN KEUANGAN", styles['Heading3']))
                story.append(Spacer(1, 10))
                
                summary_data = [
                    [Paragraph("Total Pemasukan", wrap_style_bold), Paragraph("0", wrap_style_bold)],
                    [Paragraph("Total Pengeluaran", wrap_style_bold), Paragraph("0", wrap_style_bold)],
                    [Paragraph("Saldo (Pemasukan - Pengeluaran)", wrap_style_bold), Paragraph("0", wrap_style_bold)]
                ]
                
                summary_table = Table(summary_data, colWidths=[250, 150])
                summary_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                story.append(summary_table)
                
                story.append(Spacer(1, 30))
                # Tanda tangan di kanan bawah
                tanda_tangan_style = ParagraphStyle(
                    'RightAlign',
                    parent=styles['Normal'],
                    alignment=2,
                    fontSize=10
                )
                story.append(Paragraph("Bogor, ..........................", tanda_tangan_style))
                story.append(Spacer(1, 20))
                story.append(Paragraph("WAHYU HANDAYANI", tanda_tangan_style))
                story.append(Paragraph("FINANCE", tanda_tangan_style))
            
            doc.build(story)
            buffer.seek(0)
            return buffer

        def create_jurnal_per_siswa_pdf(df_transaksi, df_siswa, nisn_siswa):
            """Membuat jurnal pembayaran per siswa dengan text wrap"""
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
            styles = getSampleStyleSheet()
            
            # Buat style untuk wrap text
            wrap_style = ParagraphStyle(
                'WrapStyle',
                parent=styles['Normal'],
                fontSize=8,
                leading=9,
                wordWrap='CJK'
            )
            
            wrap_style_bold = ParagraphStyle(
                'WrapStyleBold',
                parent=styles['Normal'],
                fontSize=8,
                leading=9,
                wordWrap='CJK',
                fontName='Helvetica-Bold'
            )
            
            wrap_style_header = ParagraphStyle(
                'WrapStyleHeader',
                parent=styles['Normal'],
                fontSize=8,
                leading=9,
                wordWrap='CJK',
                fontName='Helvetica-Bold',
                textColor=colors.whitesmoke
            )
            
            story = []
            
            # Header dengan layout yang lebih baik
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=6,
                alignment=1,
                textColor=colors.black
            )
            
            story.append(Paragraph("YAYASAN PENDIDIKAN PELITA INSANI TELAGA KAHURIPAN", title_style))
            story.append(Paragraph("SEKOLAH PELITA INSANI", title_style))
            story.append(Spacer(1, 6))
            
            # Header dengan alignment yang lebih baik
            header_table_data = [
                [Paragraph("JURNAL PEMBAYARAN PER SISWA", ParagraphStyle(
                    'CenterBold',
                    parent=styles['Normal'],
                    fontSize=14,
                    alignment=1,
                    fontName='Helvetica-Bold'
                ))]
            ]
            
            header_table = Table(header_table_data, colWidths=[600])
            header_table.setStyle(TableStyle([
                ('BOTTOMPADDING', (0, 0), (0, 0), 10),
            ]))
            
            story.append(header_table)
            story.append(Spacer(1, 10))
            
            # Data siswa
            siswa = df_siswa[df_siswa['NISN'] == nisn_siswa].iloc[0]
            
            # Layout data siswa dengan alignment yang benar
            data_siswa = [
                [Paragraph("Nama Siswa", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(siswa['Nama Lengkap']), wrap_style)],
                [Paragraph("No Induk Siswa", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(siswa['NIS']), wrap_style)],
                [Paragraph("Jenjang Pendidikan", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(siswa['Jenjang Sekolah']), wrap_style)],
                [Paragraph("Kelas", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(siswa['Kelas']), wrap_style)]
            ]
            
            siswa_table = Table(data_siswa, colWidths=[120, 15, 400])
            siswa_table.setStyle(TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (0, -1), 50),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            story.append(siswa_table)
            story.append(Spacer(1, 15))
            
            # Data transaksi siswa
            transaksi_siswa = df_transaksi[df_transaksi['NISN'] == nisn_siswa].sort_values('Tanggal', ascending=False)
            
            if not transaksi_siswa.empty:
                # Header dengan Paragraph untuk wrap text
                header = [
                    Paragraph("No", wrap_style_header),
                    Paragraph("Tanggal", wrap_style_header),
                    Paragraph("Kategori", wrap_style_header),
                    Paragraph("Deskripsi", wrap_style_header),
                    Paragraph("Jumlah", wrap_style_header)
                ]
                
                table_data = [header]
                no = 1
                total_jumlah = 0
                
                for _, row in transaksi_siswa.iterrows():
                    deskripsi = str(row['Deskripsi']).strip()
                    if not deskripsi or deskripsi == "nan":
                        deskripsi = str(row['Kategori'])
                    
                    # Gunakan Paragraph untuk semua sel agar text wrap bekerja
                    table_data.append([
                        Paragraph(str(no), wrap_style),
                        Paragraph(row['Tanggal'].strftime('%d/%m/%Y') if hasattr(row['Tanggal'], 'strftime') else str(row['Tanggal']), wrap_style),
                        Paragraph(str(row['Kategori']), wrap_style),
                        Paragraph(deskripsi, wrap_style),
                        Paragraph(f"{row['Jumlah']:,.0f}", wrap_style)
                    ])
                    
                    total_jumlah += row['Jumlah']
                    no += 1
                
                # Tambah baris kosong sampai 15 baris
                while no <= 15:
                    table_data.append([
                        Paragraph(str(no), wrap_style),
                        Paragraph("", wrap_style),
                        Paragraph("", wrap_style),
                        Paragraph("", wrap_style),
                        Paragraph("", wrap_style)
                    ])
                    no += 1
                
                # Baris total
                table_data.append([
                    Paragraph("", wrap_style),
                    Paragraph("", wrap_style),
                    Paragraph("", wrap_style),
                    Paragraph("Jumlah", wrap_style_bold),
                    Paragraph(f"{total_jumlah:,.0f}", wrap_style_bold)
                ])
                
                # Buat tabel dengan lebar kolom yang lebih lebar
                col_widths = [30, 70, 120, 280, 100]
                jurnal_table = Table(table_data, colWidths=col_widths, repeatRows=1)
                jurnal_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (3, 0), (3, -2), 'LEFT'),
                    ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('GRID', (0, 0), (-1, -2), 1, colors.black),
                    ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ]))
                
                story.append(jurnal_table)
                story.append(Spacer(1, 30))
                
                # Tanda tangan di kanan bawah
                tanda_tangan_style = ParagraphStyle(
                    'RightAlign',
                    parent=styles['Normal'],
                    alignment=2,
                    fontSize=10
                )
                
                story.append(Paragraph("Bogor ..........................", tanda_tangan_style))
                story.append(Spacer(1, 10))
                story.append(Paragraph("WAHYU HANDAYANI", tanda_tangan_style))
                story.append(Paragraph("FINANCE", tanda_tangan_style))
                
            else:
                story.append(Paragraph("Tidak ada data pembayaran untuk siswa ini.", styles['Normal']))
            
            doc.build(story)
            buffer.seek(0)
            return buffer

        def create_rekap_individual_pdf(df_transaksi, df_siswa, nisn_siswa, tahun):
            """Membuat rekap pembayaran individual per siswa dengan text wrap"""
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
            styles = getSampleStyleSheet()
            
            # Buat style untuk wrap text
            wrap_style = ParagraphStyle(
                'WrapStyle',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK'
            )
            
            wrap_style_bold = ParagraphStyle(
                'WrapStyleBold',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK',
                fontName='Helvetica-Bold'
            )
            
            wrap_style_header = ParagraphStyle(
                'WrapStyleHeader',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK',
                fontName='Helvetica-Bold',
                textColor=colors.whitesmoke
            )
            
            story = []
            
            # Header dengan layout yang lebih baik
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=6,
                alignment=1,
                textColor=colors.black
            )
            
            story.append(Paragraph("YAYASAN PENDIDIKAN PELITA INSANI KAHURIPAN", title_style))
            story.append(Paragraph("SEKOLAH PELITA INSANI", title_style))
            story.append(Spacer(1, 6))
            
            # Header dengan alignment yang tepat
            header_table_data = [
                [Paragraph("REKAPITULASI PEMBAYARAN SISWA", ParagraphStyle(
                    'CenterBold',
                    parent=styles['Normal'],
                    fontSize=14,
                    alignment=1,
                    fontName='Helvetica-Bold'
                ))]
            ]
            
            header_table = Table(header_table_data, colWidths=[600])
            header_table.setStyle(TableStyle([
                ('BOTTOMPADDING', (0, 0), (0, 0), 10),
            ]))
            
            story.append(header_table)
            story.append(Spacer(1, 10))
            
            # Data siswa dengan alignment yang baik
            siswa = df_siswa[df_siswa['NISN'] == nisn_siswa].iloc[0]
            
            # Layout data siswa dengan alignment yang benar
            data_siswa = [
                [Paragraph("Nama Siswa", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(siswa['Nama Lengkap']), wrap_style)],
                [Paragraph("No Induk Siswa", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(siswa['NIS']), wrap_style)],
                [Paragraph("Jenjang Pendidikan", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(siswa['Jenjang Sekolah']), wrap_style)],
                [Paragraph("Kelas", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(siswa['Kelas']), wrap_style)],
                [Paragraph("Tahun", wrap_style_bold), Paragraph(":", wrap_style_bold), Paragraph(str(tahun), wrap_style)]
            ]
            
            siswa_table = Table(data_siswa, colWidths=[120, 15, 400])
            siswa_table.setStyle(TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (0, -1), 50),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            story.append(siswa_table)
            story.append(Spacer(1, 15))
            
            # Data transaksi siswa untuk tahun tertentu
            df_transaksi_copy = df_transaksi.copy()
            df_transaksi_copy['Tanggal'] = pd.to_datetime(df_transaksi_copy['Tanggal'])
            transaksi_siswa = df_transaksi_copy[
                (df_transaksi_copy['NISN'] == nisn_siswa) & 
                (df_transaksi_copy['Tanggal'].dt.year == tahun)
            ]
            
            if not transaksi_siswa.empty:
                # Kategori pembayaran dengan singkatan yang lebih pendek
                kategori_list = [
                    "Pendaftaran", "UP", "SPP", "Buku", "Seragam", 
                    "Ekskul", "Catering", "Jemputan", "Kegiatan", 
                    "Tasyakuran", "Kelulusan", "Fieldtrip"
                ]
                
                # Mapping kategori lengkap ke singkatan
                kategori_mapping = {
                    "Uang Pendaftaran": "Pendaftaran",
                    "Uang Pangkal (UP)": "UP",
                    "Uang Sumbangan Pendidikan (SPP)": "SPP",
                    "Uang Buku": "Buku",
                    "Uang Seragam": "Seragam",
                    "Uang Iuran Ekskul": "Ekskul",
                    "Catering Siswa": "Catering",
                    "Jemputan Siswa": "Jemputan",
                    "Iuran Kegiatan Siswa": "Kegiatan",
                    "Tasyakuran": "Tasyakuran",
                    "Administrasi Kelulusan": "Kelulusan",
                    "Fieldtrip": "Fieldtrip"
                }
                
                # Siapkan data tabel dengan layout landscape yang lebih baik
                header = [Paragraph("No", wrap_style_header), Paragraph("BULAN", wrap_style_header)]
                for k in kategori_list:
                    header.append(Paragraph(k, wrap_style_header))
                header.append(Paragraph("Jumlah", wrap_style_header))
                
                table_data = [header]
                
                # Data per bulan
                bulan_list = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", 
                             "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
                
                # Inisialisasi total dengan semua kategori
                total_kategori = {kategori: 0 for kategori in kategori_list}
                total_keseluruhan = 0
                
                for i, bulan in enumerate(bulan_list, 1):
                    transaksi_bulan = transaksi_siswa[transaksi_siswa['Tanggal'].dt.month == i]
                    
                    if not transaksi_bulan.empty:
                        row_data = [Paragraph(str(i), wrap_style), Paragraph(f"{bulan} {tahun}", wrap_style)]
                        
                        # Hitung per kategori
                        jumlah_bulan = 0
                        for kategori_panjang, kategori_singkat in kategori_mapping.items():
                            jumlah_kategori = transaksi_bulan[transaksi_bulan['Kategori'] == kategori_panjang]['Jumlah'].sum()
                            row_data.append(Paragraph(f"{jumlah_kategori:,.0f}" if jumlah_kategori > 0 else "", wrap_style))
                            total_kategori[kategori_singkat] += jumlah_kategori
                            jumlah_bulan += jumlah_kategori
                        
                        row_data.append(Paragraph(f"{jumlah_bulan:,.0f}", wrap_style))
                        total_keseluruhan += jumlah_bulan
                        table_data.append(row_data)
                    else:
                        row_data = [Paragraph(str(i), wrap_style), Paragraph(f"{bulan} {tahun}", wrap_style)]
                        for _ in kategori_list:
                            row_data.append(Paragraph("", wrap_style))
                        row_data.append(Paragraph("", wrap_style))
                        table_data.append(row_data)
                
                # Baris total
                row_total = [Paragraph("", wrap_style_bold), Paragraph("TOTAL", wrap_style_bold)]
                for kategori in kategori_list:
                    row_total.append(Paragraph(f"{total_kategori[kategori]:,.0f}" if total_kategori[kategori] > 0 else "", wrap_style_bold))
                row_total.append(Paragraph(f"{total_keseluruhan:,.0f}", wrap_style_bold))
                table_data.append(row_total)
                
                # Buat tabel dengan lebar kolom yang sesuai landscape
                col_widths = [25, 50] + [45] * len(kategori_list) + [60]
                rekap_table = Table(table_data, colWidths=col_widths, repeatRows=1)
                rekap_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                story.append(rekap_table)
                story.append(Spacer(1, 30))
                
                # Tanda tangan di kanan bawah
                tanda_tangan_style = ParagraphStyle(
                    'RightAlign',
                    parent=styles['Normal'],
                    alignment=2,
                    fontSize=10
                )
                
                story.append(Paragraph("Bogor ..........................", tanda_tangan_style))
                story.append(Spacer(1, 10))
                story.append(Paragraph("WAHYU HANDAYANI", tanda_tangan_style))
                story.append(Paragraph("FINANCE", tanda_tangan_style))
                
            else:
                story.append(Paragraph("Tidak ada data pembayaran untuk siswa ini pada tahun yang dipilih.", styles['Normal']))
            
            doc.build(story)
            buffer.seek(0)
            return buffer

        def create_rekap_per_unit_pdf(df_transaksi, df_siswa, jenjang, bulan, tahun):
            """Membuat rekap pembayaran per unit sekolah dengan tanggal dan text wrap"""
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
            leftMargin=10,
            rightMargin=10,
            topMargin=30,
            bottomMargin=30)

            styles = getSampleStyleSheet()
            
            # Buat style untuk wrap text
            wrap_style = ParagraphStyle(
                'WrapStyle',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK'
            )
            
            wrap_style_bold = ParagraphStyle(
                'WrapStyleBold',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK',
                fontName='Helvetica-Bold'
            )
            
            wrap_style_header = ParagraphStyle(
                'WrapStyleHeader',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK',
                fontName='Helvetica-Bold',
                textColor=colors.whitesmoke
            )

            story = []

            # Konversi bulan dari integer ke nama bulan
            nama_bulan = [
                "Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"
            ]
            nama_bulan_str = nama_bulan[bulan - 1] if 1 <= bulan <= 12 else "Unknown"

            # Header
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=6,
                alignment=1,
                textColor=colors.black
            )

            story.append(Paragraph("YAYASAN PENDIDIKAN PELITA INSANI KAHURIPAN", title_style))
            story.append(Paragraph("SEKOLAH PELITA INSANI", title_style))
            story.append(Spacer(1, 6))
            
            # Header dengan alignment yang tepat
            header_table_data = [
                [Paragraph(f"REKAPITULASI PEMBAYARAN SISWA {jenjang}", ParagraphStyle(
                    'CenterBold',
                    parent=styles['Normal'],
                    fontSize=14,
                    alignment=1,
                    fontName='Helvetica-Bold'
                ))],
                [Paragraph(f"BULAN {nama_bulan_str.upper()} {tahun}", ParagraphStyle(
                    'CenterBold',
                    parent=styles['Normal'],
                    fontSize=12,
                    alignment=1,
                    fontName='Helvetica-Bold'
                ))]
            ]
            
            header_table = Table(header_table_data, colWidths=[600])
            header_table.setStyle(TableStyle([
                ('BOTTOMPADDING', (0, 0), (0, 0), 10),
                ('BOTTOMPADDING', (0, 1), (0, 1), 5),
            ]))
            
            story.append(header_table)
            story.append(Spacer(1, 10))

            # Filter siswa berdasarkan jenjang
            siswa_jenjang = df_siswa[df_siswa['Jenjang Sekolah'] == jenjang]

            if not siswa_jenjang.empty:
                # Filter transaksi berdasarkan bulan dan tahun
                df_transaksi_copy = df_transaksi.copy()
                df_transaksi_copy['Tanggal'] = pd.to_datetime(df_transaksi_copy['Tanggal'])
                transaksi_bulan = df_transaksi_copy[
                    (df_transaksi_copy['Tanggal'].dt.month == bulan) & 
                    (df_transaksi_copy['Tanggal'].dt.year == tahun) &
                    (df_transaksi_copy['NISN'].isin(siswa_jenjang['NISN']))
                ]

                if not transaksi_bulan.empty:
                    # Gabungkan data untuk mendapatkan nama siswa
                    data_gabung = pd.merge(transaksi_bulan, siswa_jenjang, on='NISN', how='left')
                    
                    # Kategori pembayaran dengan singkatan
                    kategori_list = [
                        "Pendaftaran", "UP", "SPP", "Buku", "Seragam", 
                        "Ekskul", "Catering", "Jemputan", "Kegiatan", 
                        "Tasyakuran", "Kelulusan", "Fieldtrip"
                    ]
                    
                    # Mapping kategori lengkap ke singkatan
                    kategori_mapping = {
                        "Uang Pendaftaran": "Pendaftaran",
                        "Uang Pangkal (UP)": "UP",
                        "Uang Sumbangan Pendidikan (SPP)": "SPP",
                        "Uang Buku": "Buku",
                        "Uang Seragam": "Seragam",
                        "Uang Iuran Ekskul": "Ekskul",
                        "Catering Siswa": "Catering",
                        "Jemputan Siswa": "Jemputan",
                        "Iuran Kegiatan Siswa": "Kegiatan",
                        "Tasyakuran": "Tasyakuran",
                        "Administrasi Kelulusan": "Kelulusan",
                        "Fieldtrip": "Fieldtrip"
                    }

                    # Siapkan data tabel dengan layout yang lebih baik
                    header = [
                        Paragraph("No", wrap_style_header),
                        Paragraph("Nama Siswa - Kelas", wrap_style_header),
                        Paragraph("Tanggal", wrap_style_header)
                    ]
                    for k in kategori_list:
                        header.append(Paragraph(k, wrap_style_header))
                    header.append(Paragraph("Jumlah", wrap_style_header))

                    table_data = [header]

                    # Kelompokkan per siswa
                    total_kategori = {k: 0 for k in kategori_mapping.values()}
                    total_keseluruhan = 0
                    no = 1

                    for i, (index, data_siswa) in enumerate(siswa_jenjang.iterrows(), 1):
                        transaksi_siswa = transaksi_bulan[transaksi_bulan['NISN'] == data_siswa['NISN']]
                        
                        if not transaksi_siswa.empty:
                            # Ambil tanggal transaksi terakhir
                            tanggal_transaksi = transaksi_siswa['Tanggal'].max()
                            tanggal_str = tanggal_transaksi.strftime('%d/%m/%Y') if hasattr(tanggal_transaksi, 'strftime') else ""
                            
                            # Gabungkan Nama dan Kelas menjadi satu kolom dengan Paragraph
                            nama_kelas = f"{data_siswa['Nama Lengkap']} - {data_siswa['Kelas']}"
                            row_data = [
                                Paragraph(str(no), wrap_style),
                                Paragraph(nama_kelas, wrap_style),
                                Paragraph(tanggal_str, wrap_style)
                            ]
                            
                            # Hitung per kategori
                            jumlah_siswa = 0
                            for kategori_panjang, kategori_singkat in kategori_mapping.items():
                                jumlah_kategori = transaksi_siswa[transaksi_siswa['Kategori'] == kategori_panjang]['Jumlah'].sum()
                                row_data.append(Paragraph(f"{jumlah_kategori:,.0f}" if jumlah_kategori > 0 else "", wrap_style))
                                total_kategori[kategori_singkat] += jumlah_kategori
                                jumlah_siswa += jumlah_kategori
                            
                            row_data.append(Paragraph(f"{jumlah_siswa:,.0f}", wrap_style))
                            total_keseluruhan += jumlah_siswa
                            table_data.append(row_data)
                            no += 1

                    # Baris total
                    row_total = [
                        Paragraph("", wrap_style_bold),
                        Paragraph("TOTAL", wrap_style_bold),
                        Paragraph("", wrap_style_bold)
                    ]
                    for kategori in kategori_list:
                        row_total.append(Paragraph(f"{total_kategori[kategori]:,.0f}" if total_kategori.get(kategori, 0) > 0 else "", wrap_style_bold))
                    row_total.append(Paragraph(f"{total_keseluruhan:,.0f}", wrap_style_bold))
                    table_data.append(row_total)

                    # Buat tabel dengan lebar kolom yang sesuai
                    col_widths = [25, 130, 60] + [45] * len(kategori_list) + [60]
                    rekap_table = Table(table_data, colWidths=col_widths, repeatRows=1)
                    rekap_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (1, 0), (1, -2), 'LEFT'),
                        ('ALIGN', (2, 0), (2, -2), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                        ('TOPPADDING', (0, 0), (-1, -1), 3),
                        ('LEFTPADDING', (0, 0), (-1, -1), 2),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ]))

                    story.append(rekap_table)
                    story.append(Spacer(1, 30))

                    # Tanda tangan di kanan bawah
                    tanda_tangan_style = ParagraphStyle(
                        'RightAlign',
                        parent=styles['Normal'],
                        alignment=2,
                        fontSize=10
                    )

                    story.append(Paragraph("Bogor ..........................", tanda_tangan_style))
                    story.append(Spacer(1, 10))
                    story.append(Paragraph("WAHYU HANDAYANI", tanda_tangan_style))
                    story.append(Paragraph("FINANCE", tanda_tangan_style))

                else:
                    story.append(Paragraph("Tidak ada data pembayaran untuk periode ini.", styles['Normal']))
            else:
                story.append(Paragraph(f"Tidak ada data siswa untuk jenjang {jenjang}.", styles['Normal']))

            doc.build(story)
            buffer.seek(0)
            return buffer

        def create_rekap_per_kelas_pdf(df_transaksi, df_siswa, jenjang, kelas, bulan, tahun):
            """Membuat rekap pembayaran per kelas dengan tanggal dan text wrap"""
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
            styles = getSampleStyleSheet()
            
            # Buat style untuk wrap text
            wrap_style = ParagraphStyle(
                'WrapStyle',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK'
            )
            
            wrap_style_bold = ParagraphStyle(
                'WrapStyleBold',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK',
                fontName='Helvetica-Bold'
            )
            
            wrap_style_header = ParagraphStyle(
                'WrapStyleHeader',
                parent=styles['Normal'],
                fontSize=7,
                leading=8,
                wordWrap='CJK',
                fontName='Helvetica-Bold',
                textColor=colors.whitesmoke
            )

            story = []

            # Konversi bulan dari integer ke nama bulan
            nama_bulan = [
                "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"
            ]
            nama_bulan_str = nama_bulan[bulan - 1] if 1 <= bulan <= 12 else "Unknown"

            # Header
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=6,
                alignment=1,
                textColor=colors.black
            )

            story.append(Paragraph("YAYASAN PENDIDIKAN PELITA INSANI KAHURIPAN", title_style))
            story.append(Paragraph("SEKOLAH PELITA INSANI", title_style))
            story.append(Spacer(1, 6))
            
            # Header dengan alignment yang tepat
            header_table_data = [
                [Paragraph(f"REKAPITULASI PEMBAYARAN SISWA {jenjang}", ParagraphStyle(
                    'CenterBold',
                    parent=styles['Normal'],
                    fontSize=14,
                    alignment=1,
                    fontName='Helvetica-Bold'
                ))],
                [Paragraph(f"KELAS {kelas}", ParagraphStyle(
                    'CenterBold',
                    parent=styles['Normal'],
                    fontSize=12,
                    alignment=1,
                    fontName='Helvetica-Bold'
                ))],
                [Paragraph(f"BULAN {nama_bulan_str.upper()} {tahun}", ParagraphStyle(
                    'CenterBold',
                    parent=styles['Normal'],
                    fontSize=12,
                    alignment=1,
                    fontName='Helvetica-Bold'
                ))]
            ]
            
            header_table = Table(header_table_data, colWidths=[600])
            header_table.setStyle(TableStyle([
                ('BOTTOMPADDING', (0, 0), (0, 0), 10),
                ('BOTTOMPADDING', (0, 1), (0, 1), 5),
                ('BOTTOMPADDING', (0, 2), (0, 2), 5),
            ]))
            
            story.append(header_table)
            story.append(Spacer(1, 10))

            # Filter siswa berdasarkan jenjang dan kelas
            siswa_kelas = df_siswa[
                (df_siswa['Jenjang Sekolah'] == jenjang) &
                (df_siswa['Kelas'] == kelas)
            ]

            if not siswa_kelas.empty:
                # Filter transaksi berdasarkan bulan dan tahun
                df_transaksi_copy = df_transaksi.copy()
                df_transaksi_copy['Tanggal'] = pd.to_datetime(df_transaksi_copy['Tanggal'])
                transaksi_bulan = df_transaksi_copy[
                    (df_transaksi_copy['Tanggal'].dt.month == bulan) &
                    (df_transaksi_copy['Tanggal'].dt.year == tahun) &
                    (df_transaksi_copy['NISN'].isin(siswa_kelas['NISN']))
                ]

                if not transaksi_bulan.empty:
                    # Gabungkan data untuk mendapatkan nama siswa
                    data_gabung = pd.merge(transaksi_bulan, siswa_kelas, on='NISN', how='left')

                    # Kategori pembayaran dengan singkatan
                    kategori_list = [
                        "Pendaftaran", "UP", "SPP", "Buku", "Seragam", 
                        "Ekskul", "Catering", "Jemputan", "Kegiatan", 
                        "Tasyakuran", "Kelulusan", "Fieldtrip"
                    ]
                    
                    # Mapping kategori lengkap ke singkatan
                    kategori_mapping = {
                        "Uang Pendaftaran": "Pendaftaran",
                        "Uang Pangkal (UP)": "UP",
                        "Uang Sumbangan Pendidikan (SPP)": "SPP",
                        "Uang Buku": "Buku",
                        "Uang Seragam": "Seragam",
                        "Uang Iuran Ekskul": "Ekskul",
                        "Catering Siswa": "Catering",
                        "Jemputan Siswa": "Jemputan",
                        "Iuran Kegiatan Siswa": "Kegiatan",
                        "Tasyakuran": "Tasyakuran",
                        "Administrasi Kelulusan": "Kelulusan",
                        "Fieldtrip": "Fieldtrip"
                    }

                    # Siapkan data tabel dengan layout yang lebih baik
                    header = [
                        Paragraph("No", wrap_style_header),
                        Paragraph("Nama Siswa - Kelas", wrap_style_header),
                        Paragraph("Tanggal", wrap_style_header)
                    ]
                    for k in kategori_list:
                        header.append(Paragraph(k, wrap_style_header))
                    header.append(Paragraph("Jumlah", wrap_style_header))

                    table_data = [header]

                    # Kelompokkan per siswa
                    total_kategori = {k: 0 for k in kategori_mapping.values()}
                    total_keseluruhan = 0
                    no = 1

                    for i, (index, data_siswa) in enumerate(siswa_kelas.iterrows(), 1):
                        transaksi_siswa = transaksi_bulan[transaksi_bulan['NISN'] == data_siswa['NISN']]

                        if not transaksi_siswa.empty:
                            # Ambil tanggal transaksi terakhir
                            tanggal_transaksi = transaksi_siswa['Tanggal'].max()
                            tanggal_str = tanggal_transaksi.strftime('%d/%m/%Y') if hasattr(tanggal_transaksi, 'strftime') else ""
                            
                            # Gabungkan Nama dan Kelas menjadi satu kolom dengan Paragraph
                            nama_kelas = f"{data_siswa['Nama Lengkap']} - {data_siswa['Kelas']}"
                            row_data = [
                                Paragraph(str(no), wrap_style),
                                Paragraph(nama_kelas, wrap_style),
                                Paragraph(tanggal_str, wrap_style)
                            ]

                            # Hitung per kategori
                            jumlah_siswa = 0
                            for kategori_panjang, kategori_singkat in kategori_mapping.items():
                                jumlah_kategori = transaksi_siswa[transaksi_siswa['Kategori'] == kategori_panjang]['Jumlah'].sum()
                                row_data.append(Paragraph(f"{jumlah_kategori:,.0f}" if jumlah_kategori > 0 else "", wrap_style))
                                total_kategori[kategori_singkat] += jumlah_kategori
                                jumlah_siswa += jumlah_kategori

                            row_data.append(Paragraph(f"{jumlah_siswa:,.0f}", wrap_style))
                            total_keseluruhan += jumlah_siswa
                            table_data.append(row_data)
                            no += 1

                    # Baris total
                    row_total = [
                        Paragraph("", wrap_style_bold),
                        Paragraph("TOTAL", wrap_style_bold),
                        Paragraph("", wrap_style_bold)
                    ]
                    for kategori in kategori_list:
                        row_total.append(Paragraph(f"{total_kategori[kategori]:,.0f}" if total_kategori.get(kategori, 0) > 0 else "", wrap_style_bold))
                    row_total.append(Paragraph(f"{total_keseluruhan:,.0f}", wrap_style_bold))
                    table_data.append(row_total)

                    # Buat tabel dengan lebar kolom yang sesuai
                    col_widths = [25, 130, 60] + [45] * len(kategori_list) + [60]
                    rekap_table = Table(table_data, colWidths=col_widths, repeatRows=1)
                    rekap_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (1, 0), (1, -2), 'LEFT'),
                        ('ALIGN', (2, 0), (2, -2), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                        ('TOPPADDING', (0, 0), (-1, -1), 3),
                        ('LEFTPADDING', (0, 0), (-1, -1), 2),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ]))

                    story.append(rekap_table)
                    story.append(Spacer(1, 30))

                    # Tanda tangan di kanan bawah
                    tanda_tangan_style = ParagraphStyle(
                        'RightAlign',
                        parent=styles['Normal'],
                        alignment=2,
                        fontSize=10
                    )

                    story.append(Paragraph("Bogor ..........................", tanda_tangan_style))
                    story.append(Spacer(1, 10))
                    story.append(Paragraph("WAHYU HANDAYANI", tanda_tangan_style))
                    story.append(Paragraph("FINANCE", tanda_tangan_style))

                else:
                    story.append(Paragraph("Tidak ada data pembayaran untuk periode ini.", styles['Normal']))
            else:
                story.append(Paragraph(f"Tidak ada data siswa untuk kelas {kelas} {jenjang}.", styles['Normal']))

            doc.build(story)
            buffer.seek(0)
            return buffer

        # ==================== SUBMENU LAPORAN ====================
        laporan_submenu_aktif = st.session_state.get('laporan_submenu', 'Buku Kas Harian')

        with st.container():
            if laporan_submenu_aktif == "Buku Kas Harian":
                st.subheader("Buku Kas - Jurnal Harian/Bulanan/Tahunan")
                
                col_periode1, col_periode2 = st.columns(2)
                with col_periode1:
                    jenis_laporan = st.selectbox(
                        "Jenis Laporan:",
                        ["Harian", "Bulanan", "Tahunan"],
                        key="jenis_buku_kas"
                    )
                
                with col_periode2:
                    if jenis_laporan == "Harian":
                        tanggal_laporan = st.date_input("Pilih Tanggal", value=date.today(), key="tanggal_buku_kas")
                    elif jenis_laporan == "Bulanan":
                        col_bulan1, col_bulan2 = st.columns(2)
                        with col_bulan1:
                            bulan = st.selectbox(
                                "Pilih Bulan:",
                                range(1, 13),
                                format_func=lambda x: date(2023, x, 1).strftime('%B'),
                                index=date.today().month - 1,
                                key="bulan_buku_kas"
                            )
                        with col_bulan2:
                            tahun = st.selectbox(
                                "Pilih Tahun:",
                                range(2020, date.today().year + 2),
                                index=date.today().year - 2020,
                                key="tahun_buku_kas"
                            )
                        tanggal_laporan = date(tahun, bulan, 1)
                    else:
                        tahun = st.selectbox(
                            "Pilih Tahun:",
                            range(2020, date.today().year + 2),
                            index=date.today().year - 2020,
                            key="tahun_buku_kas_tahunan"
                        )
                        tanggal_laporan = date(tahun, 1, 1)
                
                # PREVIEW SUMMARY UNTUK KAS HARIAN (HARIAN SAJA)
                if jenis_laporan == "Harian":
                    st.subheader("Preview Data Harian")
                    
                    # Filter data untuk tanggal yang dipilih
                    data_harian = df_kas_harian[df_kas_harian['Tanggal'] == tanggal_laporan]
                    
                    if not data_harian.empty:
                        # Ringkasan harian
                        total_pemasukan_harian = data_harian[data_harian['Jenis'] == 'Pemasukan']['Jumlah'].sum()
                        total_pengeluaran_harian = data_harian[data_harian['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
                        saldo_harian = total_pemasukan_harian - total_pengeluaran_harian
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Pemasukan Harian", format_rupiah(total_pemasukan_harian))
                        col2.metric("Total Pengeluaran Harian", format_rupiah(total_pengeluaran_harian))
                        col3.metric("Saldo Harian", format_rupiah(saldo_harian))
                        
                        # Format angka dalam dataframe
                        data_harian_display = data_harian.copy()
                        data_harian_display['Jumlah'] = data_harian_display['Jumlah'].apply(format_rupiah_detailed)
                        
                        # Tampilkan detail transaksi
                        st.dataframe(
                            data_harian_display[['Tanggal', 'Kategori', 'Jenis', 'Jumlah', 'Deskripsi']].sort_values('Jenis', ascending=False),
                            use_container_width=True
                        )
                    else:
                        st.info("Tidak ada transaksi pada tanggal yang dipilih")

            elif laporan_submenu_aktif == "Laporan Keuangan":
                st.subheader("Laporan Keuangan (Rentang Tanggal)")
                
                col_periode1, col_periode2 = st.columns(2)
                with col_periode1:
                    tanggal_awal = st.date_input(
                        "Tanggal Awal",
                        value=date(date.today().year, date.today().month, 1),
                        key="tanggal_awal_laporan"
                    )
                
                with col_periode2:
                    tanggal_akhir = st.date_input(
                        "Tanggal Akhir",
                        value=date.today(),
                        key="tanggal_akhir_laporan"
                    )
                
                # Validasi tanggal
                if tanggal_awal > tanggal_akhir:
                    st.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")
                else:
                    # Tampilkan preview data summary
                    st.subheader("Preview Summary Data")
                    
                    # Filter data untuk preview
                    df_preview = df.copy()
                    df_preview['Tanggal'] = pd.to_datetime(df_preview['Tanggal'])
                    transaksi_preview = df_preview[
                        (df_preview['Tanggal'] >= pd.Timestamp(tanggal_awal)) & 
                        (df_preview['Tanggal'] <= pd.Timestamp(tanggal_akhir))
                    ]
                    
                    if not transaksi_preview.empty:
                        # Buat summary per kategori
                        summary_data = transaksi_preview.groupby(['Kategori', 'Jenis'])['Jumlah'].sum().reset_index()
                        
                        # Format angka dalam summary
                        summary_data_display = summary_data.copy()
                        summary_data_display['Jumlah'] = summary_data_display['Jumlah'].apply(format_rupiah_detailed)
                        
                        # Tampilkan summary
                        st.dataframe(
                            summary_data_display.pivot_table(
                                index='Kategori', 
                                columns='Jenis', 
                                values='Jumlah', 
                                aggfunc='sum'
                            ).fillna(0),
                            use_container_width=True
                        )
                        
                        # Ringkasan
                        total_pemasukan = transaksi_preview[transaksi_preview['Jenis'] == 'Pemasukan']['Jumlah'].sum()
                        total_pengeluaran = transaksi_preview[transaksi_preview['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
                        saldo = total_pemasukan - total_pengeluaran
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Pemasukan", format_rupiah(total_pemasukan))
                        col2.metric("Total Pengeluaran", format_rupiah(total_pengeluaran))
                        col3.metric("Saldo", format_rupiah(saldo))
                        
                        if st.button("Cetak Laporan Keuangan Detail", use_container_width=True):
                            pdf_buffer = create_laporan_keuangan_periode_pdf(df, tanggal_awal, tanggal_akhir)
                            
                            file_name = f"laporan_keuangan_detail_{tanggal_awal.strftime('%Y%m%d')}_sd_{tanggal_akhir.strftime('%Y%m%d')}.pdf"
                            
                            st.download_button(
                                label="📄 Download Laporan Keuangan Detail (PDF)",
                                data=pdf_buffer,
                                file_name=file_name,
                                mime="application/pdf",
                                use_container_width=True
                            )
                    else:
                        st.info("Tidak ada data transaksi untuk periode yang dipilih")

            elif laporan_submenu_aktif == "Jurnal Per Siswa":
                st.subheader("Jurnal Pembayaran Per Siswa")
                
                if not df_siswa.empty:
                    col_siswa1, col_siswa2 = st.columns(2)
                    with col_siswa1:
                        selected_index = st.selectbox(
                            "Pilih Siswa:",
                            options=range(len(df_siswa)),
                            format_func=lambda x: f"{df_siswa.iloc[x]['NISN']} - {df_siswa.iloc[x]['Nama Lengkap']} - {df_siswa.iloc[x]['Kelas']}",
                            key="select_siswa_jurnal"
                        )
                    
                    selected_siswa = df_siswa.iloc[selected_index]
                    
                    with col_siswa2:
                        st.info(f"Terpilih: {selected_siswa['Nama Lengkap']}")
                    
                    if st.button("Cetak Jurnal Per Siswa", use_container_width=True):
                        pdf_buffer = create_jurnal_per_siswa_pdf(df, df_siswa, selected_siswa['NISN'])
                        
                        st.download_button(
                            label="📄 Download Jurnal Per Siswa (PDF - Landscape)",
                            data=pdf_buffer,
                            file_name=f"jurnal_siswa_{selected_siswa['NISN']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.info("Belum ada data siswa")

            elif laporan_submenu_aktif == "Rekap Individual":
                st.subheader("Rekapitulasi Pembayaran Per Siswa (Individual)")
                
                if not df_siswa.empty:
                    col_siswa1, col_siswa2 = st.columns(2)
                    with col_siswa1:
                        selected_index = st.selectbox(
                            "Pilih Siswa:",
                            options=range(len(df_siswa)),
                            format_func=lambda x: f"{df_siswa.iloc[x]['NISN']} - {df_siswa.iloc[x]['Nama Lengkap']} - {df_siswa.iloc[x]['Kelas']}",
                            key="select_siswa_rekap_individu"
                        )
                    
                    selected_siswa = df_siswa.iloc[selected_index]
                    
                    with col_siswa2:
                        tahun = st.selectbox(
                            "Pilih Tahun:",
                            range(2020, date.today().year + 2),
                            index=date.today().year - 2020,
                            key="tahun_rekap_individu"
                        )
                    
                    if st.button("Cetak Rekap Individual", use_container_width=True):
                        pdf_buffer = create_rekap_individual_pdf(df, df_siswa, selected_siswa['NISN'], tahun)
                        
                        st.download_button(
                            label="📄 Download Rekap Individual (PDF - Landscape)",
                            data=pdf_buffer,
                            file_name=f"rekap_individual_{selected_siswa['NISN']}_{tahun}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.info("Belum ada data siswa")

            elif laporan_submenu_aktif == "Rekap Per Unit":
                st.subheader("Rekapitulasi Pembayaran Per Unit Sekolah")
                
                col_filter1, col_filter2, col_filter3 = st.columns(3)
                with col_filter1:
                    jenjang = st.selectbox(
                        "Pilih Jenjang:",
                        ["TK", "SD", "SMP"],
                        key="jenjang_rekap_unit"
                    )
                
                with col_filter2:
                    bulan = st.selectbox(
                        "Pilih Bulan:",
                        range(1, 13),
                        format_func=lambda x: date(2023, x, 1).strftime('%B'),
                        index=date.today().month - 1,
                        key="bulan_rekap_unit"
                    )
                
                with col_filter3:
                    tahun = st.selectbox(
                        "Pilih Tahun:",
                        range(2020, date.today().year + 2),
                        index=date.today().year - 2020,
                        key="tahun_rekap_unit"
                    )
                
                if st.button("Cetak Rekap Per Unit", use_container_width=True):
                    try:
                        pdf_buffer = create_rekap_per_unit_pdf(df, df_siswa, jenjang, bulan, tahun)
                        
                        st.download_button(
                            label="📄 Download Rekap Per Unit (PDF - Landscape)",
                            data=pdf_buffer,
                            file_name=f"rekap_{jenjang}_{bulan}_{tahun}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {str(e)}")

            elif laporan_submenu_aktif == "Rekap Per Kelas":
                st.subheader("Rekapitulasi Pembayaran Per Kelas")
                
                col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
                with col_filter1:
                    jenjang = st.selectbox(
                        "Pilih Jenjang:",
                        ["TK", "SD", "SMP"],
                        key="jenjang_rekap_kelas"
                    )
                
                with col_filter2:
                    # Dapatkan kelas berdasarkan jenjang
                    if not df_siswa.empty and jenjang:
                        kelas_options = df_siswa[df_siswa['Jenjang Sekolah'] == jenjang]['Kelas'].unique()
                        if len(kelas_options) > 0:
                            kelas = st.selectbox(
                                "Pilih Kelas:",
                                kelas_options,
                                key="kelas_rekap_kelas"
                            )
                        else:
                            st.info(f"Belum ada data siswa untuk jenjang {jenjang}")
                            kelas = ""
                    else:
                        st.info("Belum ada data siswa")
                        kelas = ""
                
                with col_filter3:
                    bulan = st.selectbox(
                        "Pilih Bulan:",
                        range(1, 13),
                        format_func=lambda x: date(2023, x, 1).strftime('%B'),
                        index=date.today().month - 1,
                        key="bulan_rekap_kelas"
                    )
                
                with col_filter4:
                    tahun = st.selectbox(
                        "Pilih Tahun:",
                        range(2020, date.today().year + 2),
                        index=date.today().year - 2020,
                        key="tahun_rekap_kelas"
                    )
                
                if st.button("Cetak Rekap Per Kelas", use_container_width=True) and kelas:
                    pdf_buffer = create_rekap_per_kelas_pdf(df, df_siswa, jenjang, kelas, bulan, tahun)
                    
                    st.download_button(
                        label="📄 Download Rekap Per Kelas (PDF - Landscape)",
                        data=pdf_buffer,
                        file_name=f"rekap_{jenjang}_{kelas}_{bulan}_{tahun}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

    # Tutup container utama
    st.markdown("</div>", unsafe_allow_html=True)

    # ==================== FOOTER ====================
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Aplikasi Manajemen Data & Keuangan Sekolah Pelita Insani © 2025"
        "</div>",
        unsafe_allow_html=True
    )
