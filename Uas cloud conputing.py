# ==========================================
# IMPORT LIBRARY
# ==========================================

import streamlit as st # membangun antarmuka aplikasi
import pandas as pd # mengolah dan menampilkan data dalam bentuk tabel
import sqlite3 # mengelola database SQLite untuk riwayat perhitngan
from datetime import datetime # Mengambil fungsi tanggal dan waktu untuk mencatat riwayat perhitungan

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(
    page_title="CalorieNeeds",  # Menentukan judul aplikasi yang tampil pada tab browser
    page_icon="🥗", #ikon
    layout="wide", # tata lrtak halmn
    initial_sidebar_state="expanded" #mengatur sidebar
)

# =====================================================
# CSS / DESAIN
# =====================================================
st.markdown("""
<style>
/* Mengimpor font Inter dari Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* Mengatur jenis font untuk seluruh aplikasi */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}


/* Mengatur warna latar belakang dan tulisan utama */
.stApp {
    background-color: #f5f8f6;
    color: #24352d;
    
/* Mengatur warna tulisan pada teks, judul, dan paragraf */
.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp li,
.stMarkdown,
.stMarkdown p,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4 {
    color: #24352d !important;
}

/* Mengatur warna dan ketebalan label pada formulir */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stRadio label {
    color: #24352d !important;
    font-weight: 600 !important;
}

/* Mengatur warna tulisan di dalam kolom input */
.stNumberInput input,
.stTextInput input,
.stSelectbox div[data-baseweb="select"] div {
    color: #ffffff !important;
}

/* Mengatur warna, ukuran, dan bentuk tombol hitung */
.stButton button,
.stFormSubmitButton button {
    background-color: #1d6849 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
}

/* Mengubah warna tombol ketika kursor diarahkan ke tombol */
.stButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #145238 !important;
    color: #ffffff !important;
}

/* Mengatur warna judul halaman */
h1, h2, h3, h4 {
    color: #174d38 !important;
}


/* Mengatur warna teks keterangan */
.small-muted {
    color: #64756b !important;
}
}

/* Mengatur warna latar belakang sidebar */
[data-testid="stSidebar"] {
    background: #174d38;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] .stRadio label {
    color: white !important;
    font-weight: 500;
}


/* Mengatur tampilan judul utama aplikasi */
.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #174d38;
    margin-bottom: 5px;
}

.subtitle {
    color: #64756b;
    font-size: 15px;
    margin-bottom: 25px;
}


/* Mengatur kotak banner utama pada halaman beranda */
.hero {
    background: linear-gradient(120deg, #174d38, #2c7957);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 32px;
    font-weight: 800;
}

.hero p {
    color: #e4f1e9;
    font-size: 15px;
}

/* Mengatur tampilan kotak atau kartu informasi */
.section-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #e3ebe5;
    margin-bottom: 18px;
}

.result-card {
    background: #e7f3eb;
    border: 1px solid #c9e2d1;
    border-radius: 15px;
    padding: 22px;
    margin: 15px 0;
}

.result-number {
    color: #174d38;
    font-size: 30px;
    font-weight: 800;
}

.small-muted {
    color: #68786f;
    font-size: 13px;
}

/* Mengatur tampilan tombol aplikasi */
div.stButton > button {
    background: #1d6849;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 20px;
    font-weight: 600;
}

div.stButton > button:hover {
    background: #145238;
    color: white;
    border: none;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2ebe4;
    padding: 17px;
    border-radius: 13px;
}

hr {
    border-color: #e1e9e3;
}

footer {
    visibility: hidden;
}

/* KOTAK HASIL BMR, TDEE, BMI */
div[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #dce9df !important;
    border-radius: 15px !important;
    padding: 20px !important;
}

/* TULISAN LABEL BMR, TDEE, BMI */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] label {
    color: #174d38 !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* ANGKA HASIL */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] div {
    color: #174d38 !important;
    font-size: 36px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

/* IKON TANDA TANYA PADA LABEL */
div[data-testid="stMetricLabel"] svg {
    fill: #426451 !important;
    color: #426451 !important;
}

/* KETERANGAN BMI */
div[data-testid="stMetricDelta"] {
    color: #1d6849 !important;
    opacity: 1 !important;
}
/* WARNA TULISAN BMR, TDEE, BMI */
[data-testid="stMetric"] [data-testid="stMetricLabel"],
[data-testid="stMetric"] [data-testid="stMetricLabel"] *,
[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
    color: #174d38 !important;
    -webkit-text-fill-color: #174d38 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNGSI PERHITUNGAN
# =====================================================

# Fungsi untuk menghitung kebutuhan kalori dasar (BMR)
def hitung_bmr(jenis_kelamin, berat, tinggi, usia):
    """
    Menghitung BMR menggunakan rumus Mifflin-St Jeor.
    Berat dalam kg, tinggi dalam cm, usia dalam tahun.
    """
    if jenis_kelamin == "Laki-laki":
        return (10 * berat) + (6.25 * tinggi) - (5 * usia) + 5
    else:
        return (10 * berat) + (6.25 * tinggi) - (5 * usia) - 161

# Fungsi untuk menghitung indeks massa tubuh (BMI)
def hitung_bmi(berat, tinggi):
    tinggi_meter = tinggi / 100
    return berat / (tinggi_meter ** 2)

# Fungsi untuk menentukan kategori BMI
def kategori_bmi(bmi):
    if bmi < 18.5:
        return "Berat badan kurang"
    elif bmi < 25:
        return "Berat badan normal"
    elif bmi < 30:
        return "Berat badan berlebih"
    else:
        return "Obesitas"

# Fungsi untuk mengubah format angka kalori agar mudah dibaca
def format_kalori(nilai):
    return f"{nilai:,.0f} kkal".replace(",", ".")


# Menentukan faktor pengali berdasarkan tingkat aktivitas fisik
faktor_aktivitas = {
    "Sangat ringan (jarang olahraga)": 1.2,
    "Ringan (1–3 hari/minggu)": 1.375,
    "Sedang (3–5 hari/minggu)": 1.55,
    "Berat (6–7 hari/minggu)": 1.725,
    "Sangat berat (aktivitas intens)": 1.9
}
# =====================================================
# DATABASE SQLITE
# =====================================================

DB_NAME = "calorieneeds.db" # Menentukan nama file database SQLite

# Fungsi untuk membuat koneksi ke database SQLite
def koneksi_database():
    return sqlite3.connect(DB_NAME)

# Fungsi untuk membuat tabel riwayat jika belum tersedia
def buat_tabel():
    conn = koneksi_database()
    cursor = conn.cursor()

# Membuat tabel riwayat dengan kolom sesuai data hasil perhitungan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS riwayat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            usia INTEGER,
            jenis_kelamin TEXT,
            berat REAL,
            tinggi REAL,
            aktivitas TEXT,
            tujuan TEXT,
            bmr REAL,
            tdee REAL,
            bmi REAL,
            kategori TEXT,
            target REAL
        )
    """)

    conn.commit()
    conn.close()

