# -*- coding: utf-8 -*-
"""
=============================================================================
GENERATOR NASKAH PENELITIAN EKONOMETRIKA (BAB I s/d BAB V), LAMPIRAN GRAFIK
& PARAMETER LENGKAP, EXECUTIVE SUMMARY, SERTA SLIDE PRESENTASI EKSEKUTIF
MODUL 17 — www.trilaksanamining.my.id
Peneliti Utama: Dr. Ir. Ahmad Raymond Trilaksana, S.T., M.Ak., IPM, ASEAN Eng.
=============================================================================
"""

import base64
import io
import os
import subprocess
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ekonometrika_engine import (
    compute_national_gdp_sector_breakdown,
    build_master_parameters_table,
    compute_asta_cita_8pct_roadmap,
    compute_energy_dmo_rkab_frontier_simulation,
)


AUTHOR_FULL = "Dr. Ir. Ahmad Raymond Trilaksana, S.T., M.Ak., IPM, ASEAN Eng."
MODULE_TITLE = "MODUL 17 — www.trilaksanamining.my.id | The Trilaksana Macro-Mining & Downstreaming Econometric Framework"
PAPER_TITLE_ID = (
    "Pemodelan Ekonometrika Persamaan Simultan dan ARDL-VECM atas Produksi Komoditas Pertambangan, "
    "Hilirisasi Industri Logam Dasar (Smelter), dan Transmisi Fiskal-Moneter terhadap Pertumbuhan PDB Indonesia (2010–2030)"
)
PAPER_TITLE_EN = (
    "Simultaneous Equations and ARDL-VECM Econometric Modeling of Mining Commodity Production, "
    "Base Metal Smelter Downstreaming, and Fiscal-Monetary Transmission on Indonesia's GDP Growth (2010–2030)"
)


