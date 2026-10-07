# -*- coding: utf-8 -*-
"""
Modul Menu Khusus: Panduan Lengkap, Kamus Istilah Tambang-Hilirisasi-Makro,
Cara Membaca Grafik, Sensitivity & Stress Test, Kamus Statistik Ekonometrika,
& Spesifikasi Metodologi Model (MODUL 17 — www.trilaksanamining.my.id).
Dr. Ir. Ahmad Raymond Trilaksana, S.T., M.Ak., IPM, ASEAN Eng.
"""

import pandas as pd
import streamlit as st


def render_panduan_lengkap():
    """Merender Menu Khusus berisi seluruh penjelasan detail aplikasi Modul 17."""
    st.subheader("📖 Pusat Penjelasan Lengkap: Kamus Sektor Tambang, Variabel, Grafik, Stress Test & Metodologi Ekonometrika")
    st.markdown(
        "Menu khusus pada **MODUL 17 (`www.trilaksanamining.my.id`)** ini disusun sebagai **Pedoman Referensi Lengkap** "
        "untuk memahami **arti setiap istilah, struktur sektor PDB BPS (Lapangan Usaha A–U serta Kategori B vs Kategori C), "
        "cara kerja simulasi simultan 4-blok (2025–2030), uji validasi *Backtesting* 2025, *Sensitivity & Stress Test*, hingga spesifikasi matematis ekonometrika**."
    )

    sub_tabs = st.tabs([
        "⛏️ 1. Hulu (Kat. B) vs Hilir (Kat. C)",
        "📚 2. Kamus 20 Variabel & Satuan",
        "📊 3. Panduan Grafik & Stress Test",
        "🔬 4. Kamus Statistik Ekonometrika",
        "🧮 5. Rumus Matematika & Spesifikasi Model",
    ])

    # =========================================================================
    # SUB-TAB 1: KATEGORI B VS KATEGORI C & ALUR 4 BLOK RANTAI NILAI
    # =========================================================================
    with sub_tabs[0]:
        st.markdown("### 🏛️ Mengapa Dibedakan antara **Kategori B (Hulu)** dan **Kategori C (Hilirisasi)**?")
        st.info(
            "💡 **Inti Konsep BPS (KBLI):** Dalam perhitungan resmi Produk Domestik Bruto (PDB) oleh **Badan Pusat Statistik (BPS)** "
            "berdasarkan *Klasifikasi Baku Lapangan Usaha Indonesia (KBLI)*, seluruh kegiatan ekonomi dibagi ke dalam **17 Kategori Huruf (A sampai U)**. "
            "Sektor pertambangan dan hilirisasi mineral terbagi ke dalam **dua kategori berbeda** tergantung pada **apakah mineral tersebut masih mentah atau sudah masuk pabrik pengolahan (Smelter)**."
        )

        col_b, col_c = st.columns(2)
        with col_b:
            st.markdown(
                """
                <div class="exec-card" style="border-left: 4px solid #38bdf8;">
                    <h4>1️⃣ Kategori B: PDB Pertambangan & Penggalian (Hulu / Raw Material)</h4>
                    <p style="font-size:0.93rem; color:#e2e8f0; line-height:1.6;">
                        <b>Definisi Resmi BPS:</b> Mencakup kegiatan penggalian, pengeboran, dan pengambilan komoditas mineral/batubara/migas
                        langsung dari perut bumi hingga siap dipasarkan dalam bentuk <b>bahan mentah (raw ore / ROM / washed coal)</b>.<br><br>
                        <b>Contoh Kegiatan & Produk di Lapangan:</b><br>
                        • <b>Batubara:</b> Pengupasan <i>overburden</i>, penggalian batubara (<i>pit-to-port</i>), <i>crushing</i>, hingga pemuatan ke tongkang.<br>
                        • <b>Bijih Nikel (Nickel Ore):</b> Penambangan bijih nikel mentah kadar tinggi (<i>Saprolite</i>) maupun kadar rendah (<i>Limonite</i>) sebelum masuk tungku smelter.<br>
                        • <b>Tembaga & Emas Hulu:</b> Penambangan bijih tembaga-emas (<i>ore & concentrate</i>) sebelum pemurnian anoda/katoda.<br>
                        • <b>Migas:</b> Lifting minyak mentah (<i>crude oil</i>) dan gas bumi.<br><br>
                        <b>Karakteristik Ekonomi:</b> Sangat bergantung pada <b>Kuota RKAB (Volume X)</b> dan fluktuasi harga komoditas mentah dunia. Nilai tambah per ton relatif rendah.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_c:
            st.markdown(
                """
                <div class="exec-card" style="border-left: 4px solid #10b981;">
                    <h4>2️⃣ Kategori C: PDB Industri Pengolahan Logam Dasar (Hilirisasi Smelter — KBLI 24)</h4>
                    <p style="font-size:0.93rem; color:#e2e8f0; line-height:1.6;">
                        <b>Definisi Resmi BPS:</b> Begitu bijih tambang masuk ke gerbang pabrik <b>Smelter</b> untuk dilebur atau dimurnikan secara kimia/metalurgi,
                        maka nilai tambahnya <b>TIDAK LAGI dicatat di Kategori B (Tambang)</b>, melainkan berpindah ke <b>Kategori C (Industri Pengolahan — Subsektor Industri Logam Dasar KBLI 24)</b>.<br><br>
                        <b>Contoh Kegiatan & Produk di Lapangan:</b><br>
                        • <b>Smelter Pirometalurgi (RKEF):</b> Mengolah bijih nikel <i>Saprolite</i> menjadi <i>Nickel Pig Iron (NPI)</i>, <i>Ferronickel (FeNi)</i>, <i>Nickel Matte</i>, dan <i>Stainless Steel Slab</i>.<br>
                        • <b>Smelter Hidrometalurgi (HPAL):</b> Mengolah bijih nikel kadar rendah <i>Limonite</i> menjadi <i>Mixed Hydroxide Precipitate (MHP)</i>, <i>Nickel Sulfate</i>, dan prekursor katoda baterai mobil listrik (EV).<br>
                        • <b>Smelter Tembaga & Pemurnian Logam Mulia:</b> Mengolah konsentrat menjadi <i>Katoda Tembaga (99,99%)</i>, <i>Emas Batangan Murni (Gold Bullion)</i>, Perak, dan Asam Sulfat.<br>
                        • <b>Smelter Bauksit:</b> Mengolah bauksit menjadi <i>Smelter Grade Alumina (SGA)</i> dan <i>Aluminium Ingot</i>.<br><br>
                        <b>Karakteristik Ekonomi:</b> Memiliki efek <b>Value-Added Multiplier 4x hingga 10x lipat</b> dibanding ekspor bijih mentah.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("### 📈 Tabel Lonjakan Nilai Tambah (*Value-Added Multiplier*) dari Kategori B ke Kategori C")
        va_df = pd.DataFrame([
            {
                "Rantai Komoditas": "Nikel Jalur Baja Tahan Karat (RKEF)",
                "Produk Hulu (Kategori B - Tambang)": "Bijih Nikel Saprolite (~1.7%–1.8% Ni)",
                "Harga Indikatif Hulu": "~$35 – $48 / WMT",
                "Produk Hilir Smelter (Kategori C - KBLI 24)": "NPI / Ferronickel (FeNi) ➔ Stainless Steel",
                "Lonjakan Nilai Tambah (Multiplier)": "4,5x – 7,5x Lipat (FeNi) hingga 10x (Stainless Steel)",
            },
            {
                "Rantai Komoditas": "Nikel Jalur Baterai EV (HPAL)",
                "Produk Hulu (Kategori B - Tambang)": "Bijih Nikel Limonite (~1.1%–1.3% Ni)",
                "Harga Indikatif Hulu": "~$18 – $25 / WMT",
                "Produk Hilir Smelter (Kategori C - KBLI 24)": "MHP (Mixed Hydroxide Precipitate) ➔ Nickel Sulfate ➔ Prekursor Katoda",
                "Lonjakan Nilai Tambah (Multiplier)": "6,0x – 11,5x Lipat",
            },
            {
                "Rantai Komoditas": "Tembaga & Emas (Copper-Gold Smelting)",
                "Produk Hulu (Kategori B - Tambang)": "Konsentrat Tembaga (~25%–30% Cu + Au/Ag)",
                "Harga Indikatif Hulu": "Harga Konsentrat (Dipotong TC/RC)",
                "Produk Hilir Smelter (Kategori C - KBLI 24)": "Katoda Tembaga LME Grade A (99,99%) + Lumpur Anoda (Emas & Perak Murni)",
                "Lonjakan Nilai Tambah (Multiplier)": "2,5x – 4,0x Lipat + Retensi Devisa Emas Murni di Dalam Negeri",
            },
            {
                "Rantai Komoditas": "Bauksit & Aluminium",
                "Produk Hulu (Kategori B - Tambang)": "Washed Bauxite Ore",
                "Harga Indikatif Hulu": "~$35 – $50 / Ton",
                "Produk Hilir Smelter (Kategori C - KBLI 24)": "Smelter Grade Alumina (SGA) ➔ Aluminium Ingot",
                "Lonjakan Nilai Tambah (Multiplier)": "5,0x – 9,0x Lipat",
            },
        ])
        st.dataframe(va_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 🔗 Penjelasan 4-Blok Simulasi Simultan pada Grafik *Waterfall*")
        st.markdown(
            """
            Ketika Bapak menggeser *slider* pada **Tab 2 (Simulator)**, mesin aplikasi tidak hanya mengalikan angka secara sederhana, melainkan menghitung **4 Blok Rantai Ekonomi secara berurutan (Simultan)**:
            1. **Blok 1 — PDB Hulu Pertambangan (Kategori B):**
               Dihitung dari kombinasi **Volume Produksi Kuota RKAB ($X$)** (Batubara Juta Ton, Bijih Nikel Juta WMT, Emas Ton) dikalikan **Harga Komoditas Dunia ($Y$)** (HBA, LME Nickel, Spot Gold, ICP Oil) serta dipengaruhi **Kurs Rupiah**.
               *Catatan Penting:* Jika kuota RKAB dipangkas (misal skenario nomor 4), maka PDB Kategori B bisa tampak turun sedikit, namun penurunan volume hulu sering kali dikompensasi oleh kenaikan harga jual dan serapan smelter hilir.
            2. **Blok 2 — PDB Hilirisasi Logam Dasar / Smelter (Kategori C):**
               Dihitung dari seberapa besar bijih tambang yang diserap oleh pabrik smelter domestik (dipicu oleh **Investasi CapEx Smelter**, **Pasokan Bijih Nikel & Emas-Tembaga**, serta **Harga Logam LME**). Di sinilah lonjakan nilai tambah ratusan triliun rupiah terjadi.
            3. **Blok 3 — Efek Pengganda (*Multiplier & Spillover Effect*) + PNBP Minerba:**
               Kawasan industri tambang & smelter (seperti di Morowali, Weda Bay, Konawe, Obi, Gresik, Sumbawa) tidak berdiri sendiri. Setiap Rp 1 Triliun aktivitas hulu & smelter menciptakan *efek berantai* ke:
               * **Pembangkitan Listrik Industri** (Kategori D),
               * **Konstruksi Kawasan Industri & Pelabuhan Khusus/Jetty** (Kategori F),
               * **Jasa Logistik, Perkapalan Tongkang, Perbankan & Tenaga Kerja Lokal** (Kategori G, H, K),
               * **Penerimaan Negara Bukan Pajak (PNBP) & Royalti Minerba** yang dibelanjakan kembali oleh Pemerintah Pusat & Daerah (Dana Bagi Hasil / DBH Tambang).
            4. **Blok 4 — Sektor Ekonomi Lainnya & Total Proyeksi PDB Nasional 2026:**
               Menggabungkan sumbangan rantai nilai pertambangan-hilirisasi (Blok 1 + Blok 2 + Blok 3) dengan sektor ekonomi domestik lainnya (konsumsi rumah tangga, pertanian, jasa, yang dipengaruhi oleh **BI-Rate**, **Inflasi**, dan **Harga Minyak ICP**) untuk menghasilkan **Proyeksi PDB Riil Nasional 2026 (Triliun Rupiah)** dan **Persentase Pertumbuhan Ekonomi (%)**.
            """
        )

    # =========================================================================
    # SUB-TAB 2: KAMUS LENGKAP 20 VARIABEL & SATUAN TAMBANG
    # =========================================================================
    with sub_tabs[1]:
        st.markdown("### 📚 Kamus Lengkap 20 Variabel di Dalam Aplikasi (Definisi, Satuan, Sumber & Arah Pengaruh)")
        st.markdown(
            "Tabel berikut menjelaskan arti setiap nama kolom/variabel yang ada di *Sidebar*, *Tabel Data*, maupun *Simulator*:"
        )

        var_dict_df = pd.DataFrame([
            {
                "Kelompok": "1. Variabel Target (Y)",
                "Nama Variabel di Aplikasi": "PDB_Riil_Triliun_Rp",
                "Satuan": "Triliun Rupiah (ADHK)",
                "Sumber Data Acuan": "BPS Nasional",
                "Penjelasan Lengkap & Makna Ekonomi": "Produk Domestik Bruto (PDB) Riil atas dasar harga konstan (ADHK) per kuartal. Mengukur total nilai barang & jasa riil yang diproduksi seluruh Indonesia setelah menghilangkan efek inflasi.",
            },
            {
                "Kelompok": "1. Variabel Target (Y)",
                "Nama Variabel di Aplikasi": "Pertumbuhan_PDB_YoY_Persen",
                "Satuan": "Persen (% YoY)",
                "Sumber Data Acuan": "BPS Nasional",
                "Penjelasan Lengkap & Makna Ekonomi": "Laju pertumbuhan ekonomi Indonesia dibandingkan kuartal/tahun sebelumnya (Year-on-Year). Contoh: angka 5,18% berarti output riil ekonomi tumbuh 5,18%.",
            },
            {
                "Kelompok": "2. Sektor PDB Tambang & Hilir",
                "Nama Variabel di Aplikasi": "PDB_Pertambangan_Hulu_Triliun_Rp",
                "Satuan": "Triliun Rupiah",
                "Sumber Data Acuan": "BPS (Kategori B)",
                "Penjelasan Lengkap & Makna Ekonomi": "Nilai tambah bruto dari kegiatan penggalian komoditas tambang mentah (Batubara, Bijih Nikel, Bijih Tembaga-Emas, Bauksit, Migas) sebelum masuk industri pengolahan.",
            },
            {
                "Kelompok": "2. Sektor PDB Tambang & Hilir",
                "Nama Variabel di Aplikasi": "PDB_Hilirisasi_Logam_Triliun_Rp",
                "Satuan": "Triliun Rupiah",
                "Sumber Data Acuan": "BPS (Kategori C - KBLI 24)",
                "Penjelasan Lengkap & Makna Ekonomi": "Nilai tambah bruto dari industri pemurnian & peleburan mineral di pabrik Smelter (FeNi, NPI, Nickel Matte, MHP, Stainless Steel, Katoda Tembaga, Emas Murni, Alumina).",
            },
            {
                "Kelompok": "3. Volume Produksi Tambang (X)",
                "Nama Variabel di Aplikasi": "Produksi_Batubara_Juta_Ton",
                "Satuan": "Juta Metric Ton (MT)",
                "Sumber Data Acuan": "Kementerian ESDM (MODI)",
                "Penjelasan Lengkap & Makna Ekonomi": "Realisasi volume produksi batubara nasional berdasarkan kuota RKAB (Rencana Kerja dan Anggaran Biaya), baik untuk kebutuhan DMO (PLN/Industri domestik) maupun ekspor.",
            },
            {
                "Kelompok": "3. Volume Produksi Tambang (X)",
                "Nama Variabel di Aplikasi": "Produksi_Bijih_Nikel_Juta_WMT",
                "Satuan": "Juta WMT (Wet Metric Ton)",
                "Sumber Data Acuan": "Kementerian ESDM / APNI",
                "Penjelasan Lengkap & Makna Ekonomi": "Volume produksi bijih nikel basah (Wet Metric Ton - masih mengandung kadar air/moisture content ~30-35%), baik jenis Saprolite (umpan smelter RKEF) maupun Limonite (umpan smelter HPAL).",
            },
            {
                "Kelompok": "3. Volume Produksi Tambang (X)",
                "Nama Variabel di Aplikasi": "Produksi_Emas_Ton",
                "Satuan": "Ton Logam Murni (Au)",
                "Sumber Data Acuan": "Kementerian ESDM",
                "Penjelasan Lengkap & Makna Ekonomi": "Volume produksi emas nasional (baik dari tambang emas primer maupun produk ikutan/by-product dari tambang porfiri tembaga-emas seperti Grasberg dan Batu Hijau).",
            },
            {
                "Kelompok": "4. Harga Komoditas Dunia (Y)",
                "Nama Variabel di Aplikasi": "Harga_Batubara_HBA_USD_Ton",
                "Satuan": "USD / Metric Ton",
                "Sumber Data Acuan": "ESDM (HBA) & Yahoo Finance (MTF=F)",
                "Penjelasan Lengkap & Makna Ekonomi": "Harga Batubara Acuan (HBA) Indonesia / patokan Newcastle Global Coal. Kenaikan harga batubara meningkatkan pendapatan ekspor, royalti PNBP, dan PDB Kategori B.",
            },
            {
                "Kelompok": "4. Harga Komoditas Dunia (Y)",
                "Nama Variabel di Aplikasi": "Harga_Nikel_LME_USD_Ton",
                "Satuan": "USD / Metric Ton",
                "Sumber Data Acuan": "London Metal Exchange (LME)",
                "Penjelasan Lengkap & Makna Ekonomi": "Harga patokan nikel murni dunia di bursa LME London. Menjadi acuan penentuan Harga Patokan Mineral (HPM) bijih nikel domestik serta harga jual produk olahan FeNi/NPI/MHP.",
            },
            {
                "Kelompok": "4. Harga Komoditas Dunia (Y)",
                "Nama Variabel di Aplikasi": "Harga_Emas_USD_Oz",
                "Satuan": "USD / Troy Ounce (t.oz)",
                "Sumber Data Acuan": "LBMA / COMEX Gold (GC=F)",
                "Penjelasan Lengkap & Makna Ekonomi": "Harga emas dunia per troy ounce (1 troy ounce = 31,1035 gram). Berperan ganda sebagai komoditas ekspor bernilai tinggi dan aset lindung nilai (safe haven) cadangan devisa.",
            },
            {
                "Kelompok": "4. Harga Komoditas Dunia (Y)",
                "Nama Variabel di Aplikasi": "Harga_Minyak_ICP_USD_Barel",
                "Satuan": "USD / Barel",
                "Sumber Data Acuan": "ESDM (ICP) & Brent Crude (BZ=F)",
                "Penjelasan Lengkap & Makna Ekonomi": "Indonesian Crude Price / Harga minyak mentah dunia. Karena Indonesia adalah net-importir BBM, lonjakan harga minyak di atas batas ekstrem justru menjadi faktor risiko penekan PDB (beban subsidi & biaya logistik).",
            },
            {
                "Kelompok": "5. Hilirisasi & Fiskal Minerba",
                "Nama Variabel di Aplikasi": "Investasi_Smelter_Hilirisasi_Triliun_Rp",
                "Satuan": "Triliun Rupiah",
                "Sumber Data Acuan": "Kementerian Investasi/BKPM & ESDM",
                "Penjelasan Lengkap & Makna Ekonomi": "Belanja modal (Capital Expenditure / CapEx) pembangunan pabrik pemurnian mineral (Smelter RKEF, HPAL, Copper Smelter, Alumina) beserta infrastruktur kawasan industri.",
            },
            {
                "Kelompok": "5. Hilirisasi & Fiskal Minerba",
                "Nama Variabel di Aplikasi": "Ekspor_Olahan_Mineral_Miliar_USD",
                "Satuan": "Miliar USD",
                "Sumber Data Acuan": "BPS & Kemendag (HS 72, 74, 75, 28)",
                "Penjelasan Lengkap & Makna Ekonomi": "Nilai devisa ekspor produk hilirisasi mineral (Besi-Baja/Stainless Steel HS 72, Nikel Olahan/FeNi/Matte HS 75, Bahan Kimia Baterai/MHP HS 28, Katoda Tembaga HS 74).",
            },
            {
                "Kelompok": "5. Hilirisasi & Fiskal Minerba",
                "Nama Variabel di Aplikasi": "PNBP_Royalti_Minerba_Triliun_Rp",
                "Satuan": "Triliun Rupiah",
                "Sumber Data Acuan": "Kemenkeu & Ditjen Minerba ESDM",
                "Penjelasan Lengkap & Makna Ekonomi": "Penerimaan Negara Bukan Pajak (PNBP) dari sektor mineral dan batubara, terdiri dari Iuran Tetap (Landrent), Royalti Produksi, dan Penjualan Hasil Tambang (PHT).",
            },
            {
                "Kelompok": "6. Makroekonomi & Moneter",
                "Nama Variabel di Aplikasi": "Kurs_USD_IDR",
                "Satuan": "Rupiah per 1 USD",
                "Sumber Data Acuan": "Bank Indonesia (JISDOR) & Yahoo Finance (IDR=X)",
                "Penjelasan Lengkap & Makna Ekonomi": "Nilai tukar Rupiah terhadap Dolar AS. Depresiasi Rupiah yang moderat meningkatkan nilai konversi ekspor komoditas dalam Rupiah, namun depresiasi ekstrem memicu inflasi barang impor (imported inflation).",
            },
            {
                "Kelompok": "6. Makroekonomi & Moneter",
                "Nama Variabel di Aplikasi": "Inflasi_Tahunan_Persen",
                "Satuan": "Persen (% YoY)",
                "Sumber Data Acuan": "BPS & Bank Indonesia",
                "Penjelasan Lengkap & Makna Ekonomi": "Laju kenaikan Indeks Harga Konsumen (IHK). Inflasi yang terkendali di kisaran sasaran BI (2,5% ± 1%) menjaga daya beli masyarakat.",
            },
            {
                "Kelompok": "6. Makroekonomi & Moneter",
                "Nama Variabel di Aplikasi": "Suku_Bunga_BI_Rate_Persen",
                "Satuan": "Persen (%)",
                "Sumber Data Acuan": "Bank Indonesia (BI-Rate)",
                "Penjelasan Lengkap & Makna Ekonomi": "Suku bunga kebijakan moneter Bank Indonesia. Kenaikan BI-Rate digunakan untuk meredam inflasi dan menjaga Rupiah, namun jika terlalu tinggi dapat meningkatkan biaya bunga kredit investasi.",
            },
        ])
        st.dataframe(var_dict_df, use_container_width=True, hide_index=True)

    # =========================================================================
    # SUB-TAB 3: CARA MEMBACA GRAFIK & 4 SKENARIO KEBIJAKAN 2026
    # =========================================================================
    with sub_tabs[2]:
        st.markdown("### 📊 Panduan Praktis Membaca Grafik Visual di Tab 1 & Tab 2")

        g1, g2 = st.columns(2)
        with g1:
            st.markdown(
                """
                #### 1. Speedometer Proyeksi Pertumbuhan PDB 2026
                * **Angka Biru Besar di Tengah:** Adalah proyeksi laju pertumbuhan PDB Indonesia tahun 2026 (%) berdasarkan skenario yang sedang aktif.
                * **Angka Segitiga Kecil ($\\Delta$) di Bawahnya:** Menunjukkan selisih kenaikan/penurunan pertumbuhan dibandingkan **Baseline Aktual 2026 (`5,18%`)**.
                * **Zona Warna pada Busur Speedometer:**
                  * 🔴 **Zona Merah (`3,5% – 4,7%`):** Zona perlambatan ekonomi (waspada guncangan eksternal).
                  * 🔵 **Zona Biru (`4,7% – 5,3%`):** Zona pertumbuhan normal/moderat sesuai tren historis RPJMN.
                  * 🟢 **Zona Hijau (`5,3% – 6,5%+`):** Zona akselerasi tinggi yang didorong oleh *booming* hilirisasi mineral dan investasi.
                * **Garis Kuning pada Busur:** Penanda batas skenario optimis standar.

                #### 2. Grafik *Tornado Sensitivity* (Urutan Variabel Paling Berpengaruh)
                * Mengurutkan variabel dari atas ke bawah berdasarkan **Bobot Pengaruh Terstandarisasi (*Standardized Beta Coefficient*)**.
                * Mengapa pakai *Standardized Beta*? Karena satuan tiap variabel berbeda-beda (ada yang Juta Ton, ada yang USD, ada yang Persen). Dengan distandarisasi ke dalam simpangan baku (*standard deviation*), kita bisa membandingkan secara adil (*apple-to-apple*) variabel mana yang paling kuat menggerakkan PDB.
                * **Batang Hijau ke Kanan (+):** Variabel pendorong pertumbuhan ekonomi.
                * **Batang Merah ke Kiri (-):** Variabel penekan/risiko ekonomi (misalnya lonjakan beban harga minyak impor atau pelemahan kurs yang memicu inflasi).
                """
            )

        with g2:
            st.markdown(
                """
                #### 3. Grafik *Fan Chart* Kontrafaktual (Dengan Hilirisasi vs Tanpa Hilirisasi)
                Grafik ini menjawab pertanyaan strategis kebijakan makroekonomi: ***"Seberapa besar kerugian PDB Indonesia apabila tidak melakukan kebijakan hilirisasi smelter?"***
                * **Garis Biru Tebal (`PDB Nasional Dengan Hilirisasi`):** Jalur aktual dan proyeksi PDB Indonesia dengan beroperasinya smelter RKEF, HPAL, dan pemurnian tembaga-emas.
                * **Garis Abu-abu Putus-putus (`Simulasi Tanpa Hilirisasi / Counterfactual`):** Simulasi ekonometrika seandainya Indonesia hanya mengekspor bijih mentah (*raw ore*) tanpa nilai tambah industri logam dasar (Kategori C). Selisih jarak vertikal antara garis biru dan garis putus-putus adalah **Bukti Kuantitatif Nilai Tambah Hilirisasi (ratusan triliun Rupiah per tahun)**.
                * **Pita Bayangan Atas (Hijau) & Bawah (Merah):** Rentang ketidakpastian (*confidence fan*) antara skenario Optimis dan Skenario Waspada di tahun 2026–2027.

                #### 4. Diagram *Waterfall* 4-Blok (Rantai Nilai Tambang ke PDB)
                Menampilkan bagaimana total PDB Nasional tahun 2026 sebesar **~Rp 20.000+ Triliun** tersusun dari:
                1. Batang ke-1: Sumbangan langsung **PDB Hulu Pertambangan (Kategori B)**.
                2. Batang ke-2: Sumbangan langsung **PDB Hilirisasi Smelter Logam (Kategori C)**.
                3. Batang ke-3: **Efek Pengganda (*Multiplier*)** ke sektor listrik, konstruksi, logistik, dan belanja pemerintah dari PNBP Minerba.
                4. Batang ke-4: Sumbangan **Sektor Ekonomi Lainnya** di luar rantai minerba.
                5. Batang Biru Terakhir: **Total Proyeksi PDB Riil Nasional 2026**.
                """
            )

        st.markdown("---")
        st.markdown("### 🎛️ Penjelasan 4 Tombol Skenario Otomatis pada Simulator (Tab 2)")
        scen_exp_df = pd.DataFrame([
            {
                "Tombol Skenario": "🔵 1. Kondisi Aktual 2026 (Baseline)",
                "Asumsi Produksi (X) & Harga (Y)": "Produksi Batubara ~790 Juta Ton, Bijih Nikel ~237 Juta WMT, Emas ~119 Ton, Harga aktual 2026, Investasi Smelter Rp 294 T.",
                "Makna Kebijakan": "Menggambarkan proyeksi dasar (baseline) ekonomi Indonesia tahun 2026 sebesar ~5,18% dengan laju hilirisasi berjalan sesuai tren saat ini.",
            },
            {
                "Tombol Skenario": "🟢 2. Booming Hilirisasi & EV (+18% Smelter)",
                "Asumsi Produksi (X) & Harga (Y)": "Pasokan bijih nikel ke smelter naik +15%, CapEx Smelter naik +18%, Harga Nikel LME menguat ke $19.800/ton, Emas $2.850/oz, Kurs stabil Rp 15.400.",
                "Makna Kebijakan": "Simulasi apabila seluruh proyek smelter HPAL (baterai EV) dan ekspansi RKEF/Tembaga beroperasi penuh di tengah naiknya permintaan kendaraan listrik dunia.",
            },
            {
                "Tombol Skenario": "🔴 3. Krisis Energi (Minyak $105 & Kurs 16.850)",
                "Asumsi Produksi (X) & Harga (Y)": "Harga minyak mentah melonjak ke $105/barel, Rupiah melemah ke Rp 16.850/USD, BI-Rate naik ke 6,50%, permintaan nikel global turun.",
                "Makna Kebijakan": "Stress-test (uji ketahanan) ekonomi nasional ketika terjadi krisis geopolitik global yang memicu lonjakan beban impor BBM dan pengetatan moneter.",
            },
            {
                "Tombol Skenario": "🟡 4. Kuota RKAB Dipangkas -12% & Harga Naik",
                "Asumsi Produksi (X) & Harga (Y)": "Kuota RKAB Batubara & Bijih Nikel dipangkas -12% untuk konservasi cadangan, yang memicu kenaikan harga batubara (+16%) & nikel dunia (+18%), disertai penyesuaian tarif royalti 12%.",
                "Makna Kebijakan": "Simulasi kebijakan pengendalian produksi (supply management) oleh Kementerian ESDM: membuktikan bahwa pengendalian kuota RKAB yang terukur dapat mendongkrak harga jual dunia dan menjaga penerimaan PNBP negara.",
            },
        ])
        st.dataframe(scen_exp_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 🌪️ Cara Membaca Uji Akurasi *Backtesting* 2025, *Sensitivity Matrix* & *Stress Test*")
        st.markdown(
            """
            * **1. Uji Akurasi *Backtesting* Tahun 2025 (Proyeksi vs Aktual BPS):**
              Membandingkan hasil tebakan rumus ekonometrika pada tahun 2025 (Kuartal Q1–Q4 dan Total 2025) langsung dengan **Data Realisasi Aktual BPS Tahun 2025**. Semakin kecil angka **MAPE (*Mean Absolute Percentage Error*)** di bawah 1% (Tingkat Akurasi > 99%), semakin sahih model tersebut dipakai meramal tahun **2026–2030**.
            * **2. Matriks Sensitivitas 2-Arah (*2-Way Sensitivity Heatmap*):**
              Memetakan kombinasi perubahan serentak **Volume Produksi & Kapasitas Smelter ($X$: $-20\\%$ s/d $+20\\%$)** terhadap **Harga Komoditas Dunia ($Y$: $-30\\%$ s/d $+30\\%$)**. Sel berwarna hijau menunjukkan zona pertumbuhan tinggi, sedangkan sel merah menunjukkan zona perlambatan.
            * **3. Kurva *Spider Chart* Elastisitas ($\\pm 25\\%$):**
              Memperlihatkan kemiringan (*slope*) sensitivitas 7 variabel kunci ketika digeser dari $-25\\%$ sampai $+25\\%$. Semakin curam kemiringan garis suatu variabel, semakin besar daya ungkitnya terhadap PDB.
            * **4. *Macro-Mining Stress Test* (6 Skenario Krisis Ekstrem) & *Reverse Stress Test*:**
              Menguji ketahanan PDB Indonesia terhadap 6 guncangan krisis global (*Commodity Crash, Oil Shock, Currency Crisis, Smelter Moratorium, Combined Perfect Storm*) serta menghitung **Titik Ambang Batas Kritis (*Break-Even*)** harga komoditas dan kurs yang tidak boleh dilanggar.
            """
        )

    # =========================================================================
    # SUB-TAB 4: KAMUS STATISTIK EKONOMETRIKA (BAHASA AWAM VS AKADEMIS)
    # =========================================================================
    with sub_tabs[3]:
        st.markdown("### 🔬 Kamus Lengkap Istilah Statistik & Ekonometrika (Bahasa Praktis vs Akademis)")
        st.markdown(
            "Bagian ini menerjemahkan istilah-istilah teknis ala **EViews** ke dalam **Bahasa Awam (Praktis)** "
            "sekaligus **Bahasa Ilmiah Ekonometrika**:"
        )

        stat_dict_df = pd.DataFrame([
            {
                "Metode / Istilah Statistik": "1. Uji Stasioneritas ADF (Augmented Dickey-Fuller)",
                "Penjelasan Bahasa Awam (Mudah Dipahami)": "Mengecek apakah grafik data bergerak stabil di sekitar garis rata-ratanya atau terus melambung tanpa batas. Jika data belum stabil (tidak stasioner) langsung diregresikan, hasilnya bisa menipu (regresi lancung/spurious).",
                "Kriteria Lulus / Cara Baca Angka": "Lihat kolom 'Prob.' (p-value). Jika Prob < 0,05 berarti data STASIONER (Lulus). I(0) artinya sudah stasioner di data asli (Level); I(1) artinya baru stasioner setelah dihitung selisih perubahannya (First Difference).",
            },
            {
                "Metode / Istilah Statistik": "2. Regresi Linier Berganda (OLS - Ordinary Least Squares)",
                "Penjelasan Bahasa Awam (Mudah Dipahami)": "Menghitung seberapa besar perubahan pada PDB (Y) setiap kali variabel tambang/makro (X) naik 1 satuan, dengan asumsi variabel lainnya tetap (ceteris paribus).",
                "Kriteria Lulus / Cara Baca Angka": "• Koefisien (Beta): Tanda (+) berarti searah/mendongkrak PDB; tanda (-) berarti berlawanan/menekan PDB.\n• Prob (p-value) < 0,05 (tanda ** atau ***): Pengaruh variabel tersebut nyata/signifikan secara ilmiah.\n• R-Squared (R²): Persentase variasi PDB yang mampu dijelaskan oleh variabel-variabel di dalam model (misal 0,98 = 98%).",
            },
            {
                "Metode / Istilah Statistik": "3. Empat Uji Asumsi Klasik (Gauss-Markov / BLUE)",
                "Penjelasan Bahasa Awam (Mudah Dipahami)": "Empat syarat 'uji kelayakan mesin' agar rumus regresi OLS sah dipakai untuk mengambil kesimpulan ilmiah dan tidak bias.",
                "Kriteria Lulus / Cara Baca Angka": "1. Normalitas (Jarque-Bera): Lulus jika Prob > 0,05 (error menyebar normal).\n2. Heteroskedastisitas (Breusch-Pagan): Lulus jika Prob > 0,05 (varians error stabil/homoskedastis).\n3. Autokorelasi (Breusch-Godfrey): Lulus jika Prob > 0,05 (error antar kuartal tidak saling menular).\n4. Multikolinearitas (VIF): Lulus jika nilai VIF < 10 (antar variabel X tidak saling tumpang tindih berlebihan).",
            },
            {
                "Metode / Istilah Statistik": "4. Uji Kointegrasi & Model ARDL / ECM (Error Correction Model)",
                "Penjelasan Bahasa Awam (Mudah Dipahami)": "Memisahkan dampak kebijakan tambang menjadi dua waktu: Dampak Seketika/Jangka Pendek (1 kuartal) dan Dampak Struktural Jangka Panjang (ketika smelter sudah beroperasi penuh).",
                "Kriteria Lulus / Cara Baca Angka": "Kunci utamanya ada pada baris ECT(-1) (Error Correction Term):\n• Nilai Koefisien ECT(-1) WAJIB NEGATIF (antara -1 sampai 0) dan Prob < 0,05.\n• Contoh: ECT(-1) = -0,35 artinya jika terjadi guncangan ekonomi, maka 35% ketidakseimbangan akan pulih kembali menuju jalur keseimbangan jangka panjang pada setiap kuartal.",
            },
            {
                "Metode / Istilah Statistik": "5. Uji Kausalitas Granger (Granger Causality Test)",
                "Penjelasan Bahasa Awam (Mudah Dipahami)": "Menguji arah hubungan sebab-akibat: Apakah Hilirisasi Tambang yang mendorong PDB tumbuh, ataukah PDB yang tumbuh duluan baru mendorong tambang, atau keduanya saling mendorong (timbal balik/bidirectional)?",
                "Kriteria Lulus / Cara Baca Angka": "Jika Prob (p-value) < 0,05 pada hipotesis 'X menyebabkan Y', maka terbukti secara statistik data historis variabel X dapat digunakan untuk memprediksi pergerakan Y di masa depan.",
            },
            {
                "Metode / Istilah Statistik": "6. Impulse Response Function (IRF) pada VAR/VECM",
                "Penjelasan Bahasa Awam (Mudah Dipahami)": "Simulasi grafik kejut listrik (shock): Jika hari ini Harga Nikel atau Investasi Smelter tiba-tiba melonjak 1 standar deviasi, bagaimana kurva reaksi PDB pada Kuartal ke-1, ke-2, hingga Kuartal ke-10?",
                "Kriteria Lulus / Cara Baca Angka": "• Jika garis IRF berada di atas garis 0: Guncangan variabel tersebut memberi dampak positif terhadap PDB.\n• Jika garis berada di bawah 0: Memberi dampak negatif.\n• Lihat pada kuartal ke berapa efek guncangan mencapai puncak dan kapan mulai mereda/stabil.",
            },
            {
                "Metode / Istilah Statistik": "7. Forecast Error Variance Decomposition (FEVD)",
                "Penjelasan Bahasa Awam (Mudah Dipahami)": "Membedah kue porsi pengaruh (total 100%) dari waktu ke waktu: Dalam 1 hingga 10 kuartal ke depan, berapa persen dinamika PDB disumbang oleh Investasi Smelter, berapa persen oleh Batubara, Nikel, Emas, dan Makro?",
                "Kriteria Lulus / Cara Baca Angka": "Semakin lebar pita warna suatu variabel pada grafik batang 100% di periode ke-8 s/d ke-10, semakin besar peranan struktural variabel tersebut dalam menentukan masa depan PDB Indonesia.",
            },
        ])
        st.dataframe(stat_dict_df, use_container_width=True, hide_index=True)

    # =========================================================================
    # SUB-TAB 5: RUMUS MATEMATIKA & SPESIFIKASI METODOLOGI MODEL (BAB III)
    # =========================================================================
    with sub_tabs[4]:
        st.markdown("### 🧮 Spesifikasi Persamaan Ekonometrika & Sistem Persamaan Simultan (Metodologi Bab III)")
        st.markdown(
            "Seluruh perhitungan di dalam **MODUL 17 (`www.trilaksanamining.my.id`)** dibangun di atas landasan matematis ekonometrika yang baku "
            "dan terintegrasi langsung ke dalam **Bab III (Metodologi Penelitian)** serta **Bab IV (Hasil dan Pembahasan)** pada Laporan Naskah Ilmiah:"
        )

        st.markdown("#### 1. Model Regresi Jangka Panjang (Long-Run Cobb-Douglas / Log-Linear Specification)")
        st.latex(
            r"\ln(\text{PDB}_t) = \beta_0 + \beta_1 \ln(Q_{\text{Coal},t}) + \beta_2 \ln(Q_{\text{Nickel},t}) + \beta_3 \ln(Q_{\text{Gold},t}) "
            r"+ \beta_4 \ln(P_{\text{HBA},t}) + \beta_5 \ln(P_{\text{LME},t}) + \beta_6 \ln(P_{\text{Gold},t}) + \beta_7 \ln(\text{Inv}_{\text{Smelter},t}) "
            r"+ \beta_8 \ln(\text{Kurs}_t) + \beta_9 \text{BIRate}_t + \varepsilon_t"
        )
        st.markdown(
            "Di mana koefisien $\\beta_1, \\beta_2, \\dots, \\beta_8$ pada spesifikasi *Double-Log* langsung merepresentasikan "
            "**Elastisitas Jangka Panjang** (berapa persen perubahan PDB jika masing-masing variabel produksi/harga komoditas berubah $1\\%$), "
            "sedangkan $\\beta_9$ merupakan *semi-elastisitas* suku bunga."
        )

        st.markdown("#### 2. Model Dinamis ARDL $(p, q)$ dan *Error Correction Model* (ECM)")
        st.latex(
            r"\Delta Y_t = \alpha_0 + \sum_{i=1}^{p} \phi_i \Delta Y_{t-i} + \sum_{j=1}^{k} \sum_{l=0}^{q} \theta_{j,l} \Delta X_{j, t-l} + \lambda \text{ECT}_{t-1} + u_t"
        )
        st.markdown("Dengan komponen koreksi kesalahan (*Error Correction Term*):")
        st.latex(
            r"\text{ECT}_{t-1} = Y_{t-1} - \left( \hat{\beta}_0 + \sum_{j=1}^{k} \hat{\beta}_j X_{j, t-1} \right)"
        )
        st.markdown(
            "Parameter $\\lambda$ mengukur **Kecepatan Penyesuaian (*Speed of Adjustment*)** menuju ekuilibrium jangka panjang. "
            "Konvergensi model terpenuhi apabila $\\lambda < 0$ dan signifikan secara statistik ($p\\text{-value} < 0,05$)."
        )

        st.markdown("#### 3. Sistem Persamaan Simultan 4-Blok (*Simultaneous Equations Model* — Proyeksi PDB 2025–2030)")
        st.markdown(
            "Simulator interaktif mengintegrasikan sektor hulu pertambangan, hilirisasi industri logam dasar, "
            "penerimaan negara, dan pertumbuhan makroekonomi melalui **4 persamaan struktural simultan** berikut:"
        )
        st.markdown("**Blok 1 — Persamaan Output Hulu Pertambangan & Penggalian (Kategori B):**")
        st.latex(
            r"\text{PDB}_{\text{Hulu},t} = f\left( Q_{\text{Coal},t} \times P_{\text{HBA},t},\; Q_{\text{Nickel},t} \times P_{\text{LME},t},\; Q_{\text{Gold},t} \times P_{\text{Gold},t},\; P_{\text{ICP},t},\; \text{Kurs}_t \right)"
        )
        st.markdown("**Blok 2 — Persamaan Nilai Tambah Hilirisasi Industri Logam Dasar (Kategori C — KBLI 24):**")
        st.latex(
            r"\text{PDB}_{\text{Hilir},t} = g\left( \text{Inv}_{\text{Smelter},t},\; Q_{\text{Nickel},t},\; Q_{\text{Gold},t},\; P_{\text{LME},t},\; \mu_{\text{ValueAdded}} \right)"
        )
        st.markdown("**Blok 3 — Persamaan Penerimaan Negara (PNBP Minerba) dan Efek Pengganda (*Indirect Spillover*):**")
        st.latex(
            r"\text{PNBP}_{\text{Minerba},t} = \tau_{\text{Royalti}} \cdot \left( \text{Revenue}_{\text{Hulu},t} + \gamma \text{Revenue}_{\text{Hilir},t} \right), \quad \text{Spillover}_t = \kappa_1 \Delta \text{PDB}_{\text{Hulu},t} + \kappa_2 \Delta \text{PDB}_{\text{Hilir},t} + \kappa_3 \text{PNBP}_t"
        )
        st.markdown("**Blok 4 — Persamaan Identitas Agregat PDB Nasional Riil (ADHK 2010):**")
        st.latex(
            r"\text{PDB}_{\text{Nasional},t} = \text{PDB}_{\text{Hulu},t} + \text{PDB}_{\text{Hilir},t} + \text{Spillover}_t + \text{PDB}_{\text{NonMinerba},t}\left(\text{BIRate}_t, \text{Inflasi}_t, P_{\text{ICP},t}, \text{Kurs}_t\right)"
        )
        st.success(
            "✅ **Integrasi Dokumen Laporan & Presentasi:** Seluruh rumus matematis, parameter input, dan grafik hasil simulasi di atas terintegrasi otomatis ke dalam "
            "**Laporan Naskah Ilmiah BAB I s/d BAB V (`.PDF` & `.HTML`)** serta **Slide Presentasi Eksekutif (`.PDF` & `.HTML` Landscape)** pada **Tab 4**."
        )