# Fungsi untuk menyimpan hasil perhitungan ke tabel riwayat
def simpan_riwayat(data):
    conn = koneksi_database()
    cursor = conn.cursor()

 # Memasukkan data hasil perhitungan ke dalam tabel riwayat
    cursor.execute("""
        INSERT INTO riwayat (
            tanggal, usia, jenis_kelamin, berat,
            tinggi, aktivitas, tujuan, bmr,
            tdee, bmi, kategori, target
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["tanggal"],
        data["usia"],
        data["jenis_kelamin"],
        data["berat"],
        data["tinggi"],
        data["aktivitas"],
        data["tujuan"],
        data["bmr"],
        data["tdee"],
        data["bmi"],
        data["kategori"],
        data["target"]
    ))

    conn.commit()
    conn.close()

# Fungsi untuk mengambil seluruh data riwayat dari database
def ambil_riwayat():
    conn = koneksi_database()

# Mengambil seluruh data dan mengurutkannya dari data terbaru
    df = pd.read_sql_query(
        "SELECT * FROM riwayat ORDER BY id DESC",
        conn
    )

    conn.close()
    return df

# Fungsi untuk menghapus seluruh data riwayat
def hapus_riwayat():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM riwayat")

    conn.commit()
    conn.close()


# Membuat tabel ketika aplikasi dijalankan
buat_tabel()

# =====================================================
# SESSION STATE
# =====================================================
if "riwayat" not in st.session_state: # Memeriksa apakah variabel riwayat sudah tersedia dalam session
    st.session_state.riwayat = []

if "hasil" not in st.session_state: # Memeriksa apakah variabel hasil sudah tersedia dalam session
    st.session_state.hasil = None


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar: # Membuat bagian navigasi pada sisi kiri aplikasi
    
    # Menampilkan logo, nama aplikasi, dan deskripsi singkat
    st.markdown("""
    <div style="text-align:center; padding:15px 5px 25px;">
        <div style="font-size:45px;">🥗</div>
        <div style="font-size:23px; font-weight:800;">CalorieNeeds</div>
        <div style="font-size:12px; opacity:0.8;">
            Daily Calorie Calculator
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

# Membuat pilihan menu navigasi aplikasi
    menu = st.radio(
        "MENU NAVIGASI",
        [
            "🏠 Beranda",
            "🧮 Kalkulator Kalori",
            "📁 Riwayat",
            "📚 Informasi"
        ],
        label_visibility="visible"
    )

    st.markdown("---")

# Menampilkan deskripsi singkat aplikasi pada bagian bawah sidebar
    st.markdown(""" 
    <div style="font-size:12px; opacity:0.8;">
        <b>CalorieNeeds</b><br>
        Aplikasi penghitung kebutuhan
        kalori harian berdasarkan data
        dan aktivitas pengguna.
    </div>
    """, unsafe_allow_html=True) # Mengaktifkan format HTML pada deskripsi


# =====================================================
# HALAMAN BERANDA
# =====================================================
if menu == "🏠 Beranda": # Memeriksa apakah pengguna memilih menu Beranda


# Menampilkan judul halaman Beranda
    st.markdown(
        '<div class="main-title">Beranda</div>',
        unsafe_allow_html=True
    )

# Menampilkan teks sambutan kepada pengguna
    st.markdown(
        '<div class="subtitle">Selamat datang di aplikasi CalorieNeeds.</div>',
        unsafe_allow_html=True
    )

 # Menampilkan bagian utama (hero) berisi judul dan deskripsi aplikasi
    st.markdown("""
    <div class="hero">
        <h1>Kenali Kebutuhan Kalori Harianmu</h1>
        <p>
            Hitung kebutuhan energi harian berdasarkan usia, jenis kelamin,
            berat badan, tinggi badan, dan tingkat aktivitas fisik.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Mengenal Kebutuhan Kalori")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="section-card">
            <div style="font-size:30px;">🔥</div>
            <h4>BMR</h4>
            <p class="small-muted">
                Energi minimum yang dibutuhkan tubuh untuk menjalankan
                fungsi dasar saat beristirahat.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-card">
            <div style="font-size:30px;">⚡</div>
            <h4>TDEE</h4>
            <p class="small-muted">
                Perkiraan total energi yang digunakan tubuh dalam
                satu hari berdasarkan aktivitas.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="section-card">
            <div style="font-size:30px;">⚖️</div>
            <h4>BMI</h4>
            <p class="small-muted">
                Indeks massa tubuh yang digunakan sebagai gambaran
                kategori berat badan berdasarkan tinggi badan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Cara Menggunakan Aplikasi")

    langkah1, langkah2, langkah3 = st.columns(3)

    with langkah1:
        st.markdown("""
        **01 — Masukkan Data**

        Isi usia, jenis kelamin, berat badan, dan tinggi badan.
        """)

    with langkah2:
        st.markdown("""
        **02 — Pilih Aktivitas**

        Tentukan tingkat aktivitas fisik sehari-hari.
        """)

    with langkah3:
        st.markdown("""
        **03 — Lihat Hasil**

        Tekan tombol hitung untuk melihat estimasi kebutuhan kalori.
        """)

    st.info("Mulai perhitungan melalui menu **Kalkulator Kalori** di sidebar.")


# =====================================================
# HALAMAN KALKULATOR
# =====================================================
elif menu == "🧮 Kalkulator Kalori":

    st.markdown(
        '<div class="main-title">Kalkulator Kebutuhan Kalori</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Masukkan data diri untuk mengetahui estimasi kebutuhan kalori harian.</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Data Diri")

    with st.form("form_perhitungan"):

        col1, col2 = st.columns(2)

        with col1:
            usia = st.number_input(
                "Usia (tahun)",
                min_value=15,
                max_value=100,
                value=22,
                step=1
            )

            jenis_kelamin = st.selectbox(
                "Jenis Kelamin",
                ["Perempuan", "Laki-laki"]
            )

            berat = st.number_input(
                "Berat Badan (kg)",
                min_value=20.0,
                max_value=300.0,
                value=55.0,
                step=0.5
            )

        with col2:
            tinggi = st.number_input(
                "Tinggi Badan (cm)",
                min_value=100.0,
                max_value=250.0,
                value=160.0,
                step=0.5
            )

            aktivitas = st.selectbox(
                "Tingkat Aktivitas Fisik",
                list(faktor_aktivitas.keys())
            )

            tujuan = st.selectbox(
                "Tujuan Berat Badan",
                [
                    "Mempertahankan berat badan",
                    "Menurunkan berat badan",
                    "Menaikkan berat badan"
                ]
            )

        tombol_hitung = st.form_submit_button(
            "🔥 Hitung Kebutuhan Kalori",
            use_container_width=True
        )

    # PROSES PERHITUNGAN
    if tombol_hitung:

        bmr = hitung_bmr(
            jenis_kelamin,
            berat,
            tinggi,
            usia
        )

        tdee = bmr * faktor_aktivitas[aktivitas]

        bmi = hitung_bmi(berat, tinggi)
        kategori = kategori_bmi(bmi)

        if tujuan == "Menurunkan berat badan":
            target = tdee - 300
        elif tujuan == "Menaikkan berat badan":
            target = tdee + 300
        else:
            target = tdee

        hasil = {
            "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "usia": usia,
            "jenis_kelamin": jenis_kelamin,
            "berat": berat,
            "tinggi": tinggi,
            "aktivitas": aktivitas,
            "tujuan": tujuan,
            "bmr": bmr,
            "tdee": tdee,
            "bmi": bmi,
            "kategori": kategori,
            "target": target
        }

        st.session_state.hasil = hasil
        simpan_riwayat(hasil)

    # HASIL LANGSUNG DI BAWAH FORM
    if st.session_state.hasil is not None:

        hasil = st.session_state.hasil

        st.markdown("---")
        st.markdown("## Hasil Perhitungan")

        st.success("Perhitungan berhasil dilakukan. Berikut hasil estimasi kebutuhan kalori Anda.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "BMR",
                format_kalori(hasil["bmr"]),
                help="Basal Metabolic Rate"
            )

        with col2:
            st.metric(
                "TDEE",
                format_kalori(hasil["tdee"]),
                help="Total Daily Energy Expenditure"
            )

        with col3:
            st.metric(
                "BMI",
                f'{hasil["bmi"]:.1f}',
                hasil["kategori"]
            )

        st.markdown("""
        <div class="result-card">
            <div style="font-size:15px; color:#426451;">
                REKOMENDASI TARGET KALORI HARIAN
            </div>
            <div class="result-number">
        """, unsafe_allow_html=True)

        st.markdown(
            f'<div class="result-number">{format_kalori(hasil["target"])}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="color:#426451;">Tujuan: {hasil["tujuan"]}</div></div>',
            unsafe_allow_html=True
        )

        st.markdown("### Ringkasan Data")

        ringkasan1, ringkasan2 = st.columns(2)

        with ringkasan1:
            st.write(f"**Usia:** {hasil['usia']} tahun")
            st.write(f"**Jenis kelamin:** {hasil['jenis_kelamin']}")
            st.write(f"**Berat badan:** {hasil['berat']} kg")

        with ringkasan2:
            st.write(f"**Tinggi badan:** {hasil['tinggi']} cm")
            st.write(f"**Aktivitas:** {hasil['aktivitas']}")
            st.write(f"**Kategori BMI:** {hasil['kategori']}")

        st.markdown("### Perbandingan Kebutuhan Kalori")

        grafik = pd.DataFrame({
            "Komponen": ["BMR", "TDEE", "Target Kalori"],
            "Kalori (kkal)": [
                round(hasil["bmr"]),
                round(hasil["tdee"]),
                round(hasil["target"])
            ]
        })

        st.bar_chart(
            grafik,
            x="Komponen",
            y="Kalori (kkal)"
        )

        st.caption(
            "Catatan: Hasil ini merupakan estimasi berdasarkan rumus "
            "Mifflin-St Jeor dan faktor aktivitas yang dipilih. "
            "Kebutuhan aktual dapat berbeda pada setiap individu."
        )

        if st.button("Hapus Hasil Perhitungan"):
            st.session_state.hasil = None
            st.rerun()


# =====================================================
# HALAMAN RIWAYAT
# =====================================================
# =====================================================
# HALAMAN RIWAYAT
# =====================================================
elif menu == "📁 Riwayat":

    st.markdown(
        '<div class="main-title">Riwayat Perhitungan</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Daftar hasil perhitungan kalori yang tersimpan dalam database.</div>',
        unsafe_allow_html=True
    )

    df = ambil_riwayat()

    if not df.empty:

        kolom_tampil = {
            "tanggal": "Tanggal",
            "usia": "Usia",
            "jenis_kelamin": "Jenis Kelamin",
            "berat": "Berat (kg)",
            "tinggi": "Tinggi (cm)",
            "bmr": "BMR",
            "tdee": "TDEE",
            "bmi": "BMI",
            "kategori": "Kategori BMI",
            "target": "Target Kalori",
            "tujuan": "Tujuan"
        }

        tabel = df[list(kolom_tampil.keys())].rename(
            columns=kolom_tampil
        )

        st.dataframe(
            tabel,
            use_container_width=True,
            hide_index=True
        )

        csv = tabel.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "⬇️ Unduh Riwayat CSV",
            data=csv,
            file_name="riwayat_calorieneeds.csv",
            mime="text/csv"
        )

        st.markdown("---")

        if st.button("Hapus Semua Riwayat"):
            hapus_riwayat()
            st.success("Seluruh riwayat berhasil dihapus.")
            st.rerun()

    else:
        st.info(
            "Belum ada riwayat perhitungan. "
            "Silakan lakukan perhitungan terlebih dahulu."
        )

# =====================================================
# HALAMAN INFORMASI
# =====================================================
elif menu == "📚 Informasi":

    st.markdown(
        '<div class="main-title">Informasi Aplikasi</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Pelajari konsep dan metode yang digunakan dalam CalorieNeeds.</div>',
        unsafe_allow_html=True
    )

    with st.expander("1. Apa itu BMR?"):
        st.write("""
        **Basal Metabolic Rate (BMR)** merupakan perkiraan jumlah energi
        yang dibutuhkan tubuh untuk menjalankan fungsi dasar ketika
        berada dalam kondisi istirahat.

        Aplikasi ini menggunakan rumus Mifflin-St Jeor:
        """)

        st.latex(
            r"BMR_{pria} = 10W + 6.25H - 5A + 5"
        )

        st.latex(
            r"BMR_{wanita} = 10W + 6.25H - 5A - 161"
        )

        st.write("""
        Keterangan:
        - W = Berat badan (kg)
        - H = Tinggi badan (cm)
        - A = Usia (tahun)
        """)

    with st.expander("2. Apa itu TDEE?"):
        st.write("""
        **Total Daily Energy Expenditure (TDEE)** merupakan perkiraan
        total energi yang digunakan tubuh dalam satu hari.
        """)
        st.latex(r"TDEE = BMR \times Faktor\ Aktivitas")

        st.write("Faktor aktivitas yang digunakan:")

        data_aktivitas = pd.DataFrame({
            "Tingkat Aktivitas": list(faktor_aktivitas.keys()),
            "Faktor": list(faktor_aktivitas.values())
        })

        st.dataframe(
            data_aktivitas,
            use_container_width=True,
            hide_index=True
        )

    with st.expander("3. Apa itu BMI?"):
        st.write("""
        **Body Mass Index (BMI)** atau Indeks Massa Tubuh merupakan
        perbandingan berat badan dengan kuadrat tinggi badan.
        """)

        st.latex(r"BMI = \frac{Berat\ Badan\ (kg)}{Tinggi\ Badan\ (m)^2}")

        st.write("""
        Kategori BMI yang digunakan:
        - Di bawah 18,5: Berat badan kurang
        - 18,5–24,9: Berat badan normal
        - 25,0–29,9: Berat badan berlebih
        - 30,0 atau lebih: Obesitas
        """)

    with st.expander("4. Target Kalori"):
        st.write("""
        Target kalori dihitung berdasarkan tujuan pengguna:

        - Mempertahankan berat badan: TDEE
        - Menurunkan berat badan: TDEE dikurangi 300 kkal
        - Menaikkan berat badan: TDEE ditambah 300 kkal

        Penyesuaian ini merupakan pendekatan sederhana untuk estimasi,
        bukan rekomendasi medis atau pengganti konsultasi ahli gizi.
        """)

    with st.expander("5. Alur Perhitungan Aplikasi"):
        st.write("""
        1. Pengguna memasukkan data diri.
        2. Sistem menghitung BMR menggunakan rumus Mifflin-St Jeor.
        3. Sistem menghitung TDEE berdasarkan faktor aktivitas.
        4. Sistem menghitung BMI berdasarkan berat dan tinggi badan.
        5. Sistem menentukan estimasi target kalori sesuai tujuan.
        6. Hasil ditampilkan dan disimpan dalam riwayat sesi.
        """)

    with st.expander("6. Teknologi yang Digunakan"):
        st.write("""
        - **Python:** Bahasa pemrograman utama.
        - **Streamlit:** Framework untuk membangun antarmuka aplikasi web.
        - **Pandas:** Pengolahan dan penyajian data riwayat.
        """)

    st.warning(
        "Informasi pada aplikasi bersifat edukatif. Hasil perhitungan "
        "merupakan estimasi dan tidak menggantikan saran tenaga kesehatan."
    )


# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#829087; font-size:12px; padding:10px;">
        CalorieNeeds | Daily Calorie Calculator
    </div>
    """,
    unsafe_allow_html=True
)