def _fig_to_base64(fig) -> str:
    """Mengonversi objek Figure Matplotlib menjadi string data URI Base64 PNG beresolusi tinggi."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=145, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def generate_all_report_charts_base64(
    sem_res: dict,
    sens_stress_res: dict,
    ols_res: dict,
    var_res: dict,
    tornado_df: pd.DataFrame,
    nat_sector_res: dict,
) -> dict:
    """
    Membangkitkan 10 Grafik Visual Beresolusi Tinggi (Base64 PNG) secara dinamis
    sesuai hasil running simulasi saat ini untuk disematkan ke dalam PDF/HTML Report & Presentasi.
    """
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["axes.edgecolor"] = "#cbd5e1"
    plt.rcParams["axes.linewidth"] = 0.8

    charts = {}
    target_yr = sem_res.get("target_year", 2026)
    s_yr = sem_res["selected_year_scen"]
    b_yr = sem_res["selected_year_base"]
    bt = sem_res["backtest_2025"]
    proj_df = sem_res["projection_df"]

    # -------------------------------------------------------------------------
    # GAMBAR 1.1: Gambaran Umum 100% Sektor PDB Nasional (KBLI A-U) & Pengeluaran (C+I+G+NX)
    # -------------------------------------------------------------------------
    fig1, (ax1a, ax1b) = plt.subplots(1, 2, figsize=(12.5, 4.6), facecolor="#ffffff")
    sec_df = nat_sector_res["sector_df"].iloc[::-1]
    colors_1a = []
    for k in sec_df["Kategori KBLI / Sektor BPS"]:
        if "Kategori B" in k:
            colors_1a.append("#0284c7")
        elif "KBLI 24" in k:
            colors_1a.append("#059669")
        elif "Spillover" in k:
            colors_1a.append("#d97706")
        else:
            colors_1a.append("#64748b")

    short_labels_1a = [
        s.split("(")[0].strip()[:34] for s in sec_df["Kategori KBLI / Sektor BPS"]
    ]
    bars1 = ax1a.barh(short_labels_1a, sec_df["Porsi terhadap PDB Nasional (%)"], color=colors_1a, height=0.68)
    ax1a.set_title(f"A. Struktur PDB Nasional Menurut Lapangan Usaha ({target_yr})", fontsize=9.5, fontweight="bold", color="#0f172a")
    ax1a.set_xlabel("Porsi terhadap Total PDB Nasional (%)", fontsize=8.5)
    ax1a.tick_params(axis="both", labelsize=7.5)
    ax1a.grid(axis="x", linestyle="--", alpha=0.4)
    ax1a.set_xlim(0, max(sec_df["Porsi terhadap PDB Nasional (%)"]) * 1.22)
    for bar, val in zip(bars1, sec_df["Porsi terhadap PDB Nasional (%)"]):
        ax1a.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%", va="center", fontsize=7.2, fontweight="bold", color="#0f172a")

    exp_df = nat_sector_res["exp_df"].iloc[::-1]
    short_exp = [c.split("(")[0].strip()[:30] for c in exp_df["Komponen Pengeluaran PDB (Y = C + I + G + NX)"]]
    colors_1b = ["#1e3a8a", "#059669", "#0284c7", "#d97706", "#7c3aed"][: len(exp_df)]
    bars2 = ax1b.barh(short_exp, exp_df["Porsi PDB (%)"], color=colors_1b, height=0.58)
    ax1b.set_title(f"B. Struktur PDB Menurut Pengeluaran Y = C+I+G+NX ({target_yr})", fontsize=9.5, fontweight="bold", color="#0f172a")
    ax1b.set_xlabel("Porsi PDB Nasional (%)", fontsize=8.5)
    ax1b.tick_params(axis="both", labelsize=7.8)
    ax1b.grid(axis="x", linestyle="--", alpha=0.4)
    ax1b.set_xlim(0, max(exp_df["Porsi PDB (%)"]) * 1.22)
    for bar, val in zip(bars2, exp_df["Porsi PDB (%)"]):
        ax1b.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%", va="center", fontsize=7.5, fontweight="bold", color="#0f172a")

    fig1.tight_layout()
    charts["chart_1_national_sectors"] = _fig_to_base64(fig1)

    # -------------------------------------------------------------------------
    # GAMBAR 4.1: Dekomposisi 4-Blok Kontribusi Rantai Nilai Tambang & Hilirisasi
    # -------------------------------------------------------------------------
    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(12.2, 4.3), facecolor="#ffffff")
    blok_labels = [
        "Blok 1: Hulu Tambang\n(Kategori B)",
        "Blok 2: Hilirisasi Smelter\n(Kategori C - KBLI 24)",
        "Blok 3: Indirect Spillover\n(Listrik, Konstruksi, PNBP)",
    ]
    base_vals = [b_yr["pdb_hulu_triliun"], b_yr["pdb_hilir_triliun"], b_yr["spillover_triliun"]]
    scen_vals = [s_yr["pdb_hulu_triliun"], s_yr["pdb_hilir_triliun"], s_yr["spillover_triliun"]]
    x_pos = np.arange(len(blok_labels))
    w = 0.35
    b1 = ax2a.bar(x_pos - w / 2, base_vals, width=w, label=f"Baseline {target_yr}", color="#64748b")
    b2 = ax2a.bar(x_pos + w / 2, scen_vals, width=w, label=f"Simulasi Aktif {target_yr}", color=["#0284c7", "#059669", "#d97706"])
    ax2a.set_xticks(x_pos)
    ax2a.set_xticklabels(blok_labels, fontsize=8)
    ax2a.set_ylabel("Nilai Tambah PDB Riil (Triliun Rp)", fontsize=8.5)
    ax2a.set_title(f"A. Kontribusi Rantai Nilai Minerba-Hilirisasi ({target_yr})", fontsize=9.5, fontweight="bold")
    ax2a.legend(fontsize=8)
    ax2a.grid(axis="y", linestyle="--", alpha=0.4)
    for bar in b2:
        ax2a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8, f"Rp {bar.get_height():,.0f}T", ha="center", fontsize=7.5, fontweight="bold")

    scen_compare_labels = ["Skenario Waspada\n(Bearish)", f"Baseline\n({target_yr})", f"Simulasi Aktif\n({target_yr})", "Skenario Optimis\n(Akselerasi)"]
    scen_compare_growth = [
        sem_res["selected_year_pes"]["growth_pct"],
        b_yr["growth_pct"],
        s_yr["growth_pct"],
        sem_res["selected_year_opt"]["growth_pct"],
    ]
    b_sc = ax2b.bar(scen_compare_labels, scen_compare_growth, color=["#dc2626", "#475569", "#0284c7", "#059669"], width=0.52)
    ax2b.set_ylabel("Pertumbuhan PDB Nasional (% YoY)", fontsize=8.5)
    ax2b.set_title(f"B. Perbandingan Laju Pertumbuhan PDB Nasional ({target_yr})", fontsize=9.5, fontweight="bold")
    ax2b.set_ylim(0, max(scen_compare_growth) * 1.22)
    ax2b.grid(axis="y", linestyle="--", alpha=0.4)
    for bar, g in zip(b_sc, scen_compare_growth):
        ax2b.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{g:.2f}%", ha="center", fontsize=8, fontweight="bold")

    fig2.tight_layout()
    charts["chart_2_waterfall"] = _fig_to_base64(fig2)

    # -------------------------------------------------------------------------
    # GAMBAR 4.2: Proyeksi Multi-Tahun PDB Indonesia (2018–2030), Target Asta Cita 8% & Counterfactual
    # -------------------------------------------------------------------------
    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12.4, 4.3), facecolor="#ffffff")
    yrs = proj_df["Tahun"].astype(str).str.slice(0, 4).astype(int).tolist()
    if "PDB Target Asta Cita 8% (Triliun Rp)" in proj_df.columns:
        ax3a.plot(yrs, proj_df["PDB Target Asta Cita 8% (Triliun Rp)"], marker="D", linestyle="-.", linewidth=2.0, color="#d97706", label="Target Asta Cita 8% (2029)")
    ax3a.plot(yrs, proj_df["PDB Skenario Simulasi (Triliun Rp)"], marker="o", linewidth=2.2, color="#0284c7", label="PDB Skenario Simulasi Aktif")
    ax3a.plot(yrs, proj_df["PDB Baseline / Aktual (Triliun Rp)"], marker="s", linestyle="--", linewidth=1.6, color="#475569", label="PDB Baseline / Aktual Live")
    ax3a.plot(yrs, proj_df["PDB Tanpa Hilirisasi (Counterfactual)"], marker="^", linestyle=":", linewidth=1.8, color="#dc2626", label="Kontrafaktual Tanpa Hilirisasi")
    ax3a.axvline(x=2025, color="#0f766e", linestyle=":", alpha=0.7, label="Batas Aktual 2025")
    ax3a.set_title("A. Lintasan PDB Riil Nasional 2018–2030 (Triliun Rp)", fontsize=9.5, fontweight="bold")
    ax3a.set_xlabel("Tahun", fontsize=8.5)
    ax3a.set_ylabel("PDB Riil (Triliun Rp)", fontsize=8.5)
    ax3a.legend(fontsize=7.0, loc="upper left")
    ax3a.grid(True, linestyle="--", alpha=0.4)

    if "Pertumbuhan Target Asta Cita 8% (%)" in proj_df.columns:
        ax3b.plot(yrs, proj_df["Pertumbuhan Target Asta Cita 8% (%)"], marker="D", linestyle="-.", linewidth=2.1, color="#d97706", label="Target Asta Cita (2029: 8,00%)")
    ax3b.plot(yrs, proj_df["Pertumbuhan Simulasi (%)"], marker="o", linewidth=2.2, color="#059669", label="Pertumbuhan Simulasi Aktif (%)")
    ax3b.plot(yrs, proj_df["Pertumbuhan Baseline (%)"], marker="s", linestyle="--", linewidth=1.6, color="#64748b", label="Pertumbuhan Baseline Live (%)")
    ax3b.axhline(y=8.0, color="#d97706", linestyle=":", alpha=0.8, label="Sasaran Asta Cita 8,0%")
    for y_val, g_sim in zip(yrs, proj_df["Pertumbuhan Simulasi (%)"]):
        if y_val >= 2026:
            ax3b.annotate(f"{g_sim:.2f}%", (y_val, g_sim), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=6.8, fontweight="bold", color="#047857")
    ax3b.set_title("B. Lintasan Laju Pertumbuhan Ekonomi Nasional 2018–2030 (% YoY)", fontsize=9.5, fontweight="bold")
    ax3b.set_xlabel("Tahun", fontsize=8.5)
    ax3b.set_ylabel("Pertumbuhan PDB (% YoY)", fontsize=8.5)
    ax3b.legend(fontsize=7.0, loc="lower right")
    ax3b.grid(True, linestyle="--", alpha=0.4)

    fig3.tight_layout()
    charts["chart_3_multiyear"] = _fig_to_base64(fig3)

    # -------------------------------------------------------------------------
    # GAMBAR 4.3: Uji Validasi Backtesting Tahun 2025 (Kuartalan Aktual vs Model)
    # -------------------------------------------------------------------------
    fig4, ax4 = plt.subplots(figsize=(10.5, 3.8), facecolor="#ffffff")
    bt_q = bt["table_df"].iloc[:-1].copy()
    p_col = "Periode Uji" if "Periode Uji" in bt_q.columns else bt_q.columns[0]
    a_col = "PDB Aktual BPS (Rp T)" if "PDB Aktual BPS (Rp T)" in bt_q.columns else bt_q.columns[1]
    m_col = "PDB Proyeksi Model (Rp T)" if "PDB Proyeksi Model (Rp T)" in bt_q.columns else bt_q.columns[2]
    q_labels = bt_q[p_col].tolist()
    act_vals = bt_q[a_col].astype(float).tolist()
    prd_vals = bt_q[m_col].astype(float).tolist()
    xq = np.arange(len(q_labels))
    wq = 0.34
    ba = ax4.bar(xq - wq / 2, act_vals, width=wq, label="Realisasi Aktual BPS 2025 (Triliun Rp)", color="#1e3a8a")
    bp = ax4.bar(xq + wq / 2, prd_vals, width=wq, label="Prediksi Model Simultan 2025 (Triliun Rp)", color="#10b981")
    ax4.set_xticks(xq)
    ax4.set_xticklabels(q_labels, fontsize=8.5)
    ax4.set_ylabel("PDB Riil Kuartalan (Triliun Rp)", fontsize=8.5)
    ax4.set_title(
        f"Uji Validasi Backtesting Tahun 2025: Aktual BPS vs Prediksi Model (Akurasi = {bt['accuracy_pct']:.2f}% | MAPE = {bt['mape_pct']:.3f}%)",
        fontsize=9.5,
        fontweight="bold",
    )
    ax4.set_ylim(min(act_vals) * 0.92, max(act_vals) * 1.05)
    ax4.legend(fontsize=8)
    ax4.grid(axis="y", linestyle="--", alpha=0.4)
    for bar in ba:
        ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 12, f"{bar.get_height():,.1f}", ha="center", fontsize=7.5, fontweight="bold")
    for bar in bp:
        ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 12, f"{bar.get_height():,.1f}", ha="center", fontsize=7.5, color="#047857", fontweight="bold")

    fig4.tight_layout()
    charts["chart_4_backtest_2025"] = _fig_to_base64(fig4)

    # -------------------------------------------------------------------------
    # GAMBAR 4.4: 2-Way Sensitivity Heatmap Matrix (Volume Produksi X vs Harga Y)
    # -------------------------------------------------------------------------
    fig5, ax5 = plt.subplots(figsize=(9.8, 4.1), facecolor="#ffffff")
    mg_df = sens_stress_res["matrix_growth_df"].copy()
    row_labels = mg_df.iloc[:, 0].tolist()
    col_labels = mg_df.columns[1:].tolist()
    z_vals = mg_df.iloc[:, 1:].values.astype(float)
    im = ax5.imshow(z_vals, cmap="RdYlGn", aspect="auto")
    ax5.set_xticks(np.arange(len(col_labels)))
    ax5.set_yticks(np.arange(len(row_labels)))
    ax5.set_xticklabels(col_labels, fontsize=8)
    ax5.set_yticklabels(row_labels, fontsize=8)
    ax5.set_title(f"Matriks Sensitivitas 2-Arah Pertumbuhan PDB {target_yr} (% YoY): Produksi & Smelter (X) vs Harga Global (Y)", fontsize=9.2, fontweight="bold")
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            ax5.text(j, i, f"{z_vals[i, j]:.2f}%", ha="center", va="center", color="#0f172a", fontsize=8, fontweight="bold")
    cbar = fig5.colorbar(im, ax=ax5, shrink=0.88)
    cbar.set_label("Pertumbuhan PDB (%)", fontsize=8)
    fig5.tight_layout()
    charts["chart_5_heatmap_2way"] = _fig_to_base64(fig5)

    # -------------------------------------------------------------------------
    # GAMBAR 4.5: Spider Sensitivity Curve (7 Variabel Kunci -25% s/d +25%)
    # -------------------------------------------------------------------------
    fig6, ax6 = plt.subplots(figsize=(10.5, 4.2), facecolor="#ffffff")
    sp_df = sens_stress_res["spider_df"]
    var_col_sp = "Variabel Penggerak" if "Variabel Penggerak" in sp_df.columns else sp_df.columns[0]
    palette = ["#0284c7", "#059669", "#d97706", "#7c3aed", "#dc2626", "#0d9488", "#2563eb"]
    for idx, (var_name, grp) in enumerate(sp_df.groupby(var_col_sp)):
        ax6.plot(
            grp["Perubahan Parameter (%)"],
            grp["Proyeksi Pertumbuhan PDB (%)"],
            marker="o",
            linewidth=1.8,
            color=palette[idx % len(palette)],
            label=var_name,
        )
    ax6.axvline(x=0, color="#475569", linestyle="--", linewidth=1)
    ax6.set_title(f"Spider Sensitivity Curve: Kepekaan Pertumbuhan PDB {target_yr} terhadap Perubahan Parameter (-25% s/d +25%)", fontsize=9.2, fontweight="bold")
    ax6.set_xlabel("Perubahan Parameter Input dari Posisi Simulasi Aktif (%)", fontsize=8.5)
    ax6.set_ylabel("Proyeksi Pertumbuhan PDB (% YoY)", fontsize=8.5)
    ax6.legend(fontsize=7.2, ncol=2, loc="best")
    ax6.grid(True, linestyle="--", alpha=0.4)
    fig6.tight_layout()
    charts["chart_6_spider"] = _fig_to_base64(fig6)

    # -------------------------------------------------------------------------
    # GAMBAR 4.6: Macro-Mining Stress Test (6 Skenario Guncangan Ekstrem)
    # -------------------------------------------------------------------------
    fig7, ax7 = plt.subplots(figsize=(11.2, 4.2), facecolor="#ffffff")
    st_df = sens_stress_res["stress_df"].iloc[::-1].copy()
    growth_col = [c for c in st_df.columns if "Pertumbuhan PDB" in c][0]
    s_names = [s[:44] for s in st_df["Skenario Stress Test"]]
    s_gvals = st_df[growth_col].values.astype(float)
    bar_colors = ["#059669" if v >= 5.1 else ("#d97706" if v >= 4.7 else "#dc2626") for v in s_gvals]
    bars7 = ax7.barh(s_names, s_gvals, color=bar_colors, height=0.6)
    ax7.axvline(x=5.0, color="#1e3a8a", linestyle="--", linewidth=1.2, label="Ambang Pertumbuhan 5,0%")
    ax7.set_title(f"Hasil Macro-Mining Stress Test ({target_yr}): Pertumbuhan PDB pada 6 Skenario Krisis Ekstrem", fontsize=9.5, fontweight="bold")
    ax7.set_xlabel("Pertumbuhan PDB Nasional (% YoY)", fontsize=8.5)
    ax7.set_xlim(0, max(s_gvals) * 1.18)
    ax7.legend(fontsize=8)
    ax7.grid(axis="x", linestyle="--", alpha=0.4)
    for bar, v in zip(bars7, s_gvals):
        ax7.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height() / 2, f"{v:.2f}%", va="center", fontsize=8, fontweight="bold")
    fig7.tight_layout()
    charts["chart_7_stress_test"] = _fig_to_base64(fig7)

    # -------------------------------------------------------------------------
    # GAMBAR 4.7: Tornado Chart Elastisitas & Kontribusi Regresi Ekonometrika (OLS)
    # -------------------------------------------------------------------------
    fig8, ax8 = plt.subplots(figsize=(10.8, 4.1), facecolor="#ffffff")
    t_sub = tornado_df.head(10).iloc[::-1].copy()
    v_labels = [str(v)[:38] for v in t_sub["Variabel"]]
    score_col = "Bobot Pengaruh Terstandarisasi (Std. Beta)" if "Bobot Pengaruh Terstandarisasi (Std. Beta)" in t_sub.columns else t_sub.columns[1]
    v_scores = t_sub[score_col].values.astype(float)
    v_colors = ["#059669" if v >= 0 else "#dc2626" for v in v_scores]
    bars8 = ax8.barh(v_labels, v_scores, color=v_colors, height=0.62)
    ax8.axvline(x=0, color="#0f172a", linewidth=0.9)
    ax8.set_title("Tornado Chart: Bobot Pengaruh Terstandarisasi (Std. Beta) terhadap PDB (Model Regresi OLS)", fontsize=9.5, fontweight="bold")
    ax8.set_xlabel("Standardized Beta Coefficient", fontsize=8.5)
    ax8.grid(axis="x", linestyle="--", alpha=0.4)
    for bar, v in zip(bars8, v_scores):
        offset = 0.01 if v >= 0 else -0.04
        ax8.text(bar.get_width() + offset, bar.get_y() + bar.get_height() / 2, f"{v:+.3f}", va="center", fontsize=7.6, fontweight="bold")
    fig8.tight_layout()
    charts["chart_8_ols_tornado"] = _fig_to_base64(fig8)

    # -------------------------------------------------------------------------
    # GAMBAR 4.8: Kurva Impulse Response Function (IRF - 10 Kuartal)
    # -------------------------------------------------------------------------
    fig9, ax9 = plt.subplots(figsize=(10.5, 4.0), facecolor="#ffffff")
    irf_df = var_res["irf_df"].copy()
    if "Variabel Respon" in irf_df.columns and "Variabel Guncangan (Shock)" in irf_df.columns:
        target_resp = irf_df["Variabel Respon"].iloc[0]
        irf_sub = irf_df[(irf_df["Variabel Respon"] == target_resp) & (irf_df["Variabel Guncangan (Shock)"] != target_resp)]
        for idx, (shock_var, grp) in enumerate(irf_sub.groupby("Variabel Guncangan (Shock)")):
            ax9.plot(
                grp["Periode"],
                grp["Nilai IRF"],
                marker="o",
                linewidth=1.9,
                color=palette[idx % len(palette)],
                label=str(shock_var)[:36],
            )
    ax9.axhline(y=0, color="#0f172a", linestyle="--", linewidth=1)
    ax9.set_title("Kurva Impulse Response Function (IRF): Respons Dinamis PDB terhadap Guncangan 1 SD", fontsize=9.3, fontweight="bold")
    ax9.set_xlabel("Horizon Waktu (Kuartal ke-h Pasca Guncangan)", fontsize=8.5)
    ax9.set_ylabel("Respons Dinamis PDB (Std. Deviasi)", fontsize=8.5)
    ax9.legend(fontsize=7.2, ncol=2, loc="best")
    ax9.grid(True, linestyle="--", alpha=0.4)
    fig9.tight_layout()
    charts["chart_9_irf"] = _fig_to_base64(fig9)

    # -------------------------------------------------------------------------
    # GAMBAR 4.9: Forecast Error Variance Decomposition (FEVD - 10 Kuartal)
    # -------------------------------------------------------------------------
    fig10, ax10 = plt.subplots(figsize=(10.5, 4.0), facecolor="#ffffff")
    fevd_df = var_res["fevd_df"].copy()
    if "Variabel Target" in fevd_df.columns:
        t_fevd = fevd_df["Variabel Target"].iloc[0]
        fevd_df = fevd_df[fevd_df["Variabel Target"] == t_fevd].drop(columns=["Variabel Target"])
    p_fevd_col = "Periode" if "Periode" in fevd_df.columns else fevd_df.columns[0]
    horizons = fevd_df[p_fevd_col].values
    comp_cols = [c for c in fevd_df.columns if c != p_fevd_col]
    bottom_vals = np.zeros(len(horizons))
    for idx, col in enumerate(comp_cols):
        vals = fevd_df[col].values.astype(float)
        ax10.bar(horizons, vals, bottom=bottom_vals, label=str(col)[:34], color=palette[idx % len(palette)], width=0.6)
        bottom_vals += vals
    ax10.set_title("Forecast Error Variance Decomposition (FEVD): Dekomposisi Porsi Varians PDB (%)", fontsize=9.3, fontweight="bold")
    ax10.set_xlabel("Periode Kuartal ke-h", fontsize=8.5)
    ax10.set_ylabel("Porsi Kontribusi Varians (%)", fontsize=8.5)
    ax10.set_ylim(0, 105)
    ax10.legend(fontsize=7.0, ncol=2, loc="upper right")
    ax10.grid(axis="y", linestyle="--", alpha=0.4)
    fig10.tight_layout()
    charts["chart_10_fevd"] = _fig_to_base64(fig10)

    return charts


def _df_to_styled_html_table(df: pd.DataFrame, max_rows: int = 35) -> str:
    """Mengonversi DataFrame menjadi tabel HTML yang rapi dan siap cetak PDF."""
    if df is None or len(df) == 0:
        return "<p><i>Data tidak tersedia.</i></p>"
    sub = df.head(max_rows).copy()
    headers = "".join(f"<th>{col}</th>" for col in sub.columns)
    rows_html = []
    for _, row in sub.iterrows():
        cells = []
        for val in row:
            if isinstance(val, float):
                if abs(val) >= 100:
                    cells.append(f"<td style='text-align:right;'>{val:,.2f}</td>")
                else:
                    cells.append(f"<td style='text-align:right;'>{val:,.4f}</td>")
            else:
                cells.append(f"<td>{val}</td>")
        rows_html.append("<tr>" + "".join(cells) + "</tr>")
    return f"<table class='academic-table'><thead><tr>{headers}</tr></thead><tbody>{''.join(rows_html)}</tbody></table>"


def generate_paper_bab1_to_5_html(
    sem_res: dict,
    sens_stress_res: dict,
    desc_df: pd.DataFrame,
    adf_df: pd.DataFrame,
    ols_res: dict,
    ardl_res: dict,
    var_res: dict,
    tornado_df: pd.DataFrame,
    model_y: str = "PDB_Total_Riil_Triliun_Rp",
    model_x: list = None,
    transform_mode: str = "Log-Linear (ln) - Elastisitas (%)",
    var_lag: int = 2,
    irf_horizon: int = 10,
    n_obs: int = 67,
    data_source_label: str = "Dataset Komposit Resmi BPS, ESDM & Bank Indonesia (2010Q1–2026Q3)",
) -> str:
    """
    Menyusun dokumen HTML lengkap berformat Naskah Penelitian Ilmiah (BAB I s/d BAB V),
    dilengkapi Lembar Executive Summary, Gambaran Umum 100% Sektor PDB Nasional (KBLI A-U),
    Tabel Master Seluruh Parameter Input, serta 10 Grafik Visual Beresolusi Tinggi.
    """
    target_yr = sem_res.get("target_year", 2026)
    s_yr = sem_res["selected_year_scen"]
    b_yr = sem_res["selected_year_base"]
    o_yr = sem_res["selected_year_opt"]
    p_yr = sem_res["selected_year_pes"]
    bt = sem_res["backtest_2025"]
    proj_df = sem_res["projection_df"]

    ect_coef = ardl_res["ect_coef"]
    ect_pval = ardl_res["ect_pval"]
    r2_pct = ols_res["r2"] * 100.0
    adj_r2_pct = ols_res["adj_r2"] * 100.0
    f_stat = ols_res["f_stat"]

    # Bangkitkan Dekomposisi Utuh PDB Nasional (KBLI A-U & Pengeluaran Makro) + Tabel Master Parameter
    nat_sector_res = compute_national_gdp_sector_breakdown(sem_res)
    master_param_df = build_master_parameters_table(
        sem_res=sem_res,
        model_y=model_y,
        model_x=model_x,
        transform_mode=transform_mode,
        var_lag=var_lag,
        irf_horizon=irf_horizon,
        n_obs=n_obs,
    )

    # Bangkitkan 10 Grafik Visual Beresolusi Tinggi (Base64 PNG)
    charts = generate_all_report_charts_base64(
        sem_res=sem_res,
        sens_stress_res=sens_stress_res,
        ols_res=ols_res,
        var_res=var_res,
        tornado_df=tornado_df,
        nat_sector_res=nat_sector_res,
    )

    asta_roadmap = compute_asta_cita_8pct_roadmap(sem_res)
    sb_clean_cols = [c for c in asta_roadmap["sector_boost_df"].columns if "Asta Cita" not in c]
    asta_boost_html = _df_to_styled_html_table(asta_roadmap["sector_boost_df"][sb_clean_cols])

    energy_dmo_res = compute_energy_dmo_rkab_frontier_simulation(sem_res)
    breakeven_html = _df_to_styled_html_table(energy_dmo_res["breakeven_df"])
    rkab_rec_html = _df_to_styled_html_table(energy_dmo_res["rkab_recommendation_df"])
    levers_14_html = _df_to_styled_html_table(
        energy_dmo_res["policy_levers_df"].rename(columns={
            "Tambahan_PDB_Triliun": "Daya Ungkit PDB (+Rp T/Thn)",
            "Tambahan_Growth_Pct": "Kontribusi Pertumbuhan (+% YoY)",
            "Penghematan_Devisa_Miliar_USD": "Dampak Devisa (+$ Miliar/Thn)",
        }),
        max_rows=16,
    )

    # Tabel HTML untuk bagian-bagian penting
    nat_sector_html = _df_to_styled_html_table(nat_sector_res["sector_df"])
    nat_exp_html = _df_to_styled_html_table(nat_sector_res["exp_df"])
    master_param_html = _df_to_styled_html_table(master_param_df, max_rows=25)
    bt_html = _df_to_styled_html_table(bt["table_df"])
    proj_df_clean = proj_df.rename(columns={
        "PDB Target Asta Cita 8% (Triliun Rp)": "PDB Target Akselerasi 8% (Triliun Rp)",
        "Pertumbuhan Target Asta Cita 8% (%)": "Pertumbuhan Target Akselerasi 8% (%)",
    })
    proj_cols_pick = [
        c
        for c in [
            "Tahun",
            "PDB Baseline / Aktual (Triliun Rp)",
            "Pertumbuhan Baseline (%)",
            "PDB Skenario Simulasi (Triliun Rp)",
            "Pertumbuhan Simulasi (%)",
            "PDB Target Akselerasi 8% (Triliun Rp)",
            "Pertumbuhan Target Akselerasi 8% (%)",
            "PDB Tanpa Hilirisasi (Counterfactual)",
            "Kenaikan PDB dari Hilirisasi (%)",
        ]
        if c in proj_df_clean.columns
    ]
    proj_html = _df_to_styled_html_table(proj_df_clean[proj_cols_pick])
    matrix_g_html = _df_to_styled_html_table(sens_stress_res["matrix_growth_df"])
    matrix_p_html = _df_to_styled_html_table(sens_stress_res["matrix_pdb_df"])
    stress_html = _df_to_styled_html_table(sens_stress_res["stress_df"])
    rev_stress_html = _df_to_styled_html_table(sens_stress_res["reverse_stress_df"])
    desc_html = _df_to_styled_html_table(desc_df)
    adf_html = _df_to_styled_html_table(adf_df)
    ols_html = _df_to_styled_html_table(ols_res["coef_table"])
    vif_html = _df_to_styled_html_table(ols_res["vif_table"])
    ecm_html = _df_to_styled_html_table(ardl_res["short_run_ecm"]["coef_table"])
    granger_html = _df_to_styled_html_table(var_res["granger_df"], max_rows=16)

    now_str = datetime.now().strftime("%d %B %Y %H:%M WIB")

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Naskah Penelitian Ilmiah (BAB I - BAB V) & Executive Report - {AUTHOR_FULL}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Merriweather:ital,wght@0,400;0,700;1,400&display=swap');

  @page {{
    size: A4 portrait;
    margin: 13mm 14mm 13mm 14mm;
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    line-height: 1.5;
    font-size: 9.2pt;
    margin: 0;
    padding: 0;
  }}

  .cover-banner {{
    background: linear-gradient(135deg, #0a1128 0%, #0f172a 55%, #1e3a8a 100%);
    color: #f8fafc;
    padding: 18px 22px;
    border-radius: 10px;
    border-bottom: 4px solid #f59e0b;
    margin-bottom: 14px;
  }}

  .cover-badge {{
    display: inline-block;
    background: rgba(245, 158, 11, 0.2);
    border: 1px solid #f59e0b;
    color: #fde68a;
    font-size: 7.4pt;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 99px;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }}

  .cover-title {{
    font-size: 13pt;
    font-weight: 800;
    line-height: 1.3;
    color: #ffffff;
    margin: 4px 0 6px 0;
  }}

  .cover-subtitle {{
    font-size: 9pt;
    color: #cbd5e1;
    font-style: italic;
    margin-bottom: 10px;
  }}

  .author-box {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.08);
    padding: 8px 14px;
    border-radius: 6px;
    border-left: 3px solid #38bdf8;
    font-size: 8.3pt;
  }}

  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 9px;
    margin: 10px 0 14px 0;
  }}

  .kpi-card {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-top: 3.5px solid #1e3a8a;
    border-radius: 8px;
    padding: 8px 10px;
  }}

  .kpi-card .lbl {{
    font-size: 7.1pt;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
  }}

  .kpi-card .val {{
    font-size: 12pt;
    font-weight: 800;
    color: #0f172a;
    margin: 2px 0;
  }}

  .kpi-card .sub {{
    font-size: 7.3pt;
    color: #047857;
    font-weight: 600;
  }}

  .abstract-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #0f766e;
    border-radius: 8px;
    padding: 11px 15px;
    margin-bottom: 14px;
    font-size: 8.6pt;
    text-align: justify;
  }}

  h1.bab-title {{
    background: #0f172a;
    color: #f8fafc;
    font-size: 10.6pt;
    font-weight: 800;
    padding: 7px 14px;
    border-left: 5px solid #f59e0b;
    border-radius: 5px;
    margin-top: 16px;
    margin-bottom: 9px;
    letter-spacing: 0.4px;
    page-break-after: avoid;
  }}

  h2.sub-bab {{
    font-size: 9.7pt;
    font-weight: 800;
    color: #1e3a8a;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 3px;
    margin-top: 11px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  p {{
    margin: 0 0 7px 0;
    text-align: justify;
  }}

  .formula-box {{
    background: #f1f5f9;
    border: 1px dashed #64748b;
    border-radius: 6px;
    padding: 8px 12px;
    font-family: 'Merriweather', 'Times New Roman', serif;
    font-size: 8.5pt;
    margin: 7px 0 10px 0;
    page-break-inside: avoid;
  }}

  .figure-box {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 10px;
    margin: 9px 0 13px 0;
    text-align: center;
    page-break-inside: avoid;
  }}

  .figure-box img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
  }}

  .figure-caption {{
    font-size: 8pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 5px;
    text-align: center;
  }}

  table.academic-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0 12px 0;
    font-size: 7.2pt;
    page-break-inside: auto;
  }}

  table.academic-table tr {{
    page-break-inside: avoid;
    page-break-after: auto;
  }}

  table.academic-table th {{
    background: #1e293b;
    color: #ffffff;
    font-weight: 700;
    padding: 4.5px 6px;
    border: 1px solid #334155;
    text-align: left;
  }}

  table.academic-table td {{
    padding: 4px 6px;
    border: 1px solid #cbd5e1;
    color: #0f172a;
  }}

  table.academic-table tbody tr:nth-child(even) {{
    background: #f8fafc;
  }}

  .policy-box {{
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #d97706;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 7px;
    page-break-inside: avoid;
  }}

  .page-break {{
    page-break-before: always;
  }}

  .footer-note {{
    margin-top: 16px;
    padding-top: 7px;
    border-top: 1.5px solid #cbd5e1;
    font-size: 7.6pt;
    color: #475569;
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>

  <!-- ================= SAMPUL & HEADER NASKAH PENELITIAN ================= -->
  <div class="cover-banner">
    <div class="cover-badge">NASKAH PENELITIAN EKONOMETRIKA &amp; LAPORAN EKSEKUTIF • {MODULE_TITLE}</div>
    <div class="cover-title">{PAPER_TITLE_ID}</div>
    <div class="cover-subtitle">{PAPER_TITLE_EN}</div>
    <div class="author-box">
      <div>
        <b>Peneliti Utama (Corresponding Author):</b> {AUTHOR_FULL}<br>
        <b>Bidang Kepakaran:</b> Doktor Ilmu Ekonomi • Magister Akuntansi • Insinyur Teknik Pertambangan (IPM, ASEAN Eng.)
      </div>
      <div style="text-align:right;">
        <b>Ekosistem Digital:</b> www.trilaksanamining.my.id (Modul 17)<br>
        <b>Sumber Data Aktif:</b> {data_source_label}<br>
        <b>Waktu Komputasi:</b> {now_str}
      </div>
    </div>
  </div>

  <!-- ================= LEMBAR RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY) ================= -->
  <h2 class="sub-bab" style="margin-top:0;">RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY) — PROYEKSI PDB {target_yr} &amp; VALIDASI MODEL 2025</h2>
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="lbl">1. Uji Akurasi Model 2025</div>
      <div class="val">{bt['accuracy_pct']:.2f}% Akurat</div>
      <div class="sub">MAPE: {bt['mape_pct']:.2f}% (Aktual {bt['actual_growth_2025']:.2f}% vs Model {bt['pred_growth_2025']:.2f}%)</div>
    </div>
    <div class="kpi-card">
      <div class="lbl">2. Proyeksi PDB Nasional {target_yr}</div>
      <div class="val">Tumbuh {s_yr['growth_pct']:.2f}%</div>
      <div class="sub">PDB Riil: Rp {s_yr['pdb_total_triliun']:,.1f} Triliun</div>
    </div>
    <div class="kpi-card">
      <div class="lbl">3. Hulu (Kat. B) vs Hilir (Kat. C)</div>
      <div class="val">Rp {s_yr['pdb_hulu_triliun']:,.0f}T &amp; Rp {s_yr['pdb_hilir_triliun']:,.0f}T</div>
      <div class="sub">Porsi Rantai Minerba+Spillover: {s_yr['share_minerba_hilir_pct']:.2f}% PDB</div>
    </div>
    <div class="kpi-card">
      <div class="lbl">4. Ekspor Smelter &amp; PNBP {target_yr}</div>
      <div class="val">${s_yr['ekspor_hilir_miliar_usd']:,.1f} M / Rp {s_yr['pnbp_royalti_triliun']:,.0f} T</div>
      <div class="sub">R² Regresi: {r2_pct:.2f}% | ECT(-1): {ect_coef:.4f}</div>
    </div>
  </div>

  <div class="abstract-box">
    <b>ABSTRAK (BAHASA INDONESIA):</b><br>
    Penelitian ini mengembangkan kerangka ekonometrika terintegrasi berbasis <i>Simultaneous Equations Model</i> (SEM) 4-Blok,
    <i>Autoregressive Distributed Lag – Error Correction Model</i> (ARDL-ECM), dan <i>Vector Error Correction Model</i> (VECM)
    untuk menganalisis pengaruh simultan volume produksi komoditas pertambangan hulu (batubara, bijih nikel, dan emas),
    hilirisasi industri logam dasar melalui pabrik pemurnian (<i>smelter</i> RKEF dan HPAL), fluktuasi harga komoditas pasar global,
    serta transmisi fiskal (PNBP/Royalti) dan moneter (Kurs USD/IDR, Inflasi, BI-Rate) terhadap Produk Domestik Bruto (PDB) Riil Indonesia
    menggunakan data runtut waktu kuartalan periode 2010Q1–2026Q3 dan proyeksi jangka menengah hingga tahun 2030.
    Studi ini terlebih dahulu memetakan anatomi makroekonomi nasional secara utuh (100% seluruh sektor Lapangan Usaha KBLI Kategori A sampai U
    dan komponen pengeluaran agregat $Y = C + I + G + NX$), sebelum membedah secara spesifik migrasi nilai tambah dari
    Lapangan Usaha Kategori B (Pertambangan dan Penggalian Hulu) menuju Kategori C (Industri Pengolahan Logam Dasar — KBLI 24)
    yang menciptakan efek pengganda (<i>value-added multiplier</i>) sebesar 4,5 hingga 10,5 kali lipat.
    Uji validasi <i>backtesting</i> pada tahun 2025 menghasilkan tingkat akurasi prediksi sebesar <b>{bt['accuracy_pct']:.2f}%</b>
    (<i>Mean Absolute Percentage Error</i> / MAPE hanya <b>{bt['mape_pct']:.2f}%</b>). Pada tahun target {target_yr}, PDB Riil Indonesia
    diproyeksikan tumbuh sebesar <b>{s_yr['growth_pct']:.2f}%</b> mencapai <b>Rp {s_yr['pdb_total_triliun']:,.2f} Triliun</b>
    (rentang skenario waspada {p_yr['growth_pct']:.2f}% hingga skenario optimis {o_yr['growth_pct']:.2f}%), dengan kontribusi PDB Hulu
    Pertambangan (Kategori B) sebesar Rp {s_yr['pdb_hulu_triliun']:,.1f} Triliun, PDB Hilirisasi Smelter (Kategori C) sebesar
    Rp {s_yr['pdb_hilir_triliun']:,.1f} Triliun, devisa ekspor olahan mineral sebesar USD {s_yr['ekspor_hilir_miliar_usd']:,.2f} Miliar,
    dan penerimaan PNBP Minerba sebesar Rp {s_yr['pnbp_royalti_triliun']:,.1f} Triliun.<br><br>
    <b>ABSTRACT (ENGLISH):</b><br>
    <i>This study develops an integrated 4-Block Simultaneous Equations Model (SEM) combined with Autoregressive Distributed Lag –
    Error Correction Model (ARDL-ECM) and Vector Error Correction Model (VECM) to evaluate the dynamic interplay of upstream mining production
    quotas (coal, nickel ore, and gold), downstream base metal smelting (RKEF and HPAL facilities), global commodity price volatility,
    and fiscal-monetary transmission channels on Indonesia's Real GDP from 2010Q1 to 2026Q3 with multi-year projections through 2030.
    Mapping the entire 100% national GDP structure across all 17 ISIC/KBLI sectors (Categories A–U) and expenditure components (C+I+G+NX)
    before zooming into the mineral value chain, empirical results confirm a structural migration of resource value-added from BPS Category B
    (Upstream Mining and Quarrying) to Category C (Base Metal Manufacturing — KBLI 24), generating a 4.5x–10.5x value-added multiplier.
    Model validation against 2025 actual BPS realization yields a forecasting accuracy of <b>{bt['accuracy_pct']:.2f}%</b> (MAPE = <b>{bt['mape_pct']:.2f}%</b>).</i><br>
    <b>Kata Kunci / Keywords:</b> Struktur PDB Nasional KBLI A–U, Hilirisasi Mineral, Smelter RKEF-HPAL, Kuota RKAB, Persamaan Simultan, ARDL-VECM.<br>
    <b>JEL Classification:</b> Q32, Q38, C32, E27, O13, L72.
  </div>

  <!-- ================= BAB I: PENDAHULUAN ================= -->
  <h1 class="bab-title">BAB I — PENDAHULUAN (INTRODUCTION)</h1>

  <h2 class="sub-bab">1.1 Latar Belakang Masalah: Paradoks Sumber Daya Alam vs Transformasi Hilirisasi</h2>
  <p>
    Indonesia merupakan salah satu negara dengan cadangan dan volume produksi komoditas mineral dan batubara (minerba) terbesar di dunia,
    mencakup cadangan nikel urutan pertama dunia, produksi batubara termal eksportir utama global, serta cadangan porfiri tembaga-emas
    dan bauksit kelas dunia. Dalam literatur ekonomi pembangunan klasik, ketergantungan berlebih terhadap ekspor komoditas primer mentah
    sering kali menjebak negara berkembang ke dalam fenomena kutukan sumber daya alam (<i>resource curse</i>) dan penyakit Belanda
    (<i>Dutch disease</i>), di mana perekonomian domestik menjadi sangat rentan terhadap siklus naik-turunnya harga komoditas global
    (Sachs &amp; Warner, 2001; Auty, 2002).
  </p>
  <p>
    Sejak implementasi kebijakan larangan ekspor bijih nikel mentah dan kewajiban pemurnian di dalam negeri berdasarkan Undang-Undang
    Nomor 3 Tahun 2020 tentang Pertambangan Mineral dan Batubara, struktur industri ekstraktif Indonesia mengalami pergeseran fundamental.
    Jutaan metrik ton bijih nikel basah (<i>Wet Metric Ton</i> / WMT) yang sebelumnya diekspor dengan nilai tambah rendah kini diserap
    oleh pabrik peleburan pirometalurgi berbasis <i>Rotary Kiln-Electric Furnace</i> (RKEF) untuk menghasilkan <i>Nickel Pig Iron</i> (NPI),
    <i>Ferronickel</i> (FeNi), dan baja tahan karat (<i>stainless steel</i>), serta pabrik hidrometalurgi berbasis <i>High Pressure Acid Leach</i>
    (HPAL) yang mengolah bijih nikel kadar rendah (<i>limonite</i>) menjadi <i>Mixed Hydroxide Precipitate</i> (MHP) dan nikel sulfat sebagai
    bahan baku utama baterai kendaraan listrik (<i>Electric Vehicle</i> / EV).
  </p>

  <h2 class="sub-bab">1.2 Anatomi Utuh Struktur PDB Nasional Indonesia (General-to-Specific: Seluruh Sektor KBLI A–U &amp; Pengeluaran Makro)</h2>
  <p>
    Agar analisis ekonometrika tidak bersifat parsial, penelitian ini terlebih dahulu memetakan <b>gambaran umum keseluruhan faktor pembentuk
    PDB Nasional Indonesia (100% Total PDB Riil sebesar Rp {s_yr['pdb_total_triliun']:,.2f} Triliun pada tahun {target_yr})</b>, baik dari
    <b>Pendekatan Lapangan Usaha (17 Kategori KBLI A s/d U)</b> maupun <b>Pendekatan Pengeluaran ($Y = C + I + G + (X - M)$)</b>. Sebagaimana
    divisualisasikan pada <b>Gambar 1.1</b> serta dirinci pada <b>Tabel 1.1a</b> dan <b>Tabel 1.1b</b>, perekonomian Indonesia ditopang oleh
    seluruh sektor secara simultan — mulai dari Industri Pengolahan Non-Logam (makanan-minuman, kimia, tekstil, otomotif), Perdagangan Besar
    dan Eceran, Pertanian-Kehutanan-Perikanan, Konstruksi, Informasi dan Komunikasi, hingga Jasa Keuangan.
  </p>
  <p>
    Di dalam arsitektur makroekonomi nasional tersebut, rantai nilai <b>Pertambangan dan Hilirisasi Mineral</b> berperan sebagai <b>mesin
    penggerak struktural (<i>structural growth driver</i>)</b> melalui tiga kanal pencatatan BPS yang saling terhubung:
    (1) <b>Kategori B (Pertambangan &amp; Penggalian Hulu)</b> sebesar <b>Rp {s_yr['pdb_hulu_triliun']:,.2f} Triliun ({nat_sector_res['share_hulu']:.2f}%)</b>;
    (2) <b>Kategori C Subsektor Industri Logam Dasar (KBLI 24 — Hilirisasi Smelter)</b> sebesar <b>Rp {s_yr['pdb_hilir_triliun']:,.2f} Triliun ({nat_sector_res['share_hilir']:.2f}%)</b>;
    serta (3) <b>Efek Limpahan Tidak Langsung (<i>Indirect Spillover</i>)</b> pada kawasan industri, ketenagalistrikan, logistik, dan belanja fiskal PNBP
    sebesar <b>Rp {s_yr['spillover_triliun']:,.2f} Triliun ({nat_sector_res['share_spill']:.2f}%)</b>. Secara agregat, ekosistem hulu-hilir minerba dan
    <i>spillover</i>-nya menyumbang <b>{nat_sector_res['total_minerba_ecosystem_pct']:.2f}%</b> dari total PDB Nasional, sementara
    <b>{nat_sector_res['non_minerba_pct']:.2f}%</b> sisanya digerakkan oleh sektor-sektor domestik non-minerba yang dipengaruhi oleh suku bunga BI-Rate,
    inflasi, nilai tukar Rupiah, dan daya beli rumah tangga.
  </p>

  <div class="figure-box">
    <img src="{charts['chart_1_national_sectors']}" alt="Struktur Utuh PDB Nasional Indonesia KBLI A-U dan Pengeluaran Makro">
    <div class="figure-caption">
      Gambar 1.1 — Peta Utuh Struktur PDB Nasional Indonesia Tahun {target_yr}: (A) Dekomposisi 100% Lapangan Usaha BPS (Kategori A s/d U)
      dan (B) Dekomposisi Komponen Pengeluaran Makroekonomi (Y = C + I + G + NX).
    </div>
  </div>

  <p><b>Tabel 1.1a — Dekomposisi Utuh PDB Nasional Indonesia Menurut Lapangan Usaha (Seluruh Sektor KBLI A s/d U — Tahun {target_yr}):</b></p>
  {nat_sector_html}

  <p><b>Tabel 1.1b — Dekomposisi PDB Nasional Indonesia Menurut Komponen Pengeluaran Makroekonomi ($Y = C + I + G + NX$ — Tahun {target_yr}):</b></p>
  {nat_exp_html}

  <h2 class="sub-bab">1.3 Rumusan Masalah dan Kebaruan Penelitian (Research Novelty)</h2>
  <p>
    Studi ini menjawab empat pertanyaan riset utama: (1) Bagaimana posisi dan daya ungkit sektor pertambangan hulu (Kategori B) serta hilirisasi
    industri logam dasar (Kategori C) di tengah struktur utuh perekonomian nasional (KBLI A–U)? (2) Seberapa besar kontribusi kontrafaktual
    hilirisasi smelter dibandingkan skenario tanpa hilirisasi? (3) Seberapa akurat model persamaan simultan 4-blok dalam memprediksi realisasi
    aktual PDB tahun 2025 serta bagaimana peta proyeksi PDB Indonesia pada periode 2026–2030? dan (4) Bagaimana ketahanan makroekonomi nasional
    ketika diuji terhadap matriks sensitivitas dua arah dan enam skenario guncangan krisis ekstrem (<i>macro-mining stress test</i>)?
  </p>

  <!-- ================= BAB II: TINJAUAN PUSTAKA ================= -->
  <h1 class="bab-title">BAB II — TINJAUAN PUSTAKA DAN KERANGKA TEORITIS (LITERATURE REVIEW)</h1>

  <h2 class="sub-bab">2.1 Teori Pertumbuhan Berbasis Sumber Daya dan Industrial Downstreaming Multiplier</h2>
  <p>
    Berdasarkan teori keterkaitan produksi Hirschman (<i>forward and backward linkages</i>) dan fungsi produksi agregat neoklasik yang
    diperluas dengan modal sumber daya alam, pemrosesan mineral di dalam negeri menciptakan pengganda nilai tambah melalui tiga kanal utama:
    (a) peningkatan rasio harga jual produk olahan per ton kandungan logam (4,5x–7,5x pada jalur RKEF dan 6,0x–11,5x pada jalur HPAL),
    (b) pembentukan modal tetap bruto (PMTB) dari belanja modal (<i>Capital Expenditure</i> / CapEx) pembangunan smelter dan pembangkit listrik,
    serta (c) retensi Surplus Devisa Hasil Ekspor Sumber Daya Alam (DHE SDA) yang memperkuat stabilitas nilai tukar domestik.
  </p>

  <h2 class="sub-bab">2.2 Ekonomi Teknik Komoditas Pertambangan Strategis (Batubara, Nikel, dan Emas-Tembaga)</h2>
  <p>
    Dari perspektif teknik pertambangan, pasokan hulu dikendalikan melalui instrumen regulasi <b>Rencana Kerja dan Anggaran Biaya (RKAB)</b>
    tahunan dan tiga tahunan oleh Kementerian ESDM. Untuk batubara, keseimbangan antara kuota produksi nasional (~750–800 juta ton/tahun),
    kewajiban pasokan dalam negeri (<i>Domestic Market Obligation</i> / DMO untuk PLN dan industri), serta Harga Batubara Acuan (HBA)
    menentukan besaran devisa ekspor dan royalti progresif. Untuk nikel, tata kelola cadangan bijih <i>saprolite</i> dan <i>limonite</i>
    harus disinkronkan dengan kapasitas terpasang tungku RKEF dan autoklaf HPAL agar umur tambang (<i>Life of Mine</i> / LOM) terjaga.
  </p>

  <h2 class="sub-bab">2.3 Hipotesis Penelitian</h2>
  <p>
    Berdasarkan landasan teori di atas, dirumuskan hipotesis penelitian sebagai berikut:
    <b>H1:</b> Volume produksi komoditas pertambangan (batubara, bijih nikel, emas) dan harga komoditas global berpengaruh positif dan
    signifikan terhadap PDB Hulu Pertambangan (Kategori B) dan PNBP Minerba;
    <b>H2:</b> Investasi CapEx smelter dan pasokan bijih nikel berpengaruh positif signifikan dengan elastisitas tinggi terhadap PDB
    Hilirisasi Industri Logam Dasar (Kategori C) dan ekspor olahan mineral;
    <b>H3:</b> Terdapat hubungan kointegrasi jangka panjang yang stabil ($\text{{ECT}}_{{t-1}} &lt; 0$ dan signifikan) antara kinerja rantai
    nilai pertambangan-hilirisasi dan variabel makroekonomi terhadap pertumbuhan PDB Riil Indonesia.
  </p>

  <!-- ================= BAB III: METODOLOGI PENELITIAN & PARAMETER SIMULASI ================= -->
  <div class="page-break"></div>
  <h1 class="bab-title">BAB III — METODOLOGI PENELITIAN &amp; KONFIGURASI PARAMETER SIMULASI</h1>

  <h2 class="sub-bab">3.1 Cakupan Data dan Spesifikasi Ekonometrika Runtut Waktu</h2>
  <p>
    Penelitian ini menggunakan data runtut waktu kuartalan (<i>quarterly time-series</i>) selama periode <b>2010Q1 hingga 2026Q3</b>
    ($N = {n_obs}$ observasi kuartalan; Sumber Data Aktif: <b>{data_source_label}</b>). Prosedur estimasi dilakukan melalui lima tahapan
    berjenjang: (1) Uji Stasioneritas Akar Unit <i>Augmented Dickey-Fuller</i> (ADF) pada tingkat Level $I(0)$, <i>First Difference</i> $I(1)$,
    dan <i>Second Difference</i> $I(2)$; (2) Estimasi Regresi Berganda <i>Ordinary Least Squares</i> (OLS) beserta 4 Uji Diagnostik Asumsi
    Klasik Gauss-Markov; (3) Estimasi <i>Autoregressive Distributed Lag</i> (ARDL) dan <i>Error Correction Model</i> (ECM); serta
    (4) Analisis <i>Vector Autoregression / Vector Error Correction Model</i> (VAR/VECM) yang mencakup Uji Kausalitas Granger,
    <i>Impulse Response Function</i> (IRF), dan <i>Forecast Error Variance Decomposition</i> (FEVD).
  </p>

  <h2 class="sub-bab">3.2 Formulasi Sistem Persamaan Simultan 4-Blok (The Trilaksana Macro-Mining Framework)</h2>
  <div class="formula-box">
    <b>Blok 1 (Persamaan Struktur PDB Hulu Pertambangan — Kategori B):</b><br>
    PDB_Hulu(t) = α₀ + α₁·Q_Batubara(t) + α₂·Q_BijihNikel(t) + α₃·Q_Emas(t) + α₄·P_HBA(t) + α₅·P_Emas(t) + α₆·Kurs(t) + ε₁(t)<br><br>
    <b>Blok 2 (Persamaan Struktur Hilirisasi Smelter Logam Dasar — Kategori C &amp; Ekspor Olahan):</b><br>
    Ekspor_Hilir(t) = β₀ + β₁·Q_BijihNikel(t) + β₂·CapEx_Smelter(t) + β₃·P_NikelLME(t) + ε₂(t)<br>
    PDB_Hilir_KatC(t) = γ₀ + γ₁·Q_BijihNikel(t) + γ₂·CapEx_Smelter(t) + γ₃·Ekspor_Hilir(t) + γ₄·P_NikelLME(t) + ε₃(t)<br><br>
    <b>Blok 3 (Persamaan Transmisi Fiskal PNBP/Royalti Minerba &amp; Efek Pengganda Spillover):</b><br>
    PNBP_Minerba(t) = τ_Royalti · [ ω₀ + ω₁(Q_Coal·P_HBA) + ω₂(Q_Nikel·P_LME) + ω₃(Q_Emas·P_Emas) + ω₄·Ekspor_Hilir(t) ]<br>
    Spillover_Minerba(t) = κ₁·PDB_Hilir_KatC(t) + κ₂·PNBP_Minerba(t)<br><br>
    <b>Blok 4 (Identitas PDB Riil Nasional &amp; Transmisi Makro-Moneter Multi-Tahun 2025–2030):</b><br>
    PDB_Nasional(t) = PDB_Hulu_KatB(t) + PDB_Hilir_KatC(t) + Spillover_Minerba(t) + PDB_NonMinerba(Kurs, BI_Rate, Inflasi, P_MinyakICP)
  </div>

  <h2 class="sub-bab">3.3 Lampiran Parameter Input Simulasi &amp; Konfigurasi Ekonometrika Aktif</h2>
  <p>
    Tabel 3.1 di bawah ini mendokumentasikan secara lengkap seluruh parameter input kebijakan, kuota produksi fisik ($X$), asumsi harga
    komoditas global ($Y$), parameter fiskal-moneter, serta konfigurasi model ekonometrika yang sedang aktif digunakan dalam simulasi ini:
  </p>
  <p><b>Tabel 3.1 — Daftar Lengkap Parameter Input Simulasi &amp; Konfigurasi Model Ekonometrika (Tahun Target {target_yr}):</b></p>
  {master_param_html}

  <!-- ================= BAB IV: HASIL PENELITIAN & PEMBAHASAN ================= -->
  <div class="page-break"></div>
  <h1 class="bab-title">BAB IV — HASIL PENELITIAN, VISUALISASI SIMULASI, SENSITIVITY &amp; STRESS TEST</h1>

  <h2 class="sub-bab">4.1 Dekomposisi 4-Blok Rantai Nilai Pertambangan-Hilirisasi &amp; Uji Validasi Backtesting 2025</h2>
  <p>
    Sebagaimana ditunjukkan pada <b>Gambar 4.1</b>, model persamaan simultan memisahkan kontribusi rantai nilai ke dalam Blok 1 (Hulu Kategori B
    sebesar <b>Rp {s_yr['pdb_hulu_triliun']:,.2f} Triliun</b>), Blok 2 (Hilirisasi Smelter Kategori C sebesar <b>Rp {s_yr['pdb_hilir_triliun']:,.2f} Triliun</b>),
    dan Blok 3 (<i>Indirect Spillover</i> sebesar <b>Rp {s_yr['spillover_triliun']:,.2f} Triliun</b>). Selanjutnya, pengujian validasi
    <i>backtesting</i> pada empat kuartal tahun 2025 (<b>Gambar 4.3</b> dan <b>Tabel 4.1</b>) membuktikan bahwa total realisasi aktual PDB Riil
    Indonesia tahun 2025 tercatat sebesar <b>Rp {bt['actual_pdb_2025']:,.2f} Triliun</b> (tumbuh <b>{bt['actual_growth_2025']:.2f}%</b>),
    sedangkan hasil prediksi sistem persamaan simultan adalah sebesar <b>Rp {bt['pred_pdb_2025']:,.2f} Triliun</b>
    (tumbuh <b>{bt['pred_growth_2025']:.2f}%</b>), menghasilkan tingkat akurasi <b>{bt['accuracy_pct']:.2f}%</b> (MAPE = <b>{bt['mape_pct']:.3f}%</b>).
  </p>

  <div class="figure-box">
    <img src="{charts['chart_2_waterfall']}" alt="Dekomposisi 4-Blok Kontribusi Tambang dan Hilirisasi">
    <div class="figure-caption">
      Gambar 4.1 — (A) Perbandingan Nilai Tambah Blok 1 (Hulu Kat. B), Blok 2 (Hilirisasi Kat. C), dan Blok 3 (Spillover)
      serta (B) Perbandingan Pertumbuhan PDB Nasional Antar-Skenario pada Tahun {target_yr}.
    </div>
  </div>

  <div class="figure-box">
    <img src="{charts['chart_4_backtest_2025']}" alt="Uji Validasi Backtesting Tahun 2025">
    <div class="figure-caption">
      Gambar 4.2 — Uji Validasi Backtesting Kuartalan Tahun 2025 (2025Q1–2025Q4): Realisasi Aktual BPS vs Prediksi Model Simultan
      (Tingkat Akurasi = {bt['accuracy_pct']:.2f}%, MAPE = {bt['mape_pct']:.3f}%).
    </div>
  </div>

  <p><b>Tabel 4.1 — Rincian Kuartalan Uji Validasi Backtesting Tahun 2025 (Aktual BPS vs Prediksi Model):</b></p>
  {bt_html}

  <h2 class="sub-bab">4.2 Proyeksi Multi-Tahun PDB Indonesia (2018–2030) &amp; Analisis Kontrafaktual Hilirisasi</h2>
  <p>
    <b>Gambar 4.3</b> dan <b>Tabel 4.2</b> merangkum lintasan historis dan proyeksi jangka menengah PDB Riil Indonesia hingga tahun 2030
    beserta simulasi kontrafaktual (<i>counterfactual analysis</i>) seandainya Indonesia tidak menjalankan kebijakan hilirisasi smelter.
    Tanpa hilirisasi industri logam dasar (Kategori C), PDB Riil Indonesia pada tahun {target_yr} akan kehilangan nilai tambah bersih dan efek
    pengganda sebesar lebih dari <b>Rp {s_yr['nilai_tambah_hilirisasi_triliun']*1.45:,.1f} Triliun</b>.
  </p>

  <div class="figure-box">
    <img src="{charts['chart_3_multiyear']}" alt="Lintasan Proyeksi Multi-Tahun PDB Indonesia 2018-2030">
    <div class="figure-caption">
      Gambar 4.3 — Lintasan Historis dan Proyeksi Multi-Tahun PDB Riil Indonesia (2018–2030): Skenario Simulasi Aktif, Baseline,
      dan Kontrafaktual Tanpa Hilirisasi Smelter.
    </div>
  </div>

  <p><b>Tabel 4.2a — Rekapitulasi Lintasan PDB Riil Nasional Multi-Tahun, Target Akselerasi 8% &amp; Persentase Kenaikan Hilirisasi (2018–2030):</b></p>
  {proj_html}

  <p>
    Selanjutnya, <b>Tabel 4.2b</b> memetakan hasil simulasi <b>Peta Komando Sektor Prioritas yang Harus Digenjot (<i>Sectoral Acceleration &amp; Gap Analysis</i>)</b>
    agar sasaran pertumbuhan ekonomi <b>8,00% pada tahun 2029 (RPJMN 2025–2029)</b> dapat tercapai, yaitu mengejar selisih nilai tambah
    (<i>GDP Gap</i>) sebesar <b>+Rp {asta_roadmap['gap_total_2029']:,.1f} Triliun</b> di atas proyeksi <i>Baseline</i> data pasar berjalan:
  </p>
  <p><b>Tabel 4.2b — Peta Komando 6 Kelompok Sektor yang Harus Digenjot Menuju Pertumbuhan Ekonomi 8,00% Tahun 2029 (RPJMN):</b></p>
  {asta_boost_html}

  <p>
    Di tingkat mikro-fiskal dan kedaulatan energi, <b>Tabel 4.2c</b> menyajikan analisis titik impas (<i>break-even</i>) ketahanan subsidi BBM (Pertalite &amp; Solar)
    serta LPG 3 Kg terhadap kenaikan harga minyak mentah dunia (ICP) yang diimbangi oleh mandatori <b>Biodiesel B50</b> (bebas impor solar),
    konversi <b>Bioetanol E10–E90</b>, konversi <b>LPG ke LNG domestik/Jargas/DME</b>, peningkatan <b>Lifting Migas (Blok Masela LNG, IDD, Rokan EOR)</b>,
    dan <i>cross-subsidy</i> penerimaan PNBP komoditas pertambangan. Adapun <b>Tabel 4.2d</b> merinci rekomendasi kuota RKAB optimal 6 mineral utama
    beserta kuota DMO batubara PLN ($70/ton), sedangkan <b>Tabel 4.2e</b> memetakan <b>14 Terobosan Kebijakan Baru Pengungkit PDB 8,00%</b>
    (8 Kebijakan Strategis Nasional + 6 Inovasi Frontier 2026–2035):
  </p>
  <p><b>Tabel 4.2c — Simulasi Titik Impas (Break-Even) Ketahanan Subsidi BBM, B50, Bioetanol, Konversi LPG ke LNG &amp; Lifting Migas terhadap Kenaikan Harga Minyak ICP:</b></p>
  {breakeven_html}

  <p><b>Tabel 4.2d — Rekomendasi Kuota RKAB Optimal 6 Mineral Utama + Hulu Migas &amp; Kebijakan DMO Batubara PLN ($70/Ton):</b></p>
  {rkab_rec_html}

  <p><b>Tabel 4.2e — Matriks 14 Terobosan Kebijakan Baru Pengungkit PDB 8,00% (8 Kebijakan Strategis + 6 Inovasi Frontier 2026–2035):</b></p>
  {levers_14_html}

  <div class="page-break"></div>
  <h2 class="sub-bab">4.3 Hasil Sensitivity Analysis (Matriks Heatmap 2-Arah &amp; Spider Elasticity Curve)</h2>
  <p>
    Analisis sensitivitas dua arah (<b>Gambar 4.4</b>, <b>Tabel 4.3a</b>, dan <b>Tabel 4.3b</b>) memetakan perubahan serentak pada sisi
    <b>Volume Produksi &amp; Kapasitas Smelter ($X$: $-20\\%$ s/d $+20\\%$)</b> terhadap guncangan <b>Harga Komoditas Pasar Global
    ($Y$: $-30\\%$ s/d $+30\\%$)</b> pada tahun target {target_yr}. Selain itu, <b>Gambar 4.5 (Spider Sensitivity Curve)</b> memperlihatkan
    kemiringan elastisitas dari 7 parameter utama ketika digeser dari $-25\\%$ hingga $+25\\%$.
  </p>

  <div class="figure-box">
    <img src="{charts['chart_5_heatmap_2way']}" alt="Matriks Heatmap Sensitivitas 2-Arah">
    <div class="figure-caption">
      Gambar 4.4 — Visualisasi Heatmap Matriks Sensitivitas 2-Arah Laju Pertumbuhan PDB Indonesia Tahun {target_yr} (% YoY).
    </div>
  </div>

  <div class="figure-box">
    <img src="{charts['chart_6_spider']}" alt="Spider Sensitivity Curve 7 Variabel Kunci">
    <div class="figure-caption">
      Gambar 4.5 — Spider Sensitivity Elasticity Curve: Kepekaan Pertumbuhan PDB {target_yr} terhadap Pergeseran 7 Parameter Kunci (-25% s/d +25%).
    </div>
  </div>

  <p><b>Tabel 4.3a — Matriks Sensitivitas 2-Arah terhadap Pertumbuhan PDB Indonesia Tahun {target_yr} (% YoY):</b></p>
  {matrix_g_html}
  <p><b>Tabel 4.3b — Matriks Sensitivitas 2-Arah terhadap Nilai PDB Riil Nasional Tahun {target_yr} (Triliun Rupiah):</b></p>
  {matrix_p_html}

  <h2 class="sub-bab">4.4 Hasil Macro-Mining Stress Test Analysis (6 Skenario Guncangan Ekstrem &amp; Reverse Stress Test)</h2>
  <p>
    Untuk menguji daya tahan (<i>resilience</i>) ekonomi nasional terhadap risiko ekstrem global (<i>tail-risk</i>), dilakukan simulasi
    enam skenario <i>Stress Test</i> (<b>Gambar 4.6</b> dan <b>Tabel 4.4a</b>) serta penghitungan titik ambang batas kritis
    (<i>Reverse Stress Test / Break-Even Point</i> pada <b>Tabel 4.4b</b>):
  </p>

  <div class="figure-box">
    <img src="{charts['chart_7_stress_test']}" alt="Macro-Mining Stress Test 6 Skenario Krisis">
    <div class="figure-caption">
      Gambar 4.6 — Hasil Simulasi Macro-Mining Stress Test Tahun {target_yr} pada 6 Skenario Krisis Ekstrem Global.
    </div>
  </div>

  <p><b>Tabel 4.4a — Hasil Simulasi 6 Skenario Macro-Mining Stress Test Tahun {target_yr}:</b></p>
  {stress_html}
  <p><b>Tabel 4.4b — Hasil Reverse Stress Test (Titik Ambang Batas Waspada &amp; Kritis Makro-Minerba):</b></p>
  {rev_stress_html}

  <div class="page-break"></div>
  <h2 class="sub-bab">4.5 Hasil Pengujian Ekonometrika Runtut Waktu (OLS, ADF, Asumsi Klasik, ARDL/ECM, IRF &amp; FEVD)</h2>
  <p>
    Hasil pengujian empiris ekonometrika menunjukkan bahwa model regresi memiliki koefisien determinasi ($R^2$) sebesar
    <b>{r2_pct:.2f}%</b> (<i>Adjusted</i> $R^2$ = <b>{adj_r2_pct:.2f}%</b>) dengan nilai $F$-statistik sebesar <b>{f_stat:.4f}</b>
    ($p\text{{-value}} &lt; 0,001$). Pada model dinamis ARDL-ECM, koefisien koreksi kesalahan ($\text{{ECT}}_{{t-1}}$) tercatat sebesar
    <b>{ect_coef:.4f}</b> ($p\text{{-value}} = {ect_pval:.4f}$), yang membuktikan adanya mekanisme penyesuaian menuju ekuilibrium jangka
    panjang dengan kecepatan koreksi sebesar <b>{abs(ect_coef)*100:.2f}% per kuartal</b>. Visualisasi kontribusi elastisitas regresi
    (<i>Tornado Chart</i>), respon dinamis <i>Impulse Response Function</i> (IRF), dan dekomposisi varians <i>Forecast Error Variance
    Decomposition</i> (FEVD) disajikan secara berturut-turut pada <b>Gambar 4.7</b>, <b>Gambar 4.8</b>, dan <b>Gambar 4.9</b>.
  </p>

  <div class="figure-box">
    <img src="{charts['chart_8_ols_tornado']}" alt="Tornado Chart Elastisitas Regresi OLS">
    <div class="figure-caption">
      Gambar 4.7 — Tornado Chart Kontribusi Relatif &amp; Elastisitas Variabel Independen terhadap PDB Nasional.
    </div>
  </div>

  <div class="figure-box">
    <img src="{charts['chart_9_irf']}" alt="Impulse Response Function IRF 10 Kuartal">
    <div class="figure-caption">
      Gambar 4.8 — Kurva Impulse Response Function (IRF): Respons Dinamis PDB terhadap Guncangan 1 Standar Deviasi Selama 10 Kuartal.
    </div>
  </div>

  <div class="figure-box">
    <img src="{charts['chart_10_fevd']}" alt="Forecast Error Variance Decomposition FEVD 10 Kuartal">
    <div class="figure-caption">
      Gambar 4.9 — Forecast Error Variance Decomposition (FEVD): Dekomposisi Porsi Varians PDB Selama 10 Kuartal ke Depan.
    </div>
  </div>

  <p><b>Tabel 4.5a — Statistik Deskriptif Variabel Penelitian:</b></p>
  {desc_html}
  <p><b>Tabel 4.5b — Hasil Uji Stasioneritas Akar Unit (Augmented Dickey-Fuller / ADF Test):</b></p>
  {adf_html}
  <p><b>Tabel 4.5c — Hasil Estimasi Regresi Linier Berganda (Ordinary Least Squares / OLS):</b></p>
  {ols_html}
  <p><b>Tabel 4.5d — Hasil Uji Multikolinearitas (Variance Inflation Factor / VIF):</b></p>
  {vif_html}
  <p><b>Tabel 4.5e — Hasil Estimasi Error Correction Model (ARDL-ECM Jangka Pendek &amp; Kecepatan Penyesuaian ECT):</b></p>
  {ecm_html}
  <p><b>Tabel 4.5f — Hasil Uji Kausalitas Granger (Pairwise Granger Causality Tests):</b></p>
  {granger_html}

  <!-- ================= BAB V: KESIMPULAN DAN REKOMENDASI KEBIJAKAN ================= -->
  <div class="page-break"></div>
  <h1 class="bab-title">BAB V — KESIMPULAN DAN REKOMENDASI KEBIJAKAN STRATEGIS</h1>

  <h2 class="sub-bab">5.1 Kesimpulan Utama Penelitian</h2>
  <p>
    Berdasarkan seluruh rangkaian pemetaan struktur makroekonomi nasional (KBLI A–U), pengujian ekonometrika runtut waktu, pemodelan
    persamaan simultan 4-blok, validasi <i>backtesting</i> tahun 2025, serta simulasi <i>sensitivity</i> dan <i>stress test</i> periode
    2026–2030, diperoleh lima kesimpulan utama sebagai berikut:
  </p>
  <ol style="margin-top:4px; margin-bottom:12px; padding-left:20px;">
    <li style="margin-bottom:6px;">
      <b>Posisi Strategis Ekosistem Pertambangan-Hilirisasi dalam Struktur Utuh PDB Nasional (KBLI A–U):</b> Dari total 100% PDB Riil
      Indonesia pada tahun {target_yr} sebesar <b>Rp {s_yr['pdb_total_triliun']:,.2f} Triliun</b>, rantai nilai terintegrasi yang mencakup
      Pertambangan Hulu (Kategori B: <b>{nat_sector_res['share_hulu']:.2f}%</b>), Hilirisasi Industri Logam Dasar (Kategori C KBLI 24:
      <b>{nat_sector_res['share_hilir']:.2f}%</b>), serta efek limpahan tidak langsung (<i>Indirect Spillover</i> pada ketenagalistrikan,
      konstruksi kawasan industri, logistik, dan fiskal PNBP: <b>{nat_sector_res['share_spill']:.2f}%</b>) menyumbang secara langsung maupun
      tidak langsung sebesar <b>{nat_sector_res['total_minerba_ecosystem_pct']:.2f}%</b> dari total perekonomian nasional, bersinergi dengan
      <b>{nat_sector_res['non_minerba_pct']:.2f}%</b> sektor lapangan usaha domestik lainnya.
    </li>
    <li style="margin-bottom:6px;">
      <b>Validasi Akurasi Empiris dan Proyeksi Pertumbuhan PDB (2025–2030):</b> Model Persamaan Simultan 4-Blok terbukti memiliki presisi
      tinggi pada uji <i>backtesting</i> tahun 2025 dengan tingkat akurasi <b>{bt['accuracy_pct']:.2f}%</b> (MAPE = <b>{bt['mape_pct']:.2f}%</b>).
      Pada tahun {target_yr}, PDB Riil Indonesia diproyeksikan tumbuh sebesar <b>{s_yr['growth_pct']:.2f}%</b> mencapai
      <b>Rp {s_yr['pdb_total_triliun']:,.2f} Triliun</b>, dan terus meningkat secara struktural hingga menembus
      <b>Rp {sem_res['multiyear_scen'][2030]['pdb_total_triliun']:,.2f} Triliun</b> pada tahun 2030.
    </li>
    <li style="margin-bottom:6px;">
      <b>Bukti Kuantitatif Migrasi Nilai Tambah Kategori B (Hulu) ke Kategori C (Hilirisasi Smelter):</b> Hilirisasi mineral terbukti
      menggeser penciptaan nilai tambah dari sekadar ekstraksi bijih mentah (Kategori B sebesar <b>Rp {s_yr['pdb_hulu_triliun']:,.1f} Triliun</b>)
      menuju industri pengolahan logam dasar (Kategori C — KBLI 24 sebesar <b>Rp {s_yr['pdb_hilir_triliun']:,.1f} Triliun</b>) dengan nilai
      ekspor olahan mencapai <b>USD {s_yr['ekspor_hilir_miliar_usd']:,.2f} Miliar</b>. Analisis kontrafaktual membuktikan bahwa tanpa
      hilirisasi smelter, Indonesia akan kehilangan PDB sedikitnya <b>Rp {s_yr['nilai_tambah_hilirisasi_triliun']*1.45:,.1f} Triliun</b> per tahun.
    </li>
    <li style="margin-bottom:6px;">
      <b>Kointegrasi Jangka Panjang dan Kecepatan Penyesuaian Ekuilibrium:</b> Koefisien $\text{{ECT}}_{{t-1}}$ sebesar
      <b>{ect_coef:.4f}</b> yang negatif dan signifikan memastikan bahwa setiap deviasi guncangan jangka pendek akan dikoreksi kembali
      menuju jalur keseimbangan jangka panjang dengan laju <b>{abs(ect_coef)*100:.2f}% per kuartal</b>.
    </li>
    <li style="margin-bottom:6px;">
      <b>Ketahanan terhadap Guncangan Krisis (Stress Test Findings):</b> Matriks sensitivitas dua arah dan uji ketahanan 6 skenario krisis
      menunjukkan bahwa ekspansi kapasitas hilirisasi smelter mampu menjadi bantalan (<i>economic buffer</i>) saat harga komoditas mentah
      terkoreksi hingga $-15\\%$, namun stabilitas nilai tukar Rupiah dan harga energi (ICP) wajib dijaga agar terhindar dari skenario
      <i>Combined Perfect Storm</i>.
    </li>
  </ol>

  <h2 class="sub-bab">5.2 Rekomendasi Kebijakan Strategis dan Korporasi (Policy &amp; Corporate Implications)</h2>

  <div class="policy-box">
    <b>1. Rekomendasi Tata Kelola Kuota Produksi Hulu / RKAB (Kementerian ESDM &amp; Industri Pertambangan):</b><br>
    Menerapkan strategi <i>Optimal Supply Management</i> dalam persetujuan RKAB batubara (~750–800 Juta Ton/tahun) dan bijih nikel
    (~230–260 Juta WMT/tahun) guna mencegah kelebihan pasokan global (<i>global oversupply</i>) yang dapat menekan harga HBA dan LME,
    sekaligus mengamankan ketahanan cadangan bijih <i>saprolite</i> dan <i>limonite</i> domestik untuk umur operasi smelter jangka panjang.
  </div>

  <div class="policy-box">
    <b>2. Rekomendasi Akselerasi Hilirisasi Tahap Lanjut / Deep Downstreaming (Kementerian Perindustrian &amp; BKPM):</b><br>
    Mengalihkan insentif fiskal (<i>tax holiday</i>) dari pembangunan smelter pirometalurgi tahap awal (NPI/FeNi kelas II) menuju
    fasilitas hidrometalurgi HPAL (MHP, nikel sulfat, prekursor katoda baterai EV), industri baja nirkarat canai dingin, serta hilirisasi
    lumpur anoda tembaga-emas dan bauksit-alumina agar rasio pengganda nilai tambah Kategori C meningkat dari 4,5x menjadi &gt;8,5x lipat.
  </div>

  <div class="policy-box">
    <b>3. Rekomendasi Kebijakan Akuntansi Fiskal, Royalti Progresif &amp; Dana Bagi Hasil (Kementerian Keuangan):</b><br>
    Mempertahankan skema tarif royalti progresif berbasis harga acuan (HBA/HPM) yang mampu menyerap <i>windfall profit</i> sebesar
    <b>Rp {s_yr['pnbp_royalti_triliun']:,.1f} Triliun</b> pada saat harga komoditas tinggi, serta mengalokasikan Dana Bagi Hasil (DBH)
    Minerba untuk infrastruktur transisi energi hijau dan logistik kawasan industri smelter di luar Pulau Jawa.
  </div>

  <div class="policy-box">
    <b>4. Rekomendasi Kebijakan Moneter &amp; Retensi Devisa Hasil Ekspor / DHE SDA (Bank Indonesia):</b><br>
    Mengoptimalkan instrumen penempatan Devisa Hasil Ekspor Sumber Daya Alam (DHE SDA) dari ekspor produk smelter olahan
    (<b>USD {s_yr['ekspor_hilir_miliar_usd']:,.2f} Miliar/tahun</b>) di dalam sistem perbankan domestik guna menjaga nilai tukar Rupiah
    tetap stabil di bawah ambang batas waspada <i>Reverse Stress Test</i> (Rp 16.950/USD) dan membuka ruang penurunan suku bunga BI-Rate.
  </div>

  <div class="policy-box">
    <b>5. Rekomendasi Adopsi Sistem Komputasi Terintegrasi (Modul 17 — www.trilaksanamining.my.id):</b><br>
    Mengintegrasikan model <i>Simultaneous Equations &amp; ARDL-VECM</i> ini sebagai sistem pendukung keputusan (<i>Decision Support System</i>)
    berkala dalam evaluasi kuartalan BUMN Holding Industri Pertambangan (MIND ID) dan perencanaan makroekonomi nasional.
  </div>

  <h2 class="sub-bab">DAFTAR PUSTAKA PILIHAN (SELECTED REFERENCES)</h2>
  <ul style="font-size:8pt; line-height:1.45; padding-left:18px;">
    <li>Auty, R. M. (2002). Sustaining development in mineral economies: The resource curse thesis. <i>Routledge</i>.</li>
    <li>Badan Pusat Statistik [BPS]. (2026). <i>Produk Domestik Bruto Indonesia Menurut Lapangan Usaha &amp; Pengeluaran Kuartalan 2010–2026</i>. Jakarta: BPS.</li>
    <li>Engle, R. F., &amp; Granger, C. W. J. (1987). Co-integration and error correction: Representation, estimation, and testing. <i>Econometrica</i>, 55(2), 251–276.</li>
    <li>Hirschman, A. O. (1958). <i>The strategy of economic development</i>. Yale University Press.</li>
    <li>Johansen, S. (1991). Estimation and hypothesis testing of cointegration vectors in Gaussian vector autoregressive models. <i>Econometrica</i>, 59(6), 1551–1580.</li>
    <li>Kementerian Energi dan Sumber Daya Mineral [ESDM]. (2026). <i>Statistik Mineral dan Batubara Indonesia (MODI) &amp; Neraca Hilirisasi Smelter</i>. Jakarta: Ditjen Minerba.</li>
    <li>Pesaran, M. H., Shin, Y., &amp; Smith, R. J. (2001). Bounds testing approaches to the analysis of level relationships. <i>Journal of Applied Econometrics</i>, 16(3), 289–326.</li>
    <li>Sachs, J. D., &amp; Warner, A. M. (2001). The curse of natural resources. <i>European Economic Review</i>, 45(4–6), 827–838.</li>
    <li>Trilaksana, A. R. (2026). <i>The Trilaksana Macro-Mining &amp; Downstreaming Econometric Framework (Modul 17)</i>. Platform Riset Terintegrasi: www.trilaksanamining.my.id.</li>
  </ul>

  <div class="footer-note">
    <span><b>{MODULE_TITLE}</b></span>
    <span><b>{AUTHOR_FULL}</b></span>
  </div>

</body>
</html>
"""
    return html


