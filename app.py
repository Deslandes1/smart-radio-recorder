import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import datetime
import os
import random
from PIL import Image

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="GlobalInternet.py Radio", layout="wide")

# Password protection
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def show_haitian_flag():
    """Display the Haitian flag (blue and red with coat of arms)."""
    # Try to load local image first
    flag_path = "haiti_flag.png"
    if os.path.exists(flag_path):
        flag_img = Image.open(flag_path)
        st.image(flag_img, width=150)
    else:
        # Fallback: emoji + colored boxes
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
# AFTER LOGIN: SHOW FLAG AGAIN + SIDEBAR
# ------------------------------
# Multi-language dictionaries (same as before, but I'll keep them compact)
LANGUAGES = {"English": "en", "Español": "es", "Français": "fr"}
TEXTS = {
    "en": {
        "welcome": "Welcome to GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Live Radio", "record_tab": "🎙️ Record & Analyze", "report_tab": "📄 Download Report",
        "language": "Language", "price_label": "💰 Price (One-time)", "price_value": "**$149 USD** (lifetime license)",
        "user_info": "👤 Founder & Developer", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – All Rights Reserved",
        "radio_url": "Internet Radio Stream URL", "radio_placeholder": "http://example.com/stream.mp3",
        "play_radio": "▶️ Play", "upload_audio": "Or upload audio file",
        "voice_rec_title": "🎤 Voice Recording", "video_rec_title": "📹 Video Recording",
        "start_recording": "Start", "stop_recording": "Stop", "analyze": "📊 Analyze",
        "download_report": "⬇️ Download Report", "no_recording": "No recording yet.",
        "report_generated": "Report generated!", "analysis_result": "Analysis Result (simulated)",
        "recording_info": "Recording Info", "duration_sec": "Duration (s)", "file_size_kb": "Size (KB)",
        "mock_analysis": "Speech clarity 85%, low noise, sentiment positive."
    },
    "es": {
        "welcome": "Bienvenido a GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Radio en Vivo", "record_tab": "🎙️ Grabar y Analizar", "report_tab": "📄 Descargar Informe",
        "language": "Idioma", "price_label": "💰 Precio (único pago)", "price_value": "**149 USD** (licencia vitalicia)",
        "user_info": "👤 Fundador", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – Todos los derechos reservados",
        "radio_url": "URL de la emisora", "radio_placeholder": "http://ejemplo.com/stream.mp3",
        "play_radio": "▶️ Reproducir", "upload_audio": "O sube archivo",
        "voice_rec_title": "🎤 Grabación de Voz", "video_rec_title": "📹 Grabación de Vídeo",
        "start_recording": "Iniciar", "stop_recording": "Detener", "analyze": "📊 Analizar",
        "download_report": "⬇️ Descargar Informe", "no_recording": "Sin grabación.",
        "report_generated": "¡Informe generado!", "analysis_result": "Resultado (simulado)",
        "recording_info": "Información", "duration_sec": "Duración (s)", "file_size_kb": "Tamaño (KB)",
        "mock_analysis": "Claridad 85%, ruido bajo, sentimiento positivo."
    },
    "fr": {
        "welcome": "Bienvenue sur GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Radio en Direct", "record_tab": "🎙️ Enregistrer et Analyser", "report_tab": "📄 Télécharger Rapport",
        "language": "Langue", "price_label": "💰 Prix (unique)", "price_value": "**149 USD** (licence à vie)",
        "user_info": "👤 Fondateur", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – Tous droits réservés",
        "radio_url": "URL du flux", "radio_placeholder": "http://exemple.com/stream.mp3",
        "play_radio": "▶️ Lire", "upload_audio": "Ou téléchargez",
        "voice_rec_title": "🎤 Enregistrement vocal", "video_rec_title": "📹 Enregistrement vidéo",
        "start_recording": "Démarrer", "stop_recording": "Arrêter", "analyze": "📊 Analyser",
        "download_report": "⬇️ Télécharger", "no_recording": "Aucun enregistrement.",
        "report_generated": "Rapport généré !", "analysis_result": "Résultat (simulé)",
        "recording_info": "Infos", "duration_sec": "Durée (s)", "file_size_kb": "Taille (Ko)",
        "mock_analysis": "Clarté 85%, bruit faible, sentiment positif."
    }
}

