import streamlit as st
import time
from core.cloud_auth import (
    APP_ID,
    APP_NAME,
    check_license,
    login_online,
    get_hardware_id,
    clear_local_license,
    is_cloud_hosted,
    notify_online_visitor_async,
)


def check_authentication(module_title=None):
    """
    Unified Cloud Authentication & Licensing Gate
    Powered by www.trilaksanamining.my.id & Telegram Bot Integration
    Supports 7-Day Offline Grace-Period (.EXE) & Online Live Show Telemetry (Streamlit Cloud).
    """
    if module_title is None:
        module_title = APP_NAME

    # 1. Kirim notifikasi ke Telegram saat pengunjung baru pertama kali membuka halaman web (Online Cloud)
    if is_cloud_hosted() and not st.session_state.get("tg_initial_visit_notified"):
        st.session_state["tg_initial_visit_notified"] = True
        notify_online_visitor_async(
            visitor_name="Pengunjung Web Baru",
            visitor_email="Belum Login",
            visitor_company="Akses Web Publik",
            event_title="👀 *PENGUNJUNG MEMBUKA HALAMAN LIVE SHOW MODUL 17*",
            extra_detail="Membuka halaman utama Live Show Modul 17 di Browser",
        )

    # 2. Jika sudah login di sesi browser ini (penting untuk Streamlit Cloud multi-user)
    if st.session_state.get("authenticated") and st.session_state.get("lic_user"):
        return True

    # 3. Untuk versi Desktop (.EXE), periksa cache lisensi lokal 7 hari
    if not is_cloud_hosted():
        lic_status = check_license(silent_refresh=True)
        if lic_status.get("authenticated"):
            st.session_state["authenticated"] = True
            st.session_state["logged_in"] = True
            st.session_state["lic_user"] = lic_status.get("user", {})
            st.session_state["lic_mode"] = lic_status.get("mode", "online")
            st.session_state["username"] = lic_status.get("user", {}).get("fullName", "Engineer")
            return True

    # Render Modern Branded Security Card
    hwid = get_hardware_id()
    st.markdown(
        f"""
    <div style="background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e293b 100%); padding: 32px 24px; border-radius: 16px; border: 1px solid #334155; text-align: center; margin-bottom: 24px; box-shadow: 0 12px 35px rgba(0,0,0,0.6);">
        <div style="display: inline-block; padding: 5px 15px; background: rgba(56, 189, 248, 0.12); border: 1px solid #38bdf8; border-radius: 30px; color: #38bdf8; font-size: 11px; font-weight: 700; letter-spacing: 2px; margin-bottom: 12px; text-transform: uppercase;">
            CENTRAL CLOUD LICENSING &bull; MODUL 17 TRILAKSANA SUITE
        </div>
        <h1 style="color: #ffffff; font-size: 28px; font-weight: 800; margin: 0 0 6px 0; letter-spacing: -0.5px;">THE TRILAKSANA FRAMEWORK — MODUL 17</h1>
        <div style="color: #94a3b8; font-size: 14px; margin-bottom: 16px; font-weight: 500;">
            Sistem Intelijen Ekonometrika Makro-Tambang, Hilirisasi &amp; Proyeksi PDB Nasional &bull; Dr. Ir. Ahmad Raymond Trilaksana, S.T., M.Ak., IPM, ASEAN Eng.
        </div>
        <div style="background: rgba(255, 255, 255, 0.04); border-left: 3px solid #38bdf8; border-radius: 6px; padding: 12px 18px; font-size: 13px; color: #cbd5e1; max-width: 680px; margin: 0 auto; text-align: left; line-height: 1.5;">
            🔒 <b>Pemberitahuan Lisensi &amp; Telemetri Terpadu:</b> Modul 17 ini terhubung langsung ke Cloud Portal <a href="https://www.trilaksanamining.my.id" target="_blank" style="color: #38bdf8;">www.trilaksanamining.my.id</a> &amp; Sistem Telemetri Telegram. Silakan masuk menggunakan akun resmi Anda atau gunakan <b>Akses Cepat Live Show</b> di bawah ini.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_l, col_center, col_r = st.columns([1, 2.3, 1])
    with col_center:
        tab_member, tab_guest = st.tabs([
            "🔑 Login Akun Resmi (www.trilaksanamining.my.id)",
            "🌐 Akses Cepat Live Show (Tamu / Akademisi / Praktisi)",
        ])

        with tab_member:
            st.markdown(
                f"""
            <div style="background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 16px;">
                <div style="font-size: 13.5px; font-weight: 700; color: #ffffff; margin-bottom: 4px;">
                    Masuk Menggunakan Akun Portal www.trilaksanamining.my.id
                </div>
                <div style="font-size: 12px; color: #94a3b8; margin-bottom: 10px;">
                    Belum memiliki akun? Registrasi gratis di <a href="https://www.trilaksanamining.my.id" target="_blank" style="color: #38bdf8; font-weight: 700;">www.trilaksanamining.my.id ↗</a>
                </div>
                <div style="font-size: 11px; color: #64748b;">
                    💻 <b>ID Sesi / Perangkat:</b> <code>{hwid}</code>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            with st.form("cloud_login_form"):
                email_input = st.text_input("Email Akun:", placeholder="Contoh: ahmad.trilaksana@gmail.com")
                pass_input = st.text_input("Password:", type="password", placeholder="Masukkan password akun Anda")
                submitted = st.form_submit_button("🚀 AKTIFKAN & MASUK KE MODUL 17", type="primary", use_container_width=True)

                if submitted:
                    if not email_input.strip() or not pass_input:
                        st.error("Email dan password wajib diisi!")
                    else:
                        with st.spinner("Memverifikasi ke Cloud Server www.trilaksanamining.my.id..."):
                            res = login_online(email_input.strip(), pass_input)
                            if res.get("success"):
                                st.session_state["authenticated"] = True
                                st.session_state["logged_in"] = True
                                st.session_state["lic_user"] = res.get("user", {})
                                st.session_state["lic_mode"] = "online"
                                st.session_state["username"] = res.get("user", {}).get("fullName", email_input)
                                st.success(f"✅ {res.get('message', 'Lisensi Berhasil Diverifikasi!')}")
                                time.sleep(0.6)
                                st.rerun()
                            else:
                                st.error(f"❌ {res.get('message', 'Autentikasi gagal.')}")

        with tab_guest:
            st.info(
                "💡 **Mode Live Show Interaktif:** Masukkan Nama & Instansi/Email Anda untuk langsung mencoba "
                "seluruh simulasi ekonometrika Modul 17 secara *live*. Notifikasi kehadiran Anda akan dikirimkan otomatis ke Telegram Inovator."
            )
            with st.form("guest_liveshow_form"):
                g_name = st.text_input("Nama Lengkap Anda:", placeholder="Contoh: Budi Santoso, S.T., M.T.")
                g_org = st.text_input("Instansi / Universitas / Perusahaan:", placeholder="Contoh: Kementerian ESDM / ITB / PT Antam Tbk")
                g_email = st.text_input("Email / Kontak (Opsional):", placeholder="Contoh: budi@instansi.go.id")
                g_submit = st.form_submit_button("🌐 BUKA LIVE SHOW MODUL 17 SEKARANG", type="primary", use_container_width=True)

                if g_submit:
                    if not g_name.strip() or not g_org.strip():
                        st.error("Mohon isi Nama Lengkap dan Instansi/Universitas Anda terlebih dahulu.")
                    else:
                        guest_user = {
                            "userId": "USR-LIVESHOW-GUEST",
                            "fullName": g_name.strip(),
                            "email": g_email.strip() or "tamu.liveshow@trilaksanamining.my.id",
                            "company": g_org.strip(),
                            "role": "Live Show Visitor",
                            "status": "active",
                            "allowedApps": "ALL",
                            "validUntil": "2099-12-31",
                            "hwid": hwid,
                        }
                        st.session_state["authenticated"] = True
                        st.session_state["logged_in"] = True
                        st.session_state["lic_user"] = guest_user
                        st.session_state["lic_mode"] = "online"
                        st.session_state["username"] = g_name.strip()
                        notify_online_visitor_async(
                            visitor_name=g_name.strip(),
                            visitor_email=g_email.strip() or "-",
                            visitor_company=g_org.strip(),
                            event_title="🚀 *PENGUNJUNG MASUK KE LIVE SHOW MODUL 17*",
                            extra_detail="Login Mode Akses Cepat Live Show Online",
                        )
                        st.success(f"✅ Selamat datang di Live Show Modul 17, {g_name.strip()}!")
                        time.sleep(0.5)
                        st.rerun()

    st.stop()


def render_auth_sidebar():
    """
    Renders authenticated user badge, HWID, remaining grace period, and logout button.
    """
    u_info = st.session_state.get("lic_user", {})
    full_name = u_info.get("fullName", st.session_state.get("username", "Engineer"))
    email = u_info.get("email", "-")
    company = u_info.get("company", "PT Trilaksana Mineral Nusantara")
    hwid = u_info.get("hwid", get_hardware_id())
    mode = st.session_state.get("lic_mode", "online")
    mode_label = (
        "🌐 Online Live Show Active"
        if is_cloud_hosted()
        else ("🟢 Online Cloud Verified" if mode == "online" else "🟡 Mode Lapangan 7 Hari")
    )

    st.sidebar.markdown(
        f"""
    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #334155; border-radius: 8px; padding: 12px 14px; margin-bottom: 12px;">
        <div style="font-size: 10.5px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">Lisensi Terverifikasi &bull; Modul 17</div>
        <div style="font-size: 13.5px; font-weight: bold; color: #38bdf8; margin-top: 2px;">👤 {full_name}</div>
        <div style="font-size: 11px; color: #cbd5e1; margin-top: 2px;">📧 {email}</div>
        <div style="font-size: 11px; color: #94a3b8;">🏢 {company}</div>
        <div style="font-size: 11px; color: #22c55e; margin-top: 4px;">{mode_label}</div>
        <div style="font-size: 10px; color: #64748b; margin-top: 4px;">
            💻 <code>{hwid}</code>
        </div>
        <div style="font-size: 10px; color: #64748b; margin-top: 4px;">
            Portal: <a href="https://www.trilaksanamining.my.id" target="_blank" style="color: #38bdf8; text-decoration: none;">www.trilaksanamining.my.id</a>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if st.sidebar.button("🚪 Keluar / Logout", key="btn_auth_logout", use_container_width=True):
        if not is_cloud_hosted():
            clear_local_license()
        st.session_state["authenticated"] = False
        st.session_state["logged_in"] = False
        st.session_state["lic_user"] = {}
        st.rerun()

