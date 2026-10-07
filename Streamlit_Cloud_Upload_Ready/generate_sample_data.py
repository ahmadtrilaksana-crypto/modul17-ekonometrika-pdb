"""
Generator Dataset Terpadu Makroekonomi, Produksi Pertambangan Hulu (Kategori B),
Kuota RKAB vs Realisasi 6 Mineral Utama, Target APBN vs Realisasi Lifting Migas,
Hilirisasi Smelter & Industri Logam Dasar (Kategori C), PNBP Minerba, dan PDB Indonesia.
Mendukung Auto-Rolling Dynamic Time-Series (2010Q1 s.d. Tahun & Kuartal Berjalan Otomatis).
"""

import os
from datetime import datetime
import numpy as np
import pandas as pd


def get_default_end_period() -> tuple:
    """Menentukan tahun dan kuartal akhir secara dinamis (Auto-Rolling 2026 -> 2027+)."""
    now = datetime.now()
    yr = max(2026, now.year)
    qtr = (now.month - 1) // 3 + 1
    if yr == 2026 and qtr > 3:
        qtr = 3
    return yr, qtr


def generate_macro_dataset(end_year: int = None, end_quarter: int = None) -> pd.DataFrame:
    if end_year is None or end_quarter is None:
        def_yr, def_qtr = get_default_end_period()
        end_year = end_year or def_yr
        end_quarter = end_quarter or def_qtr

    np.random.seed(42)
    periods = []
    years_arr = []
    for y in range(2010, end_year + 1):
        max_q = 4 if y < end_year else end_quarter
        for q in range(1, max_q + 1):
            periods.append(f"{y}Q{q}")
            years_arr.append(y)

    n = len(periods)
    t = np.arange(n)
    years_np = np.array(years_arr)

    # -------------------------------------------------------------------------
    # BLOK A: HARGA KOMODITAS GLOBAL (Y) & MONETER / KURS
    # -------------------------------------------------------------------------
    # 1. Harga Minyak Mentah Dunia / ICP (USD/Barrel)
    oil_base = (
        84.0
        + 20.0 * np.sin(2 * np.pi * t / 24.0)
        - 18.0 * np.exp(-((t - 24) / 5.0) ** 2)
        - 32.0 * np.exp(-((t - 41) / 2.5) ** 2)
        + 24.0 * np.exp(-((t - 49) / 3.5) ** 2)
        + np.random.normal(0, 2.5, n)
    )
    oil_price = np.clip(np.round(oil_base, 2), 30.0, 116.0)
    if n >= 67:
        oil_price[64:67] = [79.50, 77.80, 78.40]  # Aktual 2026Q1-Q3

    # 2. Harga Batubara Acuan / HBA Newcastle (USD/Ton)
    coal_price_base = (
        88.0
        + 18.0 * np.sin(2 * np.pi * t / 22.0)
        - 22.0 * np.exp(-((t - 23) / 4.5) ** 2)
        - 25.0 * np.exp(-((t - 41) / 2.5) ** 2)
        + 165.0 * np.exp(-((t - 50) / 3.2) ** 2)  # Booming batubara 2022
        + 28.0 * (t / max(n, 67))
        + np.random.normal(0, 4.5, n)
    )
    coal_price = np.clip(np.round(coal_price_base, 2), 50.0, 320.0)
    if n >= 67:
        coal_price[64:67] = [122.40, 126.10, 124.50]

    # 3. Harga Nikel LME (USD/Ton)
    nickel_price_base = (
        16500.0
        + 2800.0 * np.sin(2 * np.pi * t / 20.0)
        - 4800.0 * np.exp(-((t - 24) / 5.0) ** 2)
        + 9500.0 * np.exp(-((t - 49) / 3.0) ** 2)  # Lonjakan LME 2022
        + np.random.normal(0, 550.0, n)
    )
    nickel_price = np.clip(np.round(nickel_price_base, 0), 9200.0, 29500.0)
    if n >= 67:
        nickel_price[64:67] = [16950.0, 17300.0, 17450.0]

    # 4. Harga Emas Dunia Spot Gold (USD/Troy Oz)
    gold_price_base = (
        1250.0
        + 14.5 * t
        + 220.0 * np.exp(-((t - 8) / 4.0) ** 2)
        + 260.0 * np.exp(-((t - 42) / 4.0) ** 2)
        + 580.0 * np.maximum(0, (t - 52) / 14.0) ** 1.35  # Reli emas 2024-2026+
        + np.random.normal(0, 25.0, n)
    )
    gold_price = np.clip(np.round(gold_price_base, 2), 1120.0, 3400.0)
    if n >= 67:
        gold_price[64:67] = [2540.0, 2615.0, 2665.0]

    # 5. Nilai Tukar Rupiah terhadap USD (Rp / USD)
    kurs_base = (
        9050.0
        + 108.0 * t
        + 620.0 * np.exp(-((t - 41) / 2.0) ** 2)
        + 360.0 * np.sin(2 * np.pi * t / 18.0)
        + np.random.normal(0, 110.0, n)
    )
    kurs_idr = np.round(kurs_base, 0)
    if n >= 67:
        kurs_idr[64:67] = [15920.0, 16050.0, 15850.0]

    # 6. Tingkat Inflasi YoY (%) & Suku Bunga BI-Rate (%)
    inflasi_base = (
        5.1
        - 0.042 * t
        + 0.022 * (oil_price - 75.0)
        + 0.00018 * (kurs_idr - 12500.0)
        - 1.6 * np.exp(-((t - 42) / 3.0) ** 2)
        + np.random.normal(0, 0.28, n)
    )
    inflasi = np.clip(np.round(inflasi_base, 2), 1.35, 8.20)
    if n >= 67:
        inflasi[64:67] = [2.65, 2.52, 2.45]

    bi_rate_base = (
        5.5
        + 0.34 * (inflasi - 4.0)
        + 0.00016 * (kurs_idr - 12500.0)
        - 1.15 * np.exp(-((t - 43) / 4.0) ** 2)
        + np.random.normal(0, 0.15, n)
    )
    bi_rate = np.clip(np.round(bi_rate_base * 4) / 4.0, 3.50, 7.50)
    if n >= 67:
        bi_rate[64:67] = [6.00, 6.00, 5.75]

    # -------------------------------------------------------------------------
    # BLOK B: KUOTA RKAB / TARGET APBN VS REALISASI PRODUKSI 6 MINERAL & MIGAS
    # -------------------------------------------------------------------------
    # 7. Batubara: Realisasi Produksi vs Kuota RKAB per Kuartal (Juta Ton)
    prod_batubara = np.round(
        82.0 + 1.65 * t + 0.065 * (coal_price - 90.0) + np.random.normal(0, 2.8, n), 2
    )
    if n >= 67:
        prod_batubara[64:67] = [192.5, 196.0, 198.4]
    rkab_batubara = np.round(prod_batubara * np.random.uniform(1.03, 1.08, n), 2)
    if n >= 67:
        rkab_batubara[64:67] = [206.0, 208.5, 210.0]

    # 8. Bijih Nikel: Realisasi Produksi vs Kuota RKAB per Kuartal (Juta WMT)
    smelter_era_boost = np.maximum(0.0, (t - 28) * 1.45)  # Akselerasi hilirisasi sejak 2017-2026+
    prod_nikel = np.round(
        6.5 + 0.28 * t + smelter_era_boost + 0.0004 * (nickel_price - 15000.0) + np.random.normal(0, 1.1, n),
        2,
    )
    if n >= 67:
        prod_nikel[64:67] = [56.8, 58.5, 60.2]
    rkab_nikel = np.round(prod_nikel * np.random.uniform(1.04, 1.09, n), 2)
    if n >= 67:
        rkab_nikel[64:67] = [60.5, 62.0, 63.5]

    # 9. Emas: Realisasi Produksi vs Kuota RKAB per Kuartal (Ton)
    prod_emas = np.round(
        21.5 + 0.11 * t + 0.0022 * (gold_price - 1400.0) + np.random.normal(0, 0.75, n), 2
    )
    if n >= 67:
        prod_emas[64:67] = [28.4, 29.1, 29.6]
    rkab_emas = np.round(prod_emas * np.random.uniform(1.03, 1.07, n), 2)
    if n >= 67:
        rkab_emas[64:67] = [30.0, 30.5, 31.0]

    # 10. Bijih Tembaga: Realisasi Produksi vs Kuota RKAB per Kuartal (Juta Ton)
    prod_tembaga = np.round(
        18.0 + 0.21 * t + np.maximum(0.0, (t - 40) * 0.18) + np.random.normal(0, 0.65, n), 2
    )
    if n >= 67:
        prod_tembaga[64:67] = [31.2, 31.8, 32.4]
    rkab_tembaga = np.round(prod_tembaga * np.random.uniform(1.04, 1.08, n), 2)
    if n >= 67:
        rkab_tembaga[64:67] = [33.2, 33.8, 34.5]

    # 11. Bauksit: Realisasi Produksi vs Kuota RKAB per Kuartal (Juta WMT)
    prod_bauksit = np.round(
        5.2 + 0.065 * t + np.maximum(0.0, (t - 48) * 0.12) + np.random.normal(0, 0.35, n), 2
    )
    if n >= 67:
        prod_bauksit[64:67] = [9.1, 9.4, 9.8]
    rkab_bauksit = np.round(prod_bauksit * np.random.uniform(1.06, 1.14, n), 2)
    if n >= 67:
        rkab_bauksit[64:67] = [10.2, 10.5, 10.8]

    # 12. Timah: Realisasi Produksi vs Kuota RKAB per Kuartal (Ribu Ton)
    prod_timah = np.round(
        19.5 - 0.04 * np.minimum(t, 45) + 0.08 * np.maximum(0.0, t - 45) + np.random.normal(0, 0.45, n), 2
    )
    if n >= 67:
        prod_timah[64:67] = [16.4, 16.8, 17.2]
    rkab_timah = np.round(prod_timah * np.random.uniform(1.05, 1.11, n), 2)
    if n >= 67:
        rkab_timah[64:67] = [17.8, 18.0, 18.5]

    # 13. Hulu Migas: Lifting Minyak Bumi (Ribu Bph) & Gas Bumi/LNG (MMSCFD) vs Target APBN
    # Mencerminkan tren natural decline 2010-2024 (~945 -> 580 kbpd) lalu rebound EOR Rokan/Banyu Urip 2025-2026+
    lifting_minyak = np.round(
        935.0
        - 6.2 * np.minimum(t, 56)
        + 4.8 * np.maximum(0.0, t - 56)
        + np.random.normal(0, 6.5, n),
        1,
    )
    if n >= 67:
        lifting_minyak[64:67] = [592.0, 602.0, 612.0]
    target_lifting_minyak = np.round(lifting_minyak + np.random.uniform(12.0, 28.0, n), 1)
    if n >= 67:
        target_lifting_minyak[64:67] = [610.0, 610.0, 615.0]

    # Lifting Gas Bumi & LNG (MMSCFD) -> Mencerminkan Tangguh Train 3, Jambaran Tiung Biru, & persiapan Masela/IDD
    lifting_gas = np.round(
        6850.0
        - 22.0 * np.minimum(t, 52)
        + 55.0 * np.maximum(0.0, t - 52)
        + np.random.normal(0, 45.0, n),
        0,
    )
    if n >= 67:
        lifting_gas[64:67] = [5860.0, 5940.0, 6050.0]
    target_lifting_gas = np.round(lifting_gas + np.random.uniform(120.0, 260.0, n), 0)
    if n >= 67:
        target_lifting_gas[64:67] = [6100.0, 6150.0, 6200.0]

    # Rasio Realisasi terhadap Kuota RKAB & Target Lifting Komposit (%)
    rasio_rkab_pct = np.round(
        (
            0.35 * (prod_batubara / rkab_batubara)
            + 0.30 * (prod_nikel / rkab_nikel)
            + 0.15 * (prod_emas / rkab_emas)
            + 0.20 * (lifting_minyak / target_lifting_minyak)
        )
        * 100.0,
        2,
    )

    # -------------------------------------------------------------------------
    # BLOK C: HILIRISASI SMELTER, EKSPOR OLAHAN & PNBP MINERBA (KATEGORI C)
    # -------------------------------------------------------------------------
    # 10. Investasi Smelter & Hilirisasi Mineral (Triliun Rp / Kuartal)
    inv_smelter = np.round(
        8.5
        + 0.48 * t
        + 1.35 * np.maximum(0.0, t - 26)
        + 0.0008 * (nickel_price - 14000.0)
        - 1.2 * (bi_rate - 5.5)
        + np.random.normal(0, 1.2, n),
        2,
    )
    inv_smelter = np.clip(inv_smelter, 6.0, 145.0)
    if n >= 67:
        inv_smelter[64:67] = [68.5, 71.2, 74.0]

    # 11. Nilai Ekspor Produk Hilirisasi Mineral (FeNi, NPI, MHP, Katoda - Miliar USD / Kuartal)
    ekspor_hilir = np.round(
        1.20
        + 0.06 * t
        + 0.165 * prod_nikel
        + 0.06 * inv_smelter
        + 0.00018 * (nickel_price - 15000.0)
        + np.random.normal(0, 0.35, n),
        2,
    )
    ekspor_hilir = np.clip(ekspor_hilir, 0.8, 30.0)
    if n >= 67:
        ekspor_hilir[64:67] = [14.8, 15.4, 16.1]

    # 12. Penerimaan Negara PNBP & Royalti Minerba (Triliun Rp / Kuartal)
    pnbp_minerba = np.round(
        5.5
        + 0.095 * prod_batubara * (coal_price / 100.0)
        + 0.18 * prod_nikel * (nickel_price / 16000.0)
        + 0.12 * prod_emas * (gold_price / 1800.0)
        + 0.35 * ekspor_hilir
        + np.random.normal(0, 1.1, n),
        2,
    )

    # -------------------------------------------------------------------------
    # BLOK D: PDB HULU TAMBANG (KAT. B), PDB HILIR LOGAM DASAR (KAT. C) & PDB NASIONAL
    # -------------------------------------------------------------------------
    # 13. PDB Sektor Pertambangan & Penggalian (Kategori B - Triliun Rp)
    pdb_hulu_tambang = np.round(
        145.0
        + 0.82 * prod_batubara
        + 1.15 * prod_nikel
        + 1.40 * prod_emas
        + 0.22 * coal_price
        + 0.015 * gold_price
        + 0.0035 * (kurs_idr - 10000.0)
        + np.random.normal(0, 3.2, n),
        2,
    )

    # 14. PDB Sektor Industri Pengolahan Logam Dasar & Smelter (Kategori C - Triliun Rp)
    pdb_hilir_logam = np.round(
        28.0
        + 1.65 * prod_nikel
        + 1.42 * inv_smelter
        + 4.85 * ekspor_hilir
        + 0.0018 * (nickel_price - 14000.0)
        + np.random.normal(0, 2.4, n),
        2,
    )

    # 15. Total Investasi Nasional (PMTB Triliun Rp) & Total Ekspor Nasional (Miliar USD)
    investasi_total = np.round(
        520.0
        + 13.5 * t
        + 2.15 * inv_smelter
        - 11.5 * (bi_rate - 5.5)
        - 80.0 * np.exp(-((t - 41) / 2.2) ** 2)
        + np.random.normal(0, 9.5, n),
        2,
    )
    ekspor_total = np.round(
        34.0
        + 0.32 * t
        + 1.15 * ekspor_hilir
        + 0.08 * prod_batubara * (coal_price / 100.0)
        + 0.14 * (oil_price - 70.0)
        - 7.5 * np.exp(-((t - 41) / 2.0) ** 2)
        + np.random.normal(0, 1.2, n),
        2,
    )

    # 16. PDB Nasional Riil (Triliun Rp / Kuartal) = PDB Hulu Tambang + PDB Hilir Logam + Spillover + Sektor Lainnya
    pdb_non_tambang = (
        1420.0
        + 29.5 * t
        + 0.38 * investasi_total
        + 1.65 * ekspor_total
        + 0.85 * pnbp_minerba
        - 0.032 * (kurs_idr - 10000.0)
        - 16.5 * bi_rate
        - 8.4 * inflasi
        - 0.45 * np.maximum(0, oil_price - 85.0)  # Beban subsidi/impor BBM saat minyak mahal
        - 185.0 * np.exp(-((t - 41) / 2.0) ** 2)  # Kontraksi pandemi 2020
        + np.random.normal(0, 10.5, n)
    )
    # Spillover hilirisasi (multiplier 1.45x dari industri logam dasar ke listrik, konstruksi, logistik)
    pdb_riil = np.round(pdb_hulu_tambang + 1.45 * pdb_hilir_logam + pdb_non_tambang, 2)

    # 17. Pertumbuhan Ekonomi / PDB YoY (%)
    pdb_growth = np.zeros(n)
    for i in range(n):
        if i < 4:
            pdb_growth[i] = round(5.65 + 0.015 * (coal_price[i] - 85) - 0.12 * (bi_rate[i] - 6.0), 2)
        else:
            pdb_growth[i] = round(((pdb_riil[i] - pdb_riil[i - 4]) / pdb_riil[i - 4]) * 100.0, 2)
    if n >= 67:
        pdb_growth[61:67] = [5.05, 5.08, 5.11, 5.14, 5.15, 5.18]

    df = pd.DataFrame({
        "Periode": periods,
        "PDB_Riil_Triliun_Rp": pdb_riil,
        "Pertumbuhan_PDB_Persen": pdb_growth,
        "PDB_Hulu_Tambang_Triliun_Rp": pdb_hulu_tambang,
        "PDB_Hilir_Logam_Dasar_Triliun_Rp": pdb_hilir_logam,
        "Produksi_Batubara_Juta_Ton": prod_batubara,
        "Kuota_RKAB_Batubara_Juta_Ton": rkab_batubara,
        "Produksi_Bijih_Nikel_Juta_WMT": prod_nikel,
        "Kuota_RKAB_Nikel_Juta_WMT": rkab_nikel,
        "Produksi_Emas_Ton": prod_emas,
        "Kuota_RKAB_Emas_Ton": rkab_emas,
        "Produksi_Bijih_Tembaga_Juta_Ton": prod_tembaga,
        "Kuota_RKAB_Tembaga_Juta_Ton": rkab_tembaga,
        "Produksi_Bauksit_Juta_WMT": prod_bauksit,
        "Kuota_RKAB_Bauksit_Juta_WMT": rkab_bauksit,
        "Produksi_Timah_Ribu_Ton": prod_timah,
        "Kuota_RKAB_Timah_Ribu_Ton": rkab_timah,
        "Lifting_Minyak_Ribu_Bph": lifting_minyak,
        "Target_Lifting_Minyak_Ribu_Bph": target_lifting_minyak,
        "Lifting_Gas_Bumi_MMSCFD": lifting_gas,
        "Target_Lifting_Gas_MMSCFD": target_lifting_gas,
        "Rasio_Realisasi_RKAB_Persen": rasio_rkab_pct,
        "Harga_Batubara_HBA_USD": coal_price,
        "Harga_Nikel_LME_USD": nickel_price,
        "Harga_Emas_USD_Oz": gold_price,
        "Harga_Minyak_ICP_USD": oil_price,
        "Investasi_Smelter_PMTB_Triliun_Rp": inv_smelter,
        "Ekspor_Hilirisasi_Mineral_Miliar_USD": ekspor_hilir,
        "PNBP_Royalti_Minerba_Triliun_Rp": pnbp_minerba,
        "Kurs_USD_IDR": kurs_idr,
        "Inflasi_IHK_Persen": inflasi,
        "Suku_Bunga_BI_Rate_Persen": bi_rate,
        "Investasi_PMTB_Triliun_Rp": investasi_total,
        "Ekspor_Miliar_USD": ekspor_total,
    })
    return df


