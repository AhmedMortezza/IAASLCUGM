import base64
import os
import pandas as pd
import streamlit as st

# Page Configuration
icon_file = "iaas.jpg" if os.path.exists("iaas.jpg") else None

st.set_page_config(
    page_title="Pengumuman Lolos Berkas IAAS LC UGM 2026",
    page_icon=icon_file,
    layout="centered",
)


# read background
def get_base64_of_bin_file(bin_file):
  with open(bin_file, "rb") as f:
    data = f.read()
  return base64.b64encode(data).decode()

base_dirs = [
    os.path.dirname(__file__) if "__file__" in locals() else os.getcwd(),
    os.getcwd(),
]

bg_image_file = None
mime_type = "jpeg"

for b_dir in base_dirs:
  if bg_image_file:
    break
  if os.path.exists(b_dir):
    for file in os.listdir(b_dir):
      if file.lower().startswith("background.") and file.lower().endswith(
          (".jpg", ".jpeg", ".png")
      ):
        bg_image_file = os.path.join(b_dir, file)
        mime_type = "png" if file.lower().endswith(".png") else "jpeg"
        break

bg_css = ""
if bg_image_file and os.path.exists(bg_image_file):
  bin_str = get_base64_of_bin_file(bg_image_file)
  bg_css = f"""
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main {{
        background-color: transparent !important;
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0) !important;
    }}
    
    [data-testid="stAppViewContainer"]::before, .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url("data:image/{mime_type};base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.35;
        z-index: -1;
    }}
    """

# Custom when dark mode
main_css = """
/* Force warna teks gelap pada seluruh komponen di dalam container */
.block-container, .block-container p, .block-container span, 
.block-container label, .block-container div, [data-testid="stMarkdownContainer"] p {
    color: #1f2937 !important;
}

/* Box Putih Transparan Khusus Tempat Konten */
.block-container {
    background-color: rgba(255, 255, 255, 0.94) !important;
    padding: 2.5rem 2rem !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12) !important;
    margin-top: 1.5rem !important;
    margin-bottom: 2rem !important;
    backdrop-filter: blur(4px) !important;
}

/* Mengurangi jarak bawah gambar logo */
[data-testid="stImage"] {
    margin-bottom: -15px !important;
}

/* Menarik tulisan pengumuman lebih dekat ke logo */
h1 {
    color: #1E5631 !important;
    font-weight: 700 !important;
    margin-top: -25px !important;
    margin-bottom: 15px !important;
    line-height: 1.2 !important;
}

/* Form & Input Field Text Fix untuk Dark Mode */
div[data-testid="stForm"] {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    padding: 20px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

/* Memastikan teks yang diketik di input tetap berwarna gelap */
input[type="text"], .stTextInput input {
    color: #1f2937 !important;
    background-color: #ffffff !important;
}

/* Detail Card Hasil */
.detail-card {
    background-color: #ffffff !important;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #1E5631;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    margin-top: 10px;
    margin-bottom: 20px;
}

.detail-card p, .detail-card b, .detail-card h4 {
    color: #1f2937 !important;
}

/* Tombol */
div.stButton > button, div.stLinkButton > a {
    background-color: #1E5631 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    border: none !important;
    transition: 0.3s !important;
}

div.stButton > button:hover, div.stLinkButton > a:hover {
    background-color: #143F23 !important;
    color: #ffffff !important;
}
"""

# merge CSS style
st.markdown(
    "<style>" + bg_css + main_css + "</style>", unsafe_allow_html=True
)

# Subheading
col1, col2, col3 = st.columns([0.2, 3.6, 0.2])
with col2:
  subheading_file = None
  for b_dir in base_dirs:
    if subheading_file:
      break
    if os.path.exists(b_dir):
      for file in os.listdir(b_dir):
        if file.lower().startswith("subheading.") and file.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
          subheading_file = os.path.join(b_dir, file)
          break

  if subheading_file:
    st.image(subheading_file, use_container_width=True)