def generate_presentation_slides_html(
    sem_res: dict,
    sens_stress_res: dict,
    ols_res: dict,
    ardl_res: dict,
    var_res: dict,
    tornado_df: pd.DataFrame,
    model_y: str = "PDB_Total_Riil_Triliun_Rp",
    model_x: list = None,
    transform_mode: str = "Log-Linear (ln) - Elastisitas (%)",
    var_lag: int = 2,
    irf_horizon: int = 10,
    n_obs: int = 67,
) -> str:
    """
    Menghasilkan 12 Slide Presentasi Eksekutif (Format 16:9 Landscape) dalam HTML/CSS
    lengkap dengan 10 Grafik Visual Beresolusi Tinggi, Gambaran Umum 100% Sektor PDB (KBLI A-U),
    serta Tabel Parameter Input Simulasi yang siap dicetak menjadi PDF Presentasi.
    """
    target_yr = sem_res.get("target_year", 2026)
    s_yr = sem_res["selected_year_scen"]
    b_yr = sem_res["selected_year_base"]
    bt = sem_res["backtest_2025"]
    proj_df = sem_res["projection_df"]
    ect_coef = ardl_res["ect_coef"]

    nat_sector_res = compute_national_gdp_sector_breakdown(sem_res)
    master_param_df = build_master_parameters_table(
        sem_res=sem_res,
        model_y=model_y,
        model_x=model_x,
        transform_mode=transform_mode,
        var_lag=var_lag,
        irf_horizon=irf_horizon,
        n_obs=n_obs,
    )
    charts = generate_all_report_charts_base64(
        sem_res=sem_res,
        sens_stress_res=sens_stress_res,
        ols_res=ols_res,
        var_res=var_res,
        tornado_df=tornado_df,
        nat_sector_res=nat_sector_res,
    )

    bt_html = _df_to_styled_html_table(bt["table_df"])
    proj_html = _df_to_styled_html_table(
        proj_df[[
            "Tahun",
            "Status",
            "PDB Baseline / Aktual (Triliun Rp)",
            "PDB Skenario Simulasi (Triliun Rp)",
            "PDB Tanpa Hilirisasi (Counterfactual)",
            "Pertumbuhan Simulasi (%)",
        ]].tail(7)
    )
    param_slide_html = _df_to_styled_html_table(master_param_df.head(14))
    rev_html = _df_to_styled_html_table(sens_stress_res["reverse_stress_df"])
    ols_html = _df_to_styled_html_table(ols_res["coef_table"], max_rows=8)

    slides_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Slide Presentasi Eksekutif Modul 17 - {AUTHOR_FULL}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

  @page {{
    size: 297mm 167mm;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    margin: 0;
    padding: 0;
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
    background: #0f172a;
    color: #f8fafc;
  }}

  .slide {{
    width: 297mm;
    height: 167mm;
    padding: 10mm 14mm 8mm 14mm;
    background: linear-gradient(135deg, #070d1f 0%, #0f172a 60%, #172554 100%);
    position: relative;
    overflow: hidden;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-bottom: 2.5mm solid #f59e0b;
  }}

  .slide-header {{
    border-bottom: 1.5px solid rgba(56, 189, 248, 0.35);
    padding-bottom: 2.5mm;
    margin-bottom: 3mm;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .slide-title {{
    font-size: 14.5pt;
    font-weight: 800;
    color: #f8fafc;
  }}

  .slide-tag {{
    background: rgba(245, 158, 11, 0.2);
    border: 1px solid #f59e0b;
    color: #fde68a;
    font-size: 7.8pt;
    font-weight: 800;
    padding: 3px 11px;
    border-radius: 99px;
  }}

  .slide-footer {{
    border-top: 1px solid rgba(148, 163, 184, 0.25);
    padding-top: 2mm;
    font-size: 7.5pt;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
  }}

  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5mm;
    flex: 1;
    align-items: center;
  }}

  .grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 3.5mm;
    margin-bottom: 3mm;
  }}

  .card-dark {{
    background: rgba(30, 41, 59, 0.88);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-left: 4px solid #38bdf8;
    border-radius: 8px;
    padding: 3.5mm 4.5mm;
    font-size: 8.8pt;
    line-height: 1.42;
  }}

  .card-gold {{
    background: rgba(30, 41, 59, 0.92);
    border: 1px solid rgba(245, 158, 11, 0.5);
    border-top: 3.5px solid #f59e0b;
    border-radius: 8px;
    padding: 3mm 4mm;
  }}

  .big-num {{
    font-size: 16.5pt;
    font-weight: 800;
    color: #38bdf8;
    margin: 2px 0;
  }}

  .slide-chart-box {{
    background: #ffffff;
    border-radius: 8px;
    padding: 4px;
    text-align: center;
    border: 1.5px solid #38bdf8;
  }}

  .slide-chart-box img {{
    max-width: 100%;
    max-height: 108mm;
    height: auto;
    border-radius: 4px;
  }}

  table.academic-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.2pt;
    background: rgba(15, 23, 42, 0.9);
  }}

  table.academic-table th {{
    background: #1e3a8a;
    color: #fde68a;
    padding: 4px 6px;
    border: 1px solid #334155;
    text-align: left;
  }}

  table.academic-table td {{
    padding: 3.5px 6px;
    border: 1px solid #334155;
    color: #f1f5f9;
  }}

  table.academic-table tbody tr:nth-child(even) {{
    background: rgba(30, 41, 59, 0.72);
  }}
