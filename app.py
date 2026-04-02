import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import datetime
import os
import random
import tempfile

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="GlobalInternet.py Radio", layout="wide")

# Password protection
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login Required")
    # Haitian Flag (Emoji + text)
    st.markdown("## 🇭🇹 **GlobalInternet.py** 🇭🇹")
    password_input = st.text_input("Enter password to access the radio suite", type="password")
    if st.button("Login"):
        if password_input == "20082010":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Access denied.")
    st.stop()  # Stop execution if not authenticated

# ------------------------------
# MULTI-LANGUAGE DICTIONARIES
# ------------------------------
LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Français": "fr"
}

TEXTS = {
    "en": {
        "welcome": "Welcome to GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Live Radio",
        "record_tab": "🎙️ Record & Analyze",
        "report_tab": "📄 Download Report",
        "language": "Language",
        "price_label": "💰 Software Price (One-time)",
        "price_value": "**$149 USD** (lifetime license, includes all updates)",
        "user_info": "👤 Founder & Developer",
        "user_name": "Gesner Deslandes",
        "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663",
        "user_email": "deslandes78@gmail.com",
        "radio_url": "Internet Radio Stream URL",
        "radio_placeholder": "http://example.com/stream.mp3",
        "play_radio": "▶️ Play",
        "upload_audio": "Or upload audio file for offline listening",
        "voice_rec_title": "🎤 Voice Recording",
        "video_rec_title": "📹 Video Recording",
        "start_recording": "Start Recording",
        "stop_recording": "Stop Recording",
        "analyze": "📊 Analyze Recording",
        "download_report": "⬇️ Download Report",
        "no_recording": "No recording available. Record first.",
        "report_generated": "Report generated!",
        "analysis_result": "Analysis Result (simulated AI)",
        "recording_info": "Recording Information",
        "duration_sec": "Duration (seconds)",
        "file_size_kb": "File size (KB)",
        "mock_analysis": "Mock analysis: Speech clarity 85%, Background noise low, Sentiment: neutral/positive."
    },
    "es": {
        "welcome": "Bienvenido a GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Radio en Vivo",
        "record_tab": "🎙️ Grabar y Analizar",
        "report_tab": "📄 Descargar Informe",
        "language": "Idioma",
        "price_label": "💰 Precio del Software (único pago)",
        "price_value": "**149 USD** (licencia vitalicia, incluye actualizaciones)",
        "user_info": "👤 Fundador y Desarrollador",
        "user_name": "Gesner Deslandes",
        "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663",
        "user_email": "deslandes78@gmail.com",
        "radio_url": "URL de la emisora",
        "radio_placeholder": "http://ejemplo.com/stream.mp3",
        "play_radio": "▶️ Reproducir",
        "upload_audio": "O sube un archivo de audio para escuchar sin conexión",
        "voice_rec_title": "🎤 Grabación de Voz",
        "video_rec_title": "📹 Grabación de Vídeo",
        "start_recording": "Iniciar Grabación",
        "stop_recording": "Detener Grabación",
        "analyze": "📊 Analizar Grabación",
        "download_report": "⬇️ Descargar Informe",
        "no_recording": "No hay grabación. Graba primero.",
        "report_generated": "¡Informe generado!",
        "analysis_result": "Resultado del Análisis (IA simulada)",
        "recording_info": "Información de la Grabación",
        "duration_sec": "Duración (segundos)",
        "file_size_kb": "Tamaño (KB)",
        "mock_analysis": "Análisis simulado: Claridad del habla 85%, Ruido bajo, Sentimiento: neutral/positivo."
    },
    "fr": {
        "welcome": "Bienvenue sur GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Radio en Direct",
        "record_tab": "🎙️ Enregistrer et Analyser",
        "report_tab": "📄 Télécharger Rapport",
        "language": "Langue",
        "price_label": "💰 Prix du Logiciel (unique)",
        "price_value": "**149 USD** (licence à vie, mises à jour incluses)",
        "user_info": "👤 Fondateur & Développeur",
        "user_name": "Gesner Deslandes",
        "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663",
        "user_email": "deslandes78@gmail.com",
        "radio_url": "URL du flux radio",
        "radio_placeholder": "http://exemple.com/stream.mp3",
        "play_radio": "▶️ Lire",
        "upload_audio": "Ou téléchargez un fichier audio pour écoute hors ligne",
        "voice_rec_title": "🎤 Enregistrement Vocal",
        "video_rec_title": "📹 Enregistrement Vidéo",
        "start_recording": "Démarrer l'enregistrement",
        "stop_recording": "Arrêter l'enregistrement",
        "analyze": "📊 Analyser l'enregistrement",
        "download_report": "⬇️ Télécharger Rapport",
        "no_recording": "Aucun enregistrement disponible. Enregistrez d'abord.",
        "report_generated": "Rapport généré !",
        "analysis_result": "Résultat de l'analyse (IA simulée)",
        "recording_info": "Informations d'enregistrement",
        "duration_sec": "Durée (secondes)",
        "file_size_kb": "Taille (Ko)",
        "mock_analysis": "Analyse simulée : Clarté de la parole 85%, Bruit faible, Sentiment : neutre/positif."
    }
}

