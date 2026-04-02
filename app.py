import streamlit as st
from streamlit_webrtc import webrtc_streamer
import datetime
import os
import random
from PIL import Image

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="GlobalInternet.py Radio", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "voice_active" not in st.session_state:
    st.session_state.voice_active = False
if "video_active" not in st.session_state:
    st.session_state.video_active = False

def show_haitian_flag():
    flag_path = "haiti_flag.png"
    if os.path.exists(flag_path):
        flag_img = Image.open(flag_path)
        st.image(flag_img, width=150)
    else:
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <div style="background-color: #00209F; width: 60px; height: 40px;"></div>
                <div style="background-color: #DE2119; width: 60px; height: 40px;"></div>
                <span style="font-size: 30px; margin-left: 10px;">🇭🇹</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption("Haitian Flag (blue & red with coat of arms)")

# Login page
if not st.session_state.authenticated:
    st.title("🔐 Login Required")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        show_haitian_flag()
        st.markdown("## **GlobalInternet.py**")
        password_input = st.text_input("Enter password to access the radio suite", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

# ------------------------------
# MULTI-LANGUAGE (4 languages)
# ------------------------------
LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Kreyòl Ayisyen": "ht"
}

TEXTS = {
    "en": {
        "welcome": "Welcome to GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Live Radio", "record_tab": "🎙️ Record & Analyze", "report_tab": "📄 Download Report",
        "language": "Language", "price_label": "💰 Price (One-time)", "price_value": "**$149 USD** (lifetime license)",
        "user_info": "👤 Founder & Developer", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – All Rights Reserved",
        "radio_url": "Internet Radio Stream URL", "radio_placeholder": "http://example.com/stream.mp3",
        "use_proxy": "Use CORS proxy (if stream doesn't play)",
        "proxy_info": "🔄 Using CORS proxy to bypass mixed content & CORS issues.",
        "upload_audio": "Or upload audio file",
        "voice_rec_title": "🎤 Voice Recording", "video_rec_title": "📹 Video Recording",
        "start_recording": "Start", "stop_recording": "Stop", "analyze": "📊 Analyze",
        "download_report": "⬇️ Download Report", "no_recording": "No recording yet.",
        "report_generated": "Report generated!", "analysis_result": "Analysis Result (simulated)",
        "recording_info": "Recording Info", "duration_sec": "Duration (s)", "file_size_kb": "Size (KB)",
        "mock_analysis": "Speech clarity 85%, low noise, sentiment positive.",
        "logout": "🚪 Logout", "demo_mode": "🎮 Demo Mode (no real recording)", "demo_active": "Demo mode active – using mock data."
    },
    "es": {
        "welcome": "Bienvenido a GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Radio en Vivo", "record_tab": "🎙️ Grabar y Analizar", "report_tab": "📄 Descargar Informe",
        "language": "Idioma", "price_label": "💰 Precio (único pago)", "price_value": "**149 USD** (licencia vitalicia)",
        "user_info": "👤 Fundador", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – Todos los derechos reservados",
        "radio_url": "URL de la emisora", "radio_placeholder": "http://ejemplo.com/stream.mp3",
        "use_proxy": "Usar proxy CORS (si la emisora no suena)",
        "proxy_info": "🔄 Usando proxy CORS para evitar problemas de contenido mixto y CORS.",
        "upload_audio": "O sube archivo",
        "voice_rec_title": "🎤 Grabación de Voz", "video_rec_title": "📹 Grabación de Vídeo",
        "start_recording": "Iniciar", "stop_recording": "Detener", "analyze": "📊 Analizar",
        "download_report": "⬇️ Descargar Informe", "no_recording": "Sin grabación.",
        "report_generated": "¡Informe generado!", "analysis_result": "Resultado (simulado)",
        "recording_info": "Información", "duration_sec": "Duración (s)", "file_size_kb": "Tamaño (KB)",
        "mock_analysis": "Claridad 85%, ruido bajo, sentimiento positivo.",
        "logout": "🚪 Cerrar sesión", "demo_mode": "🎮 Modo Demo (sin grabación real)", "demo_active": "Modo demo activo – usando datos simulados."
    },
    "fr": {
        "welcome": "Bienvenue sur GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Radio en Direct", "record_tab": "🎙️ Enregistrer et Analyser", "report_tab": "📄 Télécharger Rapport",
        "language": "Langue", "price_label": "💰 Prix (unique)", "price_value": "**149 USD** (licence à vie)",
        "user_info": "👤 Fondateur", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – Tous droits réservés",
        "radio_url": "URL du flux", "radio_placeholder": "http://exemple.com/stream.mp3",
        "use_proxy": "Utiliser un proxy CORS (si le flux ne joue pas)",
        "proxy_info": "🔄 Utilisation d'un proxy CORS pour contourner les problèmes de contenu mixte et CORS.",
        "upload_audio": "Ou téléchargez",
        "voice_rec_title": "🎤 Enregistrement vocal", "video_rec_title": "📹 Enregistrement vidéo",
        "start_recording": "Démarrer", "stop_recording": "Arrêter", "analyze": "📊 Analyser",
        "download_report": "⬇️ Télécharger", "no_recording": "Aucun enregistrement.",
        "report_generated": "Rapport généré !", "analysis_result": "Résultat (simulé)",
        "recording_info": "Infos", "duration_sec": "Durée (s)", "file_size_kb": "Taille (Ko)",
        "mock_analysis": "Clarté 85%, bruit faible, sentiment positif.",
        "logout": "🚪 Déconnexion", "demo_mode": "🎮 Mode Démo (pas d'enregistrement réel)", "demo_active": "Mode démo actif – données simulées."
    },
    "ht": {
        "welcome": "Byenveni nan GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Radyo Live", "record_tab": "🎙️ Anrejistre ak Analize", "report_tab": "📄 Telechaje Rapò",
        "language": "Lang", "price_label": "💰 Pri (yon sèl fwa)", "price_value": "**149 USD** (lisans pou tout lavi)",
        "user_info": "👤 Fondatè ak Devlopè", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – Tout dwa rezève",
        "radio_url": "URL Kouran Radyo", "radio_placeholder": "http://egzanp.com/stream.mp3",
        "use_proxy": "Sèvi ak proxy CORS (si radyo pa jwe)",
        "proxy_info": "🔄 Sèvi ak proxy CORS pou rezoud pwoblèm CORS ak kontni melanje.",
        "upload_audio": "Oswa telechaje fichye odyo",
        "voice_rec_title": "🎤 Anrejistreman Vwa", "video_rec_title": "📹 Anrejistreman Videyo",
        "start_recording": "Kòmanse", "stop_recording": "Sispann", "analyze": "📊 Analize",
        "download_report": "⬇️ Telechaje Rapò", "no_recording": "Pa gen anrejistreman.",
        "report_generated": "Rapò kreye!", "analysis_result": "Rezilta Analiz (simile)",
        "recording_info": "Enfòmasyon Anrejistreman", "duration_sec": "Dire (s)", "file_size_kb": "Gwosè (KB)",
        "mock_analysis": "Klète vwa 85%, bri ba, santiman pozitif.",
        "logout": "🚪 Dekonekte", "demo_mode": "🎮 Mòd Demo (pa gen anrejistreman reyèl)", "demo_active": "Mòd demo aktif – itilize done similes."
    }
}

