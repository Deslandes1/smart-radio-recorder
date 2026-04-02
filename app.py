import streamlit as st
import streamlit_webrtc as webrtc
import av
import datetime
import os
import numpy as np
import pandas as pd
from pathlib import Path

# ------------------------------
# Multi-language dictionaries
# ------------------------------
LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Français": "fr"
}

TEXTS = {
    "en": {
        "title": "🌐 Smart Internet Radio & Recorder",
        "subtitle": "Stream, record, analyze & report",
        "radio_tab": "📡 Internet Radio",
        "record_tab": "🎙️ Recording & Analysis",
        "report_tab": "📄 Reports",
        "language": "Language",
        "price_label": "💰 Price",
        "price_value": "**$19.99/month** or **$99 lifetime**",
        "user_info": "👤 Developer Info",
        "user_name": "Alex Johnson (your name here)",
        "user_email": "alex@example.com",
        "user_website": "www.example.com",
        "radio_url": "Radio Stream URL",
        "radio_placeholder": "http://icecast.example.com/stream.mp3",
        "play_radio": "▶️ Play",
        "upload_audio": "Or upload an audio file (offline listening)",
        "voice_rec_title": "🎤 Voice Recording",
        "video_rec_title": "📹 Video Recording",
        "start_voice": "Start Voice Recording",
        "stop_voice": "Stop Voice Recording",
        "start_video": "Start Video Recording",
        "stop_video": "Stop Video Recording",
        "analyze_voice": "📊 Analyze Voice Recording",
        "analyze_video": "📊 Analyze Video Recording",
        "download_report": "⬇️ Download Report",
        "no_file": "No recording available. Please record first.",
        "report_generated": "Report generated!",
        "analysis_result": "Analysis result",
        "recording_info": "Recording info",
        "duration": "Duration (seconds)",
        "file_size": "File size (KB)",
        "mock_analysis": "Mock analysis (real app would use speech‑to‑text / emotion detection)",
        "report_hint": "This report contains metadata + a simulated AI analysis."
    },
    "es": {
        "title": "🌐 Radio Internet Inteligente & Grabador",
        "subtitle": "Transmite, graba, analiza y genera informes",
        "radio_tab": "📡 Radio Online",
        "record_tab": "🎙️ Grabación y Análisis",
        "report_tab": "📄 Informes",
        "language": "Idioma",
        "price_label": "💰 Precio",
        "price_value": "**$19.99/mes** o **$99 de por vida**",
        "user_info": "👤 Información del Desarrollador",
        "user_name": "Alex Johnson (tu nombre aquí)",
        "user_email": "alex@example.com",
        "user_website": "www.example.com",
        "radio_url": "URL de la emisora",
        "radio_placeholder": "http://icecast.example.com/stream.mp3",
        "play_radio": "▶️ Reproducir",
        "upload_audio": "O sube un archivo de audio (escucha sin conexión)",
        "voice_rec_title": "🎤 Grabación de Voz",
        "video_rec_title": "📹 Grabación de Vídeo",
        "start_voice": "Iniciar grabación de voz",
        "stop_voice": "Detener grabación de voz",
        "start_video": "Iniciar grabación de vídeo",
        "stop_video": "Detener grabación de vídeo",
        "analyze_voice": "📊 Analizar grabación de voz",
        "analyze_video": "📊 Analizar grabación de vídeo",
        "download_report": "⬇️ Descargar Informe",
        "no_file": "No hay grabación disponible. Graba primero.",
        "report_generated": "¡Informe generado!",
        "analysis_result": "Resultado del análisis",
        "recording_info": "Información de la grabación",
        "duration": "Duración (segundos)",
        "file_size": "Tamaño del archivo (KB)",
        "mock_analysis": "Análisis simulado (la app real usaría reconocimiento de voz / emociones)",
        "report_hint": "Este informe contiene metadatos + un análisis simulado por IA."
    },
    "fr": {
        "title": "🌐 Radio Internet Intelligente & Enregistreur",
        "subtitle": "Diffusez, enregistrez, analysez et rapportez",
        "radio_tab": "📡 Radio Internet",
        "record_tab": "🎙️ Enregistrement & Analyse",
        "report_tab": "📄 Rapports",
        "language": "Langue",
        "price_label": "💰 Prix",
        "price_value": "**19,99 $/mois** ou **99 $ à vie**",
        "user_info": "👤 Infos Développeur",
        "user_name": "Alex Johnson (votre nom ici)",
        "user_email": "alex@example.com",
        "user_website": "www.example.com",
        "radio_url": "URL du flux radio",
        "radio_placeholder": "http://icecast.example.com/stream.mp3",
        "play_radio": "▶️ Lire",
        "upload_audio": "Ou téléchargez un fichier audio (écoute hors ligne)",
        "voice_rec_title": "🎤 Enregistrement vocal",
        "video_rec_title": "📹 Enregistrement vidéo",
        "start_voice": "Démarrer l'enregistrement vocal",
        "stop_voice": "Arrêter l'enregistrement vocal",
        "start_video": "Démarrer l'enregistrement vidéo",
        "stop_video": "Arrêter l'enregistrement vidéo",
        "analyze_voice": "📊 Analyser l'enregistrement vocal",
        "analyze_video": "📊 Analyser l'enregistrement vidéo",
        "download_report": "⬇️ Télécharger le rapport",
        "no_file": "Aucun enregistrement disponible. Veuillez enregistrer d'abord.",
        "report_generated": "Rapport généré !",
        "analysis_result": "Résultat de l'analyse",
        "recording_info": "Infos d'enregistrement",
        "duration": "Durée (secondes)",
        "file_size": "Taille du fichier (Ko)",
        "mock_analysis": "Analyse simulée (l'app réelle utiliserait reconnaissance vocale / émotions)",
        "report_hint": "Ce rapport contient des métadonnées + une analyse IA simulée."
    }
}

