import streamlit as st
import pandas as pd
import os

# Page
icon_page = "iaas.jpg"

st.set_page_config(
    page_title="Pengumuman Lolos Berkas IAAS LC UGM 2026",
    page_icon=icon_page,
    layout="centered"
)

# Custom Color
st.markdown("""
    <style>
    /* Background Utama Soft Light Gray/Green */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header Utama */
    h1 {
        color: #1E5631 !important;
        font-weight: 700 !important;
    }
    
    /* Kartu Detail Peserta */
    .detail-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #1E5631;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    /* Styling Tombol Utama (Cari & Link SPS) */
    div.stButton > button, div.stLinkButton > a {
        background-color: #1E5631 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        transition: 0.3s !important;
    }
    
    /* Efek Hover Tombol */
    div.stButton > button:hover, div.stLinkButton > a:hover {
        background-color: #143F23 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'> Pengumuman Lolos Berkas<br>IAAS LC UGM 2026</h1>", unsafe_allow_html=True)
st.write("Silahkan masukkan **Nama Lengkap** kamu di bawah ini!")

# Load data
@st.cache_data
def load_data():
    possible_files = ["data_peserta.csv", "database.csv", "datbase.csv"]
    target_file = None
    
    for file in possible_files:
        if os.path.exists(file):
            target_file = file
            break
            
    if not target_file:
        raise FileNotFoundError("File CSV tidak ditemukan di folder project.")
        
    try:
        df = pd.read_csv(target_file, sep=None, engine='python', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(target_file, sep=None, engine='python', encoding='latin1')
    
    df.columns = df.columns.str.strip().str.lower()
    df['nama_clean'] = df['nama'].astype(str).str.strip().str.lower()
    return df

try:
    df_peserta = load_data()
except Exception as e:
    st.error(f"❌ **Gagal membaca file data:** {e}")
    st.info("💡 Pastikan kamu sudah menyimpan file CSV (`data_peserta.csv` atau `database.csv`) di folder yang sama.")
    st.stop()

# Input
with st.form(key="search_form"):
    nama_input = st.text_input("Nama Lengkap Peserta:", placeholder="Contoh: Lionel Messi")
    submit_button = st.form_submit_button(label="🔍 ")

# Main Logic
if submit_button:
    if not nama_input.strip():
        st.warning("⚠️ Harap masukkan nama terlebih dahulu.")
    else:
        query_nama = nama_input.strip().lower()
        hasil = df_peserta[df_peserta['nama_clean'] == query_nama]
        
        if not hasil.empty:
            data = hasil.iloc[0]
            nama_resmi = data['nama']
            Department = data['Department']
            status = str(data['status']).strip()
            prodi = data['prodi']
            
            st.divider()
            
            st.markdown(f"""
                <div class="detail-card">
                    <h4 style="color: #1E5631; margin-top:0; margin-bottom:12px;">📌 Detail Peserta</h4>
                    <p style="margin-bottom: 6px;"><b>Nama:</b> {nama_resmi}</p>
                    <p style="margin-bottom: 6px;"><b>No. Peserta:</b> {Department}</p>
                    <p style="margin-bottom: 0;"><b>Program Studi:</b> {prodi}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if status.lower() == "lolos":
                st.success("🎉 **SELAMAT! kamu LOLOS BERKAS, harap perhatikan Department untuk tahap INTERNSHIP**")
                st.info("Silakan melanjutkan ke tahap pengisian jadwal Interview melalui tombol di bawah ini.")
                
                link_sps = "https://docs.google.com/spreadsheets/d/1azmboGYBXHWY31AjVfZqfB7LrCHO1P11gO0n39g4nc4/edit?usp=sharing"
                
                st.link_button(
                    label="📅 Klik di Sini untuk Mengisi Jadwal Interview", 
                    url=link_sps,
                    type="primary",
                    use_container_width=True
                )
            else:
                st.error("❌ **MOHON MAAF, Anda Dinyatakan BELUM LOLOS.**")
                st.write("Terima kasih telah berpartisipasi dalam Seleksi IAAS LC UGM 2026. Tetap semangat!")
                
        else:
            st.warning("⚠️ **Data Tidak Ditemukan.**")
            st.write("Pastikan penulisan nama sudah sesuai dan lengkap tanpa kesalahan ejaan.")