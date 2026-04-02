import streamlit as st
from streamlit_webrtc import webrtc_streamer
import datetime
import os
import random
from PIL import Image
import yt_dlp

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
if "converted_mp3_path" not in st.session_state:
    st.session_state.converted_mp3_path = None
if "converted_mp3_report" not in st.session_state:
    st.session_state.converted_mp3_report = None
if "example_url" not in st.session_state:
    st.session_state.example_url = ""

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
        "radio_tab": "📡 My Audio", "record_tab": "🎙️ Record & Analyze", "report_tab": "📄 Download Report", "convert_tab": "🎬 URL → MP3",
        "language": "Language", "price_label": "💰 Price (One-time)", "price_value": "**$149 USD** (lifetime license)",
        "user_info": "👤 Founder & Developer", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – All Rights Reserved",
        "upload_audio": "Upload audio file (MP3, WAV, OGG)",
        "voice_rec_title": "🎤 Voice Recording", "video_rec_title": "📹 Video Recording",
        "start_recording": "Start", "stop_recording": "Stop", "analyze": "📊 Analyze",
        "download_report": "⬇️ Download Report", "no_recording": "No recording yet.",
        "report_generated": "Report generated!", "analysis_result": "Analysis Result (simulated)",
        "recording_info": "Recording Info", "duration_sec": "Duration (s)", "file_size_kb": "Size (KB)",
        "mock_analysis": "Speech clarity 85%, low noise, sentiment positive.",
        "logout": "🚪 Logout", "demo_mode": "🎮 Demo Mode (no real recording)", "demo_active": "Demo mode active – using mock data.",
        "video_url": "Any URL (video, live stream, radio stream, etc.)",
        "convert_btn": "🔄 Download as MP3 & Use in App",
        "converting": "Downloading and converting audio... please wait.",
        "conversion_success": "Conversion successful! MP3 is now available below and in the 'My Audio' tab.",
        "conversion_error": "Conversion failed. Check URL or try again.",
        "analyze_converted": "📊 Analyze this MP3 (generate report)",
        "no_converted": "No MP3 converted yet. Use the converter above.",
        "converted_player": "🎵 Converted MP3 Player",
        "analyze_btn": "Generate Report from this MP3",
        "my_audio": "🎧 Your uploaded and converted audio"
    },
    "es": {
        "welcome": "Bienvenido a GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Mi Audio", "record_tab": "🎙️ Grabar y Analizar", "report_tab": "📄 Descargar Informe", "convert_tab": "🎬 URL → MP3",
        "language": "Idioma", "price_label": "💰 Precio (único pago)", "price_value": "**149 USD** (licencia vitalicia)",
        "user_info": "👤 Fundador", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – Todos los derechos reservados",
        "upload_audio": "Subir archivo de audio (MP3, WAV, OGG)",
        "voice_rec_title": "🎤 Grabación de Voz", "video_rec_title": "📹 Grabación de Vídeo",
        "start_recording": "Iniciar", "stop_recording": "Detener", "analyze": "📊 Analizar",
        "download_report": "⬇️ Descargar Informe", "no_recording": "Sin grabación.",
        "report_generated": "¡Informe generado!", "analysis_result": "Resultado (simulado)",
        "recording_info": "Información", "duration_sec": "Duración (s)", "file_size_kb": "Tamaño (KB)",
        "mock_analysis": "Claridad 85%, ruido bajo, sentimiento positivo.",
        "logout": "🚪 Cerrar sesión", "demo_mode": "🎮 Modo Demo (sin grabación real)", "demo_active": "Modo demo activo – usando datos simulados.",
        "video_url": "Cualquier URL (video, transmisión en vivo, radio, etc.)",
        "convert_btn": "🔄 Descargar como MP3 y usar en la App",
        "converting": "Descargando y convirtiendo audio... espere.",
        "conversion_success": "¡Conversión exitosa! El MP3 ya está disponible abajo y en la pestaña 'Mi Audio'.",
        "conversion_error": "Error en la conversión. Verifique la URL o intente de nuevo.",
        "analyze_converted": "📊 Analizar este MP3 (generar informe)",
        "no_converted": "No se ha convertido ningún MP3. Use el convertidor arriba.",
        "converted_player": "🎵 Reproductor de MP3 convertido",
        "analyze_btn": "Generar informe desde este MP3",
        "my_audio": "🎧 Tu audio subido y convertido"
    },
    "fr": {
        "welcome": "Bienvenue sur GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Mon Audio", "record_tab": "🎙️ Enregistrer et Analyser", "report_tab": "📄 Télécharger Rapport", "convert_tab": "🎬 URL → MP3",
        "language": "Langue", "price_label": "💰 Prix (unique)", "price_value": "**149 USD** (licence à vie)",
        "user_info": "👤 Fondateur", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – Tous droits réservés",
        "upload_audio": "Télécharger un fichier audio (MP3, WAV, OGG)",
        "voice_rec_title": "🎤 Enregistrement vocal", "video_rec_title": "📹 Enregistrement vidéo",
        "start_recording": "Démarrer", "stop_recording": "Arrêter", "analyze": "📊 Analyser",
        "download_report": "⬇️ Télécharger", "no_recording": "Aucun enregistrement.",
        "report_generated": "Rapport généré !", "analysis_result": "Résultat (simulé)",
        "recording_info": "Infos", "duration_sec": "Durée (s)", "file_size_kb": "Taille (Ko)",
        "mock_analysis": "Clarté 85%, bruit faible, sentiment positif.",
        "logout": "🚪 Déconnexion", "demo_mode": "🎮 Mode Démo (pas d'enregistrement réel)", "demo_active": "Mode démo actif – données simulées.",
        "video_url": "N'importe quelle URL (vidéo, direct, radio, etc.)",
        "convert_btn": "🔄 Télécharger en MP3 et utiliser dans l'app",
        "converting": "Téléchargement et conversion audio... veuillez patienter.",
        "conversion_success": "Conversion réussie ! Le MP3 est maintenant disponible ci-dessous et dans l'onglet 'Mon Audio'.",
        "conversion_error": "Échec de la conversion. Vérifiez l'URL ou réessayez.",
        "analyze_converted": "📊 Analyser ce MP3 (générer un rapport)",
        "no_converted": "Aucun MP3 converti. Utilisez le convertisseur ci-dessus.",
        "converted_player": "🎵 Lecteur MP3 converti",
        "analyze_btn": "Générer un rapport à partir de ce MP3",
        "my_audio": "🎧 Votre audio téléchargé et converti"
    },
    "ht": {
        "welcome": "Byenveni nan GlobalInternet.py Radio Suite",
        "radio_tab": "📡 Odyo Mwen", "record_tab": "🎙️ Anrejistre ak Analize", "report_tab": "📄 Telechaje Rapò", "convert_tab": "🎬 URL → MP3",
        "language": "Lang", "price_label": "💰 Pri (yon sèl fwa)", "price_value": "**149 USD** (lisans pou tout lavi)",
        "user_info": "👤 Fondatè ak Devlopè", "user_name": "Gesner Deslandes", "user_company": "GlobalInternet.py",
        "user_phone": "(509) 4738-5663", "user_email": "deslandes78@gmail.com",
        "license": "© 2025 GlobalInternet.py – Tout dwa rezève",
        "upload_audio": "Telechaje fichye odyo (MP3, WAV, OGG)",
        "voice_rec_title": "🎤 Anrejistreman Vwa", "video_rec_title": "📹 Anrejistreman Videyo",
        "start_recording": "Kòmanse", "stop_recording": "Sispann", "analyze": "📊 Analize",
        "download_report": "⬇️ Telechaje Rapò", "no_recording": "Pa gen anrejistreman.",
        "report_generated": "Rapò kreye!", "analysis_result": "Rezilta Analiz (simile)",
        "recording_info": "Enfòmasyon Anrejistreman", "duration_sec": "Dire (s)", "file_size_kb": "Gwosè (KB)",
        "mock_analysis": "Klète vwa 85%, bri ba, santiman pozitif.",
        "logout": "🚪 Dekonekte", "demo_mode": "🎮 Mòd Demo (pa gen anrejistreman reyèl)", "demo_active": "Mòd demo aktif – itilize done similes.",
        "video_url": "Nenpòt URL (videyo, live, radyo, elth)",
        "convert_btn": "🔄 Telechaje kòm MP3 epi itilize nan App",
        "converting": "Telechaje ak konvèti odyo... tanpri tann.",
        "conversion_success": "Konvèsyon siksè! MP3 la disponib anba a ak nan tab 'Odyo Mwen'.",
        "conversion_error": "Konvèsyon echwe. Tcheke URL la oswa eseye ankò.",
        "analyze_converted": "📊 Analize MP3 sa a (kreye rapò)",
        "no_converted": "Pa gen MP3 konvèti. Sèvi ak konvètisè pi wo a.",
        "converted_player": "🎵 Lektè MP3 konvèti",
        "analyze_btn": "Kreye rapò apati MP3 sa a",
        "my_audio": "🎧 Odyo ou telechaje ak konvèti"
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

# ========= ENHANCED CONVERTER WITH MULTI-STRATEGY =========
def find_converted_mp3():
    mp3_files = [f for f in os.listdir('.') if f.startswith('converted_audio') and f.endswith('.mp3')]
    if mp3_files:
        return max(mp3_files, key=os.path.getctime)
    return None

def try_strategy_1(url):
    """Default method with modern headers"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'converted_audio_%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)
    return find_converted_mp3()

def try_strategy_2(url):
    """Use cookies.txt file if available"""
    if not os.path.exists('cookies.txt'):
        return None
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'converted_audio_%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)
    return find_converted_mp3()

def try_strategy_3(url):
    """Alternative audio format (m4a)"""
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'converted_audio_%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)
    return find_converted_mp3()

def convert_url_to_mp3(url):
    """Multi‑strategy converter"""
    strategies = [
        ("Default method", try_strategy_1),
        ("Using cookies.txt", try_strategy_2),
        ("Alternative audio format (m4a)", try_strategy_3),
    ]
    for strategy_name, strategy_func in strategies:
        try:
            st.info(f"🔄 Trying: {strategy_name}...")
            result = strategy_func(url)
            if result:
                st.success(f"✅ Success using {strategy_name}")
                return result
        except Exception as e:
            st.warning(f"⚠️ {strategy_name} failed: {str(e)[:100]}")
            continue
    return None

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
# MAIN TABS (4 tabs)
# ------------------------------
tab1, tab2, tab3, tab4 = st.tabs([get_text("radio_tab"), get_text("record_tab"), get_text("report_tab"), get_text("convert_tab")])

# ========= TAB 1: MY AUDIO =========
with tab1:
    st.markdown(f"### {get_text('my_audio')}")
    uploaded_file = st.file_uploader(get_text("upload_audio"), type=["mp3","wav","ogg"])
    if uploaded_file:
        st.audio(uploaded_file)
    if st.session_state.converted_mp3_path and os.path.exists(st.session_state.converted_mp3_path):
        st.markdown("---")
        st.markdown(f"### {get_text('converted_player')}")
        st.audio(st.session_state.converted_mp3_path)

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

# ========= TAB 3: DOWNLOAD REPORT =========
with tab3:
    st.markdown("### 📥 Download Report")
    report_choice = st.radio("Choose:", ["Voice Report", "Video Report", "Converted MP3 Report"])
    if report_choice == "Voice Report":
        content = st.session_state.get("voice_report", "")
    elif report_choice == "Video Report":
        content = st.session_state.get("video_report", "")
    else:
        content = st.session_state.get("converted_mp3_report", "")
    if content:
        fname = save_report_file(content, report_choice.replace(" ", "_").lower())
        if fname:
            with open(fname, "r") as f:
                st.download_button(get_text("download_report"), f.read(), file_name=fname, mime="text/plain")
            os.remove(fname)
    else:
        st.info("No report yet. Record/convert and analyze first.")

# ========= TAB 4: URL → MP3 CONVERTER =========
with tab4:
    st.markdown("## 🎬 Convert any URL (video, live stream, radio) to MP3")
    st.caption("Supports YouTube, Vimeo, Facebook, Twitter, TikTok, direct video URLs, live streams, icecast radio, etc.")
    
    example_urls = {
        "YouTube Music (test)": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "Radio France Inter (MP3 stream)": "http://icecast.radiofrance.fr/franceinter-midfi.mp3",
        "BBC World Service": "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
    }
    selected_example = st.selectbox("Try one of these working URLs:", list(example_urls.keys()))
    if st.button("Use this example URL"):
        video_url = example_urls[selected_example]
        st.session_state.example_url = video_url
        st.rerun()
    
    default_url = st.session_state.get("example_url", "")
    video_url = st.text_input(get_text("video_url"), value=default_url, placeholder="https://www.youtube.com/watch?v=... or http://radio.stream/live")
    
    if st.button(get_text("convert_btn")):
        if video_url:
            with st.spinner(get_text("converting")):
                mp3_file = convert_url_to_mp3(video_url)
                if mp3_file and os.path.exists(mp3_file):
                    st.session_state.converted_mp3_path = mp3_file
                    st.success(get_text("conversion_success"))
                    st.audio(mp3_file)
                else:
                    st.error(get_text("conversion_error"))
                    st.info("If the URL is a live radio stream, try extracting the direct .mp3/.aac link from the station's website. For YouTube, the converter works fine.")
        else:
            st.warning("Please enter a URL.")
    
    if st.session_state.converted_mp3_path and os.path.exists(st.session_state.converted_mp3_path):
        st.markdown(f"### {get_text('converted_player')}")
        st.audio(st.session_state.converted_mp3_path)
        if st.button(get_text("analyze_btn"), key="analyze_converted"):
            report = generate_mock_report(st.session_state.converted_mp3_path, "Converted MP3 from URL")
            if report:
                st.session_state["converted_mp3_report"] = report
                st.success(get_text("report_generated"))
                st.text_area("Preview", report, height=200)
    else:
        st.info(get_text("no_converted"))