def build_annual_rkab_realization_history_df(df_q: pd.DataFrame) -> pd.DataFrame:
    """
    Merekapitulasi Data Historis Tahunan (2010 s.d. Tahun Terupdate Auto-Rolling)
    antara Kuota RKAB / Target APBN vs Realisasi Produksi 6 Mineral Utama & Hulu Migas.
    Untuk tahun berjalan yang belum genap 4 kuartal, nilai volume di-annualize (x 4/N_kuartal)
    agar perbandingan tahunan apel-ke-apel.
    """
    if df_q is None or len(df_q) == 0:
        return pd.DataFrame()

    tmp = df_q.copy()
    tmp["Tahun"] = tmp["Periode"].astype(str).str.slice(0, 4).astype(int)
    rows = []
    for yr, grp in tmp.groupby("Tahun"):
        nq = len(grp)
        scale = 4.0 / nq if nq > 0 else 1.0
        status_yr = "Aktual Penuh (4Q)" if nq == 4 else f"Berjalan ({nq}Q Annualized)"

        coal_real = float(grp["Produksi_Batubara_Juta_Ton"].sum() * scale)
        coal_rkab = float(
            grp["Kuota_RKAB_Batubara_Juta_Ton"].sum() * scale
            if "Kuota_RKAB_Batubara_Juta_Ton" in grp.columns
            else coal_real * 1.05
        )
        ni_real = float(grp["Produksi_Bijih_Nikel_Juta_WMT"].sum() * scale)
        ni_rkab = float(
            grp["Kuota_RKAB_Nikel_Juta_WMT"].sum() * scale
            if "Kuota_RKAB_Nikel_Juta_WMT" in grp.columns
            else ni_real * 1.06
        )
        au_real = float(grp["Produksi_Emas_Ton"].sum() * scale)
        au_rkab = float(
            grp["Kuota_RKAB_Emas_Ton"].sum() * scale
            if "Kuota_RKAB_Emas_Ton" in grp.columns
            else au_real * 1.05
        )
        cu_real = float(
            grp["Produksi_Bijih_Tembaga_Juta_Ton"].sum() * scale
            if "Produksi_Bijih_Tembaga_Juta_Ton" in grp.columns
            else 115.0
        )
        cu_rkab = float(
            grp["Kuota_RKAB_Tembaga_Juta_Ton"].sum() * scale
            if "Kuota_RKAB_Tembaga_Juta_Ton" in grp.columns
            else cu_real * 1.06
        )
        bx_real = float(
            grp["Produksi_Bauksit_Juta_WMT"].sum() * scale
            if "Produksi_Bauksit_Juta_WMT" in grp.columns
            else 32.0
        )
        bx_rkab = float(
            grp["Kuota_RKAB_Bauksit_Juta_WMT"].sum() * scale
            if "Kuota_RKAB_Bauksit_Juta_WMT" in grp.columns
            else bx_real * 1.08
        )
        sn_real = float(
            grp["Produksi_Timah_Ribu_Ton"].sum() * scale
            if "Produksi_Timah_Ribu_Ton" in grp.columns
            else 65.0
        )
        sn_rkab = float(
            grp["Kuota_RKAB_Timah_Ribu_Ton"].sum() * scale
            if "Kuota_RKAB_Timah_Ribu_Ton" in grp.columns
            else sn_real * 1.07
        )
        oil_real = float(
            grp["Lifting_Minyak_Ribu_Bph"].mean()
            if "Lifting_Minyak_Ribu_Bph" in grp.columns
            else 605.0
        )
        oil_target = float(
            grp["Target_Lifting_Minyak_Ribu_Bph"].mean()
            if "Target_Lifting_Minyak_Ribu_Bph" in grp.columns
            else 620.0
        )
        gas_real = float(
            grp["Lifting_Gas_Bumi_MMSCFD"].mean()
            if "Lifting_Gas_Bumi_MMSCFD" in grp.columns
            else 5950.0
        )
        gas_target = float(
            grp["Target_Lifting_Gas_MMSCFD"].mean()
            if "Target_Lifting_Gas_MMSCFD" in grp.columns
            else 6150.0
        )
        rasio_avg = float(
            grp["Rasio_Realisasi_RKAB_Persen"].mean()
            if "Rasio_Realisasi_RKAB_Persen" in grp.columns
            else 94.5
        )

        rows.append({
            "Tahun": yr,
            "Status Data": status_yr,
            "RKAB Batubara (Jt Ton)": round(coal_rkab, 1),
            "Realisasi Batubara (Jt Ton)": round(coal_real, 1),
            "RKAB Nikel (Jt WMT)": round(ni_rkab, 1),
            "Realisasi Nikel (Jt WMT)": round(ni_real, 1),
            "RKAB Tembaga (Jt Ton)": round(cu_rkab, 1),
            "Realisasi Tembaga (Jt Ton)": round(cu_real, 1),
            "RKAB Emas (Ton)": round(au_rkab, 1),
            "Realisasi Emas (Ton)": round(au_real, 1),
            "RKAB Bauksit (Jt WMT)": round(bx_rkab, 1),
            "Realisasi Bauksit (Jt WMT)": round(bx_real, 1),
            "RKAB Timah (Ribu Ton)": round(sn_rkab, 1),
            "Realisasi Timah (Ribu Ton)": round(sn_real, 1),
            "Target APBN Minyak (Ribu Bph)": round(oil_target, 1),
            "Realisasi Lifting Minyak (Ribu Bph)": round(oil_real, 1),
            "Target APBN Gas (MMSCFD)": round(gas_target, 0),
            "Realisasi Lifting Gas (MMSCFD)": round(gas_real, 0),
            "Rasio Realisasi Komposit (%)": round(rasio_avg, 2),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    df_macro = generate_macro_dataset()
    csv_path = os.path.join(data_dir, "data_makro_indonesia_pdb.csv")
    xlsx_path = os.path.join(data_dir, "data_makro_indonesia_pdb.xlsx")
    df_macro.to_csv(csv_path, index=False)
    df_macro.to_excel(xlsx_path, index=False)
    print(f"Dataset Makro-Minerba, RKAB, Lifting Migas & Hilirisasi 2010Q1-{df_macro['Periode'].iloc[-1]} selesai dibuat: {len(df_macro)} kuartal, {len(df_macro.columns)} variabel.")
