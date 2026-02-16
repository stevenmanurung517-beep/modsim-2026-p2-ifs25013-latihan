import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Dashboard Kuesioner",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Dashboard Visualisasi Data Kuesioner")
st.markdown("Analisis distribusi dan evaluasi hasil kuesioner")

# ===============================
# LOAD DATA (TANPA UPLOAD)
# ===============================
@st.cache_data
def load_data():
    return pd.read_excel("data_kuesioner.xlsx")

df = load_data()

# ===============================
# PREPROCESSING
# ===============================
pertanyaan = df.columns[1:]

df_long = df.melt(
    id_vars=["Partisipan"],
    value_vars=pertanyaan,
    var_name="Pertanyaan",
    value_name="Jawaban"
)

# Mapping Skor Likert
skor_map = {
    "STS": 1,
    "TS": 2,
    "N": 3,
    "CS": 3,
    "S": 4,
    "SS": 5
}

df_long["Skor"] = df_long["Jawaban"].map(skor_map)

# ===============================
# KPI SECTION
# ===============================
col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Responden", df["Partisipan"].nunique())
col2.metric("Jumlah Pertanyaan", len(pertanyaan))
col3.metric("Rata-rata Skor Keseluruhan", round(df_long["Skor"].mean(), 2))

st.divider()

# ====================================================
# 1️⃣ BAR CHART DISTRIBUSI KESELURUHAN
# ====================================================
st.subheader("1️⃣ Distribusi Jawaban Keseluruhan")

distribusi_total = df_long["Jawaban"].value_counts().reset_index()
distribusi_total.columns = ["Jawaban", "Jumlah"]

fig1 = px.bar(
    distribusi_total,
    x="Jawaban",
    y="Jumlah",
    text="Jumlah",
    color="Jawaban",
    title="Distribusi Jawaban Seluruh Data"
)

st.plotly_chart(fig1, use_container_width=True)

# ====================================================
# 2️⃣ PIE CHART PROPORSI KESELURUHAN
# ====================================================
st.subheader("2️⃣ Proporsi Jawaban Keseluruhan")

fig2 = px.pie(
    distribusi_total,
    names="Jawaban",
    values="Jumlah",
    title="Proporsi Jawaban"
)

st.plotly_chart(fig2, use_container_width=True)

# ====================================================
# 3️⃣ STACKED BAR PER PERTANYAAN
# ====================================================
st.subheader("3️⃣ Distribusi Jawaban per Pertanyaan (Stacked Bar)")

distribusi_per_q = (
    df_long.groupby(["Pertanyaan", "Jawaban"])
    .size()
    .reset_index(name="Jumlah")
)

fig3 = px.bar(
    distribusi_per_q,
    x="Pertanyaan",
    y="Jumlah",
    color="Jawaban",
    barmode="stack",
    title="Distribusi Jawaban per Pertanyaan"
)

st.plotly_chart(fig3, use_container_width=True)

# ====================================================
# 4️⃣ RATA-RATA SKOR PER PERTANYAAN
# ====================================================
st.subheader("4️⃣ Rata-Rata Skor per Pertanyaan")

rata_rata = (
    df_long.groupby("Pertanyaan")["Skor"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    rata_rata,
    x="Pertanyaan",
    y="Skor",
    text_auto=True,
    title="Rata-Rata Skor per Pertanyaan"
)

st.plotly_chart(fig4, use_container_width=True)

# ====================================================
# 5️⃣ DISTRIBUSI POSITIF / NETRAL / NEGATIF
# ====================================================
st.subheader("5️⃣ Distribusi Kategori Positif, Netral, Negatif")

def kategori(j):
    if j in ["SS", "S"]:
        return "Positif"
    elif j in ["N", "CS"]:
        return "Netral"
    else:
        return "Negatif"

df_long["Kategori"] = df_long["Jawaban"].apply(kategori)

distribusi_kategori = df_long["Kategori"].value_counts().reset_index()
distribusi_kategori.columns = ["Kategori", "Jumlah"]

fig5 = px.bar(
    distribusi_kategori,
    x="Kategori",
    y="Jumlah",
    text="Jumlah",
    color="Kategori",
    title="Distribusi Berdasarkan Kategori"
)

st.plotly_chart(fig5, use_container_width=True)

# ====================================================
# 🎁 BONUS – HEATMAP
# ====================================================
st.subheader("🎁 Bonus: Heatmap Rata-Rata Skor")

heatmap_data = rata_rata.pivot_table(
    values="Skor",
    index=lambda x: "Rata-rata",
    columns="Pertanyaan"
)

fig6 = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=["Rata-rata"],
    colorscale="Viridis"
))

fig6.update_layout(title="Heatmap Rata-Rata Skor per Pertanyaan")

st.plotly_chart(fig6, use_container_width=True)
