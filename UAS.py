import streamlit as st
import pandas as pd

# ---------------------------------------------------------------
# Konfigurasi halaman
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Kalkulator Kebutuhan Kalori Harian",
    page_icon="🔥",
    layout="centered",
)

# ---------------------------------------------------------------
# Fungsi perhitungan
# ---------------------------------------------------------------
def bmr_mifflin(jk, berat, tinggi, usia):
    """Mifflin-St Jeor (1990)."""
    dasar = 10 * berat + 6.25 * tinggi - 5 * usia
    return dasar + 5 if jk == "Laki-laki" else dasar - 161


def bmr_harris_benedict(jk, berat, tinggi, usia):
    """Harris-Benedict (revisi Roza & Shizgal, 1984)."""
    if jk == "Laki-laki":
        return 88.362 + 13.397 * berat + 4.799 * tinggi - 5.677 * usia
    return 447.593 + 9.247 * berat + 3.098 * tinggi - 4.330 * usia


def hitung_bmi(berat, tinggi):
    return berat / ((tinggi / 100) ** 2)


def kategori_bmi(bmi):
    if bmi < 18.5:
        return "Berat badan kurang"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Berat badan berlebih"
    return "Obesitas"


AKTIVITAS = {
    "Sangat jarang bergerak (tanpa olahraga)": 1.2,
    "Aktivitas ringan (olahraga 1-3 hari/minggu)": 1.375,
    "Aktivitas sedang (olahraga 3-5 hari/minggu)": 1.55,
    "Aktivitas berat (olahraga 6-7 hari/minggu)": 1.725,
    "Sangat berat (atlet / pekerja fisik berat)": 1.9,
}

TUJUAN = {
    "Menjaga berat badan": 0,
    "Menurunkan berat badan (±0,5 kg/minggu)": -500,
    "Menaikkan berat badan (±0,5 kg/minggu)": 500,
}

# ---------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------
st.title("🔥 Kalkulator Kebutuhan Kalori Harian")
st.caption(
    "Hitung kebutuhan kalori harian berdasarkan usia, jenis kelamin, "
    "tinggi badan, dan berat badan."
)

with st.sidebar:
    st.header("ℹ️ Tentang Aplikasi")
    st.write(
        "Aplikasi ini menghitung **BMR** (Basal Metabolic Rate) dan "
        "**TDEE** (Total Daily Energy Expenditure)."
    )
    st.markdown("**Rumus Mifflin-St Jeor**")
    st.latex(r"BMR_{pria} = 10W + 6{,}25H - 5A + 5")
    st.latex(r"BMR_{wanita} = 10W + 6{,}25H - 5A - 161")
    st.markdown("**Rumus TDEE**")
    st.latex(r"TDEE = BMR \times \text{Faktor Aktivitas}")
    st.caption("W = berat (kg), H = tinggi (cm), A = usia (tahun)")

st.subheader("📝 Data Diri")
col1, col2 = st.columns(2)
with col1:
    usia = st.number_input("Usia (tahun)", min_value=10, max_value=100, value=20, step=1)
    tinggi = st.number_input("Tinggi badan (cm)", min_value=100.0, max_value=250.0, value=165.0, step=0.5)
with col2:
    jk = st.radio("Jenis kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
    berat = st.number_input("Berat badan (kg)", min_value=20.0, max_value=300.0, value=60.0, step=0.5)

st.subheader("⚙️ Pengaturan Tambahan")
metode = st.selectbox("Rumus BMR", ["Mifflin-St Jeor (direkomendasikan)", "Harris-Benedict"])
aktivitas = st.selectbox("Tingkat aktivitas", list(AKTIVITAS.keys()), index=1)
tujuan = st.selectbox("Tujuan", list(TUJUAN.keys()))

if st.button("Hitung Kebutuhan Kalori", type="primary", use_container_width=True):
    # BMR
    if metode.startswith("Mifflin"):
        bmr = bmr_mifflin(jk, berat, tinggi, usia)
    else:
        bmr = bmr_harris_benedict(jk, berat, tinggi, usia)

    faktor = AKTIVITAS[aktivitas]
    tdee = bmr * faktor
    target = tdee + TUJUAN[tujuan]

    # Batas aman minimum
    batas_min = 1500 if jk == "Laki-laki" else 1200
    if target < batas_min:
        st.warning(
            f"Target {target:,.0f} kkal berada di bawah batas minimum umum "
            f"({batas_min:,} kkal). Konsultasikan dengan ahli gizi."
        )
        target = max(target, batas_min)

    bmi = hitung_bmi(berat, tinggi)

    st.divider()
    st.subheader("📊 Hasil Perhitungan")
    m1, m2, m3 = st.columns(3)
    m1.metric("BMR", f"{bmr:,.0f} kkal")
    m2.metric("TDEE", f"{tdee:,.0f} kkal")
    m3.metric("Target Harian", f"{target:,.0f} kkal")

    st.info(f"**BMI: {bmi:.1f}** — {kategori_bmi(bmi)}")

    # Makronutrien (karbohidrat 55%, protein 15%, lemak 30%)
    st.subheader("🍽️ Perkiraan Kebutuhan Makronutrien")
    makro = pd.DataFrame(
        {
            "Zat Gizi": ["Karbohidrat", "Protein", "Lemak"],
            "Porsi Energi": ["55%", "15%", "30%"],
            "Kalori (kkal)": [target * 0.55, target * 0.15, target * 0.30],
            "Gram": [target * 0.55 / 4, target * 0.15 / 4, target * 0.30 / 9],
        }
    )
    st.dataframe(
        makro.style.format({"Kalori (kkal)": "{:,.0f}", "Gram": "{:,.0f}"}),
        use_container_width=True,
        hide_index=True,
    )
    st.bar_chart(makro.set_index("Zat Gizi")["Kalori (kkal)"])

    with st.expander("🔍 Lihat langkah perhitungan"):
        st.write(f"1. BMR ({metode.split(' (')[0]}) = **{bmr:,.2f}** kkal/hari")
        st.write(f"2. Faktor aktivitas = **{faktor}**")
        st.write(f"3. TDEE = {bmr:,.2f} × {faktor} = **{tdee:,.2f}** kkal/hari")
        st.write(f"4. Penyesuaian tujuan = **{TUJUAN[tujuan]:+d}** kkal")
        st.write(f"5. Target kalori harian = **{target:,.0f}** kkal/hari")

st.caption("⚠️ Hasil ini hanya estimasi dan bukan pengganti saran medis atau ahli gizi.")