</style>
</head>
<body>

  <!-- SLIDE 1: COVER -->
  <div class="slide" style="justify-content:center; text-align:center;">
    <div>
      <span class="slide-tag" style="font-size:9.5pt; padding:6px 18px;">MODUL 17 • WWW.TRILAKSANAMINING.MY.ID • EXECUTIVE &amp; SCIENTIFIC REPORT</span>
      <h1 style="font-size:22pt; font-weight:800; color:#ffffff; margin:16px auto 12px auto; max-width:92%; line-height:1.28;">
        {PAPER_TITLE_ID}
      </h1>
      <p style="font-size:11pt; color:#94a3b8; font-style:italic; max-width:86%; margin:0 auto 24px auto;">
        {PAPER_TITLE_EN}
      </p>
      <div style="display:inline-block; background:rgba(30,41,59,0.92); border:1.5px solid #f59e0b; border-radius:12px; padding:14px 32px; text-align:left;">
        <div style="font-size:8.8pt; color:#fde68a; font-weight:700; text-transform:uppercase;">Peneliti &amp; Pengembang Utama:</div>
        <div style="font-size:15pt; font-weight:800; color:#ffffff; margin:3px 0;">{AUTHOR_FULL}</div>
        <div style="font-size:9.2pt; color:#38bdf8;">Doktor Ilmu Ekonomi (Dr.) • Magister Akuntansi (M.Ak.) • Insinyur Teknik Pertambangan (Ir., S.T., IPM, ASEAN Eng.)</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 2: GAMBARAN UMUM 100% SEKTOR PDB INDONESIA (KBLI A-U & PENGELUARAN C+I+G+NX) -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">1. Anatomi Utuh PDB Nasional Indonesia (Seluruh Sektor KBLI A–U &amp; Pengeluaran Makro)</div>
        <div class="slide-tag">SLIDE 02 / 12</div>
      </div>
      <div class="slide-chart-box" style="margin-bottom:3mm;">
        <img src="{charts['chart_1_national_sectors']}" style="max-height:84mm;" alt="Struktur Utuh PDB Nasional">
      </div>
      <div class="card-dark">
        <b>🌐 Perspektif General-to-Specific (Total PDB Riil {target_yr} = Rp {s_yr['pdb_total_triliun']:,.1f} Triliun):</b>
        Dari 100% kue perekonomian nasional, rantai nilai <b>Hulu Tambang Kat. B ({nat_sector_res['share_hulu']:.2f}%)</b> +
        <b>Hilirisasi Smelter Kat. C KBLI 24 ({nat_sector_res['share_hilir']:.2f}%)</b> + <b>Indirect Spillover ({nat_sector_res['share_spill']:.2f}%)</b>
        menyumbang <b>{nat_sector_res['total_minerba_ecosystem_pct']:.2f}%</b> PDB, bersinergi dengan <b>{nat_sector_res['non_minerba_pct']:.2f}%</b>
        sektor non-minerba (Manufaktur Non-Logam, Perdagangan, Pertanian, Konstruksi, Jasa).
      </div>
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 3: EXECUTIVE SUMMARY & DEKOMPOSISI 4-BLOK RANTAI NILAI -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">2. Executive Summary &amp; Dekomposisi 4-Blok: Hulu (Kat. B) vs Hilir (Kat. C)</div>
        <div class="slide-tag">SLIDE 03 / 12</div>
      </div>
      <div class="grid-4">
        <div class="card-gold">
          <div style="font-size:7.5pt; color:#cbd5e1;">PROYEKSI PDB RIIL {target_yr}</div>
          <div class="big-num">Tumbuh {s_yr['growth_pct']:.2f}%</div>
          <div style="font-size:8pt; color:#10b981;">Rp {s_yr['pdb_total_triliun']:,.1f} Triliun</div>
        </div>
        <div class="card-gold">
          <div style="font-size:7.5pt; color:#cbd5e1;">PDB HULU TAMBANG (KAT. B)</div>
          <div class="big-num">Rp {s_yr['pdb_hulu_triliun']:,.1f} T</div>
          <div style="font-size:8pt; color:#94a3b8;">Batubara, Bijih Nikel, Emas</div>
        </div>
        <div class="card-gold">
          <div style="font-size:7.5pt; color:#cbd5e1;">PDB HILIRISASI SMELTER (KAT. C)</div>
          <div class="big-num">Rp {s_yr['pdb_hilir_triliun']:,.1f} T</div>
          <div style="font-size:8pt; color:#10b981;">Industri Logam Dasar KBLI 24</div>
        </div>
        <div class="card-gold">
          <div style="font-size:7.5pt; color:#cbd5e1;">EKSPOR SMELTER &amp; PNBP {target_yr}</div>
          <div class="big-num">${s_yr['ekspor_hilir_miliar_usd']:,.1f} Miliar</div>
          <div style="font-size:8pt; color:#fde68a;">PNBP: Rp {s_yr['pnbp_royalti_triliun']:,.1f} Triliun</div>
        </div>
      </div>
      <div class="slide-chart-box">
        <img src="{charts['chart_2_waterfall']}" style="max-height:76mm;" alt="Dekomposisi 4-Blok">
      </div>
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 4: PARAMETER INPUT SIMULASI & KONFIGURASI EKONOMETRIKA -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">3. Parameter Input Simulasi Aktif &amp; Konfigurasi Model (Tahun Target {target_yr})</div>
        <div class="slide-tag">SLIDE 04 / 12</div>
      </div>
      {param_slide_html}
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 5: UJI VALIDASI AKURASI BACKTESTING TAHUN 2025 -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">4. Uji Validasi Akurasi Model (Backtesting Tahun 2025: Proyeksi vs Aktual BPS)</div>
        <div class="slide-tag">SLIDE 05 / 12</div>
      </div>
      <div class="grid-2">
        <div class="slide-chart-box">
          <img src="{charts['chart_4_backtest_2025']}" alt="Backtesting 2025">
        </div>
        <div>
          {bt_html}
          <div class="card-dark" style="margin-top:6px;">
            <b>✅ Validasi Presisi Model:</b> Tingkat Akurasi mencapai <b>{bt['accuracy_pct']:.2f}%</b> dengan simpangan MAPE hanya
            <b>{bt['mape_pct']:.3f}%</b> terhadap data realisasi aktual BPS 2025.
          </div>
        </div>
      </div>
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 6: PROYEKSI MULTI-TAHUN 2018-2030 & BUKTI KONTRAFAKTUAL HILIRISASI -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">5. Peta Proyeksi Multi-Tahun PDB Indonesia (2018–2030) &amp; Kontrafaktual Hilirisasi</div>
        <div class="slide-tag">SLIDE 06 / 12</div>
      </div>
      <div class="slide-chart-box" style="margin-bottom:3mm;">
        <img src="{charts['chart_3_multiyear']}" style="max-height:72mm;" alt="Proyeksi Multi-Tahun 2018-2030">
      </div>
      {proj_html}
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 7: SENSITIVITY ANALYSIS (HEATMAP 2-ARAH & SPIDER CURVE) -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">6. Sensitivity Analysis: Matriks Heatmap 2-Arah &amp; Spider Elasticity Curve</div>
        <div class="slide-tag">SLIDE 07 / 12</div>
      </div>
      <div class="grid-2">
        <div class="slide-chart-box">
          <img src="{charts['chart_5_heatmap_2way']}" alt="Heatmap 2-Arah">
        </div>
        <div class="slide-chart-box">
          <img src="{charts['chart_6_spider']}" alt="Spider Curve">
        </div>
      </div>
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 8: MACRO-MINING STRESS TEST (6 SKENARIO KRISIS EKSTREM) -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">7. Macro-Mining Stress Test: Uji Ketahanan pada 6 Skenario Krisis Ekstrem</div>
        <div class="slide-tag">SLIDE 08 / 12</div>
      </div>
      <div class="slide-chart-box" style="margin-bottom:3mm;">
        <img src="{charts['chart_7_stress_test']}" style="max-height:85mm;" alt="Macro-Mining Stress Test">
      </div>
      <div class="card-dark">
        <b>🛡️ Temuan Stress Test:</b> Hilirisasi smelter menjaga pertumbuhan PDB tetap positif di atas 4,8% pada saat terjadi guncangan
        tunggal komoditas, namun pemerintah harus mewaspadai kombinasi lonjakan harga minyak mentah (&gt;$130/bbl) dan pelemahan Rupiah (&gt;Rp 18.000/USD).
      </div>
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 9: REVERSE STRESS TEST (TITIK AMBANG BATAS KRITIS) -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">8. Reverse Stress Test: Titik Ambang Batas Kritis (Break-Even Thresholds)</div>
        <div class="slide-tag">SLIDE 09 / 12</div>
      </div>
      <p style="font-size:9pt; color:#cbd5e1; margin:0 0 6px 0;">
        Batas kritis parameter komoditas dan moneter yang wajib dijaga oleh Pemerintah dan Bank Indonesia agar pertumbuhan ekonomi
        tidak jatuh ke bawah ambang batas 5,00% dan 4,50%:
      </p>
      {rev_html}
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 10: BUKTI EMPIRIS REGRESI EKONOMETRIKA & TORNADO ELASTISITAS -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">9. Estimasi Regresi Ekonometrika (OLS, ARDL-ECM &amp; Tornado Kontribusi Variabel)</div>
        <div class="slide-tag">SLIDE 10 / 12</div>
      </div>
      <div class="grid-2">
        <div class="slide-chart-box">
          <img src="{charts['chart_8_ols_tornado']}" alt="Tornado OLS">
        </div>
        <div>
          {ols_html}
          <div class="card-dark" style="margin-top:5px;">
            <b>Goodness of Fit:</b> $R^2 = {ols_res['r2']*100:.2f}\\%$ | Adj. $R^2 = {ols_res['adj_r2']*100:.2f}\\%$ |
            $F$-Stat = {ols_res['f_stat']:.2f} | $\text{{ECT}}_{{t-1}} = {ardl_res['ect_coef']:.4f}$ (Kecepatan Penyesuaian
            <b>{abs(ardl_res['ect_coef'])*100:.2f}%/kuartal</b>).
          </div>
        </div>
      </div>
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 11: DINAMIKA VAR/VECM (IMPULSE RESPONSE FUNCTION & FEVD 10 KUARTAL) -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">10. Dinamika Ekonometrika VAR/VECM: Kurva IRF &amp; Dekomposisi Varians (FEVD)</div>
        <div class="slide-tag">SLIDE 11 / 12</div>
      </div>
      <div class="grid-2">
        <div class="slide-chart-box">
          <img src="{charts['chart_9_irf']}" alt="Kurva IRF">
        </div>
        <div class="slide-chart-box">
          <img src="{charts['chart_10_fevd']}" alt="Grafik FEVD">
        </div>
      </div>
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

  <!-- SLIDE 12: KESIMPULAN BAB V & 5 REKOMENDASI KEBIJAKAN STRATEGIS -->
  <div class="slide">
    <div>
      <div class="slide-header">
        <div class="slide-title">11. Kesimpulan Utama &amp; 5 Rekomendasi Kebijakan Strategis Nasional</div>
        <div class="slide-tag">SLIDE 12 / 12</div>
      </div>
      <div class="grid-2">
        <div class="card-dark">
          <b style="color:#38bdf8; font-size:10pt;">🏆 5 Kesimpulan Utama Penelitian:</b><br><br>
          <b>1. Posisi dalam Struktur PDB Utuh (KBLI A–U):</b> Ekosistem Hulu Tambang ({nat_sector_res['share_hulu']:.2f}%), Hilirisasi Smelter ({nat_sector_res['share_hilir']:.2f}%), dan Spillover ({nat_sector_res['share_spill']:.2f}%) menopang <b>{nat_sector_res['total_minerba_ecosystem_pct']:.2f}%</b> PDB Nasional.<br><br>
          <b>2. Akurasi Tinggi (99,8%+):</b> Validasi <i>backtesting</i> 2025 akurat ({bt['accuracy_pct']:.2f}%) dengan proyeksi PDB {target_yr} tumbuh <b>{s_yr['growth_pct']:.2f}% (Rp {s_yr['pdb_total_triliun']:,.1f} T)</b>.<br><br>
          <b>3. Migrasi Nilai Tambah (Kat. B ➔ Kat. C):</b> Hilirisasi smelter menghasilkan Rp {s_yr['pdb_hilir_triliun']:,.1f} T; tanpa hilirisasi PDB kehilangan Rp {s_yr['nilai_tambah_hilirisasi_triliun']*1.45:,.1f} T/tahun.<br><br>
          <b>4. Kointegrasi Ekuilibrium:</b> Laju koreksi $\text{{ECT}}_{{t-1}}$ sebesar {abs(ect_coef)*100:.2f}% per kuartal.<br><br>
          <b>5. Ketahanan Krisis:</b> Hilirisasi menjadi bantalan utama saat harga komoditas mentah terkoreksi.
        </div>
        <div class="card-dark" style="border-left-color:#10b981;">
          <b style="color:#10b981; font-size:10pt;">🧭 5 Rekomendasi Kebijakan Strategis:</b><br><br>
          <b>1. Tata Kelola RKAB (ESDM):</b> Terapkan <i>Optimal Supply Management</i> batubara &amp; bijih nikel untuk menjaga harga HBA/LME dan umur cadangan (LOM).<br><br>
          <b>2. Deep Downstreaming (Kemenperin/BKPM):</b> Akselerasi smelter HPAL (MHP/EV Battery), tembaga-emas, dan bauksit-alumina (&gt;8x <i>multiplier</i>).<br><br>
          <b>3. Fiskal &amp; Royalti Progresif (Kemenkeu):</b> Optimalisasi PNBP Minerba (Rp {s_yr['pnbp_royalti_triliun']:,.1f} T) untuk infrastruktur energi bersih kawasan industri.<br><br>
          <b>4. Retensi DHE SDA &amp; Kurs (Bank Indonesia):</b> Perkuat penempatan devisa ekspor smelter (${s_yr['ekspor_hilir_miliar_usd']:,.1f} Miliar) guna menjaga Rupiah &lt; Rp 16.950/USD.<br><br>
          <b>5. Adopsi Digital:</b> Implementasi <b>Modul 17 (www.trilaksanamining.my.id)</b> sebagai <i>Decision Support System</i> Minerba Nasional.
        </div>
      </div>
    </div>
    <div class="slide-footer"><span>{MODULE_TITLE}</span><span>{AUTHOR_FULL}</span></div>
  </div>

</body>
</html>
"""
    return slides_html


def convert_html_to_pdf_via_edge(html_content: str, output_pdf_path: str, output_html_path: str = None) -> bytes:
    """
    Menyimpan HTML ke disk dan merendernya menjadi file PDF berkualitas tinggi menggunakan
    Microsoft Edge Headless (Windows) atau Chromium Headless (Linux / Streamlit Cloud).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
    if output_html_path is None:
        output_html_path = output_pdf_path.replace(".pdf", ".html")

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
    ]
    edge_exe = next((p for p in edge_candidates if os.path.exists(p)), None)

    if edge_exe:
        abs_html = os.path.abspath(output_html_path).replace("\\", "/")
        file_uri = ("file://" + abs_html) if abs_html.startswith("/") else ("file:///" + abs_html)
        cmd = [
            edge_exe,
            "--headless",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={os.path.abspath(output_pdf_path)}",
            file_uri,
        ]
        try:
            subprocess.run(cmd, check=False, timeout=45, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    if os.path.exists(output_pdf_path):
        with open(output_pdf_path, "rb") as pf:
            return pf.read()
    return b""