def get_text(key):
    lang_code = st.session_state.get("language", "en")
    return TEXTS[lang_code].get(key, key)

def generate_mock_report(file_path, rec_type):
    if not st.session_state.demo_mode and file_path and os.path.exists(file_path):
        file_size_kb = os.path.getsize(file_path) / 1024
    else:
        file_size_kb = random.randint(50, 500)
    duration_sec = random.randint(3, 30)
    report = f"""
{'='*50}
{get_text('report_generated').upper()}
{'='*50}
{get_text('recording_info')}:
- Type: {rec_type}
- File: {os.path.basename(file_path) if file_path else 'demo_recording.wav'}
- {get_text('file_size_kb')}: {file_size_kb:.2f} KB
- {get_text('duration_sec')}: {duration_sec} s
- Timestamp: {datetime.datetime.now()}
{get_text('analysis_result')}:
{get_text('mock_analysis')}
{'='*50}
"""
    return report

def save_report_file(report_text, prefix):
    if not report_text:
        return None
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    return filename

# ------------------------------
# SIDEBAR
# ------------------------------
st.sidebar.markdown("# 🇭🇹 GlobalInternet.py 🇭🇹")
show_haitian_flag()
st.sidebar.markdown(f"### {get_text('welcome')}")

lang = st.sidebar.selectbox(get_text("language"), list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang]

demo_toggle = st.sidebar.checkbox(get_text("demo_mode"), value=st.session_state.demo_mode)
if demo_toggle != st.session_state.demo_mode:
    st.session_state.demo_mode = demo_toggle
    st.rerun()
if st.session_state.demo_mode:
    st.sidebar.info(get_text("demo_active"))

st.sidebar.markdown(f"## {get_text('user_info')}")
st.sidebar.info(f"""
**{get_text('user_name')}**  
🏢 {get_text('user_company')}  
📞 {get_text('user_phone')}  
📧 {get_text('user_email')}
""")

st.sidebar.markdown(f"## {get_text('price_label')}")
st.sidebar.success(get_text("price_value"))

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {get_text('license')}")
st.sidebar.caption("This software is protected by copyright law. Unauthorized distribution or reproduction is prohibited.")

if st.sidebar.button(get_text("logout")):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("## 🇭🇹 Fièrement fait en Haïti")

# ------------------------------
# MAIN TABS
# ------------------------------
tab1, tab2, tab3 = st.tabs([get_text("radio_tab"), get_text("record_tab"), get_text("report_tab")])

