# -*- coding: utf-8 -*-
"""
=============================================================================
MODUL 17 — WWW.TRILAKSANAMINING.MY.ID
SISTEM INTELIJEN EKONOMETRIKA MAKROEKONOMI, PERTAMBANGAN, HILIRISASI & PROYEKSI PDB (2010–2030)
(Berbasis Simultaneous Equation Model 4-Blok, ARDL/ECM, VAR/VECM, Sensitivity & Stress Test)
Peneliti Utama: Dr. Ir. Ahmad Raymond Trilaksana, S.T., M.Ak., IPM, ASEAN Eng.
=============================================================================
"""

import importlib
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

import ekonometrika_engine
import generate_sample_data
import live_market_data
import panduan_kamus
import report_paper_generator

importlib.reload(ekonometrika_engine)
importlib.reload(generate_sample_data)
importlib.reload(live_market_data)
importlib.reload(panduan_kamus)
importlib.reload(report_paper_generator)

from ekonometrika_engine import (
    build_master_parameters_table,
    compute_asta_cita_8pct_roadmap,
    compute_correlation_matrix,
    compute_descriptive_stats,
    compute_energy_dmo_rkab_frontier_simulation,
    compute_national_gdp_sector_breakdown,
    compute_tornado_sensitivity,
    export_results_to_docx,
    export_results_to_excel,
    generate_academic_interpretation,
    run_ardl_ecm,
    run_ols_regression,
    run_sensitivity_and_stress_analysis,
    run_simultaneous_mining_gdp_simulation,
    run_stationarity_tests,
    run_var_analysis,
)
from core.auth_portal import check_authentication, render_auth_sidebar
from generate_sample_data import (
    build_annual_rkab_realization_history_df,
    generate_macro_dataset,
)
from live_market_data import fetch_live_macro_commodity_quotes
from panduan_kamus import render_panduan_lengkap
from report_paper_generator import (
    AUTHOR_FULL,
    MODULE_TITLE,
    convert_html_to_pdf_via_edge,
    generate_paper_bab1_to_5_html,
    generate_presentation_slides_html,
)