# ------------------------------
# Helper functions
# ------------------------------
def get_text(key):
    lang_code = st.session_state.get("language", "en")
    return TEXTS[lang_code].get(key, key)

def generate_report(file_path, rec_type):
    """Generate a simple report from recorded file (mock analysis)."""
    if not file_path or not os.path.exists(file_path):
        return None
    file_size_kb = os.path.getsize(file_path) / 1024
    mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    # Mock duration (in a real app you would extract from audio/video)
    # Here we simulate a random duration between 2 and 60 seconds
    import random
    duration_sec = random.randint(3, 45)
    
    report = f"""
    {'='*50}
    {get_text('report_generated').upper()}
    {'='*50}
    
    {get_text('recording_info')}:
    - Type: {rec_type}
    - File: {os.path.basename(file_path)}
    - {get_text('file_size')}: {file_size_kb:.2f} KB
    - {get_text('duration')}: {duration_sec} s
    - Timestamp: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}
    
    {get_text('analysis_result')}:
    {get_text('mock_analysis')}
    - Speech clarity: 87% (simulated)
    - Background noise: low
    - Dominant emotion (if voice): neutral/positive
    - Keywords extracted: [demo, radio, analysis]
    
    {get_text('report_hint')}
    
    {'='*50}
    """
    return report

def save_report(report_text, prefix="report"):
    """Save report to a temporary file and return path."""
    if not report_text:
        return None
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    return filename

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Smart Radio & Recorder", layout="wide")
st.markdown("<h1 style='text-align: center;'>🎧 Smart Internet Radio & Recorder</h1>", unsafe_allow_html=True)

# --- Language selection ---
lang = st.sidebar.selectbox(get_text("language"), list(LANGUAGES.keys()))
st.session_state["language"] = LANGUAGES[lang]

# --- User Info & Price ---
st.sidebar.markdown(f"## {get_text('user_info')}")
st.sidebar.info(f"""
**{get_text('user_name')}**  
📧 {get_text('user_email')}  
🌐 {get_text('user_website')}
""")
st.sidebar.markdown(f"## {get_text('price_label')}")
st.sidebar.success(get_text("price_value"))

# --- Main tabs ---
tab1, tab2, tab3 = st.tabs([get_text("radio_tab"), get_text("record_tab"), get_text("report_tab")])