def get_text(key):
    lang_code = st.session_state.get("language", "en")
    return TEXTS[lang_code].get(key, key)

def generate_mock_report(file_path, rec_type):
    if not file_path or not os.path.exists(file_path):
        return None
    file_size_kb = os.path.getsize(file_path) / 1024
    duration_sec = random.randint(2, 45)
    report = f"""
{'='*50}
{get_text('report_generated').upper()}
{'='*50}
{get_text('recording_info')}:
- Type: {rec_type}
- File: {os.path.basename(file_path)}
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
# SIDEBAR (after login)
# ------------------------------
st.sidebar.markdown("# 🇭🇹 GlobalInternet.py 🇭🇹")
# Show the real flag again in sidebar
show_haitian_flag()
st.sidebar.markdown(f"### {get_text('welcome')}")

# Language selection
lang = st.sidebar.selectbox(get_text("language"), list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang]

# Developer info
st.sidebar.markdown(f"## {get_text('user_info')}")
st.sidebar.info(f"""
**{get_text('user_name')}**  
🏢 {get_text('user_company')}  
📞 {get_text('user_phone')}  
📧 {get_text('user_email')}
""")

# Price
st.sidebar.markdown(f"## {get_text('price_label')}")
st.sidebar.success(get_text("price_value"))

# License and rights
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {get_text('license')}")
st.sidebar.caption("This software is protected by copyright law. Unauthorized distribution or reproduction is prohibited.")

# Haitian flag reminder
st.sidebar.markdown("---")
st.sidebar.markdown("## 🇭🇹 Fièrement fait en Haïti")

# ------------------------------
# MAIN APP TABS (same functional logic as before)
# ------------------------------
tab1, tab2, tab3 = st.tabs([get_text("radio_tab"), get_text("record_tab"), get_text("report_tab")])

# TAB 1: RADIO
with tab1:
    col1, col2 = st.columns([3,1])
    with col1:
        radio_url = st.text_input(get_text("radio_url"), placeholder=get_text("radio_placeholder"))
        if radio_url:
            st.audio(radio_url, format="audio/mpeg")
    with col2:
        st.markdown("### 🎧 Offline")
        uploaded_file = st.file_uploader(get_text("upload_audio"), type=["mp3","wav","ogg"])
        if uploaded_file:
            st.audio(uploaded_file)

# TAB 2: RECORDING & ANALYSIS
with tab2:
    # Voice
    st.markdown(f"## {get_text('voice_rec_title')}")
    voice_file = "voice_output.wav"
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button(f"🎙️ {get_text('start_recording')}", key="voice_start"):
            st.session_state.voice_active = True
    with col_v2:
        if st.button(f"⏹️ {get_text('stop_recording')}", key="voice_stop"):
            st.session_state.voice_active = False
    
    if st.session_state.get("voice_active", False):
        st.info("🔴 Recording voice...")
        webrtc_streamer(key="voice", mode=WebRtcMode.SENDRECV, audio_receiver_size=1024,
                        media_stream_constraints={"audio": True, "video": False},
                        out_recorder_filename=voice_file)
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
    video_file = "video_output.mp4"
    col_vid1, col_vid2 = st.columns(2)
    with col_vid1:
        if st.button(f"📹 {get_text('start_recording')}", key="video_start"):
            st.session_state.video_active = True
    with col_vid2:
        if st.button(f"⏹️ {get_text('stop_recording')}", key="video_stop"):
            st.session_state.video_active = False
    
    if st.session_state.get("video_active", False):
        st.info("🔴 Recording video...")
        webrtc_streamer(key="video", mode=WebRtcMode.SENDRECV, audio_receiver_size=1024,
                        media_stream_constraints={"audio": True, "video": True},
                        out_recorder_filename=video_file)
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

# TAB 3: REPORT DOWNLOAD
with tab3:
    st.markdown("### 📥 Download Report")
    report_choice = st.radio("Choose:", ["Voice Report", "Video Report"])
    content = st.session_state.get("voice_report" if "Voice" in report_choice else "video_report", "")
    if content:
        fname = save_report_file(content, report_choice.replace(" ", "_").lower())
        if fname:
            with open(fname, "r") as f:
                st.download_button(get_text("download_report"), f.read(), file_name=fname, mime="text/plain")
            os.remove(fname)
    else:
        st.info("No report yet. Record and analyze first.")