# Header Text
st.markdown(
    "<h1 style='text-align: center; margin-top: -30px !important;'>"
    " Pengumuman Lolos Berkas<br>IAAS LC UGM 2026</h1>",
    unsafe_allow_html=True,
)
st.write("Silahkan masukkan **Nama Lengkap** kamu di bawah ini!")


# Load Data
@st.cache_data
def load_data():
  possible_files = ["database_updated.csv", "data_peserta.csv", "database.csv"]
  target_file = None

  for b_dir in base_dirs:
    if target_file:
      break
    for file_name in possible_files:
      file_path = os.path.join(b_dir, file_name)
      if os.path.exists(file_path):
        target_file = file_path
        break

  if not target_file:
    raise FileNotFoundError("File CSV tidak ditemukan di folder project.")

  try:
    df = pd.read_csv(target_file, sep=None, engine="python", encoding="utf-8")
  except UnicodeDecodeError:
    df = pd.read_csv(target_file, sep=None, engine="python", encoding="latin1")

  df.columns = df.columns.str.strip().str.lower()
  df["nama_clean"] = df["nama"].astype(str).str.strip().str.lower()
  return df


try:
  df_peserta = load_data()
except Exception as e:
  st.error(f"❌ **Gagal membaca file data:** {e}")
  st.info(
      "💡 Pastikan kamu sudah menyimpan file CSV (`database_updated.csv` atau"
      " `data_peserta.csv`) di folder yang sama."
  )
  st.stop()

# Input Form
with st.form(key="search_form"):
  nama_input = st.text_input(
      "Nama Lengkap Peserta:", placeholder="Contoh: Lionel Messi"
  )
  submit_button = st.form_submit_button(label="🔍 Cari")

# Main Logic
if submit_button:
  if not nama_input.strip():
    st.warning("⚠️ Harap masukkan nama terlebih dahulu.")
  else:
    query_nama = nama_input.strip().lower()
    hasil = df_peserta[df_peserta["nama_clean"] == query_nama]

    if not hasil.empty:
      data = hasil.iloc[0]
      nama_resmi = data.get("nama", "")
      department = data.get("department", data.get("departemen", ""))
      status = str(data.get("status", "")).strip()
      prodi = data.get("prodi", "")

      st.divider()

      st.markdown(
          f"""
                <div class="detail-card">
                    <h4 style="color: #1E5631; margin-top:0; margin-bottom:12px;">📌 Detail Peserta</h4>
                    <p style="margin-bottom: 6px;"><b>Nama:</b> {nama_resmi}</p>
                    <p style="margin-bottom: 6px;"><b>Department:</b> {department}</p>
                    <p style="margin-bottom: 0;"><b>Program Studi:</b> {prodi}</p>
                </div>
            """,
          unsafe_allow_html=True,
      )

      if status.lower() == "lolos":
        st.success(
            "🎉 **SELAMAT! Kamu LOLOS BERKAS, harap perhatikan Department untuk"
            " tahap INTERNSHIP**"
        )
        st.info(
            "Silakan melanjutkan ke tahap pengisian jadwal Interview melalui"
            " tombol di bawah ini."
        )

        link_sps = (
            "https://docs.google.com/spreadsheets/d/1azmboGYBXHWY31AjVfZqfB7LrCHO1P11gO0n39g4nc4/edit?usp=sharing"
        )

        st.link_button(
            label="📅 Klik di Sini untuk Mengisi Jadwal Interview",
            url=link_sps,
            type="primary",
            use_container_width=True,
        )
      else:
        st.error("❌ **MOHON MAAF, Anda Dinyatakan BELUM LOLOS.**")
        st.write(
            "Terima kasih telah berpartisipasi dalam Seleksi IAAS LC UGM 2026."
            " Tetap semangat!"
        )

    else:
      st.warning("⚠️ **Data Tidak Ditemukan.**")
      st.write(
          "Pastikan penulisan nama sudah sesuai dan lengkap tanpa kesalahan"
          " ejaan."
      )