def get_text(key):
    lang_code = st.session_state.get("language", "en")
    return TEXTS[lang_code].get(key, key)

# ------------------------------
# HELPER FUNCTIONS FOR REPORT
# ------------------------------
def generate_mock_report(file_path, rec_type):
    if not file_path or not os.path.exists(file_path):
        return None
    file_size_kb = os.path.getsize(file_path) / 1024
    mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    # Mock duration (in real app you would extract from media file)
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
- Timestamp: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}

{get_text('analysis_result')}:
{get_text('mock_analysis')}
- Keywords detected: radio, software, analysis
- Recommendation: Good quality for further processing.

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
# SIDEBAR: LANGUAGE, USER INFO, PRICE, FLAG
# ------------------------------
st.sidebar.markdown("# 🇭🇹 GlobalInternet.py 🇭🇹")
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

# Haitian Flag always visible
st.sidebar.markdown("---")
st.sidebar.markdown("## 🇭🇹🇭🇹🇭🇹")
st.sidebar.caption("Proudly Haitian-made software")

# ------------------------------
# MAIN TABS
# ------------------------------
tab1, tab2, tab3 = st.tabs([get_text("radio_tab"), get_text("record_tab"), get_text("report_tab")])

# ========= TAB 1: RADIO =========
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

# ========= TAB 2: RECORDING & ANALYSIS =========
with tab2:
    # We'll use webrtc_streamer with in-memory recording.
    # To avoid the previous error, we create two separate streamers for voice and video.
    # They will only be active when the user clicks the respective start button.
    
    # --- Voice Recording ---
    st.markdown(f"## {get_text('voice_rec_title')}")
    voice_key = "voice_recorder"
    voice_file = "voice_output.wav"
    
    voice_start = st.button(f"🎙️ {get_text('start_recording')}", key="voice_start")
    voice_stop = st.button(f"⏹️ {get_text('stop_recording')}", key="voice_stop")
    
    if voice_start:
        st.session_state.voice_active = True
    if voice_stop:
        st.session_state.voice_active = False
    
    if st.session_state.get("voice_active", False):
        st.info("🔴 Recording voice... Click 'Stop Recording' when done.")
        ctx_voice = webrtc_streamer(
            key=voice_key,
            mode=WebRtcMode.SENDRECV,
            audio_receiver_size=1024,
            media_stream_constraints={"audio": True, "video": False},
            out_recorder_filename=voice_file
        )
        if ctx_voice and ctx_voice.audio_receiver:
            # keep the component alive
            pass
    else:
        # When not active, just show placeholder
        webrtc_streamer(key=voice_key + "_idle", desired_playing_state=False)
    
    if os.path.exists(voice_file):
        st.audio(voice_file)
        if st.button(get_text("analyze"), key="analyze_voice"):
            report = generate_mock_report(voice_file, "Voice Recording")
            if report:
                st.session_state["voice_report"] = report
                st.success(get_text("report_generated"))
                st.text_area("Preview", report, height=200)
    else:
        st.info(get_text("no_recording"))
    
    st.divider()
    
    # --- Video Recording ---
    st.markdown(f"## {get_text('video_rec_title')}")
    video_key = "video_recorder"
    video_file = "video_output.mp4"
    
    video_start = st.button(f"📹 {get_text('start_recording')}", key="video_start")
    video_stop = st.button(f"⏹️ {get_text('stop_recording')}", key="video_stop")
    
    if video_start:
        st.session_state.video_active = True
    if video_stop:
        st.session_state.video_active = False
    
    if st.session_state.get("video_active", False):
        st.info("🔴 Recording video + audio... Click 'Stop Recording' when done.")
        ctx_video = webrtc_streamer(
            key=video_key,
            mode=WebRtcMode.SENDRECV,
            audio_receiver_size=1024,
            media_stream_constraints={"audio": True, "video": True},
            out_recorder_filename=video_file
        )
    else:
        webrtc_streamer(key=video_key + "_idle", desired_playing_state=False)
    
    if os.path.exists(video_file):
        st.video(video_file)
        if st.button(get_text("analyze"), key="analyze_video"):
            report = generate_mock_report(video_file, "Video Recording")
            if report:
                st.session_state["video_report"] = report
                st.success(get_text("report_generated"))
                st.text_area("Preview", report, height=200)
    else:
        st.info(get_text("no_recording"))

# ========= TAB 3: REPORT DOWNLOAD =========
with tab3:
    st.markdown("### 📥 Download Analysis Report")
    report_choice = st.radio("Choose report:", ["Voice Report", "Video Report"])
    if report_choice == "Voice Report":
        report_content = st.session_state.get("voice_report", "")
    else:
        report_content = st.session_state.get("video_report", "")
    
    if report_content:
        filename = save_report_file(report_content, report_choice.replace(" ", "_").lower())
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                st.download_button(
                    label=get_text("download_report"),
                    data=f.read(),
                    file_name=filename,
                    mime="text/plain"
                )
            os.remove(filename)
    else:
        st.info("No report yet. Please record and analyze in the 'Record & Analyze' tab.")