st.set_page_config(
    page_title=f"Modul 17: Intelijen Ekonometrika PDB & Hilirisasi — {AUTHOR_FULL}",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling termasuk Native App Window Styling (Tanpa Header/Toolbar Bawaan) & Menu Bar Tombol Pil Multi-Baris
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    .block-container {padding-top: 1.2rem !important;}
    .main-header {
        background: linear-gradient(135deg, #0a1128 0%, #0f172a 50%, #1e3a8a 100%);
        padding: 1.35rem 1.8rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 0.9rem;
        border: 1px solid rgba(245, 158, 11, 0.45);
        border-bottom: 4px solid #f59e0b;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .main-header .mod-badge {
        display: inline-block;
        background: rgba(245, 158, 11, 0.2);
        border: 1px solid #f59e0b;
        color: #fde68a;
        font-size: 0.76rem;
        font-weight: 800;
        padding: 0.2rem 0.75rem;
        border-radius: 999px;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.52rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.25;
    }
    .main-header p {
        margin: 0.35rem 0 0 0;
        color: #93c5fd;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .exec-card {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        height: 100%;
    }
    .exec-card h4 {
        margin: 0 0 0.4rem 0;
        color: #38bdf8;
        font-size: 0.96rem;
    }
    .exec-card .big-val {
        font-size: 1.5rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.35rem;
    }
    .exec-card p {
        margin: 0;
        color: #cbd5e1;
        font-size: 0.85rem;
        line-height: 1.45;
    }
    .live-badge {
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid rgba(16, 185, 129, 0.55);
        color: #34d399;
        padding: 0.3rem 0.85rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
    }

    /* MENU BAR TOMBOL PIL MULTI-BARIS KONTRAS TINGGI (TANPA GESER KANAN-KIRI) */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        background: rgba(15, 23, 42, 0.92) !important;
        padding: 10px 12px !important;
        border-radius: 14px !important;
        border: 1.5px solid rgba(56, 189, 248, 0.35) !important;
        margin-bottom: 14px !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: auto !important;
        padding: 9px 15px !important;
        background: rgba(30, 41, 59, 0.95) !important;
        border: 1px solid rgba(148, 163, 184, 0.4) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        transition: all 0.18s ease-in-out !important;
        white-space: nowrap !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        background: rgba(30, 58, 138, 0.75) !important;
        transform: translateY(-1px);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #1e3a8a 100%) !important;
        border: 1.5px solid #f59e0b !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.45) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- UNIFIED CLOUD AUTHENTICATION & TELEGRAM GATE (SAMA SEPERTI MODUL 06) ---
check_authentication("Modul 17: Intelijen Ekonometrika Makro-Tambang, Hilirisasi & Proyeksi PDB")
render_auth_sidebar()

# =============================================================================
# INISIALISASI LIVE MARKET FEED & DATASET
# =============================================================================
if "live_feed" not in st.session_state:
    st.session_state["live_feed"] = fetch_live_macro_commodity_quotes()

live_feed = st.session_state["live_feed"]
quotes = live_feed["quotes"]

st.markdown(
    f"""
    <div class="main-header">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
            <div>
                <span class="mod-badge">🏛️ MODUL 17 • WWW.TRILAKSANAMINING.MY.ID • THE TRILAKSANA MACRO-MINING & DOWNSTREAMING FRAMEWORK</span>
                <h1>⛏️ Sistem Intelijen Ekonometrika Makroekonomi, Komoditas Tambang, Hilirisasi Smelter & Proyeksi PDB (2010–2030)</h1>
                <p>Arsitektur Persamaan Simultan 4-Blok (Struktur PDB Nasional KBLI A–U • Hulu Kat. B • Hilirisasi Smelter Kat. C • Kedaulatan Energi B50/Etanol/LNG • Fiskal PNBP & Stress Test) — <b>{AUTHOR_FULL}</b></p>
            </div>
            <span class="live-badge">📡 Data Pasar Online: {'LIVE REAL-TIME' if live_feed['is_live'] else 'BENCHMARK 2026'} ({live_feed['timestamp']})</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# BAR HARGA PASAR LIVE HARI INI + PEMILIH TAHUN TARGET PROYEKSI (2025 s/d 2030)
base_dir = os.path.dirname(os.path.abspath(__file__))
default_csv = os.path.join(base_dir, "data", "data_makro_indonesia_pdb.csv")
active_period_str = live_feed.get("active_period_label", "2026Q3")

col_btn_live, col_yr_pick, col_q1, col_q2, col_q3, col_q4, col_q5 = st.columns([1.15, 1.35, 0.95, 0.95, 0.95, 0.95, 0.95])
with col_btn_live:
    if st.button("🔄 Update Data Live", use_container_width=True, type="primary"):
        new_feed = fetch_live_macro_commodity_quotes()
        st.session_state["live_feed"] = new_feed
        # Auto-Rolling Historical Dataset: perpanjang otomatis hingga tahun & kuartal berjalan
        os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
        df_rolled = generate_macro_dataset(
            end_year=new_feed.get("active_year", 2026),
            end_quarter=new_feed.get("active_quarter", 3),
        )
        df_rolled.to_csv(default_csv, index=False)
        st.rerun()
    st.caption(f"Live Harga, RKAB & Auto-Roll ({active_period_str}).")

with col_yr_pick:
    year_options = [2025, 2026, 2027, 2028, 2029, 2030]
    year_labels = {
        2025: "2025 (Trial Backtest vs Aktual)",
        2026: "2026 (Proyeksi Tahun Berjalan)",
        2027: "2027 (Proyeksi Jangka Menengah)",
        2028: "2028 (Proyeksi Ekspansi HPAL)",
        2029: "2029 (Target Akselerasi RPJMN 8,00%)",
        2030: "2030 (Target Visi Hilirisasi 2030)",
    }
    if "target_year_select" not in st.session_state:
        st.session_state["target_year_select"] = 2026
    selected_target_year = st.selectbox(
        "📅 Pilih Tahun Target Analisis & Proyeksi:",
        options=year_options,
        key="target_year_select",
        format_func=lambda y: year_labels[y],
        help="Pilih tahun 2025 untuk menguji akurasi model terhadap data aktual BPS, tahun 2029 untuk Target Akselerasi Pertumbuhan 8,00% (RPJMN), atau tahun 2026 s/d 2030.",
    )

col_q1.metric(
    "💵 Kurs USD/IDR",
    f"Rp {quotes['Kurs_USD_IDR']['value']:,.0f}",
    f"{quotes['Kurs_USD_IDR']['change_pct']:+.2f}%",
)
col_q2.metric(
    "🛢️ Minyak Brent/ICP",
    f"${quotes['Harga_Minyak_ICP_USD']['value']:,.1f}/bbl",
    f"{quotes['Harga_Minyak_ICP_USD']['change_pct']:+.2f}%",
)
col_q3.metric(
    "🪨 Batubara (HBA)",
    f"${quotes['Harga_Batubara_HBA_USD']['value']:,.1f}/ton",
    f"{quotes['Harga_Batubara_HBA_USD']['change_pct']:+.2f}%",
)
col_q4.metric(
    "🔋 Nikel LME",
    f"${quotes['Harga_Nikel_LME_USD']['value']:,.0f}/ton",
    f"{quotes['Harga_Nikel_LME_USD']['change_pct']:+.2f}%",
)
col_q5.metric(
    "🥇 Emas Dunia",
    f"${quotes['Harga_Emas_USD_Oz']['value']:,.1f}/oz",
    f"{quotes['Harga_Emas_USD_Oz']['change_pct']:+.2f}%",
)

# Baris ringkas indikator live tambahan (Tembaga, Timah, Bauksit/Alumina, Gas/LNG Asia & RKAB Auto-Rolling)
if "Harga_Tembaga_LME_USD" in quotes:
    rkab_live_info = live_feed.get("rkab_lifting_live", {})
    coal_rkab_str = (
        f"RKAB Batubara: {rkab_live_info['Batubara']['rkab_thn']:,.0f} Jt Ton (Realisasi {rkab_live_info['Batubara']['rasio_pct']:.1f}%)"
        if "Batubara" in rkab_live_info
        else "RKAB & Lifting Migas Live Aktif"
    )
    st.markdown(
        f"<div style='background:rgba(15,23,42,0.85); border:1px solid rgba(56,189,248,0.28); border-radius:8px; padding:5px 12px; margin-bottom:10px; font-size:0.8rem; color:#cbd5e1;'>"
        f"📡 <b>Indikator Komoditas, Energi & RKAB Live (Auto-Rolling 2010Q1–{active_period_str}):</b> &nbsp; "
        f"🟠 <b>Tembaga:</b> ${quotes['Harga_Tembaga_LME_USD']['value']:,.0f}/t ({quotes['Harga_Tembaga_LME_USD']['change_pct']:+.2f}%) &nbsp;|&nbsp; "
        f"⚪ <b>Timah:</b> ${quotes['Harga_Timah_LME_USD']['value']:,.0f}/t ({quotes['Harga_Timah_LME_USD']['change_pct']:+.2f}%) &nbsp;|&nbsp; "
        f"🧱 <b>Bauksit:</b> ${quotes['Harga_Bauksit_USD']['value']:,.1f}/t &nbsp;|&nbsp; "
        f"🔥 <b>LNG Asia (JKM):</b> ${quotes['Harga_LNG_MMBTU_USD']['value']:,.2f}/MMBTU &nbsp;|&nbsp; "
        f"⛏️ <b>{coal_rkab_str}</b> &nbsp;|&nbsp; "
        f"🏦 <b>BI-Rate:</b> {quotes['Suku_Bunga_BI_Rate_Persen']['value']:.2f}% &nbsp;|&nbsp; "
        f"📈 <b>Inflasi:</b> {quotes['Inflasi_IHK_Persen']['value']:.2f}%"
        f"</div>",
        unsafe_allow_html=True,
    )

# =============================================================================
# SIDEBAR: IDENTITAS PENELITI, SUMBER DATA & SPESIFIKASI VARIABEL EKONOMETRIKA
# =============================================================================
st.sidebar.markdown(
    f"""
    <div style="background:rgba(30,41,59,0.9); border:1px solid #f59e0b; border-radius:10px; padding:10px 12px; margin-bottom:12px;">
        <div style="font-size:0.72rem; color:#fde68a; font-weight:800;">MODUL 17 • TRILAKSANAMINING.MY.ID</div>
        <div style="font-size:0.86rem; color:#ffffff; font-weight:800; margin-top:2px;">{AUTHOR_FULL}</div>
        <div style="font-size:0.74rem; color:#93c5fd; margin-top:2px;">Doktor Ekonomi • Magister Akuntansi • Insinyur Pertambangan</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("⚙️ 1. Sumber Data Penelitian")
data_source = st.sidebar.radio(
    "Pilih Sumber Dataset:",
    options=[
        f"Dataset Makro-Minerba, RKAB & Hilirisasi (2010Q1–{active_period_str} Auto-Rolling)",
        "Upload File Excel (.xlsx) / CSV (.csv) Sendiri",
    ],
)

if not os.path.exists(default_csv):
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
    df_init = generate_macro_dataset(
        end_year=live_feed.get("active_year", 2026),
        end_quarter=live_feed.get("active_quarter", 3),
    )
    df_init.to_csv(default_csv, index=False)

default_ref_df = pd.read_csv(default_csv)
if (
    len(default_ref_df.columns) < 30
    or str(default_ref_df["Periode"].iloc[-1]) != active_period_str
):
    default_ref_df = generate_macro_dataset(
        end_year=live_feed.get("active_year", 2026),
        end_quarter=live_feed.get("active_quarter", 3),
    )
    default_ref_df.to_csv(default_csv, index=False)

# Tombol Unduh Template CSV Standar agar memudahkan input manual
st.sidebar.download_button(
    "📥 Unduh Template CSV Standar",
    data=default_ref_df.to_csv(index=False).encode("utf-8"),
    file_name="Template_Data_Ekonometrika_PDB_Modul17.csv",
    mime="text/csv",
    use_container_width=True,
    help=f"Unduh format standar CSV ({len(default_ref_df.columns)} variabel kuartalan 2010Q1–{active_period_str} termasuk Historis RKAB & Lifting Migas) untuk diisi manual dan diunggah kembali.",
)

data_source_label = f"Dataset Komposit Resmi BPS, ESDM MODI/MOMI, SKK Migas & Bank Indonesia (2010Q1–{active_period_str})"
if data_source.startswith("Upload"):
    uploaded = st.sidebar.file_uploader("Unggah File CSV atau Excel:", type=["csv", "xlsx", "xls"])
    if uploaded is not None:
        if uploaded.name.endswith(".csv"):
            raw_df = pd.read_csv(uploaded)
        else:
            raw_df = pd.read_excel(uploaded)
        data_source_label = f"Dataset Input Manual Pengguna ({uploaded.name}, N={len(raw_df)} baris)"
        st.sidebar.success(f"✅ File '{uploaded.name}' aktif ({len(raw_df)} observasi). Seluruh grafik & PDF otomatis mengikuti data ini!")
    else:
        st.sidebar.info("Menampilkan dataset bawaan sambil menunggu file CSV/Excel diunggah.")
        raw_df = default_ref_df.copy()
else:
    raw_df = default_ref_df.copy()

# Sinkronkan baris kuartal terakhir dengan harga live pasar hari ini jika diaktifkan
use_live_in_dataset = st.sidebar.checkbox(f"Sinkronkan Kuartal Terakhir ({active_period_str}) dengan Harga Pasar Live", value=True)
if use_live_in_dataset and "Kurs_USD_IDR" in raw_df.columns:
    raw_df = raw_df.copy()
    last_idx = raw_df.index[-1]
    for col_key, q_info in quotes.items():
        if col_key in raw_df.columns:
            raw_df.loc[last_idx, col_key] = q_info["value"]

# Siapkan sim_base_df yang menggabungkan data upload manual dengan kolom standar bila ada kolom yang tidak diikutsertakan
sim_base_df = default_ref_df.copy()
if len(raw_df) > 0:
    for col in raw_df.columns:
        if col in sim_base_df.columns and len(raw_df) == len(sim_base_df):
            sim_base_df[col] = raw_df[col].values
        elif col in sim_base_df.columns:
            sim_base_df.loc[sim_base_df.index[-1], col] = raw_df[col].iloc[-1]

numeric_cols = [
    c for c in raw_df.columns if c.lower() not in ["periode", "tahun", "kuartal", "date", "waktu"]
]
time_col = next(
    (c for c in raw_df.columns if c.lower() in ["periode", "tahun", "date", "waktu"]),
    raw_df.columns[0],
)

st.sidebar.header("📐 2. Spesifikasi Variabel Ekonometrika")
default_y_idx = numeric_cols.index("PDB_Riil_Triliun_Rp") if "PDB_Riil_Triliun_Rp" in numeric_cols else 0
y_var = st.sidebar.selectbox(
    "Variabel Dependen (Y - Target Sasaran):",
    options=numeric_cols,
    index=default_y_idx,
)

preset_group = st.sidebar.selectbox(
    "Pilih Paket Variabel Independen (X):",
    options=[
        "1. Model Lengkap: Tambang + Hilirisasi + Makro (Rekomendasi Utama)",
        "2. Fokus Volume Produksi Komoditas (Batubara, Nikel, Emas & Smelter)",
        "3. Fokus Harga Komoditas Dunia (HBA, Nikel LME, Emas, Minyak ICP)",
        "4. Fokus Makroekonomi & Moneter (Investasi, Ekspor, Kurs, BI-Rate, Inflasi)",
        "5. Fokus Historis Kuota RKAB vs Realisasi 6 Mineral & Lifting Migas",
    ],
)

available_x = [c for c in numeric_cols if c != y_var]
if preset_group.startswith("1."):
    preferred_x = [
        "Produksi_Batubara_Juta_Ton",
        "Produksi_Bijih_Nikel_Juta_WMT",
        "Produksi_Emas_Ton",
        "Harga_Batubara_HBA_USD",
        "Harga_Nikel_LME_USD",
        "Harga_Emas_USD_Oz",
        "Investasi_Smelter_PMTB_Triliun_Rp",
        "Ekspor_Hilirisasi_Mineral_Miliar_USD",
        "Kurs_USD_IDR",
        "Suku_Bunga_BI_Rate_Persen",
    ]
elif preset_group.startswith("2."):
    preferred_x = [
        "Produksi_Batubara_Juta_Ton",
        "Produksi_Bijih_Nikel_Juta_WMT",
        "Produksi_Emas_Ton",
        "Produksi_Bijih_Tembaga_Juta_Ton",
        "Lifting_Minyak_Ribu_Bph",
        "Lifting_Gas_Bumi_MMSCFD",
        "Investasi_Smelter_PMTB_Triliun_Rp",
        "PDB_Hilir_Logam_Dasar_Triliun_Rp",
        "PNBP_Royalti_Minerba_Triliun_Rp",
    ]
elif preset_group.startswith("3."):
    preferred_x = [
        "Harga_Batubara_HBA_USD",
        "Harga_Nikel_LME_USD",
        "Harga_Emas_USD_Oz",
        "Harga_Minyak_ICP_USD",
        "Ekspor_Hilirisasi_Mineral_Miliar_USD",
        "Kurs_USD_IDR",
    ]
elif preset_group.startswith("4."):
    preferred_x = [
        "Investasi_PMTB_Triliun_Rp",
        "Ekspor_Miliar_USD",
        "PNBP_Royalti_Minerba_Triliun_Rp",
        "Inflasi_IHK_Persen",
        "Suku_Bunga_BI_Rate_Persen",
        "Kurs_USD_IDR",
    ]
else:
    preferred_x = [
        "Kuota_RKAB_Batubara_Juta_Ton",
        "Produksi_Batubara_Juta_Ton",
        "Kuota_RKAB_Nikel_Juta_WMT",
        "Produksi_Bijih_Nikel_Juta_WMT",
        "Kuota_RKAB_Tembaga_Juta_Ton",
        "Kuota_RKAB_Emas_Ton",
        "Target_Lifting_Minyak_Ribu_Bph",
        "Lifting_Minyak_Ribu_Bph",
        "Target_Lifting_Gas_MMSCFD",
        "Lifting_Gas_Bumi_MMSCFD",
        "Rasio_Realisasi_RKAB_Persen",
    ]

default_x = [c for c in preferred_x if c in available_x]
if not default_x:
    default_x = available_x[:6]

x_vars = st.sidebar.multiselect(
    "Variabel Independen (X - Faktor Penjelas):",
    options=available_x,
    default=default_x,
)

transform_mode = st.sidebar.selectbox(
    "Transformasi Fungsional Data:",
    options=[
        "Level Asli (Linear Model)",
        "Logaritma Natural / Ln (Double-Log Elasticity Model)",
        "Semi-Log (Ln pada Nilai Uang/Volume, Level pada % Rate)",
        "First Difference / Δ (Perubahan Kuartalan)",
    ],
)

var_lag = st.sidebar.slider("Ordo Lag Maksimum (ARDL / VAR / Granger):", min_value=1, max_value=4, value=2)
irf_horizon = st.sidebar.slider("Horizon Proyeksi IRF & FEVD (Kuartal):", min_value=4, max_value=20, value=10)

if len(x_vars) < 1:
    st.warning("⚠️ Silakan pilih minimal 1 Variabel Independen (X) pada panel sebelah kiri.")
    st.stop()

# =============================================================================
# PERSIAPAN DATA & PERHITUNGAN ENGINE EKONOMETRIKA + SIMULASI 4-BLOK (2025-2030)
# =============================================================================
work_df = raw_df.copy()
selected_cols = [y_var] + list(x_vars)

if transform_mode.startswith("Logaritma"):
    new_y = y_var
    new_x = []
    for col in selected_cols:
        s = pd.to_numeric(work_df[col], errors="coerce")
        if (s <= 0).any():
            if col == y_var:
                new_y = y_var
            else:
                new_x.append(col)
        else:
            ln_name = f"Ln_{col}"
            work_df[ln_name] = np.log(s)
            if col == y_var:
                new_y = ln_name
            else:
                new_x.append(ln_name)
    model_y, model_x = new_y, new_x

elif transform_mode.startswith("Semi-Log"):
    new_y = y_var
    new_x = []
    for col in selected_cols:
        s = pd.to_numeric(work_df[col], errors="coerce")
        is_rate_or_pct = "persen" in col.lower() or "rate" in col.lower() or "inflasi" in col.lower() or (s <= 0).any()
        if not is_rate_or_pct:
            ln_name = f"Ln_{col}"
            work_df[ln_name] = np.log(s)
            if col == y_var:
                new_y = ln_name
            else:
                new_x.append(ln_name)
        else:
            if col == y_var:
                new_y = col
            else:
                new_x.append(col)
    model_y, model_x = new_y, new_x

elif transform_mode.startswith("First Difference"):
    new_y = f"D_{y_var}"
    new_x = []
    for col in selected_cols:
        d_name = f"D_{col}"
        work_df[d_name] = pd.to_numeric(work_df[col], errors="coerce").diff()
        if col == y_var:
            new_y = d_name
        else:
            new_x.append(d_name)
    work_df = work_df.dropna().reset_index(drop=True)
    model_y, model_x = new_y, new_x
else:
    model_y, model_x = y_var, list(x_vars)

model_all_cols = [model_y] + list(model_x)

desc_df = compute_descriptive_stats(work_df, model_all_cols)
corr_df, corr_pvals = compute_correlation_matrix(work_df, model_all_cols)
adf_df = run_stationarity_tests(work_df, model_all_cols)
ols_res = run_ols_regression(work_df, model_y, model_x)
ardl_res = run_ardl_ecm(work_df, model_y, model_x, p_lag=var_lag, q_lag=var_lag)
var_res = run_var_analysis(work_df, model_all_cols, lag_p=var_lag, horizon=irf_horizon)
tornado_df = compute_tornado_sensitivity(work_df, model_y, model_x, ols_res)

# Jalankan Simulasi Persamaan Simultan 4-Blok Multi-Tahun (2025 s/d 2030)
if "custom_sem_scenario" not in st.session_state:
    st.session_state["custom_sem_scenario"] = None

sem_res = run_simultaneous_mining_gdp_simulation(
    sim_base_df, st.session_state["custom_sem_scenario"], target_year=selected_target_year
)
sens_stress_res = run_sensitivity_and_stress_analysis(
    sim_base_df, st.session_state["custom_sem_scenario"], target_year=selected_target_year
)

base_yr = sem_res["selected_year_base"]
scen_yr = sem_res["selected_year_scen"]
opt_yr = sem_res["selected_year_opt"]
pes_yr = sem_res["selected_year_pes"]
asta_yr = sem_res["selected_year_asta"]
bt_2025 = sem_res["backtest_2025"]
asta_roadmap = compute_asta_cita_8pct_roadmap(sem_res)

nat_sector_overview = compute_national_gdp_sector_breakdown(sem_res)
master_param_overview_df = build_master_parameters_table(
    sem_res=sem_res,
    model_y=model_y,
    model_x=model_x,
    transform_mode=transform_mode,
    var_lag=var_lag,
    irf_horizon=irf_horizon,
    n_obs=len(work_df),
)


def _activate_asta_cita_8pct():
    st.session_state["custom_sem_scenario"] = dict(sem_res["asta_cita_params"])
    st.session_state["target_year_select"] = 2029


def _reset_baseline_live():
    st.session_state["custom_sem_scenario"] = dict(sem_res["base_params"])
    st.session_state["target_year_select"] = 2026


# =============================================================================
# SUSUNAN 9 MENU TAB KONTRAS TINGGI (TAMPIL UTUH TANPA PERLU GESER PANAH KECIL)
# =============================================================================
tabs = st.tabs([
    f"🎯 1. Kesimpulan & Proyeksi ({selected_target_year})",
    "⛏️ 2. Simulator Produksi (X) × Harga (Y)",
    "⚡ 3. Subsidi BBM, B50/Etanol/LNG, DMO, RKAB & 14 Ide PDB 8%",
    "🌪️ 4. Sensitivity & Stress Test Krisis",
    "🏆 5. Kesimpulan Bab V & Unduh Paper/Slide PDF",
    "📊 6. Data, Deskriptif & Korelasi",
    "🔬 7. Uji Stasioneritas (ADF)",
    "📈 8. Regresi OLS, ARDL/ECM & VECM",
    "📖 9. Panduan Lengkap & Kamus",
])

# -----------------------------------------------------------------------------
# TAB 1: LEMBAR KESIMPULAN EKSEKUTIF, GAMBARAN UMUM 100% PDB NASIONAL & PROYEKSI
# -----------------------------------------------------------------------------
with tabs[0]:
    # 6 KARTU PANDUAN CEPAT KAPABILITAS SIMULASI DI BAGIAN PALING ATAS HALAMAN 1
    st.markdown(
        """
        <div style="background:rgba(15,23,42,0.92); border:1.5px solid rgba(245,158,11,0.55); border-radius:14px; padding:14px 18px; margin-bottom:14px;">
            <div style="font-size:0.96rem; font-weight:800; color:#fde68a; margin-bottom:8px;">
                🧭 PANDUAN CEPAT EKSEKUTIF: 6 SIMULASI KEBIJAKAN &amp; EKONOMETRIKA YANG DAPAT ANDA UJI DI LABORATORIUM MODUL 17 INI
            </div>
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; font-size:0.81rem; color:#e2e8f0; line-height:1.42;">
                <div style="background:rgba(30,41,59,0.9); border-left:3.5px solid #38bdf8; padding:8px 11px; border-radius:8px;">
                    <b style="color:#38bdf8;">1️⃣ Simulasi Kuota RKAB 6 Mineral &amp; Lifting Migas (X):</b><br>
                    Uji perubahan volume produksi Batubara, Bijih Nikel, Tembaga, Emas, Bauksit, Timah, serta Lifting Minyak &amp; LNG (Blok Masela/IDD/Rokan) terhadap PDB Hulu (Kat. B).
                </div>
                <div style="background:rgba(30,41,59,0.9); border-left:3.5px solid #10b981; padding:8px 11px; border-radius:8px;">
                    <b style="color:#10b981;">2️⃣ Simulasi Harga Komoditas &amp; Energi Live Online (Y):</b><br>
                    Tarik otomatis harga <i>real-time</i> (Minyak ICP, HBA Batubara, Nikel LME, Emas, Tembaga, Timah, LNG, Kurs USD/IDR) atau geser manual untuk menguji dampak ke PDB.
                </div>
                <div style="background:rgba(30,41,59,0.9); border-left:3.5px solid #f59e0b; padding:8px 11px; border-radius:8px;">
                    <b style="color:#f59e0b;">3️⃣ Simulasi Hilirisasi Smelter, DMO PLN &amp; Royalti:</b><br>
                    Hitung lonjakan nilai tambah Smelter RKEF/HPAL (Kat. C KBLI 24), kuota DMO Batubara PLN ($70/t) vs Ekspor, dan tarif Royalti Progresif (PP 26/2022).
                </div>
                <div style="background:rgba(30,41,59,0.9); border-left:3.5px solid #a855f7; padding:8px 11px; border-radius:8px;">
                    <b style="color:#c084fc;">4️⃣ Simulasi Subsidi BBM, B50, Bioetanol E10–E90 &amp; LNG:</b><br>
                    Di <b>Tab 3</b>, uji apakah lonjakan subsidi Pertalite/Solar saat harga minyak naik dapat ditutupi oleh Biodiesel B50, Bioetanol E10–E90, Konversi LPG ke LNG, &amp; PNBP Tambang.
                </div>
                <div style="background:rgba(30,41,59,0.9); border-left:3.5px solid #ec4899; padding:8px 11px; border-radius:8px;">
                    <b style="color:#f472b6;">5️⃣ Simulasi Target PDB 8,00% (2029) &amp; 14 Terobosan Baru:</b><br>
                    Aktifkan 1-Klik Peta Komando 6 Sektor Prioritas serta uji <b>14 Ide Kebijakan Baru</b> (8 Strategis + 6 Inovasi <i>Fresh from the Oven</i>) untuk mengejar PDB 8,00%.
                </div>
                <div style="background:rgba(30,41,59,0.9); border-left:3.5px solid #14b8a6; padding:8px 11px; border-radius:8px;">
                    <b style="color:#2dd4bf;">6️⃣ Upload CSV Sendiri &amp; Cetak Paper BAB I–V / Slide PDF:</b><br>
                    Unggah dataset kustom Anda di panel kiri dan unduh Naskah Ilmiah BAB I–V (.PDF/.DOCX) serta Slide Presentasi Eksekutif (.PDF) secara otomatis di <b>Tab 5</b>.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(
        f"🎯 Ringkasan Eksekutif: Proyeksi PDB Indonesia Tahun {selected_target_year} & Validasi Akurasi Model (2025–2030)"
    )

    # BAR TOMBOL CEPAT SIMULASI TARGET AKSELERASI PERTUMBUHAN 8,00% (RPJMN 2029) VS KONDISI AKTUAL LIVE
    ac_col1, ac_col2, ac_col3 = st.columns([1.45, 1.15, 1.8])
    with ac_col1:
        st.button(
            "🚀 1-KLIK: Aktifkan Simulasi Target Akselerasi Ekonomi 8,00% (RPJMN 2029) & Peta Sektor Prioritas",
            type="primary",
            use_container_width=True,
            on_click=_activate_asta_cita_8pct,
            key="btn_asta_tab1",
        )
    with ac_col2:
        st.button(
            "🔵 Kembali ke Kondisi Aktual (Data Real Live / Baseline)",
            use_container_width=True,
            on_click=_reset_baseline_live,
            key="btn_base_tab1",
        )
    with ac_col3:
        if sem_res.get("scen_is_asta_cita"):
            st.success(
                f"✅ **Mode Target Akselerasi 8,00% (RPJMN 2029) Aktif!** Tahun **{selected_target_year}** diproyeksikan tumbuh **`{scen_yr['growth_pct']:.2f}%`** (`Rp {scen_yr['pdb_total_triliun']:,.1f} T`). Lihat peta sektor yang digenjot di bawah."
            )
        else:
            st.info(
                f"💡 Saat ini menampilkan **Skenario Simulasi Aktif / Data Live ({selected_target_year}: `{scen_yr['growth_pct']:.2f}%`)**. Klik tombol **🚀 Target Akselerasi 8,00% (2029)** di kiri untuk melihat sektor yang harus digenjot."
            )

    pos_drivers = tornado_df[tornado_df["Bobot Pengaruh Terstandarisasi (Std. Beta)"] > 0].sort_values(
        by="Kekuatan Absolut", ascending=False
    )
    neg_drivers = tornado_df[tornado_df["Bobot Pengaruh Terstandarisasi (Std. Beta)"] < 0].sort_values(
        by="Kekuatan Absolut", ascending=False
    )
    top_pos_name = pos_drivers.iloc[0]["Variabel"] if len(pos_drivers) > 0 else model_x[0]
    top_neg_name = neg_drivers.iloc[0]["Variabel"] if len(neg_drivers) > 0 else "Kurs_USD_IDR / Harga_Minyak_ICP_USD"

    # 3 KARTU TANYA-JAWAB EKSEKUTIF
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        st.markdown(
            f"""
            <div class="exec-card">
                <h4>🟢 1. Berapa Proyeksi PDB Indonesia Tahun {selected_target_year}?</h4>
                <div class="big-val">Tumbuh {scen_yr['growth_pct']:.2f}% (Rp {scen_yr['pdb_total_triliun']:,.0f} T)</div>
                <p>
                    Berdasarkan model persamaan simultan 4-blok, PDB Riil tahun <b>{selected_target_year}</b> diproyeksikan mencapai
                    <b>Rp {scen_yr['pdb_total_triliun']:,.1f} Triliun</b> (naik dari Rp {scen_yr['pdb_prev_triliun']:,.1f} T pada tahun sebelumnya).
                    Baseline Live: <b>{base_yr['growth_pct']:.2f}%</b> | Target Akselerasi {selected_target_year}: <b>{asta_yr['growth_pct']:.2f}%</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ec2:
        st.markdown(
            f"""
            <div class="exec-card">
                <h4>⛏️ 2. Sumbangan Hulu (Kat. B) vs Hilirisasi Smelter (Kat. C) {selected_target_year}</h4>
                <div class="big-val">{scen_yr['share_minerba_hilir_pct']:.2f}% dari Total PDB</div>
                <p>
                    PDB Hulu Pertambangan (Kat. B) menyumbang <b>Rp {scen_yr['pdb_hulu_triliun']:,.1f} T</b>, sedangkan
                    <b>Hilirisasi Logam Dasar Smelter (Kat. C — KBLI 24)</b> menyumbang <b>Rp {scen_yr['pdb_hilir_triliun']:,.1f} T</b>
                    (+Nilai Tambah Hilirisasi <b>Rp {scen_yr['nilai_tambah_hilirisasi_triliun']:,.1f} T</b> & PNBP <b>Rp {scen_yr['pnbp_royalti_triliun']:,.1f} T</b>).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ec3:
        st.markdown(
            f"""
            <div class="exec-card">
                <h4>✅ 3. Uji Akurasi Trial Tahun 2025 (Proyeksi vs Aktual BPS)</h4>
                <div class="big-val" style="color:#10b981;">Akurasi {bt_2025['accuracy_pct']:.2f}% (MAPE {bt_2025['mape_pct']:.2f}%)</div>
                <p>
                    Hasil <i>Backtesting</i> tahun 2025 membuktikan proyeksi model (<b>Rp {bt_2025['pred_pdb_2025']:,.1f} T / {bt_2025['pred_growth_2025']:.2f}%</b>)
                    sangat presisi terhadap realisasi aktual BPS 2025 (<b>Rp {bt_2025['actual_pdb_2025']:,.1f} T / {bt_2025['actual_growth_2025']:.2f}%</b>),
                    sehingga sahih dipakai memproyeksikan tahun <b>2026–2030</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # =========================================================================
    # GAMBARAN UMUM 100% STRUKTUR PDB NASIONAL INDONESIA (KBLI A-U & PENGELUARAN C+I+G+NX)
    # =========================================================================
    st.markdown("---")
    st.subheader(
        f"🌐 Anatomi Utuh Struktur PDB Nasional Indonesia Tahun {selected_target_year} (Seluruh Sektor KBLI A–U & Pengeluaran Makro) ➔ Posisi Spesifik Pertambangan & Hilirisasi"
    )
    st.markdown(
        f"Sebelum masuk ke analisis spesifik pertambangan dan smelter, grafik di bawah ini menampilkan **gambaran umum keseluruhan faktor pembentuk 100% PDB Nasional Indonesia** "
        f"(Total Proyeksi PDB Riil {selected_target_year}: **Rp {scen_yr['pdb_total_triliun']:,.1f} Triliun**). Terlihat bagaimana **Ekosistem Pertambangan Hulu (Kat. B: {nat_sector_overview['share_hulu']:.2f}%)**, "
        f"**Hilirisasi Industri Logam Dasar Smelter (Kat. C KBLI 24: {nat_sector_overview['share_hilir']:.2f}%)**, dan **Efek Limpahan / Spillover ({nat_sector_overview['share_spill']:.2f}%)** "
        f"menyumbang **{nat_sector_overview['total_minerba_ecosystem_pct']:.2f}%** dari kue PDB Nasional dan bersinergi dengan **{nat_sector_overview['non_minerba_pct']:.2f}%** sektor domestik lainnya:"
    )

    col_sec_chart, col_exp_chart = st.columns([1.35, 1.0])
    with col_sec_chart:
        sec_plot_df = nat_sector_overview["sector_df"].iloc[::-1].copy()
        fig_nat_sec = px.bar(
            sec_plot_df,
            x="Porsi terhadap PDB Nasional (%)",
            y="Kategori KBLI / Sektor BPS",
            color="Kelompok Analisis",
            orientation="h",
            text="Porsi terhadap PDB Nasional (%)",
            hover_data=["Nilai PDB Riil (Triliun Rp)", "Laju Pertumbuhan Sektoral (% YoY)"],
            color_discrete_map={
                "⛏️ Fokus Utama 1: Hulu Pertambangan (Kat. B)": "#38bdf8",
                "🏭 Fokus Utama 2: Hilirisasi Smelter (Kat. C - KBLI 24)": "#10b981",
                "⚡ Fokus Utama 3: Efek Pengganda (Spillover Minerba)": "#f59e0b",
                "🏢 Sektor Makro Domestik Lainnya (Non-Minerba)": "#64748b",
            },
            title=f"1. Struktur 100% PDB Menurut Seluruh Lapangan Usaha BPS (KBLI A–U, Tahun {selected_target_year})",
            template="plotly_dark",
            height=440,
        )
        fig_nat_sec.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_nat_sec.update_layout(
            xaxis_range=[0, max(sec_plot_df["Porsi terhadap PDB Nasional (%)"]) * 1.22],
            legend=dict(orientation="h", yanchor="bottom", y=-0.32, xanchor="left", x=0),
            margin=dict(l=10, r=25, t=45, b=90),
        )
        st.plotly_chart(fig_nat_sec, use_container_width=True)

    with col_exp_chart:
        exp_plot_df = nat_sector_overview["exp_df"].copy()
        fig_nat_exp = px.pie(
            exp_plot_df,
            names="Komponen Pengeluaran PDB (Y = C + I + G + NX)",
            values="Porsi PDB (%)",
            hole=0.45,
            color_discrete_sequence=["#38bdf8", "#10b981", "#f59e0b", "#a855f7", "#64748b"],
            title=f"2. Struktur PDB Menurut Pengeluaran Y = C+I+G+NX ({selected_target_year})",
            template="plotly_dark",
            height=440,
        )
        fig_nat_exp.update_traces(textposition="inside", textinfo="percent+label")
        fig_nat_exp.update_layout(
            showlegend=False,
            margin=dict(l=15, r=15, t=45, b=20),
        )
        st.plotly_chart(fig_nat_exp, use_container_width=True)

    with st.expander(f"📋 Klik untuk Melihat Tabel Lengkap 100% Sektor Lapangan Usaha (KBLI A–U), Pengeluaran Makro & Daftar Parameter Simulasi ({selected_target_year})", expanded=False):
        st.markdown(f"**A. Tabel Dekomposisi 100% PDB Nasional Menurut Lapangan Usaha BPS (Kategori A s/d U — Tahun {selected_target_year}):**")
        st.dataframe(nat_sector_overview["sector_df"], use_container_width=True, hide_index=True)
        st.markdown(f"**B. Tabel Dekomposisi PDB Nasional Menurut Pengeluaran Makroekonomi ($Y = C + I + G + NX$ — Tahun {selected_target_year}):**")
        st.dataframe(nat_sector_overview["exp_df"], use_container_width=True, hide_index=True)
        st.markdown(f"**C. Tabel Master Seluruh Parameter Input & Konfigurasi Model Ekonometrika Aktif (Tahun Target {selected_target_year}):**")
        st.dataframe(master_param_overview_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    # BARIS GRAFIK UTAMA: SPEEDOMETER PREDIKSI TAHUN TERPILIH (SKALA 9.0%) + GAMBAR 2 PETA JALAN 2018–2030 DENGAN LABEL %
    col_gauge, col_fan = st.columns([1, 1.55])
    with col_gauge:
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=scen_yr["growth_pct"],
                number={"suffix": "%", "font": {"size": 42, "color": "#38bdf8"}},
                delta={
                    "reference": base_yr["growth_pct"],
                    "increasing": {"color": "#10b981"},
                    "decreasing": {"color": "#f43f5e"},
                    "valueformat": ".2f",
                },
                title={
                    "text": (
                        f"<b>Speedometer Proyeksi Pertumbuhan PDB {selected_target_year} (%)</b>"
                        f"<br><span style='font-size:0.78em;color:#94a3b8'>Baseline Live: {base_yr['growth_pct']:.2f}% | Target Akselerasi 2029: 8.00%</span>"
                    ),
                    "font": {"size": 14},
                },
                gauge={
                    "axis": {"range": [3.5, 9.0], "tickwidth": 1},
                    "bar": {"color": "#f59e0b" if sem_res.get("scen_is_asta_cita") else "#38bdf8"},
                    "steps": [
                        {"range": [3.5, 4.7], "color": "rgba(244, 63, 94, 0.28)"},
                        {"range": [4.7, 5.8], "color": "rgba(56, 189, 248, 0.25)"},
                        {"range": [5.8, 7.5], "color": "rgba(16, 185, 129, 0.28)"},
                        {"range": [7.5, 9.0], "color": "rgba(245, 158, 11, 0.32)"},
                    ],
                    "threshold": {
                        "line": {"color": "#fbbf24", "width": 4},
                        "thickness": 0.85,
                        "value": 8.00,
                    },
                },
            )
        )
        fig_gauge.update_layout(template="plotly_dark", height=320, margin=dict(l=25, r=25, t=60, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

        scen_summary_df = pd.DataFrame([
            {
                f"Skenario Tahun {selected_target_year}": "🚀 Target Akselerasi 8% (RPJMN 2029)",
                "Pertumbuhan PDB (%)": f"{asta_yr['growth_pct']:.2f}%",
                "PDB Riil (Triliun Rp)": f"Rp {asta_yr['pdb_total_triliun']:,.1f} T",
                "Ekspor Hilirisasi": f"${asta_yr['ekspor_hilir_miliar_usd']:,.1f} Miliar",
            },
            {
                f"Skenario Tahun {selected_target_year}": "🟢 Optimis (Booming Hilirisasi & EV)",
                "Pertumbuhan PDB (%)": f"{opt_yr['growth_pct']:.2f}%",
                "PDB Riil (Triliun Rp)": f"Rp {opt_yr['pdb_total_triliun']:,.1f} T",
                "Ekspor Hilirisasi": f"${opt_yr['ekspor_hilir_miliar_usd']:,.1f} Miliar",
            },
            {
                f"Skenario Tahun {selected_target_year}": f"🔵 Simulasi Aktif ({selected_target_year})",
                "Pertumbuhan PDB (%)": f"{scen_yr['growth_pct']:.2f}%",
                "PDB Riil (Triliun Rp)": f"Rp {scen_yr['pdb_total_triliun']:,.1f} T",
                "Ekspor Hilirisasi": f"${scen_yr['ekspor_hilir_miliar_usd']:,.1f} Miliar",
            },
            {
                f"Skenario Tahun {selected_target_year}": f"⚪ Baseline Data Live ({selected_target_year})",
                "Pertumbuhan PDB (%)": f"{base_yr['growth_pct']:.2f}%",
                "PDB Riil (Triliun Rp)": f"Rp {base_yr['pdb_total_triliun']:,.1f} T",
                "Ekspor Hilirisasi": f"${base_yr['ekspor_hilir_miliar_usd']:,.1f} Miliar",
            },
            {
                f"Skenario Tahun {selected_target_year}": "🔴 Waspada (Lonjakan Minyak & Kurs)",
                "Pertumbuhan PDB (%)": f"{pes_yr['growth_pct']:.2f}%",
                "PDB Riil (Triliun Rp)": f"Rp {pes_yr['pdb_total_triliun']:,.1f} T",
                "Ekspor Hilirisasi": f"${pes_yr['ekspor_hilir_miliar_usd']:,.1f} Miliar",
            },
        ])
        st.dataframe(scen_summary_df, use_container_width=True, hide_index=True)

    with col_fan:
        proj_df = sem_res["projection_df"].copy()
        # Buat label teks persentase kenaikan pada setiap titik tahun proyeksi (2025-2030)
        sim_labels = [
            f"{row['Pertumbuhan Simulasi (%)']:.2f}%" if int(row["Tahun_Int"]) >= 2025 else ""
            for _, row in proj_df.iterrows()
        ]
        asta_labels = [
            f"{row['Pertumbuhan Target Asta Cita 8% (%)']:.2f}%" if int(row["Tahun_Int"]) >= 2026 else ""
            for _, row in proj_df.iterrows()
        ]
        cf_labels = [
            f"{row['Pertumbuhan Tanpa Hilirisasi (%)']:.2f}%" if int(row["Tahun_Int"]) >= 2026 else ""
            for _, row in proj_df.iterrows()
        ]

        fig_proj = go.Figure()
        fig_proj.add_trace(
            go.Scatter(
                x=proj_df["Tahun"],
                y=proj_df["PDB Target Asta Cita 8% (Triliun Rp)"],
                mode="lines+markers+text",
                text=asta_labels,
                textposition="top center",
                textfont=dict(color="#fde68a", size=10),
                line=dict(color="#f59e0b", width=3.0, dash="dashdot"),
                marker=dict(size=8, symbol="diamond"),
                name="🚀 Lintasan Target Akselerasi 8% (RPJMN 2029: 8,00%)",
            )
        )
        fig_proj.add_trace(
            go.Scatter(
                x=proj_df["Tahun"],
                y=proj_df["PDB Optimis (Triliun Rp)"],
                mode="lines",
                line=dict(color="rgba(16, 185, 129, 0.55)", dash="dot"),
                name="Batas Atas (Skenario Optimis 2026–2030)",
            )
        )
        fig_proj.add_trace(
            go.Scatter(
                x=proj_df["Tahun"],
                y=proj_df["PDB Waspada (Triliun Rp)"],
                mode="lines",
                fill="tonexty",
                fillcolor="rgba(56, 189, 248, 0.11)",
                line=dict(color="rgba(244, 63, 94, 0.55)", dash="dot"),
                name="Batas Bawah (Skenario Waspada 2026–2030)",
            )
        )
        fig_proj.add_trace(
            go.Scatter(
                x=proj_df["Tahun"],
                y=proj_df["PDB Skenario Simulasi (Triliun Rp)"],
                mode="lines+markers+text",
                text=sim_labels,
                textposition="bottom center",
                textfont=dict(color="#38bdf8", size=10.5),
                line=dict(color="#38bdf8", width=3.6),
                marker=dict(size=9),
                name="🔵 PDB Simulasi Aktif (Dengan Hilirisasi Smelter Kat. C)",
            )
        )
        fig_proj.add_trace(
            go.Scatter(
                x=proj_df["Tahun"],
                y=proj_df["PDB Tanpa Hilirisasi (Counterfactual)"],
                mode="lines+markers+text",
                text=cf_labels,
                textposition="bottom center",
                textfont=dict(color="#94a3b8", size=9.5),
                line=dict(color="#94a3b8", width=2.3, dash="dash"),
                name="⚪ Simulasi Tanpa Hilirisasi (Hanya Ekspor Bijih Mentah)",
            )
        )
        fig_proj.update_layout(
            title="📈 Gambar 2 — Peta Jalan PDB Indonesia 2018–2030: Lengkap dengan Label % Kenaikan YoY & Lintasan Target Akselerasi 8%",
            yaxis_title="PDB Riil Tahunan (Triliun Rupiah)",
            xaxis_title="Tahun Historis (2018–2025) & Proyeksi Jangka Menengah (2026–2030)",
            template="plotly_dark",
            height=485,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        st.plotly_chart(fig_proj, use_container_width=True)

    # TABEL LENGKAP PROYEKSI PERSENTASE KENAIKAN PDB & NILAI TAMBAH HILIRISASI (2018-2030) TEPAT DI BAWAH GAMBAR 2
    st.markdown(
        "#### 📊 Tabel Rincian Proyeksi Persentase Kenaikan PDB (`% YoY`) & Nilai Tambah Hilirisasi Tahun 2018–2030 (Pendamping Gambar 2)"
    )
    tbl_g2_rows = []
    for _, r_p in proj_df.iterrows():
        tbl_g2_rows.append({
            "Tahun": r_p["Tahun"],
            "PDB Baseline Live (Rp T)": f"Rp {r_p['PDB Baseline / Aktual (Triliun Rp)']:,.1f} T",
            "Kenaikan Baseline Live (% YoY)": f"{r_p['Pertumbuhan Baseline (%)']:.2f}%",
            "PDB Simulasi Aktif (Rp T)": f"Rp {r_p['PDB Skenario Simulasi (Triliun Rp)']:,.1f} T",
            "Kenaikan Simulasi Aktif (% YoY)": f"{r_p['Pertumbuhan Simulasi (%)']:.2f}%",
            "PDB Target Akselerasi 8% (Rp T)": f"Rp {r_p['PDB Target Asta Cita 8% (Triliun Rp)']:,.1f} T",
            "Target Akselerasi (% YoY)": f"{r_p['Pertumbuhan Target Asta Cita 8% (%)']:.2f}%",
            "PDB Tanpa Hilirisasi (Rp T)": f"Rp {r_p['PDB Tanpa Hilirisasi (Counterfactual)']:,.1f} T",
            "Tanpa Hilirisasi (% YoY)": f"{r_p['Pertumbuhan Tanpa Hilirisasi (%)']:.2f}%",
            "Nilai Tambah Hilirisasi (+Rp T & +%)": f"+Rp {r_p['Nilai Tambah Hilirisasi (Triliun Rp)']:,.1f} T (+{r_p['Kenaikan PDB dari Hilirisasi (%)']:.2f}%)",
        })
    st.dataframe(pd.DataFrame(tbl_g2_rows), use_container_width=True, hide_index=True)

    # =========================================================================
    # PANEL KHUSUS: PETA KOMANDO SEKTOR YANG HARUS DIGENJOT MENUJU TARGET AKSELERASI 8% (RPJMN 2029)
    # =========================================================================
    st.markdown("---")
    st.subheader(
        "🚀 Peta Komando Sektor yang Harus Digenjot agar Target Akselerasi Pertumbuhan Ekonomi 8,00% Tahun 2029 (RPJMN 2025–2029) Tercapai"
    )
    st.markdown(
        f"Berdasarkan data *real live* hari ini (*Business-as-Usual*), pertumbuhan ekonomi nasional pada tahun 2029 diproyeksikan berada di **`{asta_roadmap['base_2029']['growth_pct']:.2f}%`** "
        f"(`Rp {asta_roadmap['base_2029']['pdb_total_triliun']:,.1f} Triliun`). Untuk mencapai **Target Akselerasi Pertumbuhan Ekonomi `8,00%` pada tahun 2029** "
        f"(`Rp {asta_roadmap['asta_2029']['pdb_total_triliun']:,.1f} Triliun`), terdapat **selisih nilai tambah (*GDP Gap*) sebesar `+Rp {asta_roadmap['gap_total_2029']:,.1f} Triliun`** "
        f"yang wajib dikejar melalui **6 Mesin Penggerak Sektoral** berikut:"
    )

    ac_chart1, ac_chart2 = st.columns([1.15, 1.15])
    with ac_chart1:
        sb_df = asta_roadmap["sector_boost_df"]
        fig_boost = go.Figure()
        fig_boost.add_trace(
            go.Bar(
                y=sb_df["Sektor Lapangan Usaha (KBLI BPS) / Mesin Penggerak"],
                x=sb_df["Laju Saat Ini (Data Live %)"],
                name="Laju Saat Ini (Data Live / Baseline %)",
                orientation="h",
                marker_color="#64748b",
                text=[f"{v:.2f}%" for v in sb_df["Laju Saat Ini (Data Live %)"]],
                textposition="outside",
            )
        )
        fig_boost.add_trace(
            go.Bar(
                y=sb_df["Sektor Lapangan Usaha (KBLI BPS) / Mesin Penggerak"],
                x=sb_df["Target Laju Asta Cita 8% (%)"],
                name="Target Harus Digenjot (Akselerasi 8% - 2029)",
                orientation="h",
                marker_color="#f59e0b",
                text=[f"{v:.2f}%" for v in sb_df["Target Laju Asta Cita 8% (%)"]],
                textposition="outside",
            )
        )
        fig_boost.update_layout(
            barmode="group",
            title="🚀 Perbandingan Laju Pertumbuhan Sektoral: Kondisi Live Saat Ini vs Target Akselerasi 8% (2029)",
            xaxis_title="Laju Pertumbuhan Tahunan Sektor (% YoY)",
            xaxis=dict(range=[0, 23.5]),
            yaxis=dict(autorange="reversed"),
            template="plotly_dark",
            height=410,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        st.plotly_chart(fig_boost, use_container_width=True)

    with ac_chart2:
        traj_df = asta_roadmap["trajectory_df"]
        fig_traj_g = go.Figure()
        fig_traj_g.add_trace(
            go.Scatter(
                x=traj_df["Tahun"],
                y=traj_df["Pertumbuhan Target Asta Cita (%)"],
                mode="lines+markers+text",
                text=[f"{v:.2f}%" for v in traj_df["Pertumbuhan Target Asta Cita (%)"]],
                textposition="top center",
                line=dict(color="#f59e0b", width=3.5),
                marker=dict(size=9, symbol="diamond"),
                name="🚀 Target Akselerasi RPJMN (Menuju 8,00% di 2029)",
            )
        )
        fig_traj_g.add_trace(
            go.Scatter(
                x=traj_df["Tahun"],
                y=traj_df["Pertumbuhan Simulasi Aktif (%)"],
                mode="lines+markers+text",
                text=[f"{v:.2f}%" for v in traj_df["Pertumbuhan Simulasi Aktif (%)"]],
                textposition="bottom center",
                line=dict(color="#38bdf8", width=3.0),
                marker=dict(size=8),
                name="🔵 Skenario Simulasi Aktif Saat Ini",
            )
        )
        fig_traj_g.add_trace(
            go.Scatter(
                x=traj_df["Tahun"],
                y=traj_df["Pertumbuhan Baseline Live (%)"],
                mode="lines+markers+text",
                text=[f"{v:.2f}%" for v in traj_df["Pertumbuhan Baseline Live (%)"]],
                textposition="bottom center",
                line=dict(color="#94a3b8", width=2.2, dash="dash"),
                marker=dict(size=7),
                name="⚪ Baseline Data Real Live (Business-as-Usual)",
            )
        )
        fig_traj_g.update_layout(
            title="📈 Lintasan Pertumbuhan Ekonomi (% YoY) 2025–2030: Baseline Live vs Target Akselerasi 8%",
            yaxis_title="Laju Pertumbuhan PDB Nasional (% YoY)",
            yaxis=dict(range=[4.2, 8.9]),
            template="plotly_dark",
            height=410,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        st.plotly_chart(fig_traj_g, use_container_width=True)

    st.markdown("#### 📋 Tabel Komando 6 Kelompok Sektor yang Harus Digenjot Menuju Pertumbuhan 8,00% (RPJMN 2029)")
    sb_disp_cols = [c for c in asta_roadmap["sector_boost_df"].columns if "Asta Cita" not in c]
    st.dataframe(asta_roadmap["sector_boost_df"][sb_disp_cols], use_container_width=True, hide_index=True)

    st.markdown("---")
    # BAGIAN KHUSUS: TRIAL UJI AKURASI MODEL TAHUN 2025 (PROYEKSI VS AKTUAL BPS)
    st.subheader("🎯 Trial Uji Akurasi Model Tahun 2025 (Backtesting: Proyeksi Ekonometrika vs Realisasi Aktual BPS)")
    st.markdown(
        "Sesuai kaidah metodologi ekonometrika ilmiah, sebelum model dipakai memproyeksikan tahun **2026–2030**, "
        "dilakukan uji *Backtesting* pada **4 Kuartal Tahun 2025 (2025Q1–2025Q4)** untuk menguji seberapa presisi hasil prediksi model terhadap data aktual BPS:"
    )

    bt_c1, bt_c2 = st.columns([1.15, 1.45])
    with bt_c1:
        bt_q_only = bt_2025["table_df"].iloc[:-1].copy()
        fig_bt = go.Figure()
        fig_bt.add_trace(
            go.Bar(
                x=bt_q_only["Periode Uji"],
                y=bt_q_only["PDB Aktual BPS 2025 (Rp T)"],
                name="PDB Aktual BPS 2025 (Rp T)",
                marker_color="#10b981",
                text=bt_q_only["PDB Aktual BPS (Rp T)"],
                textposition="outside",
            )
            if "PDB Aktual BPS 2025 (Rp T)" in bt_q_only.columns
            else go.Bar(
                x=bt_q_only["Periode Uji"],
                y=bt_q_only["PDB Aktual BPS (Rp T)"],
                name="PDB Aktual BPS 2025 (Rp T)",
                marker_color="#10b981",
                text=bt_q_only["PDB Aktual BPS (Rp T)"],
                textposition="outside",
            )
        )
        fig_bt.add_trace(
            go.Bar(
                x=bt_q_only["Periode Uji"],
                y=bt_q_only["PDB Proyeksi Model (Rp T)"],
                name="PDB Proyeksi Model 2025 (Rp T)",
                marker_color="#38bdf8",
                text=bt_q_only["PDB Proyeksi Model (Rp T)"],
                textposition="outside",
            )
        )
        fig_bt.update_layout(
            barmode="group",
            title=f"Perbandingan Kuartalan 2025: Aktual BPS vs Proyeksi Model (Akurasi {bt_2025['accuracy_pct']:.2f}%)",
            yaxis_title="PDB Riil Kuartalan (Triliun Rp)",
            yaxis=dict(range=[4400, 5200]),
            template="plotly_dark",
            height=350,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        st.plotly_chart(fig_bt, use_container_width=True)

    with bt_c2:
        st.dataframe(bt_2025["table_df"], use_container_width=True, hide_index=True, height=250)
        st.success(
            f"✅ **Kesimpulan Validasi 2025:** Selisih rata-rata (*Mean Absolute Percentage Error* / MAPE) antara prediksi model "
            f"(`Rp {bt_2025['pred_pdb_2025']:,.2f} T` | tumbuh `{bt_2025['pred_growth_2025']:.2f}%`) dengan realisasi aktual BPS 2025 "
            f"(`Rp {bt_2025['actual_pdb_2025']:,.2f} T` | tumbuh `{bt_2025['actual_growth_2025']:.2f}%`) hanya sebesar **`{bt_2025['mape_pct']:.3f}%`** "
            f"(**Tingkat Akurasi `{bt_2025['accuracy_pct']:.2f}%`**). Dalam literatur peramalan makroekonomi, MAPE < 1% dikategorikan **Sangat Presisi (*Highly Accurate*)**."
        )

    st.markdown("---")
    # GRAFIK TORNADO RANKING PENGARUH VARIABEL
    st.subheader("📊 Peta Sensitivitas (Tornado Chart): Urutan Variabel Paling Berpengaruh terhadap PDB")
    fig_tornado = px.bar(
        tornado_df,
        x="Bobot Pengaruh Terstandarisasi (Std. Beta)",
        y="Variabel",
        color="Peran Ekonomi",
        orientation="h",
        text="Bobot Pengaruh Terstandarisasi (Std. Beta)",
        color_discrete_map={
            "Pendorong Positif PDB (+)": "#10b981",
            "Faktor Penekan / Risiko PDB (-)": "#f43f5e",
        },
        title=f"Ranking Kekuatan Pengaruh Variabel terhadap {model_y} (Standardized Beta Coefficient)",
        template="plotly_dark",
        height=390,
    )
    fig_tornado.update_traces(textposition="outside")
    st.plotly_chart(fig_tornado, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: SIMULATOR PRODUKSI TAMBANG (X) x HARGA (Y) & HILIRISASI (MULTI-TAHUN 2025-2030)
# -----------------------------------------------------------------------------
with tabs[1]:
    st.subheader(
        f"⛏️ Simulator Interaktif Multi-Tahun: Produksi Komoditas ($X$) $\\times$ Harga Dunia ($Y$) $\\rightarrow$ Proyeksi PDB {selected_target_year}"
    )
    st.markdown(
        "Anda dapat memilih **Tahun Target (2025 s/d 2030)** pada kotak di bagian atas layar, mengklik **5 Tombol Preset Skenario 1-Klik (termasuk Target Akselerasi 8% Tahun 2029)**, "
        "atau menggeser **Volume Produksi Tambang (Batubara, Bijih Nikel, Emas, Smelter)** dan **Harga Komoditas** di bawah ini:"
    )

    bp = sem_res["base_params"]
    pcol1, pcol2, pcol3, pcol4, pcol5 = st.columns(5)
    if pcol1.button("🔵 1. Kondisi Aktual (Baseline Live)", use_container_width=True):
        st.session_state["custom_sem_scenario"] = dict(bp)
        st.rerun()
    if pcol2.button("🟢 2. Booming Hilirisasi & EV (+18% Smelter)", use_container_width=True):
        s_opt = dict(bp)
        s_opt.update({
            "prod_batubara_thn": round(bp["prod_batubara_thn"] * 1.05, 1),
            "prod_nikel_thn": round(bp["prod_nikel_thn"] * 1.15, 1),
            "inv_smelter_thn": round(bp["inv_smelter_thn"] * 1.18, 1),
            "harga_nikel_lme": 19800.0,
            "harga_emas_usd": 2850.0,
            "harga_batubara_hba": 138.0,
            "kurs_usd_idr": 15400.0,
            "bi_rate": 5.25,
        })
        st.session_state["custom_sem_scenario"] = s_opt
        st.rerun()
    if pcol3.button("🔴 3. Krisis Energi (Minyak $105 & Kurs 16.850)", use_container_width=True):
        s_pes = dict(bp)
        s_pes.update({
            "prod_batubara_thn": round(bp["prod_batubara_thn"] * 0.94, 1),
            "prod_nikel_thn": round(bp["prod_nikel_thn"] * 0.92, 1),
            "harga_nikel_lme": 14800.0,
            "harga_minyak_icp": 105.0,
            "kurs_usd_idr": 16850.0,
            "bi_rate": 6.50,
            "inflasi": 4.20,
        })
        st.session_state["custom_sem_scenario"] = s_pes
        st.rerun()
    if pcol4.button("🟡 4. Kuota RKAB Dipangkas -12% & Harga Naik", use_container_width=True):
        s_rkab = dict(bp)
        s_rkab.update({
            "prod_batubara_thn": round(bp["prod_batubara_thn"] * 0.88, 1),
            "prod_nikel_thn": round(bp["prod_nikel_thn"] * 0.88, 1),
            "harga_batubara_hba": round(bp["harga_batubara_hba"] * 1.16, 1),
            "harga_nikel_lme": round(bp["harga_nikel_lme"] * 1.18, 0),
            "tarif_royalti_pct": 12.0,
        })
        st.session_state["custom_sem_scenario"] = s_rkab
        st.rerun()
    pcol5.button(
        "🚀 5. Target Akselerasi 8,00% (2029)",
        type="primary",
        use_container_width=True,
        on_click=_activate_asta_cita_8pct,
        key="btn_asta_tab2",
    )

    cur_s = sem_res["scenario_params"]

    st.markdown(f"#### 🎛️ Panel Pengaturan Parameter Simulasi (Basis Tahun Target: **{selected_target_year}**)")
    sc_left, sc_mid, sc_right = st.columns(3)

    with sc_left:
        st.markdown("**⛏️ A. Sisi Volume Produksi Hulu (Kuota RKAB $X$)**")
        in_coal_q = st.slider(
            "Produksi Batubara Nasional (Juta Ton/Thn):",
            min_value=500.0,
            max_value=950.0,
            value=float(round(cur_s["prod_batubara_thn"], 1)),
            step=5.0,
        )
        in_nikel_q = st.slider(
            "Produksi Bijih Nikel Nasional (Juta WMT/Thn):",
            min_value=120.0,
            max_value=360.0,
            value=float(round(cur_s["prod_nikel_thn"], 1)),
            step=2.0,
        )
        in_emas_q = st.slider(
            "Produksi Emas Nasional (Ton/Thn):",
            min_value=60.0,
            max_value=180.0,
            value=float(round(cur_s["prod_emas_thn"], 1)),
            step=1.0,
        )

    with sc_mid:
        st.markdown("**💰 B. Sisi Harga Komoditas Dunia ($Y$)**")
        in_hba = st.slider(
            "Harga Batubara Acuan / HBA (USD/Ton):",
            min_value=60.0,
            max_value=250.0,
            value=float(round(cur_s["harga_batubara_hba"], 1)),
            step=1.0,
        )
        in_lme = st.slider(
            "Harga Nikel LME (USD/Ton):",
            min_value=11000.0,
            max_value=28000.0,
            value=float(round(cur_s["harga_nikel_lme"], 0)),
            step=100.0,
        )
        in_gold = st.slider(
            "Harga Emas Dunia Spot Gold (USD/Oz):",
            min_value=1800.0,
            max_value=3500.0,
            value=float(round(cur_s["harga_emas_usd"], 0)),
            step=10.0,
        )
        in_oil = st.slider(
            "Harga Minyak Mentah Brent/ICP (USD/Barel):",
            min_value=45.0,
            max_value=140.0,
            value=float(round(cur_s["harga_minyak_icp"], 1)),
            step=0.5,
        )

    with sc_right:
        st.markdown("**🏭 C. Sisi Hilirisasi Smelter, Fiskal & Moneter**")
        in_smelter = st.slider(
            "Investasi Smelter & Hilirisasi (Triliun Rp/Thn):",
            min_value=150.0,
            max_value=650.0,
            value=float(round(cur_s["inv_smelter_thn"], 1)),
            step=5.0,
        )
        in_royalti = st.slider(
            "Tarif Efektif Royalti & PNBP Minerba (%):",
            min_value=5.0,
            max_value=18.0,
            value=float(round(cur_s.get("tarif_royalti_pct", 10.5), 1)),
            step=0.5,
        )
        in_kurs = st.slider(
            "Nilai Tukar Rupiah (Rp / USD):",
            min_value=13500.0,
            max_value=18500.0,
            value=float(round(cur_s["kurs_usd_idr"], 0)),
            step=50.0,
        )
        in_bi = st.slider(
            "Suku Bunga Acuan BI-Rate (%):",
            min_value=3.50,
            max_value=8.00,
            value=float(round(cur_s["bi_rate"], 2)),
            step=0.25,
        )

    live_custom_params = {
        "prod_batubara_thn": in_coal_q,
        "prod_nikel_thn": in_nikel_q,
        "prod_emas_thn": in_emas_q,
        "inv_smelter_thn": in_smelter,
        "harga_batubara_hba": in_hba,
        "harga_nikel_lme": in_lme,
        "harga_emas_usd": in_gold,
        "harga_minyak_icp": in_oil,
        "kurs_usd_idr": in_kurs,
        "bi_rate": in_bi,
        "inflasi": cur_s["inflasi"],
        "tarif_royalti_pct": in_royalti,
    }
    sim_live = run_simultaneous_mining_gdp_simulation(
        sim_base_df, live_custom_params, target_year=selected_target_year
    )
    s_out = sim_live["selected_year_scen"]
    b_out = sim_live["selected_year_base"]

    st.markdown("---")
    st.subheader(
        f"🚀 Hasil Perhitungan Simulasi 4-Blok Tahun {selected_target_year} (Hulu Kat. B ➔ Hilirisasi Kat. C ➔ PNBP ➔ PDB Nasional)"
    )

    r1, r2, r3, r4, r5 = st.columns(5)
    r1.metric(
        "1️⃣ PDB Hulu Tambang (Kat. B)",
        f"Rp {s_out['pdb_hulu_triliun']:,.1f} T",
        f"{s_out['pdb_hulu_triliun'] - b_out['pdb_hulu_triliun']:+,.1f} T vs Baseline",
        help="Kategori B (KBLI BPS): Nilai tambah kegiatan penggalian komoditas tambang mentah (Batubara, Bijih Nikel, Bijih Tembaga-Emas, Migas) sebelum masuk smelter.",
    )
    r2.metric(
        "2️⃣ PDB Hilirisasi Logam (Kat. C)",
        f"Rp {s_out['pdb_hilir_triliun']:,.1f} T",
        f"{s_out['pdb_hilir_triliun'] - b_out['pdb_hilir_triliun']:+,.1f} T vs Baseline",
        help="Kategori C (KBLI 24 BPS - Industri Logam Dasar): Nilai tambah pengolahan bijih tambang di pabrik Smelter (FeNi, NPI, MHP Baterai EV, Stainless Steel, Katoda Tembaga & Emas Murni).",
    )
    r3.metric(
        "3️⃣ Ekspor Olahan Smelter",
        f"${s_out['ekspor_hilir_miliar_usd']:,.2f} Miliar",
        f"{s_out['ekspor_hilir_miliar_usd'] - b_out['ekspor_hilir_miliar_usd']:+,.2f} Miliar USD",
        help="Total devisa ekspor produk hilirisasi mineral olahan (HS 72 Besi-Baja/Stainless, HS 75 Nikel Olahan, HS 28 Bahan Baterai MHP, HS 74 Katoda Tembaga).",
    )
    r4.metric(
        "4️⃣ PNBP & Royalti Minerba",
        f"Rp {s_out['pnbp_royalti_triliun']:,.1f} T",
        f"{s_out['pnbp_royalti_triliun'] - b_out['pnbp_royalti_triliun']:+,.1f} T vs Baseline",
        help="Penerimaan Negara Bukan Pajak (PNBP) & Royalti sektor Mineral dan Batubara yang masuk ke kas negara dan Dana Bagi Hasil (DBH) daerah.",
    )
    r5.metric(
        f"🏆 PROYEKSI PDB NASIONAL {selected_target_year}",
        f"Tumbuh {s_out['growth_pct']:.2f}%",
        f"Rp {s_out['pdb_total_triliun']:,.1f} T ({s_out['growth_pct'] - b_out['growth_pct']:+.2f}%)",
        help=f"Total Proyeksi Produk Domestik Bruto (PDB) Riil Indonesia Tahun {selected_target_year} beserta laju pertumbuhannya (% YoY).",
    )

    pdb_non_minerba = (
        s_out["pdb_total_triliun"]
        - s_out["pdb_hulu_triliun"]
        - s_out["pdb_hilir_triliun"]
        - s_out["spillover_triliun"]
    )
    fig_wf = go.Figure(
        go.Waterfall(
            name=str(selected_target_year),
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=[
                "1. PDB Hulu Pertambangan (Kat. B)",
                "2. PDB Hilirisasi Smelter Logam (Kat. C)",
                "3. Efek Pengganda (Listrik, Konstruksi, Logistik & PNBP)",
                "4. Sektor Ekonomi Lainnya (Konsumsi, Pertanian, Jasa, dll.)",
                f"TOTAL PROYEKSI PDB NASIONAL {selected_target_year}",
            ],
            textposition="outside",
            text=[
                f"Rp {s_out['pdb_hulu_triliun']:,.1f} T",
                f"Rp {s_out['pdb_hilir_triliun']:,.1f} T",
                f"Rp {s_out['spillover_triliun']:,.1f} T",
                f"Rp {pdb_non_minerba:,.1f} T",
                f"Rp {s_out['pdb_total_triliun']:,.1f} T ({s_out['growth_pct']:.2f}%)",
            ],
            y=[
                s_out["pdb_hulu_triliun"],
                s_out["pdb_hilir_triliun"],
                s_out["spillover_triliun"],
                pdb_non_minerba,
                0,
            ],
            connector={"line": {"color": "#64748b"}},
            increasing={"marker": {"color": "#10b981"}},
            totals={"marker": {"color": "#38bdf8"}},
        )
    )
    fig_wf.update_layout(
        title=f"🔗 Diagram Rantai Nilai (Waterfall): Dari Produksi Hulu Tambang & Hilirisasi Smelter Menuju Total PDB {selected_target_year}",
        yaxis_title="Nilai PDB Riil (Triliun Rupiah)",
        template="plotly_dark",
        height=430,
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    # Tabel Ringkasan Multi-Tahun 2025 s/d 2030 dari Skenario Slider Aktif
    st.markdown("#### 📅 Tabel Proyeksi Berkelanjutan Multi-Tahun (2025 s/d 2030) Berdasarkan Pengaturan Slider di Atas")
    my_rows = []
    for yr_k in (2025, 2026, 2027, 2028, 2029, 2030):
        m_s = sim_live["multiyear_scen"][yr_k]
        m_b = sim_live["multiyear_base"][yr_k]
        my_rows.append({
            "Tahun": f"{yr_k} {'(Trial Backtest)' if yr_k == 2025 else '(Proyeksi)'}",
            "PDB Hulu Kat. B (Rp T)": f"Rp {m_s['pdb_hulu_triliun']:,.1f} T",
            "PDB Hilirisasi Kat. C (Rp T)": f"Rp {m_s['pdb_hilir_triliun']:,.1f} T",
            "Spillover & Multiplier (Rp T)": f"Rp {m_s['spillover_triliun']:,.1f} T",
            "Ekspor Smelter ($ Miliar)": f"${m_s['ekspor_hilir_miliar_usd']:,.2f} Miliar",
            "PNBP Minerba (Rp T)": f"Rp {m_s['pnbp_royalti_triliun']:,.1f} T",
            "Total PDB Riil Simulasi (Rp T)": f"Rp {m_s['pdb_total_triliun']:,.1f} T",
            "Pertumbuhan Simulasi (%)": f"{m_s['growth_pct']:.2f}%",
            "Pertumbuhan Baseline (%)": f"{m_b['growth_pct']:.2f}%",
        })
    st.dataframe(pd.DataFrame(my_rows), use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 3: SIMULATOR KETAHANAN SUBSIDI BBM, B50, BIOETANOL E10-E90, KONVERSI LPG KE LNG,
#        LIFTING MIGAS (BLOK MASELA/IDD/ROKAN), DMO BATUBARA PLN, RKAB 6 MINERAL & 14 TEROBOSAN PDB 8%
# -----------------------------------------------------------------------------
with tabs[2]:
    st.subheader(
        "⚡ Simulator Kedaulatan Energi (B50, Bioetanol E10–E90, Konversi LPG ke LNG, Lifting Migas Masela/IDD/Rokan), Kuota DMO Batubara, Rekomendasi RKAB 6 Mineral & 14 Terobosan PDB 8%"
    )
    st.markdown(
        "Menu strategis ini dirancang khusus dalam **3 Sub-Menu Terpisah** agar tidak membingungkan, menghubungkan kebijakan **mikro-fiskal & energi** "
        "(ketahanan subsidi Pertalite/Solar/LPG saat harga minyak dunia bergejolak) dengan **kuota DMO & RKAB 6 mineral** serta **14 terobosan kebijakan baru** menuju **Target Pertumbuhan Ekonomi 8,00% (RPJMN 2029)**:"
    )

    sub_tabs_t3 = st.tabs([
        "⛽ 3A. Subsidi BBM, B50, Bioetanol E10–E90, LNG & Lifting Migas (Masela/IDD)",
        "⚖️ 3B. Simulasi DMO Batubara PLN ($70/t) & Rekomendasi Kuota RKAB 6 Mineral",
        "🚀 3C. Simulator 14 Terobosan Kebijakan Baru Pengungkit PDB 8% (8 Strategis + 6 Inovasi Baru)",
    ])

    # Ambil harga komoditas live dari quotes / slider Tab 2 sebagai default awal
    q_cu_default = float(quotes.get("Harga_Tembaga_LME_USD", {}).get("value", 9680.0))
    q_sn_default = float(quotes.get("Harga_Timah_LME_USD", {}).get("value", 32450.0))
    q_bx_default = float(quotes.get("Harga_Bauksit_USD", {}).get("value", 74.0))
    q_lng_default = float(quotes.get("Harga_LNG_MMBTU_USD", {}).get("value", 11.85))

    with sub_tabs_t3[0]:
        st.markdown(
            "#### ⛽ Sub-Menu 3A: Simulator Ketahanan Subsidi BBM (Pertalite & Solar) + LPG 3 Kg vs Kenaikan Harga Minyak Dunia, Lifting Blok Migas Raksasa (Masela, IDD, Rokan), B50, Bioetanol & Cross-Subsidy Komoditas Tambang"
        )
        st.info(
            "💡 **Pertanyaan Kunci yang Dijawab Simulator Ini:** Ketika harga minyak mentah dunia (*Brent/ICP*) melonjak naik, apakah beban subsidi BBM (Pertalite & Solar) "
            "dapat **ditutupi sepenuhnya (Surplus)** oleh kombinasi: **(1) Penghematan Biodiesel B50 (0% Impor Solar), Konversi Pertalite ke Bioetanol (E10–E90 ala Brasil), & Konversi LPG 3 Kg ke LNG Domestik/Jargas/DME**, "
            "**(2) Windfall Penerimaan Lifting Hulu Migas & LNG (termasuk aktivasi Blok Masela Inpex Jepang, IDD, Andaman, Rokan EOR)**, serta **(3) Kenaikan PNBP/Royalti Komoditas Tambang (Batubara, Nikel, Emas, Tembaga, Timah)**?"
        )

        e_col1, e_col2, e_col3 = st.columns(3)
        with e_col1:
            st.markdown("**🛢️ 1. Harga Minyak & Lifting Hulu Migas Nasional**")
            sim_icp_oil = st.slider(
                "Harga Minyak Mentah Brent / ICP (USD/Barel):",
                min_value=50.0,
                max_value=140.0,
                value=float(in_oil),
                step=1.0,
                key="sim_t3_icp",
            )
            sim_lift_oil = st.slider(
                "Lifting Minyak Bumi Nasional (Ribu Barel/Hari - Target 1 Juta Bph):",
                min_value=550.0,
                max_value=1050.0,
                value=635.0 if not sem_res.get("scen_is_asta_cita") else 950.0,
                step=10.0,
                help="Baseline saat ini ~585-605 ribu bph; target akselerasi s/d 1.000 ribu bph (1 Juta Bph) melalui Chemical EOR Blok Rokan, Banyu Urip & reaktivasi 4.500 sumur idle.",
                key="sim_t3_lift_oil",
            )
            sim_lift_gas = st.slider(
                "Lifting Gas Bumi & LNG (MMSCFD - Termasuk Blok Masela, IDD & Tangguh):",
                min_value=5400.0,
                max_value=12000.0,
                value=6500.0 if not sem_res.get("scen_is_asta_cita") else 10800.0,
                step=100.0,
                help="Termasuk tambahan produksi raksasa dari Blok Masela (Inpex Jepang: 9,5 MTPA LNG + 150 MMSCFD gas pipa), IDD Gendalo-Gehem, Andaman, dan Tangguh Train 3.",
                key="sim_t3_lift_gas",
            )

        with e_col2:
            st.markdown("**🌱 2. Substitusi Impor BBM & LPG (B50, Bioetanol & LNG)**")
            sim_b_mandate = st.selectbox(
                "Program Mandatori Biodiesel Sawit (Pengganti Impor Solar):",
                options=[
                    "B50 (0% Impor Solar - Mandiri Penuh)",
                    "B60 (Surplus Ekspor Bio-Solar Hijau)",
                    "B40 (Transisi Menuju B50)",
                    "B35 (Baseline Lama)",
                ],
                index=0,
                key="sim_t3_b50",
            )
            sim_eth_pct = st.slider(
                "Konversi Bensin Pertalite ke Bioetanol Tebu/Singkong/Sorgum (E0% s/d E90% ala Brasil):",
                min_value=0.0,
                max_value=90.0,
                value=20.0 if not sem_res.get("scen_is_asta_cita") else 50.0,
                step=5.0,
                help="E10 = 10% Bioetanol, E50 = 50% Bioetanol, E90 = 90% Bioetanol (seperti flex-fuel di Brasil) untuk memangkas impor bensin secara drastis.",
                key="sim_t3_eth",
            )
            sim_lpg_lng_pct = st.slider(
                "Konversi Impor LPG 3 Kg ke LNG Domestik, Jargas Rumah Tangga/Industri & DME (%):",
                min_value=0.0,
                max_value=100.0,
                value=40.0 if not sem_res.get("scen_is_asta_cita") else 75.0,
                step=5.0,
                help="Mengganti impor LPG 3 Kg (~6,9 juta ton/thn) dengan jaringan gas (Jargas), mikro-LNG domestik, kompor induksi, dan DME batubara.",
                key="sim_t3_lpg_lng",
            )

        with e_col3:
            st.markdown("**💎 3. Harga Komoditas Tambang Penutup Subsidi (Cross-Subsidy)**")
            sim_hba_t3 = st.slider(
                "Harga Batubara Acuan / HBA (USD/Ton):",
                min_value=70.0,
                max_value=240.0,
                value=float(in_hba),
                step=2.0,
                key="sim_t3_hba",
            )
            sim_lme_t3 = st.slider(
                "Harga Nikel LME (USD/Ton):",
                min_value=12000.0,
                max_value=28000.0,
                value=float(in_lme),
                step=200.0,
                key="sim_t3_lme",
            )
            sim_gold_t3 = st.slider(
                "Harga Emas Dunia Spot Gold (USD/Oz):",
                min_value=1900.0,
                max_value=3500.0,
                value=float(in_gold),
                step=25.0,
                key="sim_t3_gold",
            )
            sim_cu_t3 = st.slider(
                "Harga Tembaga Dunia LME/COMEX (USD/Ton):",
                min_value=7500.0,
                max_value=13500.0,
                value=float(q_cu_default),
                step=100.0,
                key="sim_t3_cu",
            )

    with sub_tabs_t3[1]:
        st.markdown(
            "#### ⚖️ Sub-Menu 3B: Simulator Kebijakan Kuota DMO Batubara PLN (`$70/ton`) vs Ekspor & Royalti Progresif + Rekomendasi Kuota RKAB Optimal 6 Mineral Utama"
        )
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            sim_dmo_share = st.slider(
                "Kewajiban Kuota DMO Batubara Domestik (% dari Total Produksi RKAB):",
                min_value=15.0,
                max_value=45.0,
                value=28.0,
                step=1.0,
                help="Porsi produksi batubara yang wajib dipasok ke dalam negeri (PLN, Smelter, Semen, Pupuk, DME). Standar regulasi minimal 25–30%.",
                key="sim_t3_dmo_share",
            )
        with d_col2:
            sim_dmo_pln_cap = st.slider(
                "Harga Patokan DMO Batubara Khusus Listrik PLN (USD/Ton):",
                min_value=50.0,
                max_value=100.0,
                value=70.0,
                step=2.0,
                help="Harga batas atas (price cap) batubara DMO untuk pembangkit listrik PLN agar tarif listrik rakyat & industri tidak naik saat HBA dunia melonjak.",
                key="sim_t3_dmo_pln",
            )
        with d_col3:
            sim_dmo_ind_cap = st.slider(
                "Harga Patokan DMO Batubara Industri (Semen/Pupuk/Smelter - USD/Ton):",
                min_value=70.0,
                max_value=120.0,
                value=90.0,
                step=2.0,
                key="sim_t3_dmo_ind",
            )

    # Jalankan mesin simulasi terpadu Energi + DMO + RKAB 6 Mineral + 14 Terobosan Kebijakan
    energy_dmo_res = compute_energy_dmo_rkab_frontier_simulation(
        sim_live,
        custom_energy_policy={
            "icp_oil_usd": sim_icp_oil,
            "lifting_oil_kbpd": sim_lift_oil,
            "lifting_gas_mmscfd": sim_lift_gas,
            "biodiesel_mandate": sim_b_mandate,
            "bioethanol_blend_pct": sim_eth_pct,
            "lpg_to_lng_dme_pct": sim_lpg_lng_pct,
            "dmo_coal_share_pct": sim_dmo_share,
            "dmo_pln_price_cap_usd": sim_dmo_pln_cap,
            "dmo_ind_price_cap_usd": sim_dmo_ind_cap,
            "coal_hba_usd": sim_hba_t3,
            "nickel_lme_usd": sim_lme_t3,
            "gold_usd_oz": sim_gold_t3,
            "copper_lme_usd": sim_cu_t3,
            "tin_lme_usd": q_sn_default,
            "bauxite_usd_ton": q_bx_default,
            "lng_jkm_usd_mmbtu": q_lng_default,
            "kurs_usd_idr": float(in_kurs),
        },
    )

    # Render hasil Sub-Menu 3A (Subsidi BBM, B50, Bioetanol, LNG & Lifting Migas)
    with sub_tabs_t3[0]:
        if energy_dmo_res["is_subsidy_covered"]:
            st.success(
                f"🟢 **KESIMPULAN SIMULASI KETAHANAN SUBSIDI BBM & ENERGI: TERTUTUPI PENUH / SURPLUS FISKAL (`+Rp {energy_dmo_res['net_fiscal_surplus_deficit_triliun']:,.1f} Triliun` | Rasio Coverage `{energy_dmo_res['coverage_ratio_pct']:.1f}%`)** — "
                f"Pada harga minyak ICP **${sim_icp_oil:,.1f}/barel**, beban subsidi kotor (`Rp {energy_dmo_res['gross_total_subsidy_without_reform']:,.1f} T`) berhasil ditutup sepenuhnya oleh "
                f"**Penghematan {energy_dmo_res['b_label_short']} + Bioetanol E{int(sim_eth_pct)} + Konversi LNG (`Rp {energy_dmo_res['total_energy_transition_saving']:,.1f} T`)**, "
                f"**PNBP Lifting Hulu Migas & Blok Masela (`Rp {energy_dmo_res['total_migas_pnbp_triliun']:,.1f} T`)**, serta **Windfall PNBP Komoditas Tambang (`Rp {energy_dmo_res['total_minerba_pnbp_cover_triliun']:,.1f} T`)**!"
            )
        else:
            st.error(
                f"🔴 **KESIMPULAN SIMULASI KETAHANAN SUBSIDI BBM & ENERGI: DEFISIT FISKAL (`{energy_dmo_res['net_fiscal_surplus_deficit_triliun']:+,.1f} Triliun` | Rasio Coverage `{energy_dmo_res['coverage_ratio_pct']:.1f}%`)** — "
                f"Lonjakan harga minyak ICP ke **${sim_icp_oil:,.1f}/barel** belum tertutup penuh. Naikkan bauran **Bioetanol (E25–E50)**, **Konversi LPG ke LNG**, **Lifting Migas**, atau **Harga/Kuota Ekspor Komoditas**!"
            )

        k_e1, k_e2, k_e3, k_e4, k_e5 = st.columns(5)
        k_e1.metric(
            "1️⃣ Beban Subsidi Kotor",
            f"Rp {energy_dmo_res['gross_total_subsidy_without_reform']:,.1f} T",
            f"Pada ICP ${sim_icp_oil:,.0f}/bbl",
            delta_color="inverse",
        )
        k_e2.metric(
            f"2️⃣ Hemat {energy_dmo_res['b_label_short']} + E{int(sim_eth_pct)} + LNG",
            f"Rp {energy_dmo_res['total_energy_transition_saving']:,.1f} T",
            f"B50: {energy_dmo_res['saving_b50_triliun']:,.0f}T | E{int(sim_eth_pct)}: {energy_dmo_res['saving_bioethanol_triliun']:,.0f}T | LNG: {energy_dmo_res['saving_lpg_to_lng_triliun']:,.0f}T",
        )
        k_e3.metric(
            "3️⃣ PNBP Lifting Hulu Migas",
            f"Rp {energy_dmo_res['total_migas_pnbp_triliun']:,.1f} T",
            f"Minyak {sim_lift_oil:,.0f} kbpd & Gas {sim_lift_gas:,.0f} MMSCFD",
        )
        k_e4.metric(
            "4️⃣ PNBP Komoditas Minerba",
            f"Rp {energy_dmo_res['total_minerba_pnbp_cover_triliun']:,.1f} T",
            f"Batubara {energy_dmo_res['pnbp_coal_triliun']:,.0f}T | Nikel {energy_dmo_res['pnbp_nickel_smelter_triliun']:,.0f}T | Au-Cu-Sn {energy_dmo_res['pnbp_gold_copper_tin_triliun']:,.0f}T",
        )
        k_e5.metric(
            "🏆 SALDO BERSIH COVER SUBSIDI",
            f"{energy_dmo_res['net_fiscal_surplus_deficit_triliun']:+,.1f} T",
            f"Coverage {energy_dmo_res['coverage_ratio_pct']:.1f}% ({'TERTUTUPI' if energy_dmo_res['is_subsidy_covered'] else 'DEFISIT'})",
        )

        ch_sub1, ch_sub2 = st.columns([1.15, 1.15])
        with ch_sub1:
            fig_sub_bar = go.Figure()
            fig_sub_bar.add_trace(
                go.Bar(
                    x=[
                        "1. Beban Subsidi Kotor\n(Tanpa Transisi Energi)",
                        f"2. Hemat {energy_dmo_res['b_label_short']} (Solar)\n+ Bioetanol E{int(sim_eth_pct)} + LNG",
                        "3. Penerimaan Lifting\nHulu Migas & Masela",
                        "4. PNBP & Royalti\n6 Mineral Tambang",
                        "5. TOTAL PERISAI FISKAL\nPENUTUP SUBSIDI",
                    ],
                    y=[
                        energy_dmo_res["gross_total_subsidy_without_reform"],
                        energy_dmo_res["total_energy_transition_saving"],
                        energy_dmo_res["total_migas_pnbp_triliun"],
                        energy_dmo_res["total_minerba_pnbp_cover_triliun"],
                        energy_dmo_res["total_fiscal_shield_triliun"],
                    ],
                    marker_color=["#f43f5e", "#10b981", "#0ea5e9", "#f59e0b", "#38bdf8"],
                    text=[
                        f"Rp {energy_dmo_res['gross_total_subsidy_without_reform']:,.1f} T",
                        f"Rp {energy_dmo_res['total_energy_transition_saving']:,.1f} T",
                        f"Rp {energy_dmo_res['total_migas_pnbp_triliun']:,.1f} T",
                        f"Rp {energy_dmo_res['total_minerba_pnbp_cover_triliun']:,.1f} T",
                        f"Rp {energy_dmo_res['total_fiscal_shield_triliun']:,.1f} T",
                    ],
                    textposition="outside",
                )
            )
            fig_sub_bar.update_layout(
                title=f"🛡️ Neraca Perisai Fiskal vs Beban Subsidi BBM & LPG (ICP ${sim_icp_oil:,.0f}/bbl)",
                yaxis_title="Triliun Rupiah / Tahun",
                yaxis=dict(range=[0, max(energy_dmo_res["total_fiscal_shield_triliun"], energy_dmo_res["gross_total_subsidy_without_reform"]) * 1.25]),
                template="plotly_dark",
                height=390,
            )
            st.plotly_chart(fig_sub_bar, use_container_width=True)

        with ch_sub2:
            fig_eth_save = go.Figure()
            fig_eth_save.add_trace(
                go.Bar(
                    x=["Biodiesel B50/B60\n(Stop Impor Solar)", f"Bioetanol E{int(sim_eth_pct)}\n(Substitusi Pertalite)", f"Konversi LPG 3 Kg\nke LNG & Jargas ({int(sim_lpg_lng_pct)}%)"],
                    y=[
                        energy_dmo_res["saving_b50_triliun"],
                        energy_dmo_res["saving_bioethanol_triliun"],
                        energy_dmo_res["saving_lpg_to_lng_triliun"],
                    ],
                    marker_color=["#22c55e", "#a855f7", "#06b6d4"],
                    text=[
                        f"Rp {energy_dmo_res['saving_b50_triliun']:,.1f} T",
                        f"Rp {energy_dmo_res['saving_bioethanol_triliun']:,.1f} T",
                        f"Rp {energy_dmo_res['saving_lpg_to_lng_triliun']:,.1f} T",
                    ],
                    textposition="outside",
                )
            )
            fig_eth_save.update_layout(
                title="🌱 Rincian Penghematan Subsidi & Devisa Impor dari 3 Program Kedaulatan Energi",
                yaxis_title="Penghematan (Triliun Rupiah / Tahun)",
                yaxis=dict(range=[0, max(energy_dmo_res["saving_b50_triliun"], energy_dmo_res["saving_bioethanol_triliun"], energy_dmo_res["saving_lpg_to_lng_triliun"], 50.0) * 1.3]),
                template="plotly_dark",
                height=390,
            )
            st.plotly_chart(fig_eth_save, use_container_width=True)

        st.markdown("#### 🎯 Tabel Simulasi *Break-Even* Harga Komoditas & Lifting Migas untuk Menutup Subsidi BBM pada Berbagai Level Harga Minyak ICP")
        st.dataframe(energy_dmo_res["breakeven_df"], use_container_width=True, hide_index=True)

    # Render hasil Sub-Menu 3B (DMO Batubara PLN & Tabel Rekomendasi Kuota RKAB Optimal 6 Mineral + Migas)
    with sub_tabs_t3[1]:
        d_m1, d_m2, d_m3, d_m4, d_m5 = st.columns(5)
        d_m1.metric(
            "⚡ Kuota DMO Listrik PLN",
            f"{energy_dmo_res['q_coal_dmo_pln']:,.1f} Jt Ton",
            f"Harga Cap ${sim_dmo_pln_cap:.0f}/ton",
        )
        d_m2.metric(
            "🏭 Kuota DMO Industri/DME",
            f"{energy_dmo_res['q_coal_dmo_ind']:,.1f} Jt Ton",
            f"Harga Cap ${sim_dmo_ind_cap:.0f}/ton",
        )
        d_m3.metric(
            "🚢 Kuota Ekspor Batubara",
            f"{energy_dmo_res['q_coal_export']:,.1f} Jt Ton",
            f"Harga HBA ${sim_hba_t3:,.1f}/ton",
        )
        d_m4.metric(
            "🏛️ Tarif Royalti Progresif",
            f"{energy_dmo_res['prog_coal_royalty_rate_pct']:.1f}%",
            f"PNBP Batubara: Rp {energy_dmo_res['pnbp_coal_triliun']:,.1f} T",
        )
        d_m5.metric(
            "💡 Penghematan Biaya Listrik PLN",
            f"Rp {energy_dmo_res['pln_dmo_cost_saving_triliun']:,.1f} T/thn",
            "Berkat DMO $70/t vs HBA Pasar",
        )

        st.markdown(
            "#### 📋 Tabel Rekomendasi Kuota RKAB Optimal 6 Mineral Utama + Hulu Migas (Jangka Pendek: Cover Subsidi BBM vs Jangka Panjang 2029: Target PDB 8,00%)"
        )
        st.dataframe(energy_dmo_res["rkab_recommendation_df"], use_container_width=True, hide_index=True)

        st.markdown("---")
        hist_rkab_df = build_annual_rkab_realization_history_df(sim_base_df)
        latest_hist_yr = int(hist_rkab_df["Tahun"].max()) if len(hist_rkab_df) > 0 else 2026
        st.markdown(
            f"#### 📈 Rekam Jejak Historis Kuota RKAB / Target APBN vs Realisasi Produksi 6 Mineral & Lifting Migas (`2010–{latest_hist_yr}` • *Auto-Rolling Live Update*)"
        )
        st.caption(
            f"Data historis ini **otomatis memanjang (*Auto-Rolling*)** setiap tahun ketika tombol **🔄 Update Data Live** diklik (misalnya pada tahun 2027, 2028, dst.) dan terhubung langsung sebagai variabel independen ($X$) dalam model ekonometrika."
        )

        if len(hist_rkab_df) > 0:
            rkab_pair_map = {
                "🪨 1. Batubara Nasional (Juta Ton/Thn)": ("RKAB Batubara (Jt Ton)", "Realisasi Batubara (Jt Ton)", "Juta Ton / Tahun"),
                "🔋 2. Bijih Nikel Nasional (Juta WMT/Thn)": ("RKAB Nikel (Jt WMT)", "Realisasi Nikel (Jt WMT)", "Juta WMT / Tahun"),
                "🟠 3. Bijih Tembaga Nasional (Juta Ton/Thn)": ("RKAB Tembaga (Jt Ton)", "Realisasi Tembaga (Jt Ton)", "Juta Ton / Tahun"),
                "🥇 4. Emas Murni Nasional (Ton/Thn)": ("RKAB Emas (Ton)", "Realisasi Emas (Ton)", "Ton / Tahun"),
                "🧱 5. Bauksit Nasional (Juta WMT/Thn)": ("RKAB Bauksit (Jt WMT)", "Realisasi Bauksit (Jt WMT)", "Juta WMT / Tahun"),
                "⚪ 6. Timah Murni Nasional (Ribu Ton/Thn)": ("RKAB Timah (Ribu Ton)", "Realisasi Timah (Ribu Ton)", "Ribu Ton / Tahun"),
                "🛢️ 7. Lifting Minyak Bumi vs Target APBN (Ribu Bph)": ("Target APBN Minyak (Ribu Bph)", "Realisasi Lifting Minyak (Ribu Bph)", "Ribu Barel / Hari"),
                "🔥 8. Lifting Gas Bumi & LNG vs Target APBN (MMSCFD)": ("Target APBN Gas (MMSCFD)", "Realisasi Lifting Gas (MMSCFD)", "MMSCFD"),
            }
            sel_rkab_comm = st.selectbox(
                "🔍 Pilih Komoditas Tambang / Migas untuk Melihat Grafik Historis Kuota RKAB vs Realisasi Produksi (2010–Tahun Terupdate):",
                options=list(rkab_pair_map.keys()),
                key="sel_hist_rkab_comm",
            )
            col_rkab_q, col_real_q, unit_q = rkab_pair_map[sel_rkab_comm]

            fig_hist_rkab = go.Figure()
            fig_hist_rkab.add_trace(
                go.Bar(
                    x=hist_rkab_df["Tahun"].astype(str),
                    y=hist_rkab_df[col_rkab_q],
                    name=f"Kuota RKAB / Target APBN ({unit_q})",
                    marker_color="rgba(56, 189, 248, 0.55)",
                    text=hist_rkab_df[col_rkab_q],
                    textposition="outside",
                )
            )
            fig_hist_rkab.add_trace(
                go.Scatter(
                    x=hist_rkab_df["Tahun"].astype(str),
                    y=hist_rkab_df[col_real_q],
                    name=f"Realisasi Produksi Aktual ({unit_q})",
                    mode="lines+markers+text",
                    text=hist_rkab_df[col_real_q],
                    textposition="top center",
                    line=dict(color="#10b981", width=3.5),
                    marker=dict(size=9, color="#f59e0b"),
                )
            )
            fig_hist_rkab.update_layout(
                title=f"📊 Tren Historis Kuota RKAB / Target APBN vs Realisasi Aktual: {sel_rkab_comm} (2010–{latest_hist_yr})",
                xaxis_title="Tahun Historis (Auto-Rolling s.d. Tahun Berjalan)",
                yaxis_title=unit_q,
                template="plotly_dark",
                height=410,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            )
            st.plotly_chart(fig_hist_rkab, use_container_width=True)

            with st.expander(f"🗂️ Klik untuk Melihat Tabel Lengkap Historis Tahunan RKAB & Target APBN vs Realisasi 6 Mineral + Hulu Migas (2010–{latest_hist_yr})", expanded=True):
                st.dataframe(hist_rkab_df, use_container_width=True, hide_index=True)

    # Render hasil Sub-Menu 3C (Simulator Interaktif 14 Terobosan Kebijakan Baru Pengungkit PDB 8%: 8 Strategis + 6 Inovasi "Fresh from the Oven")
    with sub_tabs_t3[2]:
        st.markdown(
            "#### 🚀 Sub-Menu 3C: Simulator Interaktif 14 Terobosan Kebijakan Baru Pengungkit PDB 8,00% (`8 Terobosan Strategis + 6 Inovasi 'Fresh from the Oven'`)"
        )
        st.markdown(
            "Pilih kombinasi kebijakan di bawah ini untuk melihat **tambahan nilai PDB Riil (`+Rp Triliun/tahun`)**, **tambahan laju pertumbuhan (`+% YoY`)**, "
            "dan **penghematan/tambahan devisa (`+$ Miliar USD/tahun`)** dalam menutup *GDP Gap* menuju **Target Pertumbuhan Ekonomi 8,00% (RPJMN 2029)**:"
        )

        pl_df = energy_dmo_res["policy_levers_df"]
        all_lever_names = pl_df["Nama Terobosan Kebijakan"].tolist()

        selected_levers = st.multiselect(
            "✅ Pilih Terobosan Kebijakan yang Diaktifkan dalam Simulasi (Default: Seluruh 14 Terobosan Aktif):",
            options=all_lever_names,
            default=all_lever_names,
            key="sim_t3_14_levers",
        )

        active_pl_df = pl_df[pl_df["Nama Terobosan Kebijakan"].isin(selected_levers)].copy()
        tot_boost_rp = float(active_pl_df["Tambahan_PDB_Triliun"].sum()) if len(active_pl_df) > 0 else 0.0
        # Kalibrasi sinergi kebijakan terhadap pertumbuhan PDB menuju 8,00%
        raw_boost_g = float(active_pl_df["Tambahan_Growth_Pct"].sum()) if len(active_pl_df) > 0 else 0.0
        effective_boost_g = round(min(3.35, raw_boost_g * 0.62), 2)
        tot_fx_usd = float(active_pl_df["Penghematan_Devisa_Miliar_USD"].sum()) if len(active_pl_df) > 0 else 0.0
        base_g_2029 = float(asta_roadmap["base_2029"]["growth_pct"])
        Result_g_2029 = round(min(8.45, base_g_2029 + effective_boost_g), 2)

        p_k1, p_k2, p_k3, p_k4 = st.columns(4)
        p_k1.metric(
            "1️⃣ Kebijakan Diaktifkan",
            f"{len(active_pl_df)} dari 14 Ide",
            "8 Strategis + 6 Frontier Baru",
        )
        p_k2.metric(
            "2️⃣ Tambahan PDB Riil Tahunan",
            f"+Rp {tot_boost_rp:,.1f} Triliun",
            f"Menutup Gap RPJMN (+Rp {asta_roadmap['gap_total_2029']:,.0f} T)",
        )
        p_k3.metric(
            "3️⃣ Tambahan & Penghematan Devisa",
            f"+${tot_fx_usd:,.1f} Miliar USD",
            "Memperkuat Kurs Rupiah & Cadangan BI",
        )
        p_k4.metric(
            "🏆 PROYEKSI PERTUMBUHAN 2029",
            f"{Result_g_2029:.2f}% YoY",
            f"+{effective_boost_g:.2f}% di atas Baseline ({base_g_2029:.2f}%)",
        )

        fig_14 = px.bar(
            pl_df.iloc[::-1],
            x="Tambahan_PDB_Triliun",
            y="Nama Terobosan Kebijakan",
            color="Kelompok",
            orientation="h",
            text="Tambahan_PDB_Triliun",
            color_discrete_map={
                "A. 8 Terobosan Strategis Nasional": "#38bdf8",
                "B. 6 Inovasi Baru 'Fresh from the Oven' (Frontier 2026–2035)": "#f59e0b",
            },
            title="🚀 Peta Daya Ungkit 14 Terobosan Kebijakan terhadap PDB Riil Nasional (+Triliun Rp / Tahun)",
            template="plotly_dark",
            height=540,
        )
        fig_14.update_traces(texttemplate="+Rp %{text:,.0f} T", textposition="outside")
        fig_14.update_layout(
            xaxis_title="Tambahan Nilai PDB Riil (+Triliun Rupiah / Tahun)",
            xaxis=dict(range=[0, 620]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        st.plotly_chart(fig_14, use_container_width=True)

        st.markdown("#### 📋 Tabel Matriks 14 Terobosan Kebijakan Pengungkit PDB (`8 Strategis + 6 Inovasi Baru 'Fresh from the Oven'`)")
        disp_pl_df = pl_df.rename(columns={
            "Tambahan_PDB_Triliun": "Daya Ungkit PDB (+Rp T/Thn)",
            "Tambahan_Growth_Pct": "Kontribusi Pertumbuhan (+% YoY)",
            "Penghematan_Devisa_Miliar_USD": "Dampak Devisa (+$ Miliar/Thn)",
        })
        st.dataframe(disp_pl_df, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 4: SENSITIVITY ANALYSIS (MATRIKS 2-ARAH & SPIDER CHART) & STRESS TEST KRISIS
# -----------------------------------------------------------------------------
with tabs[3]:
    st.subheader(
        f"🌪️ Sensitivity Analysis (Matriks 2-Arah & Spider Chart) dan Macro-Mining Stress Test Tahun {selected_target_year}"
    )
    st.markdown(
        "Menu ini menguji **kepekaan (*sensitivity*)** dan **daya tahan (*stress resilience*)** PDB Indonesia ketika terjadi perubahan "
        "kombinasi **Volume Produksi/Smelter ($X$)**, **Harga Komoditas Dunia ($Y$)**, serta **6 Skenario Guncangan Krisis Global Ekstrem**."
    )

    sens_live = run_sensitivity_and_stress_analysis(
        sim_base_df, live_custom_params, target_year=selected_target_year
    )
    mat_g_df = sens_live["matrix_growth_df"]
    mat_p_df = sens_live["matrix_pdb_df"]
    spider_df = sens_live["spider_df"]
    stress_df = sens_live["stress_df"]
    rev_stress_df = sens_live["reverse_stress_df"]

    col_hm1, col_hm2 = st.columns(2)
    with col_hm1:
        st.markdown(f"#### 🟩🟨🟥 1. Heatmap Sensitivitas 2-Arah: Pertumbuhan PDB {selected_target_year} (% YoY)")
        hm_g_z = mat_g_df.set_index("Kombinasi Volume (X) \\ Harga (Y)")
        fig_hm_g = px.imshow(
            hm_g_z,
            text_auto=".2f",
            color_continuous_scale="RdYlGn",
            aspect="auto",
            title=f"Matriks Pertumbuhan PDB {selected_target_year} (%) — Volume (X) vs Harga Dunia (Y)",
            template="plotly_dark",
        )
        fig_hm_g.update_layout(height=360)
        st.plotly_chart(fig_hm_g, use_container_width=True)

    with col_hm2:
        st.markdown(f"#### 💰 2. Heatmap Sensitivitas 2-Arah: Nilai PDB Riil {selected_target_year} (Triliun Rp)")
        hm_p_z = mat_p_df.set_index("Kombinasi Volume (X) \\ Harga (Y)")
        fig_hm_p = px.imshow(
            hm_p_z,
            text_auto=",.1f",
            color_continuous_scale="YlGnBu",
            aspect="auto",
            title=f"Matriks Nilai PDB Riil {selected_target_year} (Triliun Rp) — Volume (X) vs Harga (Y)",
            template="plotly_dark",
        )
        fig_hm_p.update_layout(height=360)
        st.plotly_chart(fig_hm_p, use_container_width=True)

    st.markdown("---")
    col_sp, col_st_chart = st.columns([1.05, 1.15])
    with col_sp:
        st.markdown("#### 🕸️ 3. Kurva *Spider Chart* Elastisitas ($\\pm 25\\%$ Perubahan Variabel)")
        fig_spider = px.line(
            spider_df,
            x="Perubahan Parameter (%)",
            y="Proyeksi Pertumbuhan PDB (%)",
            color="Variabel Penggerak",
            markers=True,
            title=f"Kemiringan Sensitivitas 7 Variabel Kunci terhadap Pertumbuhan PDB {selected_target_year} (%)",
            template="plotly_dark",
            height=410,
        )
        fig_spider.add_vline(x=0, line_dash="dash", line_color="#94a3b8")
        st.plotly_chart(fig_spider, use_container_width=True)

    with col_st_chart:
        st.markdown(f"#### 🚨 4. Grafik Uji Ketahanan (*Stress Test*) 6 Skenario Krisis Ekstrem ({selected_target_year})")
        fig_stress = px.bar(
            stress_df,
            x=f"Pertumbuhan PDB {selected_target_year} (%)",
            y="Skenario Stress Test",
            color="Status Ketahanan Ekonomi",
            orientation="h",
            text=f"Pertumbuhan PDB {selected_target_year} (%)",
            color_discrete_map={
                "🟢 Tahan Uji / Resilien (≥ 5,0%)": "#10b981",
                "🟡 Moderasi Terkendali (4,5%–5,0%)": "#fbbf24",
                "🟠 Waspada Fiskal-Moneter (4,0%–4,5%)": "#f97316",
                "🔴 Tekanan Berat / Siaga Krisis (< 4,0%)": "#f43f5e",
            },
            title=f"Dampak 6 Skenario Krisis Ekstrem terhadap Pertumbuhan PDB {selected_target_year} (%)",
            template="plotly_dark",
            height=410,
        )
        fig_stress.add_vline(x=5.0, line_dash="dot", line_color="#38bdf8", annotation_text="Batas 5,0%")
        fig_stress.update_traces(textposition="outside")
        st.plotly_chart(fig_stress, use_container_width=True)

    st.markdown("#### 📋 Tabel Detail Hasil *Macro-Mining Stress Test* (6 Skenario Guncangan Ekstrem)")
    st.dataframe(stress_df, use_container_width=True, hide_index=True)

    st.markdown("#### 🎯 Tabel *Reverse Stress Test* (Titik Ambang Batas Waspada & Kritis / *Break-Even Point*)")
    st.dataframe(rev_stress_df, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 5: KESIMPULAN BAB V, REKOMENDASI KEBIJAKAN & UNDUH NASKAH ILMIAH / SLIDE PDF
# -----------------------------------------------------------------------------
with tabs[4]:
    st.subheader("🏆 Kesimpulan Utama (Bab V), Rekomendasi Strategis & Pusat Unduhan Naskah Penelitian / Slide (HTML & PDF)")
    st.markdown(
        f"Halaman ini merangkum **Kesimpulan & Rekomendasi Kebijakan (Bab V)** serta menyediakan fasilitas **1-Klik Unduh Naskah Penelitian Lengkap "
        f"BAB I s/d BAB V (Beserta Lampiran 10 Grafik Visual, Tabel 100% Sektor PDB KBLI A–U, Analisis Kedaulatan Energi B50/Etanol/LNG, RKAB 6 Mineral, 14 Terobosan PDB 8% & Parameter Input)** dan **Slide Presentasi Eksekutif 12-Slide (PDF & HTML Landscape)** "
        f"yang **100% Dinamis** mengikuti pengaturan simulasi maupun unggahan CSV untuk **MODUL 17 (`www.trilaksanamining.my.id`) — {AUTHOR_FULL}**."
    )

    # Generate HTML & PDF Paper (BAB I - V) serta Slide Presentasi (12 Slide) Lengkap dengan 10 Grafik & Parameter
    paper_html_str = generate_paper_bab1_to_5_html(
        sem_res=sim_live,
        sens_stress_res=sens_live,
        desc_df=desc_df,
        adf_df=adf_df,
        ols_res=ols_res,
        ardl_res=ardl_res,
        var_res=var_res,
        tornado_df=tornado_df,
        model_y=model_y,
        model_x=model_x,
        transform_mode=transform_mode,
        var_lag=var_lag,
        irf_horizon=irf_horizon,
        n_obs=len(work_df),
        data_source_label=data_source_label,
    )
    slides_html_str = generate_presentation_slides_html(
        sem_res=sim_live,
        sens_stress_res=sens_live,
        ols_res=ols_res,
        ardl_res=ardl_res,
        var_res=var_res,
        tornado_df=tornado_df,
        model_y=model_y,
        model_x=model_x,
        transform_mode=transform_mode,
        var_lag=var_lag,
        irf_horizon=irf_horizon,
        n_obs=len(work_df),
    )

    out_dir = os.path.join(base_dir, "hasil_analisis")
    os.makedirs(out_dir, exist_ok=True)
    paper_pdf_path = os.path.join(out_dir, "Laporan_Paper_Jurnal_BAB1_5_Modul17_Trilaksana.pdf")
    paper_html_path = os.path.join(out_dir, "Laporan_Paper_Jurnal_BAB1_5_Modul17_Trilaksana.html")
    slides_pdf_path = os.path.join(out_dir, "Presentasi_Eksekutif_Modul17_Trilaksana.pdf")
    slides_html_path = os.path.join(out_dir, "Presentasi_Eksekutif_Modul17_Trilaksana.html")

    # Deteksi perubahan state parameter agar file PDF otomatis diregenerasi setiap kali slider/tahun/CSV berubah
    current_report_state_hash = str((
        selected_target_year,
        tuple(sorted(live_custom_params.items())),
        model_y,
        tuple(model_x),
        transform_mode,
        var_lag,
        irf_horizon,
        data_source_label,
        len(work_df),
    ))

    with open(paper_html_path, "w", encoding="utf-8") as fh:
        fh.write(paper_html_str)
    with open(slides_html_path, "w", encoding="utf-8") as fs:
        fs.write(slides_html_str)

    if (
        not os.path.exists(paper_pdf_path)
        or not os.path.exists(slides_pdf_path)
        or st.session_state.get("last_report_state_hash") != current_report_state_hash
    ):
        convert_html_to_pdf_via_edge(paper_html_str, paper_pdf_path, paper_html_path)
        convert_html_to_pdf_via_edge(slides_html_str, slides_pdf_path, slides_html_path)
        st.session_state["last_report_state_hash"] = current_report_state_hash

    if st.button("🔄 Regenerasi & Perbarui File PDF Laporan (BAB I–V) & PDF Presentasi Sesuai Skenario Aktif", type="primary"):
        convert_html_to_pdf_via_edge(paper_html_str, paper_pdf_path, paper_html_path)
        convert_html_to_pdf_via_edge(slides_html_str, slides_pdf_path, slides_html_path)
        st.session_state["last_report_state_hash"] = current_report_state_hash
        st.success("✅ File PDF Naskah Ilmiah (BAB I–V + 10 Grafik + Parameter) dan PDF Slide Presentasi berhasil diperbarui!")

    paper_pdf_bytes = open(paper_pdf_path, "rb").read() if os.path.exists(paper_pdf_path) else b""
    slides_pdf_bytes = open(slides_pdf_path, "rb").read() if os.path.exists(slides_pdf_path) else b""
    excel_bytes = export_results_to_excel(desc_df, adf_df, ols_res, ardl_res, var_res)
    docx_bytes = export_results_to_docx(
        f"Naskah Ekonometrika Produksi Tambang, Hilirisasi Smelter & Proyeksi PDB ({AUTHOR_FULL})",
        desc_df,
        adf_df,
        ols_res,
        ardl_res,
        var_res,
    )

    st.markdown("#### 📥 Pusat Unduhan Dokumen Lengkap (Naskah BAB I–V + 10 Grafik Visual + Tabel Parameter & Slide Presentasi)")
    dl1, dl2, dl3, dl4, dl5, dl6 = st.columns(6)
    dl1.download_button(
        "📕 1. Naskah BAB I–V (.PDF)",
        data=paper_pdf_bytes,
        file_name="Laporan_Paper_Jurnal_BAB1_5_Modul17_Trilaksana.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    dl2.download_button(
        "🌐 2. Naskah BAB I–V (.HTML)",
        data=paper_html_str.encode("utf-8"),
        file_name="Laporan_Paper_Jurnal_BAB1_5_Modul17_Trilaksana.html",
        mime="text/html",
        use_container_width=True,
    )
    dl3.download_button(
        "📽️ 3. Slide Presentasi (.PDF)",
        data=slides_pdf_bytes,
        file_name="Presentasi_Eksekutif_Modul17_Trilaksana.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    dl4.download_button(
        "🖥️ 4. Slide Presentasi (.HTML)",
        data=slides_html_str.encode("utf-8"),
        file_name="Presentasi_Eksekutif_Modul17_Trilaksana.html",
        mime="text/html",
        use_container_width=True,
    )
    dl5.download_button(
        "📝 5. Naskah Word (.DOCX)",
        data=docx_bytes,
        file_name="Laporan_Paper_Ekonometrika_Modul17_Trilaksana.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
    )
    dl6.download_button(
        "📊 6. Tabel Data (.XLSX)",
        data=excel_bytes,
        file_name="Tabel_Ekonometrika_Modul17_Trilaksana.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    st.markdown("---")
    # TAMPILAN KESIMPULAN BAB V & 5 REKOMENDASI KEBIJAKAN STRATEGIS LANGSUNG DI LAYAR
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown(
            f"""
            <div class="exec-card" style="border-left: 4px solid #38bdf8;">
                <h4>🏆 BAB V (5.1) — 5 Kesimpulan Utama Penelitian</h4>
                <p style="font-size:0.9rem; line-height:1.58; color:#f1f5f9;">
                    <b>1. Posisi dalam Struktur Utuh PDB Nasional (KBLI A–U):</b> Dari 100% PDB Nasional ({selected_target_year}: <b>Rp {s_out['pdb_total_triliun']:,.1f} T</b>),
                    ekosistem Pertambangan Hulu Kat. B ({nat_sector_overview['share_hulu']:.2f}%), Hilirisasi Smelter Kat. C KBLI 24 ({nat_sector_overview['share_hilir']:.2f}%),
                    dan Efek Limpahan Spillover ({nat_sector_overview['share_spill']:.2f}%) menyumbang <b>{nat_sector_overview['total_minerba_ecosystem_pct']:.2f}%</b> PDB,
                    bersinergi dengan <b>{nat_sector_overview['non_minerba_pct']:.2f}%</b> sektor non-minerba.<br><br>
                    <b>2. Validasi Akurasi 2025 & Proyeksi 2026–2030:</b> Uji <i>backtesting</i> tahun 2025 membuktikan akurasi model sebesar
                    <b>{bt_2025['accuracy_pct']:.2f}% (MAPE {bt_2025['mape_pct']:.2f}%)</b>. Pada tahun <b>{selected_target_year}</b>, PDB Riil Indonesia
                    diproyeksikan tumbuh <b>{s_out['growth_pct']:.2f}%</b> mencapai <b>Rp {s_out['pdb_total_triliun']:,.1f} Triliun</b>
                    (dan meningkat hingga <b>Rp {sim_live['multiyear_scen'][2030]['pdb_total_triliun']:,.1f} Triliun</b> pada 2030).<br><br>
                    <b>3. Bukti Migrasi Nilai Tambah Kategori B ke Kategori C:</b> Hilirisasi mineral menggeser penciptaan nilai tambah dari
                    ekstraksi bijih mentah (<b>Kategori B: Rp {s_out['pdb_hulu_triliun']:,.1f} T</b>) menuju industri pengolahan logam dasar
                    smelter RKEF/HPAL (<b>Kategori C — KBLI 24: Rp {s_out['pdb_hilir_triliun']:,.1f} T</b>) dengan devisa ekspor olahan
                    <b>USD {s_out['ekspor_hilir_miliar_usd']:,.2f} Miliar</b>. Tanpa hilirisasi, PDB kehilangan sedikitnya <b>Rp {s_out['nilai_tambah_hilirisasi_triliun']*1.45:,.1f} T/tahun</b>.<br><br>
                    <b>4. Dinamika Ekuilibrium Jangka Panjang (ARDL-ECM):</b> Koefisien $\\text{{ECT}}_{{t-1}} = {ardl_res['ect_coef']:.4f}$
                    ($p = {ardl_res['ect_pval']:.4f}$) membuktikan setiap guncangan jangka pendek akan pulih menuju keseimbangan jangka panjang
                    dengan kecepatan <b>{abs(ardl_res['ect_coef'])*100:.2f}% per kuartal</b>.<br><br>
                    <b>5. Ketahanan Subsidi Energi & Krisis (Stress Test):</b> Kombinasi Mandatori Biodiesel B50, Bioetanol E10–E50, Konversi LPG ke LNG, Lifting Migas Blok Masela/IDD, dan royalti progresif Minerba mampu menutup beban subsidi BBM serta menahan guncangan harga komoditas global.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_k2:
        st.markdown(
            f"""
            <div class="exec-card" style="border-left: 4px solid #10b981;">
                <h4>🧭 BAB V (5.2) — 5 Rekomendasi Kebijakan Strategis & Korporasi</h4>
                <p style="font-size:0.9rem; line-height:1.58; color:#f1f5f9;">
                    <b>1. ⛏️ Tata Kelola Kuota RKAB 6 Mineral & Lifting Migas (Kementerian ESDM):</b> Terapkan <i>Smart Supply Management</i> pada RKAB
                    Batubara, Nikel, Tembaga, Emas, Bauksit, Timah, serta percepat <i>onstream</i> Blok Masela LNG, IDD & Rokan EOR menuju 1 Juta Bph.<br><br>
                    <b>2. ⛽ Kedaulatan Energi B50, Bioetanol E10–E90 & Konversi LPG ke LNG:</b> Hentikan impor solar via B50, konversi Pertalite ke
                    Bioetanol tebu/singkong/sorgum, dan substitusi impor LPG 3 Kg dengan LNG domestik, Jargas & DME batubara.<br><br>
                    <b>3. 🏭 Akselerasi Deep Downstreaming & 14 Terobosan Baru (Kemenperin & BKPM):</b> Eksekusi ekstraksi Logam Tanah Jarang (LTJ),
                    <i>Compute-for-Minerals</i> (AI Gigafactory), <i>Urban Mining</i> baterai EV, dan kuota serapan industri hilir domestik 35%.<br><br>
                    <b>4. 🏦 Bank Emas (Bullion Bank), Bursa IMEX & DHE SDA (Kemenkeu & BI):</b> Optimalkan PNBP Minerba (<b>Rp {s_out['pnbp_royalti_triliun']:,.1f} T</b>),
                    DMO Batubara PLN ($70/t), serta retensi devisa ekspor smelter (<b>${s_out['ekspor_hilir_miliar_usd']:,.2f} Miliar</b>) untuk menjaga Kurs Rupiah.<br><br>
                    <b>5. 💻 Adopsi Sistem Komputasi (Modul 17 — www.trilaksanamining.my.id):</b> Gunakan arsitektur <i>4-Block Simultaneous
                    Equations & ARDL-VECM</i> ini sebagai <i>Decision Support System</i> resmi perencanaan strategis BUMN Tambang (MIND ID) & Nasional.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    preview_mode = st.radio(
        "👁️ Pratinjau Dokumen Langsung di Layar:",
        options=[
            "📄 Pratinjau Naskah Penelitian Lengkap (BAB I s/d BAB V + 10 Grafik + Tabel Parameter)",
            "📽️ Pratinjau Slide Presentasi Eksekutif 12-Slide (Format 16:9 Landscape + Grafik)",
        ],
        horizontal=True,
    )
    if preview_mode.startswith("📄"):
        components.html(paper_html_str, height=760, scrolling=True)
    else:
        components.html(slides_html_str, height=680, scrolling=True)

# -----------------------------------------------------------------------------
# TAB 6: DATA, STATISTIK DESKRIPTIF & MATRIKS KORELASI
# -----------------------------------------------------------------------------
with tabs[5]:
    st.subheader("📈 Visualisasi Tren Time-Series Makroekonomi, Komoditas Tambang & PDB")
    col_plot1, col_plot2 = st.columns(2)
    with col_plot1:
        fig_y = px.line(
            work_df,
            x=time_col if time_col in work_df.columns else work_df.index,
            y=model_y,
            markers=True,
            title=f"Perkembangan Variabel Dependen: {model_y}",
            template="plotly_dark",
        )
        fig_y.update_traces(line_color="#38bdf8", line_width=2.5)
        st.plotly_chart(fig_y, use_container_width=True)

    with col_plot2:
        scatter_x = st.selectbox("Pilih Variabel X untuk Scatter Plot & Garis Regresi terhadap Y:", options=model_x)
        fig_sc = px.scatter(
            work_df,
            x=scatter_x,
            y=model_y,
            trendline="ols",
            title=f"Hubungan Linier {scatter_x} terhadap {model_y}",
            template="plotly_dark",
        )
        fig_sc.update_traces(marker=dict(size=9, color="#fbbf24"))
        st.plotly_chart(fig_sc, use_container_width=True)

    st.subheader("📋 Tabel Statistik Deskriptif Ekonometrika")
    st.dataframe(
        desc_df.style.format({
            "Mean (Rata-rata)": "{:,.4f}",
            "Median": "{:,.4f}",
            "Maximum": "{:,.4f}",
            "Minimum": "{:,.4f}",
            "Std. Dev.": "{:,.4f}",
            "Skewness": "{:,.4f}",
            "Kurtosis": "{:,.4f}",
            "Jarque-Bera": "{:,.4f}",
            "Prob. (JB)": "{:,.4f}",
        }),
        use_container_width=True,
    )

    col_c1, col_c2 = st.columns([1.2, 1])
    with col_c1:
        st.subheader("🔗 Heatmap Matriks Korelasi Pearson")
        fig_corr = px.imshow(
            corr_df.round(4),
            text_auto=True,
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Matriks Korelasi Antar Variabel",
            template="plotly_dark",
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    with col_c2:
        st.subheader("🗂️ Tabel Data Penelitian Lengkap (2010Q1–2026Q3)")
        st.dataframe(raw_df, use_container_width=True, height=380)

# -----------------------------------------------------------------------------
# TAB 7: UJI STASIONERITAS (UNIT ROOT TEST - ADF)
# -----------------------------------------------------------------------------
with tabs[6]:
    st.subheader("🔬 Hasil Uji Akar Unit (Augmented Dickey-Fuller / ADF Test)")
    st.markdown(
        "Uji stasioneritas dilakukan pada tingkat **Level $I(0)$**, **First Difference $I(1)$**, dan **Second Difference $I(2)$**. "
        "Variabel dinyatakan **Stasioner** apabila nilai **Prob. (p-value) < 0.05** atau nilai *ADF t-Statistic* lebih negatif dari Nilai Kritis MacKinnon 5%."
    )
    st.dataframe(
        adf_df.style.format({
            "ADF Level I(0)": "{:.4f}",
            "Prob. Level I(0)": "{:.4f}",
            "ADF 1st Diff I(1)": "{:.4f}",
            "Prob. 1st Diff I(1)": "{:.4f}",
            "ADF 2nd Diff I(2)": "{:.4f}",
            "Prob. 2nd Diff I(2)": "{:.4f}",
            "Kriteria 5% MacKinnon": "{:.4f}",
        }),
        use_container_width=True,
    )

    st.info(
        "💡 **Pedoman Pemilihan Model Ekonometrika Berdasarkan Uji ADF:**\n"
        "- Jika seluruh variabel stasioner pada **Level $I(0)$** ➔ Gunakan **Regresi OLS** atau **VAR pada Level**.\n"
        "- Jika variabel stasioner campuran antara **Level $I(0)$** dan **First Difference $I(1)$** ➔ Gunakan **Model ARDL / Bounds Testing**.\n"
        "- Jika seluruh variabel stasioner pada **First Difference $I(1)$** dan terkointegrasi ➔ Gunakan **Model ECM (Error Correction Model)** atau **VECM**."
    )

# -----------------------------------------------------------------------------
# TAB 8: REGRESI OLS, 4 UJI ASUMSI KLASIK, ARDL/ECM & VAR/VECM
# -----------------------------------------------------------------------------
with tabs[7]:
    st.subheader(f"📈 1. Hasil Estimasi Regresi Berganda (OLS) — Variabel Dependen: `{model_y}`")
    st.dataframe(
        ols_res["coef_table"].style.format({
            "Koefisien (Beta)": "{:,.6f}",
            "Std. Error": "{:,.6f}",
            "t-Statistic": "{:,.4f}",
            "Prob. (p-value)": "{:,.4f}",
            "CI 95% Bawah": "{:,.6f}",
            "CI 95% Atas": "{:,.6f}",
        }),
        use_container_width=True,
    )

    c_stat1, c_stat2 = st.columns(2)
    with c_stat1:
        st.markdown("#### 📊 Statistik Ringkasan Model (Goodness of Fit)")
        summary_stats_df = pd.DataFrame([
            {"Indikator Statistik": "R-Squared (R²)", "Nilai": f"{ols_res['r2']:.4f} ({ols_res['r2']*100:.2f}%)"},
            {"Indikator Statistik": "Adjusted R-Squared", "Nilai": f"{ols_res['adj_r2']:.4f} ({ols_res['adj_r2']*100:.2f}%)"},
            {"Indikator Statistik": "F-Statistic", "Nilai": f"{ols_res['f_stat']:.4f}"},
            {"Indikator Statistik": "Prob(F-Statistic)", "Nilai": f"{ols_res['f_pval']:.6f}"},
            {"Indikator Statistik": "S.E. of Regression", "Nilai": f"{ols_res['se_reg']:.4f}"},
            {"Indikator Statistik": "Akaike Info Criterion (AIC)", "Nilai": f"{ols_res['aic']:.4f}"},
            {"Indikator Statistik": "Schwarz Criterion (SIC/BIC)", "Nilai": f"{ols_res['sic']:.4f}"},
            {"Indikator Statistik": "Durbin-Watson Stat", "Nilai": f"{ols_res['dw_stat']:.4f}"},
        ])
        st.table(summary_stats_df)

    with c_stat2:
        st.markdown("#### ✅ Hasil 4 Uji Asumsi Klasik (Gauss-Markov Diagnostics)")
        diag_df = pd.DataFrame([
            {
                "Uji Asumsi Klasik": "1. Normalitas Residual (Jarque-Bera)",
                "Statistik Hitung": f"JB = {ols_res['jb_stat']:.4f}",
                "Prob. (p-value)": f"{ols_res['jb_pval']:.4f}",
                "Kesimpulan (Alpha 5%)": "✅ Berdistribusi Normal" if ols_res['jb_pval'] > 0.05 else "⚠️ Tidak Normal (p < 0.05)",
            },
            {
                "Uji Asumsi Klasik": "2. Heteroskedastisitas (Breusch-Pagan-Godfrey)",
                "Statistik Hitung": f"Obs*R² = {ols_res['bp_lm']:.4f}",
                "Prob. (p-value)": f"{ols_res['bp_pval']:.4f}",
                "Kesimpulan (Alpha 5%)": "✅ Homoskedastisitas (Lolos)" if ols_res['bp_pval'] > 0.05 else "⚠️ Ada Heteroskedastisitas",
            },
            {
                "Uji Asumsi Klasik": "3. Autokorelasi (Breusch-Godfrey Serial Correlation LM)",
                "Statistik Hitung": f"Obs*R² = {ols_res['bg_lm']:.4f}",
                "Prob. (p-value)": f"{ols_res['bg_pval']:.4f}",
                "Kesimpulan (Alpha 5%)": "✅ Bebas Autokorelasi (Lolos)" if ols_res['bg_pval'] > 0.05 else "⚠️ Ada Autokorelasi",
            },
        ])
        st.table(diag_df)
        st.markdown("**4. Uji Multikolinearitas (Variance Inflation Factor / VIF):**")
        st.dataframe(ols_res["vif_table"], use_container_width=True)

    st.markdown("---")
    st.subheader("⚖️ 2. Model ARDL & Error Correction Model (ECM - Jangka Pendek & Jangka Panjang)")
    c_ect1, c_ect2, c_ect3 = st.columns(3)
    c_ect1.metric(
        "Uji Kointegrasi Engle-Granger (ADF Residual)",
        f"{ardl_res['coint_adf_stat']:.4f}",
        f"Prob: {ardl_res['coint_p_value']:.4f}",
    )
    c_ect2.metric(
        "Koefisien Error Correction Term ECT(-1)",
        f"{ardl_res['ect_coef']:.4f}",
        "Valid (Negatif & Signifikan)" if (ardl_res['ect_coef'] < 0 and ardl_res['ect_pval'] < 0.05) else f"p-val: {ardl_res['ect_pval']:.4f}",
    )
    c_ect3.metric(
        "Kecepatan Penyesuaian (Speed of Adjustment)",
        f"{abs(ardl_res['ect_coef'])*100:.2f}% / kuartal",
        f"Pesaran Bounds 5%: I(0)={ardl_res['bounds_i0_5pct']}, I(1)={ardl_res['bounds_i1_5pct']}",
    )

    st.dataframe(
        ardl_res["short_run_ecm"]["coef_table"].style.format({
            "Koefisien (Beta)": "{:,.6f}",
            "Std. Error": "{:,.6f}",
            "t-Statistic": "{:,.4f}",
            "Prob. (p-value)": "{:,.4f}",
            "CI 95% Bawah": "{:,.6f}",
            "CI 95% Atas": "{:,.6f}",
        }),
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader(f"🌐 3. Model VAR/VECM: Kausalitas Granger, Impulse Response (IRF) & Variance Decomposition (FEVD)")
    st.dataframe(var_res["granger_df"], use_container_width=True)

    irf_target_df = var_res["irf_df"][
        (var_res["irf_df"]["Variabel Respon"] == model_y)
        & (var_res["irf_df"]["Variabel Guncangan (Shock)"] != model_y)
    ]
    col_irf, col_fevd = st.columns(2)
    with col_irf:
        fig_irf = px.line(
            irf_target_df,
            x="Periode",
            y="Nilai IRF",
            color="Variabel Guncangan (Shock)",
            markers=True,
            title=f"Impulse Response Function (IRF) pada {model_y}",
            template="plotly_dark",
        )
        fig_irf.add_hline(y=0, line_dash="dash", line_color="#94a3b8")
        st.plotly_chart(fig_irf, use_container_width=True)

    with col_fevd:
        fevd_target_df = var_res["fevd_df"][var_res["fevd_df"]["Variabel Target"] == model_y].drop(columns=["Variabel Target"])
        fevd_melt = fevd_target_df.melt(id_vars=["Periode"], var_name="Sumber Variabel", value_name="Kontribusi (%)")
        fig_fevd = px.bar(
            fevd_melt,
            x="Periode",
            y="Kontribusi (%)",
            color="Sumber Variabel",
            title=f"Variance Decomposition (FEVD) dari {model_y}",
            template="plotly_dark",
        )
        st.plotly_chart(fig_fevd, use_container_width=True)

    st.markdown("---")
    st.subheader("📝 4. Narasi Pembahasan Akademis Otomatis (Bab IV Hasil dan Pembahasan)")
    narrative_md = generate_academic_interpretation(ols_res, ardl_res)
    st.markdown(narrative_md)

# -----------------------------------------------------------------------------
# TAB 9: MENU KHUSUS PANDUAN LENGKAP, KAMUS TAMBANG-HILIRISASI & METODOLOGI
# -----------------------------------------------------------------------------
with tabs[8]:
    render_panduan_lengkap()