# ========= TAB 1: RADIO with proxy fallback =========
with tab1:
    col1, col2 = st.columns([3,1])
    with col1:
        radio_url = st.text_input(get_text("radio_url"), placeholder=get_text("radio_placeholder"))
        use_proxy = st.checkbox(get_text("use_proxy"), value=True)
        
        if radio_url:
            # If proxy enabled and URL is HTTP, wrap it
            if use_proxy and radio_url.startswith("http://"):
                proxy_url = f"https://cors-anywhere.herokuapp.com/{radio_url}"
                st.info(get_text("proxy_info"))
            else:
                proxy_url = radio_url
            
            audio_html = f"""
            <audio controls autoplay style="width: 100%;">
                <source src="{proxy_url}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            """
            st.components.v1.html(audio_html, height=100)
            st.caption("ℹ️ If still not playing, try a direct MP3 link (e.g., from radio.garden or TuneIn).")
    with col2:
        st.markdown("### 🎧 Offline")
        uploaded_file = st.file_uploader(get_text("upload_audio"), type=["mp3","wav","ogg"])
        if uploaded_file:
            st.audio(uploaded_file)

# ========= TAB 2: RECORDING & ANALYSIS =========
with tab2:
    # Voice
    st.markdown(f"## {get_text('voice_rec_title')}")
    if st.session_state.demo_mode:
        st.info("Demo mode: recording is simulated. Click 'Analyze' to generate a mock report.")
        if st.button(get_text("analyze"), key="demo_voice"):
            report = generate_mock_report(None, "Voice (Demo)")
            if report:
                st.session_state["voice_report"] = report
                st.success(get_text("report_generated"))
                st.text_area("Preview", report, height=200)
    else:
        voice_file = "voice_output.wav"
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button(f"🎙️ {get_text('start_recording')}", key="voice_start"):
                st.session_state.voice_active = True
        with col_v2:
            if st.button(f"⏹️ {get_text('stop_recording')}", key="voice_stop"):
                st.session_state.voice_active = False
        
        if st.session_state.voice_active:
            st.info("🔴 Recording voice... Click 'Stop Recording' when done.")
            webrtc_streamer(
                key="voice",
                media_stream_constraints={"audio": True, "video": False},
                out_recorder_filename=voice_file
            )
        else:
            webrtc_streamer(key="voice_idle", desired_playing_state=False)
        
        if os.path.exists(voice_file):
            st.audio(voice_file)
            if st.button(get_text("analyze"), key="analyze_voice"):
                report = generate_mock_report(voice_file, "Voice")
                if report:
                    st.session_state["voice_report"] = report
                    st.success(get_text("report_generated"))
                    st.text_area("Preview", report, height=200)
        else:
            st.info(get_text("no_recording"))
    
    st.divider()
    
    # Video
    st.markdown(f"## {get_text('video_rec_title')}")
    if st.session_state.demo_mode:
        st.info("Demo mode: video recording is simulated. Click 'Analyze' to generate a mock report.")
        if st.button(get_text("analyze"), key="demo_video"):
            report = generate_mock_report(None, "Video (Demo)")
            if report:
                st.session_state["video_report"] = report
                st.success(get_text("report_generated"))
                st.text_area("Preview", report, height=200)
    else:
        video_file = "video_output.mp4"
        col_vid1, col_vid2 = st.columns(2)
        with col_vid1:
            if st.button(f"📹 {get_text('start_recording')}", key="video_start"):
                st.session_state.video_active = True
        with col_vid2:
            if st.button(f"⏹️ {get_text('stop_recording')}", key="video_stop"):
                st.session_state.video_active = False
        
        if st.session_state.video_active:
            st.info("🔴 Recording video + audio... Click 'Stop Recording' when done.")
            webrtc_streamer(
                key="video",
                media_stream_constraints={"audio": True, "video": True},
                out_recorder_filename=video_file
            )
        else:
            webrtc_streamer(key="video_idle", desired_playing_state=False)
        
        if os.path.exists(video_file):
            st.video(video_file)
            if st.button(get_text("analyze"), key="analyze_video"):
                report = generate_mock_report(video_file, "Video")
                if report:
                    st.session_state["video_report"] = report
                    st.success(get_text("report_generated"))
                    st.text_area("Preview", report, height=200)
        else:
            st.info(get_text("no_recording"))

# ========= TAB 3: REPORT DOWNLOAD =========
with tab3:
    st.markdown("### 📥 Download Report")
    report_choice = st.radio("Choose:", ["Voice Report", "Video Report"])
    if "Voice" in report_choice:
        content = st.session_state.get("voice_report", "")
    else:
        content = st.session_state.get("video_report", "")
    if content:
        fname = save_report_file(content, report_choice.replace(" ", "_").lower())
        if fname:
            with open(fname, "r") as f:
                st.download_button(get_text("download_report"), f.read(), file_name=fname, mime="text/plain")
            os.remove(fname)
    else:
        st.info("No report yet. Record and analyze first.")
