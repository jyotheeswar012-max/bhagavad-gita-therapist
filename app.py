import streamlit as st
from therapist import get_gita_guidance
from gita_data import SHLOKAS, CHAPTER_NAMES
from music import MUSIC_TRACKS
from export_utils import build_text_export, build_pdf_export
from i18n import LANGUAGES, LABELS, t
from analytics import log_query, render_analytics
import asyncio
import edge_tts
import os
import tempfile
import requests
from gtts import gTTS
import io
import re
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import base64
import json

st.set_page_config(
    page_title="Bhagavad Gita AI Therapist",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Inter:wght@300;400;500&display=swap');

  .stApp {
    background: #0d0500 !important;
    font-family: 'Inter', sans-serif;
  }
  .block-container {
    padding: 0 !important;
    max-width: 100% !important;
  }

  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  .stDeployButton { display: none !important; }
  header[data-testid="stHeader"] { background: transparent !important; }
  header[data-testid="stHeader"] a,
  header[data-testid="stHeader"] span { visibility: hidden !important; }
  button[data-testid="collapsedControl"],
  button[kind="header"],
  [data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
  }

  div[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #0a0300 !important;
    border-right: 1px solid #2a1200 !important;
    min-width: 240px !important;
  }
  div[data-testid="stSidebar"] * { color: #d4a96a !important; }
  div[data-testid="stSidebar"] h2 { color: #ffd700 !important; font-family: 'Playfair Display', serif !important; }

  .hero-wrap {
    min-height: 100vh;
    background: radial-gradient(ellipse at 30% 50%, #2a0e00 0%, #0d0500 60%);
    display: flex;
    align-items: center;
    padding: 60px 6vw;
    gap: 4vw;
  }
  .hero-left { flex: 1.1; min-width: 0; }
  .hero-right { flex: 0.9; min-width: 0; }
  .tagline { letter-spacing:.22em;font-size:11px;color:#8a6030;text-transform:uppercase;margin-bottom:28px;font-weight:400; }
  .hero-h1 { font-family:'Playfair Display',Georgia,serif;font-size:clamp(2.4rem,5vw,4rem);font-weight:700;color:#f5e6cc;line-height:1.15;margin:0 0 8px 0; }
  .hero-h1 em { font-style:italic;font-weight:400;color:#e8d5b0; }
  .hero-sub { font-size:15px;color:#9a8060;line-height:1.75;margin:22px 0 36px 0;max-width:480px;font-weight:300; }
  .cta-row { display:flex;align-items:flex-start;gap:22px;margin-bottom:44px;flex-wrap:wrap; }
  .krishna-card { position:relative;border-radius:24px;overflow:hidden;background:#1a0800;box-shadow:0 32px 80px rgba(0,0,0,0.7),0 0 0 1px rgba(255,180,50,0.12); }
  .krishna-card img { width:100%;display:block;border-radius:24px;object-fit:cover;max-height:520px; }
  .verse-overlay { position:absolute;bottom:0;left:0;right:0;background:linear-gradient(0deg,rgba(5,2,0,0.95) 0%,rgba(5,2,0,0.6) 70%,transparent 100%);padding:28px 24px 24px 24px;border-radius:0 0 24px 24px; }
  .verse-sanskrit { font-family:'Playfair Display',serif;font-size:17px;color:#f5e6cc;margin-bottom:8px;line-height:1.5; }
  .verse-english { font-size:13px;color:#c8a060;font-style:italic;line-height:1.6; }
  .verse-ref { font-size:11px;color:#8a6030;margin-top:4px;letter-spacing:.05em; }
  .input-section { background:radial-gradient(ellipse at 50% 0%,#1a0800 0%,#0d0500 70%);padding:70px 8vw 60px 8vw;border-top:1px solid #1e0d00; }
  .stTextArea textarea { background:rgba(255,255,255,0.03)!important;border:1px solid #2a1800!important;border-radius:14px!important;color:#f0e6d3!important;font-size:15px!important;font-family:'Inter',sans-serif!important;padding:16px!important; }
  .stTextArea textarea:focus { border-color:#e87000!important;box-shadow:0 0 0 2px rgba(232,112,0,0.15)!important; }
  .stButton > button { background:linear-gradient(135deg,#e87000,#ffc200)!important;color:#1a0800!important;font-weight:700!important;border-radius:50px!important;border:none!important;font-size:15px!important;padding:14px 36px!important;font-family:'Inter',sans-serif!important;letter-spacing:.02em!important; }
  .shloka-box { background:linear-gradient(135deg,rgba(45,18,0,0.9),rgba(74,30,0,0.8));border:1px solid rgba(255,140,0,0.3);border-radius:20px;padding:28px;margin:16px 0; }
  .guidance-box { background:linear-gradient(135deg,rgba(10,22,40,0.9),rgba(26,45,74,0.8));border:1px solid rgba(74,158,255,0.25);border-radius:20px;padding:28px;margin:16px 0; }
  .disclaimer-box { background:rgba(26,10,0,0.7);border:1px solid rgba(255,107,53,0.3);border-left:3px solid #ff6b35;border-radius:12px;padding:16px 20px;margin:10px 0 18px 0; }
  .privacy-box { background:rgba(0,26,10,0.6);border:1px solid rgba(46,204,113,0.25);border-left:3px solid #2ecc71;border-radius:12px;padding:14px 20px;margin:10px 0; }
  .stats-bar { display:flex;gap:40px;margin:40px 0 0 0;flex-wrap:wrap; }
  .stat-item { text-align:left; }
  .stat-num { font-family:'Playfair Display',serif;font-size:1.8rem;color:#ffd700;font-weight:700;line-height:1; }
  .stat-label { font-size:11px;color:#6a5030;letter-spacing:.1em;text-transform:uppercase;margin-top:4px; }

  /* Featured shloka mini-card next to CTA button */
  .hero-verse-chip {
    background: linear-gradient(135deg, rgba(50,20,0,0.85), rgba(80,35,0,0.7));
    border: 1px solid rgba(255,160,40,0.25);
    border-radius: 16px;
    padding: 14px 20px;
    max-width: 320px;
    backdrop-filter: blur(4px);
  }
  .hero-verse-chip .hvc-sanskrit {
    font-family: 'Playfair Display', serif;
    font-size: 15px;
    color: #f5c97a;
    line-height: 1.6;
    margin: 0 0 5px 0;
  }
  .hero-verse-chip .hvc-english {
    font-size: 12px;
    color: #9a7a50;
    font-style: italic;
    line-height: 1.5;
    margin: 0 0 4px 0;
  }
  .hero-verse-chip .hvc-ref {
    font-size: 10px;
    color: #6a4a20;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin: 0;
  }

  @media (max-width:768px) {
    .hero-wrap { flex-direction:column;padding:40px 5vw;min-height:auto; }
    .hero-right { width:100%; }
    .hero-h1 { font-size:2rem; }
    .input-section { padding:50px 5vw 40px 5vw; }
    .stats-bar { gap:24px; }
    .hero-verse-chip { max-width:100%; }
  }
</style>
""", unsafe_allow_html=True)

CACHE_DIR = "/tmp/gita_audio"
os.makedirs(CACHE_DIR, exist_ok=True)

HERO_IMG_LOCAL = "assets/krishna-flute.jpg"
HERO_IMG_URL   = "https://raw.githubusercontent.com/jyotheeswar012-max/bhagavad-gita-therapist/main/assets/krishna-flute.jpg"

IMAGE_SETS = {
    "krishna_arjuna": {"local": "assets/krishna_arjuna.jpg", "min_size": 5000, "urls": ["https://www.holy-bhagavad-gita.org/public/img/arjuna-and-krishna-on-chariot.jpg"], "label": "Krishna & Arjuna"},
    "krishna_flute":  {"local": HERO_IMG_LOCAL, "min_size": 100000, "urls": [HERO_IMG_URL, "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/BhagavatamKrishna.jpg/800px-BhagavatamKrishna.jpg"], "label": "Lord Krishna"},
    "kurukshetra":    {"local": "assets/kurukshetra.jpg", "min_size": 5000, "urls": ["https://www.holy-bhagavad-gita.org/public/img/kurukshetra.jpg"], "label": "Kurukshetra"},
    "gita_teaching":  {"local": "assets/gita_teaching.jpg", "min_size": 5000, "urls": ["https://www.holy-bhagavad-gita.org/public/img/krishna-teaching.jpg"], "label": "Gita Teaching"},
}


def make_placeholder(label):
    w, h = 600, 520
    img = Image.new("RGB", (w, h), (13, 5, 0))
    draw = ImageDraw.Draw(img)
    for i, col in enumerate([(80, 40, 0), (60, 28, 0)]):
        draw.rectangle([i*2, i*2, w-1-i*2, h-1-i*2], outline=col, width=1)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    draw.text((w//2-30, h//2-20), "🕉️", fill=(255, 215, 0), font=font)
    return img


@st.cache_resource
def load_images():
    imgs = {}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "image/*"}
    for name, cfg in IMAGE_SETS.items():
        min_size = cfg.get("min_size", 5000)
        if os.path.exists(cfg["local"]):
            try:
                if os.path.getsize(cfg["local"]) >= min_size:
                    imgs[name] = Image.open(cfg["local"]).convert("RGB")
                    continue
            except Exception:
                pass
        for url in cfg["urls"]:
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200 and len(r.content) > 5000:
                    imgs[name] = Image.open(io.BytesIO(r.content)).convert("RGB")
                    break
            except Exception:
                continue
        if name not in imgs:
            imgs[name] = make_placeholder(cfg["label"])
    return imgs


IMGS = load_images()


def img_to_b64(img):
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


from config import ELEVENLABS_VOICES as GURU_VOICES
from config import (
    EDGE_TTS_SHLOKA_VOICE, EDGE_TTS_SHLOKA_RATE, EDGE_TTS_SHLOKA_PITCH,
    EDGE_TTS_GUIDANCE_VOICE, EDGE_TTS_GUIDANCE_RATE, EDGE_TTS_GUIDANCE_PITCH,
)


def is_valid_mp3(data):
    if len(data) < 4: return False
    if data[:3] == b"ID3": return True
    if data[0] == 0xFF and (data[1] & 0xE0) == 0xE0: return True
    return False


def clean_meaning(text):
    text = (text or "").strip()
    if not text: return ""
    has_devanagari = bool(re.search(r"[\u0900-\u097F]", text))
    has_gloss_marks = "?" in text
    if not (has_devanagari and has_gloss_marks): return text
    ascii_text = text.encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"\b\d+(?:\.\d+)?\b", " ", ascii_text)
    ascii_text = re.sub(r"\b[A-Za-z]+\?\b", " ", ascii_text)
    ascii_text = re.sub(r"\?+", " ", ascii_text)
    ascii_text = re.sub(r"\b(?:No commentary|No commentry)\.?\b", " ", ascii_text, flags=re.IGNORECASE)
    ascii_text = re.sub(r"\s+", " ", ascii_text).strip()
    sentences = re.findall(r"[A-Z][^.?!]*[.?!]", ascii_text)
    cleaned = " ".join(s.strip() for s in sentences)
    if cleaned: return cleaned
    fragments = [frag.strip(" -,:;") for frag in re.split(r"(?<=[a-z])\s+(?=[A-Z])", ascii_text) if frag.strip()]
    english_like = [frag for frag in fragments if len(frag.split()) >= 3]
    return " ".join(english_like).strip() or "English meaning unavailable."


def get_sanskrit_display(shloka):
    """Return (text, type) for display. type is 'devanagari', 'transliteration', or 'none'."""
    sanskrit = (shloka.get("sanskrit") or "").strip()
    if sanskrit and re.search(r"[\u0900-\u097F]", sanskrit):
        return sanskrit, "devanagari"
    transliteration = (shloka.get("transliteration") or "").strip()
    if transliteration:
        return transliteration, "transliteration"
    roman = (shloka.get("roman") or shloka.get("iast") or "").strip()
    if roman:
        return roman, "transliteration"
    if sanskrit:
        return sanskrit, "transliteration"
    return "", "none"


def build_voice_script(shloka):
    ch, v = shloka["chapter"], shloka["verse"]
    meaning = clean_meaning(shloka.get("meaning", ""))
    sanskrit_text, sanskrit_type = get_sanskrit_display(shloka)
    if sanskrit_type == "devanagari" and sanskrit_text:
        script = (
            f"Chapter {ch}, Verse {v}. "
            f"{sanskrit_text} "
            f"... meaning ... {meaning} "
            f"... Contemplate on this wisdom."
        )
    elif sanskrit_type == "transliteration" and sanskrit_text:
        script = (
            f"Chapter {ch}, Verse {v}. "
            f"{sanskrit_text} "
            f"... meaning ... {meaning} "
            f"... Contemplate on this wisdom."
        )
    else:
        script = (
            f"Chapter {ch}, Verse {v}. "
            f"The Lord says ... {meaning} "
            f"Contemplate on this wisdom."
        )
    return script


def get_elevenlabs_audio(text, voice_id):
    try:
        api_key = st.secrets.get("ELEVENLABS_API_KEY", "")
        if not api_key: return None
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.85, "similarity_boost": 0.80, "style": 0.40, "use_speaker_boost": True}
        }
        r = requests.post(url, json=payload, headers=headers, timeout=25)
        if r.status_code == 200 and is_valid_mp3(r.content): return r.content
    except Exception:
        pass
    return None


def get_shloka_audio(shloka):
    ch, v = shloka["chapter"], shloka["verse"]
    cache_file = os.path.join(CACHE_DIR, f"{ch}_{v}.mp3")
    if os.path.exists(cache_file):
        data = open(cache_file, "rb").read()
        if is_valid_mp3(data): return data
        os.remove(cache_file)
    script = build_voice_script(shloka)
    for vid in GURU_VOICES:
        audio = get_elevenlabs_audio(script, vid)
        if audio:
            open(cache_file, "wb").write(audio)
            return audio
    sanskrit_text, sanskrit_type = get_sanskrit_display(shloka)
    edge_voice = "hi-IN-MadhurNeural" if sanskrit_type == "devanagari" else EDGE_TTS_SHLOKA_VOICE
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        async def _g():
            await edge_tts.Communicate(
                script, edge_voice,
                rate=EDGE_TTS_SHLOKA_RATE, pitch=EDGE_TTS_SHLOKA_PITCH
            ).save(tmp_path)
        asyncio.run(_g())
        data = open(tmp_path, "rb").read()
        os.unlink(tmp_path)
        if is_valid_mp3(data):
            open(cache_file, "wb").write(data)
            return data
    except Exception:
        pass
    try:
        gtts_lang = "hi" if sanskrit_type == "devanagari" else "en"
        gtts_text = (sanskrit_text + " ... " + clean_meaning(shloka.get("meaning", ""))) if sanskrit_text else clean_meaning(shloka.get("meaning", ""))
        tts = gTTS(text=gtts_text, lang=gtts_lang, slow=True)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        data = buf.read()
        if is_valid_mp3(data):
            open(cache_file, "wb").write(data)
            return data
    except Exception:
        pass
    return None


def make_guidance_voice(script):
    for vid in GURU_VOICES:
        audio = get_elevenlabs_audio(script, vid)
        if audio: return audio
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        async def _g():
            await edge_tts.Communicate(script, EDGE_TTS_GUIDANCE_VOICE, rate=EDGE_TTS_GUIDANCE_RATE, pitch=EDGE_TTS_GUIDANCE_PITCH).save(tmp_path)
        asyncio.run(_g())
        data = open(tmp_path, "rb").read()
        os.unlink(tmp_path)
        return data
    except Exception:
        return None


def render_shloka_card(s, show_chapter=True):
    chapter_name = CHAPTER_NAMES.get(s["chapter"], "") if show_chapter else ""
    meaning = clean_meaning(s.get("meaning", ""))
    sanskrit_text, sanskrit_type = get_sanskrit_display(s)
    if sanskrit_type == "devanagari":
        sanskrit_html = f"<p style='color:#e8a060;font-size:22px;font-family:serif;line-height:2.0;margin:0 0 4px 0;letter-spacing:0.03em;'>{sanskrit_text}</p>"
        sanskrit_label = ""
    elif sanskrit_type == "transliteration":
        sanskrit_html = f"<p style='color:#e8a060;font-size:17px;font-family:Playfair Display,serif;font-style:italic;line-height:1.9;margin:0 0 4px 0;'>{sanskrit_text}</p>"
        sanskrit_label = "<span style='color:#6a5030;font-size:11px;letter-spacing:.1em;text-transform:uppercase;'>Transliteration</span><br/>"
    else:
        sanskrit_html = "<p style='color:#4a3020;font-size:13px;font-style:italic;margin:0 0 4px 0;'>[ Sanskrit text not available ]</p>"
        sanskrit_label = ""
    return f"""
    <div class='shloka-box'>
      <div style='margin-bottom:14px;'>
        <span style='font-family:Playfair Display,serif;font-size:1.1rem;color:#ffd700;font-weight:700;'>🕉️ Chapter {s['chapter']}, Verse {s['verse']}</span>
        <span style='color:#4a3020;font-size:12px;margin-left:10px;'>{chapter_name}</span>
      </div>
      {sanskrit_label}{sanskrit_html}
      <hr style='border:none;border-top:1px solid rgba(255,140,0,0.15);margin:12px 0;'/>
      <p style='color:#c8a878;font-size:15px;line-height:1.8;margin:0;'><em>{meaning}</em></p>
    </div>
    """


# ── Session state ──
DEFAULTS = {
    "preset": "",
    "result": None,
    "voice_audio": {},
    "chat_history": [],
    "feedback": {},
    "show_input": False,
    "favourites": [],
    "language": "English",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── SIDEBAR ──
with st.sidebar:
    lang = st.selectbox(
        "🌐 Language / भाषा / భాష",
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.language),
        key="lang_select",
    )
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.rerun()
    L = LABELS[lang]

    st.image(IMGS["krishna_flute"], use_container_width=True)

    st.markdown(f"## {L['sidebar_music']}")
    selected_track = st.selectbox(L["sidebar_choose_music"], list(MUSIC_TRACKS.keys()), index=0)
    track_path = MUSIC_TRACKS[selected_track]
    if track_path:
        try:
            ab = open(track_path, "rb").read()
            st.markdown(f"<p style='color:#ffd700;font-size:13px;'>▶️ {selected_track}</p>", unsafe_allow_html=True)
            st.audio(ab, format="audio/mp3", loop=True)
        except FileNotFoundError:
            st.error("❌ Audio file not found.")
    else:
        st.markdown("<p style='color:#888;font-size:13px;'>🔇 Music off</p>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"## {L['sidebar_chapters']}")
    selected_chapter = st.selectbox(
        L["sidebar_jump_chapter"],
        options=[""] + list(CHAPTER_NAMES.keys()),
        format_func=lambda x: L["sidebar_select_chapter"] if x == "" else f"Ch {x}: {CHAPTER_NAMES[x].split(' — ')[0]}",
        key="chapter_select",
    )
    if selected_chapter:
        chapter_shlokas = [s for s in SHLOKAS if s["chapter"] == selected_chapter]
        st.markdown(f"**{CHAPTER_NAMES[selected_chapter]}**")
        st.markdown(f"*{len(chapter_shlokas)} shlokas*")
        for s in chapter_shlokas:
            with st.expander(f"Verse {s['verse']}"):
                meaning = clean_meaning(s.get("meaning", ""))
                sanskrit_text, _ = get_sanskrit_display(s)
                st.markdown(f"<p style='color:#ff8c00;font-size:13px;font-family:serif;line-height:1.8;'>{sanskrit_text or '[ Sanskrit unavailable ]'}</p><p style='color:#c8a878;font-size:12px;'><b>Meaning:</b> {meaning}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<p style='color:#6a5030;font-size:12px;'>{t(lang, 'sidebar_shlokas_stat', n=len(SHLOKAS))}</p>", unsafe_allow_html=True)

    if st.session_state.favourites:
        st.markdown("---")
        st.markdown(f"## {L['sidebar_favourites']} ({len(st.session_state.favourites)})")
        for idx, fav in enumerate(st.session_state.favourites):
            meaning = clean_meaning(fav.get("meaning", ""))
            sanskrit_text, _ = get_sanskrit_display(fav)
            with st.expander(f"🕉️ Ch {fav['chapter']}.{fav['verse']}"):
                st.markdown(f"<p style='color:#ff8c00;font-size:13px;font-family:serif;'>{sanskrit_text or '[ Sanskrit unavailable ]'}</p><p style='color:#c8a878;font-size:12px;'>{meaning[:100]}...</p>", unsafe_allow_html=True)
                if st.button("🗑️ Remove", key=f"rm_fav_{idx}"):
                    st.session_state.favourites.pop(idx)
                    st.rerun()
        fav_export = json.dumps(st.session_state.favourites, ensure_ascii=False, indent=2)
        st.download_button(L["export_favs"], data=fav_export, file_name="gita_favourites.json", mime="application/json", use_container_width=True)
    else:
        st.markdown("---")
        st.markdown(f"## {L['sidebar_favourites']}")
        st.caption(L["no_favourites"])

    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown(f"## {L['sidebar_history']}")
        for idx, entry in enumerate(reversed(st.session_state.chat_history), 1):
            fb = entry.get("feedback")
            fb_icon = " 👍" if fb == 1 else (" 👎" if fb == -1 else "")
            with st.expander(f"Turn {len(st.session_state.chat_history)-idx+1}{fb_icon}: {entry['input'][:38]}..."):
                st.markdown(f"*{entry['ts']}*")
                for s in entry["shlokas"]:
                    meaning = clean_meaning(s.get("meaning", ""))
                    st.markdown(f"- Ch {s['chapter']}.{s['verse']}: {meaning[:55]}...")

    render_analytics(st, lang)

    st.markdown("---")
    st.markdown(f"<div style='font-size:11px;color:#4a3020;line-height:1.6;'>🔒 Inputs sent to Groq AI only. Nothing stored.<br><a href='https://groq.com/privacy-policy/' target='_blank' style='color:#6a5030;'>Groq Privacy Policy</a></div>", unsafe_allow_html=True)


# ── HERO ──
FEATURED_VERSES = [
    {
        "sanskrit": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन ।",
        "english": "You have a right to perform your duties, never to the fruits.",
        "ref": "Bhagavad Gita 2.47"
    },
    {
        "sanskrit": "वासांसि जीर्णानि यथा विहाय नवानि गृह्णाति नरोऀपराणि ।",
        "english": "As one casts off worn-out clothes, the soul casts off worn-out bodies to take new ones.",
        "ref": "Bhagavad Gita 2.22"
    },
    {
        "sanskrit": "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत ।",
        "english": "Whenever righteousness declines, I manifest myself to restore dharma.",
        "ref": "Bhagavad Gita 4.7"
    },
    {
        "sanskrit": "नैनं छिन्दन्ति शस्त्राणि नैनं दहति पावकः ।",
        "english": "Weapons cannot cut the soul; fire cannot burn it — it is eternal and indestructible.",
        "ref": "Bhagavad Gita 2.23"
    },
    {
        "sanskrit": "सर्वधर्मान् परित्यज्य मामेकं शरणं व्रज ।",
        "english": "Abandon all duties and surrender unto Me alone — I shall liberate you from all sins.",
        "ref": "Bhagavad Gita 18.66"
    },
]
import hashlib
hour_seed = int(hashlib.md5(datetime.now().strftime("%Y%m%d%H").encode()).hexdigest(), 16)
featured = FEATURED_VERSES[hour_seed % len(FEATURED_VERSES)]
overlay = FEATURED_VERSES[(hour_seed + 1) % len(FEATURED_VERSES)]
krishna_b64 = img_to_b64(IMGS["krishna_flute"])
L = LABELS[st.session_state.language]

st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-left">
    <p class="tagline">{L['hero_tagline']}</p>
    <h1 class="hero-h1">{L['hero_h1_line1']}<br><em>{L['hero_h1_line2']}</em></h1>
    <p class="hero-sub">{L['hero_sub']}</p>
    <div class="cta-row">
      <span style="background:linear-gradient(135deg,#e87000,#ffc200);color:#1a0800;font-weight:600;font-size:15px;padding:14px 32px;border-radius:50px;white-space:nowrap;">{L['btn_seek']} &rarr;</span>
      <div class="hero-verse-chip">
        <p class="hvc-sanskrit">{featured['sanskrit']}</p>
        <p class="hvc-english">{featured['english']}</p>
        <p class="hvc-ref">— {featured['ref']}</p>
      </div>
    </div>
    <div class="stats-bar">
      <div class="stat-item"><div class="stat-num">{len(SHLOKAS)}</div><div class="stat-label">Shlokas</div></div>
      <div class="stat-item"><div class="stat-num">18</div><div class="stat-label">Chapters</div></div>
      <div class="stat-item"><div class="stat-num">100+</div><div class="stat-label">Themes</div></div>
      <div class="stat-item"><div class="stat-num">{len(st.session_state.chat_history)}</div><div class="stat-label">Turns</div></div>
    </div>
  </div>
  <div class="hero-right">
    <div class="krishna-card">
      <img src="data:image/jpeg;base64,{krishna_b64}" alt="Lord Krishna" />
      <div class="verse-overlay">
        <div class="verse-sanskrit">{overlay['sanskrit']}</div>
        <div class="verse-english">{overlay['english']}</div>
        <div class="verse-ref">— {overlay['ref']}</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── INPUT SECTION ──
st.markdown(f"""
<div class="input-section">
  <p style='font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6a5030;margin-bottom:10px;'>{L['input_label']}</p>
  <h2 style='font-family:Playfair Display,serif;font-size:clamp(1.8rem,3vw,2.6rem);color:#f5e6cc;margin-bottom:10px;font-weight:700;'>{L['input_h2']}</h2>
  <p style='font-size:14px;color:#7a6040;margin-bottom:36px;font-weight:300;'>{L['input_sub']}</p>
</div>
""", unsafe_allow_html=True)

EMOTIONS = L["emotions"]
st.markdown(f"<p style='color:#6a5030;font-size:11px;letter-spacing:.18em;text-transform:uppercase;margin:0 0 12px 0;'>{L['feeling_label']}</p>", unsafe_allow_html=True)
cols = st.columns(6)
for i, (label, val) in enumerate(EMOTIONS.items()):
    if cols[i % 6].button(label, use_container_width=True, key=f"chip_{label}"):
        st.session_state.preset = val
        st.session_state.result = None
        st.session_state.voice_audio = {}

user_input = st.text_area(
    "", value=st.session_state.preset,
    placeholder="Share what's on your mind…",
    height=140, label_visibility="collapsed",
)
col1, col2, col3 = st.columns([1.5, 2, 1.5])
with col2:
    seek = st.button(L["btn_seek"], use_container_width=True)

if seek:
    if not user_input.strip():
        st.warning(L["warning_empty"])
    else:
        with st.spinner(L["spinner_seeking"]):
            lang_instruction = L.get("ai_lang_instruction", "Respond in simple English.")
            st.session_state.result = get_gita_guidance(user_input, lang=lang, lang_instruction=lang_instruction)
        st.session_state.voice_audio = {}
        themes = [th for s in st.session_state.result["shlokas"] for th in s.get("themes", [])]
        log_query(themes, language=lang, emotion=st.session_state.preset[:40] if st.session_state.preset else "")
        st.session_state.chat_history.append({
            "input":    user_input,
            "shlokas":  st.session_state.result["shlokas"],
            "guidance": st.session_state.result["guidance"],
            "feedback": None,
            "ts":       datetime.now().strftime("%I:%M %p"),
            "lang":     lang,
        })
        st.session_state.preset = ""


# ── RESULTS ──
if st.session_state.result:
    result = st.session_state.result
    turn_idx = len(st.session_state.chat_history) - 1

    st.markdown("<div style='padding:0 4vw;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;padding:50px 0 20px 0;'>
      <p style='font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6a5030;margin-bottom:10px;'>{L['krishna_speaks']}</p>
      <h2 style='font-family:Playfair Display,serif;font-size:2rem;color:#f5e6cc;margin:0;'>{L['verses_heading']}</h2>
    </div>
    """, unsafe_allow_html=True)

    for i, s in enumerate(result["shlokas"]):
        st.markdown(render_shloka_card(s), unsafe_allow_html=True)

        fav_key = f"{s['chapter']}_{s['verse']}"
        already_saved = any(f"{x['chapter']}_{x['verse']}" == fav_key for x in st.session_state.favourites)
        fa_col1, fa_col2 = st.columns([1, 5])
        with fa_col1:
            if not already_saved:
                if st.button(L["btn_save_fav"], key=f"fav_{fav_key}"):
                    st.session_state.favourites.append(s)
                    st.toast("❤️ Saved to favourites!")
                    st.rerun()
            else:
                st.markdown(f"<span style='color:#ff6b6b;font-size:13px;'>{L['btn_saved_fav']}</span>", unsafe_allow_html=True)

        vkey = f"s_{s['chapter']}_{s['verse']}"
        if vkey not in st.session_state.voice_audio:
            with st.spinner("🕉️ Loading Sanskrit recitation…"):
                audio = get_shloka_audio(s)
            if audio:
                st.session_state.voice_audio[vkey] = audio
        if vkey in st.session_state.voice_audio:
            st.markdown(f"<p style='color:#6a5030;font-size:12px;margin:8px 0 2px 0;'>🔉 Ch {s['chapter']}.{s['verse']} — Sanskrit recitation</p>", unsafe_allow_html=True)
            st.audio(st.session_state.voice_audio[vkey], format="audio/mp3")
        else:
            st.caption("⚠️ Audio unavailable.")

    st.markdown(f"""
    <div style='text-align:center;padding:40px 0 20px 0;'>
      <p style='font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6a5030;margin-bottom:10px;'>{L['guidance_label']}</p>
      <h2 style='font-family:Playfair Display,serif;font-size:2rem;color:#f5e6cc;margin:0;'>{L['guidance_heading']}</h2>
    </div>
    """, unsafe_allow_html=True)

    guidance_text = result["guidance"]
    st.markdown(f"<div class='guidance-box'><p style='color:#c8d8f0;line-height:1.9;font-size:16px;font-family:Playfair Display,serif;font-style:italic;margin:0;'>{guidance_text.replace(chr(10), '<br>')}</p></div>", unsafe_allow_html=True)

    if st.button(L["btn_voice"], key="btn_guidance"):
        full_script = f"O Arjuna. {guidance_text} This is the eternal truth. Go forward with courage. Surrender to the divine will. Tat Tvam Asi."
        with st.spinner(L["spinner_voice"]):
            audio = make_guidance_voice(full_script)
        if audio:
            st.session_state.voice_audio["guidance"] = audio
        else:
            st.error("❌ Voice generation failed.")

    if "guidance" in st.session_state.voice_audio:
        st.audio(st.session_state.voice_audio["guidance"], format="audio/mp3")

    current_fb = st.session_state.chat_history[turn_idx].get("feedback") if st.session_state.chat_history else None
    st.markdown(f"<p style='color:#4a3020;font-size:13px;margin-top:24px;letter-spacing:.05em;'>{L['helpful_q']}</p>", unsafe_allow_html=True)
    fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 5])
    with fb_col1:
        if st.button(L["btn_helpful"] if current_fb != 1 else "✅", key=f"fb_up_{turn_idx}"):
            st.session_state.chat_history[turn_idx]["feedback"] = 1
            st.toast("👍 Thank you!", icon="✅")
            st.rerun()
    with fb_col2:
        if st.button(L["btn_not_helpful"] if current_fb != -1 else "❌", key=f"fb_dn_{turn_idx}"):
            st.session_state.chat_history[turn_idx]["feedback"] = -1
            st.toast("🙏 Thank you for the feedback.", icon="🔄")
            st.rerun()

    st.markdown("<p style='text-align:center;color:#4a3020;font-size:14px;padding:30px 0;font-style:italic;'>✨ Tat Tvam Asi — Thou Art That ✨</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ── HISTORY ──
if st.session_state.chat_history:
    st.markdown(f"""
    <div style='padding:50px 4vw 20px 4vw;border-top:1px solid #1e0d00;'>
      <p style='font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6a5030;margin-bottom:10px;'>{L['history_label']}</p>
      <h2 style='font-family:Playfair Display,serif;font-size:2rem;color:#f5e6cc;margin:0 0 24px 0;'>{L['history_heading']}</h2>
    </div>
    """, unsafe_allow_html=True)
    for idx, entry in enumerate(st.session_state.chat_history):
        fb = entry.get("feedback")
        fb_icon = " 👍" if fb == 1 else (" 👎" if fb == -1 else "")
        entry_lang = entry.get("lang", "English")
        with st.expander(f"Turn {idx+1}{fb_icon}  —  \"{entry['input'][:55]}…\"  ({entry['ts']}) [{entry_lang}]", expanded=False):
            st.markdown(f"**You asked:** {entry['input']}")
            for s in entry["shlokas"]:
                st.markdown(render_shloka_card(s), unsafe_allow_html=True)
            st.markdown(f"<div class='guidance-box' style='padding:16px;'><p style='color:#c8d8f0;font-size:14px;font-style:italic;margin:0;'>{entry['guidance'].replace(chr(10), '<br>')}</p></div>", unsafe_allow_html=True)


# ── EXPORT ──
if st.session_state.chat_history:
    st.markdown("<div style='padding:20px 4vw 40px 4vw;'>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6a5030;margin-bottom:8px;'>{L['export_label']}</p><h3 style='font-family:Playfair Display,serif;color:#f5e6cc;margin:0 0 20px 0;'>{L['export_heading']}</h3>", unsafe_allow_html=True)
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        txt_data = build_text_export(st.session_state.chat_history)
        st.download_button(label=L["export_txt"], data=txt_data, file_name=f"gita_session_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime="text/plain", use_container_width=True)
    with exp_col2:
        try:
            pdf_data = build_pdf_export(st.session_state.chat_history)
            st.download_button(label=L["export_pdf"], data=pdf_data, file_name=f"gita_session_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", mime="application/pdf", use_container_width=True)
        except RuntimeError as e:
            st.info(f"ℹ️ PDF export unavailable: {e}")
    st.markdown("</div>", unsafe_allow_html=True)


# ── FOOTER ──
st.markdown("""
<div style='background:#080300;border-top:1px solid #1a0900;padding:40px 6vw;margin-top:40px;'>
  <div class='disclaimer-box'>
    <p style='color:#ffaa80;font-size:13px;margin:0;line-height:1.7;'>
    ⚠️ <b style='color:#ff6b35;'>Disclaimer:</b> This app offers spiritual reflection inspired by the Bhagavad Gita. It is <b>not a substitute</b> for professional psychological or medical advice.<br>
    🇮🇳 <b>iCall:</b> 9152987821 &nbsp;| 🇮🇳 <b>Vandrevala:</b> 1860-2662-345 &nbsp;| 🇺🇸 <b>988 Lifeline:</b> Call/text 988
    </p>
  </div>
  <div class='privacy-box' style='margin-top:12px;'>
    <p style='color:#a8e6c1;font-size:12px;margin:0;line-height:1.6;'>
    🔒 <b style='color:#2ecc71;'>Privacy:</b> Inputs sent to <a href='https://groq.com/privacy-policy/' target='_blank' style='color:#4a9eff;'>Groq AI</a> for inference only. No data stored. Session clears on tab close.
    </p>
  </div>
  <p style='text-align:center;color:#2a1800;font-size:12px;margin-top:24px;'>Built with ❤️ using Streamlit &amp; Groq AI · Inspired by the eternal wisdom of the Bhagavad Gita</p>
</div>
""", unsafe_allow_html=True)