# ======================
# TAB 1: INTERNET RADIO
# ======================
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        radio_url = st.text_input(get_text("radio_url"), placeholder=get_text("radio_placeholder"))
        if radio_url:
            st.audio(radio_url, format="audio/mpeg")
    with col2:
        st.markdown("### 🎵 Offline option")
        uploaded_file = st.file_uploader(get_text("upload_audio"), type=["mp3", "wav", "ogg"])
        if uploaded_file:
            st.audio(uploaded_file, format="audio/mpeg")

# ======================
# TAB 2: RECORDING & ANALYSIS
# ======================
with tab2:
    st.markdown(f"## {get_text('voice_rec_title')}")
    # Voice recording using streamlit-webrtc (audio only)
    voice_file = "voice_recording.wav"
    voice_recording_active = st.session_state.get("voice_recording_active", False)
    
    col_voice1, col_voice2 = st.columns(2)
    with col_voice1:
        if st.button(get_text("start_voice")):
            st.session_state["voice_recording_active"] = True
            st.rerun()
    with col_voice2:
        if st.button(get_text("stop_voice")):
            st.session_state["voice_recording_active"] = False
            st.rerun()
    
    if voice_recording_active:
        st.info("🎙️ Recording voice... click 'Stop' when done.")
        webrtc_voice = webrtc.webrtc_streamer(
            key="voice",
            video=False,
            audio=True,
            out_recorder_filename=voice_file,
            media_stream_constraints={"audio": True, "video": False}
        )
    else:
        # If not active, we still show the component without recording to avoid re-initialization
        webrtc_voice = webrtc.webrtc_streamer(key="voice_idle", video=False, audio=False)
    
    if os.path.exists(voice_file):
        st.audio(voice_file, format="audio/wav")
        if st.button(get_text("analyze_voice")):
            with st.spinner("Analyzing voice..."):
                report_text = generate_report(voice_file, "Voice Recording")
                if report_text:
                    st.session_state["voice_report"] = report_text
                    st.success(get_text("report_generated"))
                    st.text_area("Preview", report_text, height=250)
    else:
        st.warning(get_text("no_file"))
    
    st.divider()
    
    # Video recording
    st.markdown(f"## {get_text('video_rec_title')}")
    video_file = "video_recording.mp4"
    video_recording_active = st.session_state.get("video_recording_active", False)
    
    col_vid1, col_vid2 = st.columns(2)
    with col_vid1:
        if st.button(get_text("start_video")):
            st.session_state["video_recording_active"] = True
            st.rerun()
    with col_vid2:
        if st.button(get_text("stop_video")):
            st.session_state["video_recording_active"] = False
            st.rerun()
    
    if video_recording_active:
        st.info("📹 Recording video + audio... click 'Stop' when done.")
        webrtc_video = webrtc.webrtc_streamer(
            key="video",
            video=True,
            audio=True,
            out_recorder_filename=video_file,
            media_stream_constraints={"audio": True, "video": True}
        )
    else:
        webrtc_video = webrtc.webrtc_streamer(key="video_idle", video=False, audio=False)
    
    if os.path.exists(video_file):
        st.video(video_file)
        if st.button(get_text("analyze_video")):
            with st.spinner("Analyzing video..."):
                report_text = generate_report(video_file, "Video Recording")
                if report_text:
                    st.session_state["video_report"] = report_text
                    st.success(get_text("report_generated"))
                    st.text_area("Preview", report_text, height=250)

# ======================
# TAB 3: REPORT DOWNLOAD
# ======================
with tab3:
    st.markdown("### 📥 Download analysis report")
    report_choice = st.radio("Select report to download:", ["Voice report", "Video report"])
    
    if report_choice == "Voice report":
        report_content = st.session_state.get("voice_report", "")
    else:
        report_content = st.session_state.get("video_report", "")
    
    if report_content:
        filename = save_report(report_content, prefix=report_choice.replace(" ", "_").lower())
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                st.download_button(
                    label=get_text("download_report"),
                    data=f.read(),
                    file_name=filename,
                    mime="text/plain"
                )
            os.remove(filename)  # clean up temp file
    else:
        st.info("No report available. Please record and analyze first in the 'Recording & Analysis' tab.")
