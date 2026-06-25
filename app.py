import streamlit as st
from therapist import get_gita_guidance
from gita_data import SHLOKAS, CHAPTER_NAMES
from music import MUSIC_TRACKS
from export_utils import build_text_export, build_pdf_export
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

st.set_page_config(
    page_title="Bhagavad Gita AI Therapist",
    page_icon="🕉️",
    layout="centered",
)

st.markdown("""
<style>
    /* ── Base ── */
    .stApp { background: linear-gradient(135deg, #1a0800 0%, #2d1200 50%, #1a0800 100%); }

    /* ── Cards ── */
    .shloka-box {
        background: linear-gradient(135deg, #2d1200, #4a1e00);
        border: 1px solid #ff8c00;
        border-radius: 14px;
        padding: 22px;
        margin: 12px 0;
    }
    .guidance-box {
        background: linear-gradient(135deg, #0a1628, #1a2d4a);
        border: 1px solid #4a9eff;
        border-radius: 14px;
        padding: 22px;
        margin: 12px 0;
    }
    .history-card {
        background: linear-gradient(135deg, #1a1a0a, #2a2a10);
        border: 1px solid #888820;
        border-left: 4px solid #ffd700;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .disclaimer-box {
        background: linear-gradient(135deg, #1a0a00, #2a1500);
        border: 1px solid #ff6b35;
        border-left: 4px solid #ff6b35;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 10px 0 18px 0;
    }
    .privacy-box {
        background: linear-gradient(135deg, #001a0a, #00290f);
        border: 1px solid #2ecc71;
        border-left: 4px solid #2ecc71;
        border-radius: 10px;
        padding: 14px 20px;
        margin: 10px 0;
    }

    /* ── Typography ── */
    h1, h2, h3 { color: #ffd700 !important; }
    p { color: #f0e6d3; }

    /* ── Inputs ── */
    .stTextArea textarea {
        background-color: #2d1200 !important;
        color: #fff !important;
        border: 1px solid #ff8c00 !important;
        border-radius: 10px !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b00, #ffd700) !important;
        color: #1a0800 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 16px !important;
    }
    .feedback-btn > button {
        font-size: 20px !important;
        background: transparent !important;
        border: 1px solid #555 !important;
        border-radius: 8px !important;
        color: #ccc !important;
        padding: 4px 14px !important;
        min-height: 0 !important;
    }

    /* ── Sidebar ── */
    div[data-testid="stSidebar"] { background-color: #1a0800 !important; }

    /* ── Mobile responsiveness ── */
    @media (max-width: 640px) {
        h1 { font-size: 1.6rem !important; }
        .shloka-box, .guidance-box, .history-card { padding: 14px 12px; }
        .stButton > button { font-size: 13px !important; }
        div[data-testid="column"] { min-width: 48% !important; }
        div[data-testid="stMetric"] label { font-size: 11px !important; }
    }
    @media (max-width: 400px) {
        h1 { font-size: 1.25rem !important; }
        div[data-testid="column"] { min-width: 100% !important; }
    }
</style>
""", unsafe_allow_html=True)

CACHE_DIR = "/tmp/gita_audio"
os.makedirs(CACHE_DIR, exist_ok=True)

IMAGE_SETS = {
    "krishna_arjuna": {
        "local": "assets/krishna_arjuna.jpg",
        "urls": [
            "https://www.holy-bhagavad-gita.org/public/img/arjuna-and-krishna-on-chariot.jpg",
            "https://i.pinimg.com/originals/2e/3d/85/2e3d859e3c27c2c39d1e03462f97d6e2.jpg",
        ],
        "label": "Krishna & Arjuna on the Battlefield of Kurukshetra",
    },
    "krishna_flute": {
        "local": "assets/krishna_flute.jpg",
        "urls": [
            "https://www.holy-bhagavad-gita.org/public/img/krishna-flute.jpg",
            "https://i.pinimg.com/originals/5f/0e/c3/5f0ec3e5a7a9e2a3c0e9d8b7f6a1d2e4.jpg",
        ],
        "label": "Lord Krishna",
    },
    "kurukshetra": {
        "local": "assets/kurukshetra.jpg",
        "urls": [
            "https://www.holy-bhagavad-gita.org/public/img/kurukshetra.jpg",
            "https://i.pinimg.com/originals/a1/b2/c3/a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6.jpg",
        ],
        "label": "The Battle of Kurukshetra",
    },
    "gita_teaching": {
        "local": "assets/gita_teaching.jpg",
        "urls": [
            "https://www.holy-bhagavad-gita.org/public/img/krishna-teaching.jpg",
            "https://i.pinimg.com/originals/f1/e2/d3/f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6.jpg",
        ],
        "label": "Krishna's Divine Teaching",
    },
}


def make_placeholder(label: str) -> Image.Image:
    w, h = 800, 300
    img  = Image.new("RGB", (w, h), (30, 12, 0))
    draw = ImageDraw.Draw(img)
    for i, col in enumerate([(255, 140, 0), (200, 100, 0), (255, 200, 0)]):
        draw.rectangle([i * 2, i * 2, w - 1 - i * 2, h - 1 - i * 2], outline=col, width=1)
    draw.ellipse([w // 2 - 60, h // 2 - 55, w // 2 + 60, h // 2 + 55], outline=(255, 215, 0), width=2)
    try:
        from config import FONT_PATHS_BOLD, FONT_PATHS_REGULAR
        font_big = font_sm = None
        for p in FONT_PATHS_BOLD:
            try: font_big = ImageFont.truetype(p, 32); break
            except Exception: pass
        for p in FONT_PATHS_REGULAR:
            try: font_sm = ImageFont.truetype(p, 18); break
            except Exception: pass
        font_big = font_big or ImageFont.load_default()
        font_sm  = font_sm  or ImageFont.load_default()
    except Exception:
        font_big = font_sm = ImageFont.load_default()
    draw.text((w // 2 - 20, h // 2 - 20), "🕉️", fill=(255, 215, 0), font=font_big)
    bbox = draw.textbbox((0, 0), label, font=font_sm)
    draw.text(((w - (bbox[2] - bbox[0])) // 2, h - 50), label, fill=(255, 200, 100), font=font_sm)
    return img


@st.cache_resource
def load_images() -> dict:
    imgs = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
        "Referer": "https://www.google.com/",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    }
    for name, cfg in IMAGE_SETS.items():
        if os.path.exists(cfg["local"]):
            try:
                imgs[name] = Image.open(cfg["local"]).convert("RGB")
                continue
            except Exception:
                pass
        for url in cfg["urls"]:
            try:
                r = requests.get(url, headers=headers, timeout=8)
                if r.status_code == 200 and len(r.content) > 5000:
                    imgs[name] = Image.open(io.BytesIO(r.content)).convert("RGB")
                    break
            except Exception:
                continue
        if name not in imgs:
            imgs[name] = make_placeholder(cfg["label"])
    return imgs


IMGS = load_images()


def show_image(key: str, caption: str = ""):
    st.image(IMGS[key], caption=caption, use_container_width=True)


from config import ELEVENLABS_VOICES as GURU_VOICES
from config import (
    EDGE_TTS_SHLOKA_VOICE, EDGE_TTS_SHLOKA_RATE, EDGE_TTS_SHLOKA_PITCH,
    EDGE_TTS_GUIDANCE_VOICE, EDGE_TTS_GUIDANCE_RATE, EDGE_TTS_GUIDANCE_PITCH,
)


def is_valid_mp3(data: bytes) -> bool:
    if len(data) < 4:
        return False
    if data[:3] == b"ID3":
        return True
    if data[0] == 0xFF and (data[1] & 0xE0) == 0xE0:
        return True
    return False


def build_voice_script(shloka: dict) -> str:
    """English-only TTS script — no Sanskrit."""
    ch      = shloka["chapter"]
    v       = shloka["verse"]
    meaning = shloka.get("meaning", "")
    return (
        f"Shloka. Chapter {ch}, Verse {v}. "
        f"The Lord says ... {meaning} "
        f"Contemplate on this."
    )


def get_elevenlabs_audio(text: str, voice_id: str) -> bytes | None:
    try:
        api_key = st.secrets.get("ELEVENLABS_API_KEY", "")
        if not api_key:
            return None
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.85, "similarity_boost": 0.80, "style": 0.40, "use_speaker_boost": True},
        }
        r = requests.post(url, json=payload, headers=headers, timeout=25)
        if r.status_code == 200 and is_valid_mp3(r.content):
            return r.content
    except Exception:
        pass
    return None


def get_shloka_audio(shloka: dict) -> bytes | None:
    ch = shloka["chapter"]
    v  = shloka["verse"]
    cache_file = os.path.join(CACHE_DIR, f"{ch}_{v}.mp3")
    if os.path.exists(cache_file):
        data = open(cache_file, "rb").read()
        if is_valid_mp3(data):
            return data
        os.remove(cache_file)
    script = build_voice_script(shloka)
    for vid in GURU_VOICES:
        audio = get_elevenlabs_audio(script, vid)
        if audio:
            with open(cache_file, "wb") as f:
                f.write(audio)
            return audio
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        async def _g():
            await edge_tts.Communicate(
                script, EDGE_TTS_SHLOKA_VOICE,
                rate=EDGE_TTS_SHLOKA_RATE, pitch=EDGE_TTS_SHLOKA_PITCH
            ).save(tmp_path)
        asyncio.run(_g())
        data = open(tmp_path, "rb").read()
        os.unlink(tmp_path)
        if is_valid_mp3(data):
            with open(cache_file, "wb") as f:
                f.write(data)
            return data
    except Exception:
        pass
    try:
        # gTTS fallback: read English meaning aloud
        tts = gTTS(text=shloka.get("meaning", ""), lang="en", slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        data = buf.read()
        if is_valid_mp3(data):
            with open(cache_file, "wb") as f:
                f.write(data)
            return data
    except Exception:
        pass
    return None


def make_guidance_voice(script: str) -> bytes | None:
    for vid in GURU_VOICES:
        audio = get_elevenlabs_audio(script, vid)
        if audio:
            return audio
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        async def _g():
            await edge_tts.Communicate(
                script, EDGE_TTS_GUIDANCE_VOICE,
                rate=EDGE_TTS_GUIDANCE_RATE, pitch=EDGE_TTS_GUIDANCE_PITCH
            ).save(tmp_path)
        asyncio.run(_g())
        data = open(tmp_path, "rb").read()
        os.unlink(tmp_path)
        return data
    except Exception:
        return None


# ── Session state init ───────────────────────────────────────────────────────────
DEFAULTS = {
    "preset": "",
    "result": None,
    "voice_audio": {},
    "chat_history": [],    # list of {input, shlokas, guidance, feedback, ts}
    "feedback": {},        # turn_index -> 1 or -1
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    show_image("krishna_flute", "🪈 Lord Krishna")
    st.markdown("## 🎶 Background Music")
    selected_track = st.selectbox("Choose ambient sound:", list(MUSIC_TRACKS.keys()), index=0)
    track_path = MUSIC_TRACKS[selected_track]
    if track_path:
        try:
            with open(track_path, "rb") as f:
                ab = f.read()
            st.markdown(f"<p style='color:#ffd700; font-size:13px;'>▶️ Now playing: {selected_track}</p>", unsafe_allow_html=True)
            st.audio(ab, format="audio/mp3", loop=True)
            st.caption("🔉 Adjust volume using the player")
        except FileNotFoundError:
            st.error("❌ Audio file not found.")
    else:
        st.markdown("<p style='color:#aaa; font-size:13px;'>🔇 Music is off.</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📚 Browse All 18 Chapters")
    selected_chapter = st.selectbox(
        "Jump to chapter:",
        options=[""] + list(CHAPTER_NAMES.keys()),
        format_func=lambda x: "Select a chapter..." if x == "" else f"Ch {x}: {CHAPTER_NAMES[x].split(' — ')[0]}",
        key="chapter_select",
    )
    if selected_chapter:
        chapter_shlokas = [s for s in SHLOKAS if s["chapter"] == selected_chapter]
        st.markdown(f"**{CHAPTER_NAMES[selected_chapter]}**")
        st.markdown(f"*{len(chapter_shlokas)} shlokas loaded*")
        for s in chapter_shlokas:
            with st.expander(f"Verse {s['verse']}"):
                # ── English meaning only ──
                st.markdown(f"**Ch {s['chapter']}, Verse {s['verse']}**")
                st.markdown(s["meaning"])

    st.markdown("---")
    st.markdown(f"**Total Shlokas:** {len(SHLOKAS)} across 18 chapters  \n**Themes:** 100+")

    # ── Chat history summary in sidebar ─────────────────────────────
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("## 💬 Session History")
        for idx, entry in enumerate(reversed(st.session_state.chat_history), 1):
            fb = entry.get("feedback")
            fb_icon = " 👍" if fb == 1 else (" 👎" if fb == -1 else "")
            with st.expander(f"Turn {len(st.session_state.chat_history) - idx + 1}{fb_icon}: {entry['input'][:40]}..."):
                st.markdown(f"*{entry['ts']}*")
                for s in entry["shlokas"]:
                    st.markdown(f"- Ch {s['chapter']}, Verse {s['verse']}: {s['meaning'][:60]}...")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#888; line-height:1.6;'>
    🔒 <b style='color:#aaa;'>Privacy:</b> Your inputs are sent to Groq AI for inference only.
    Nothing is stored by this app. No personal data is collected.
    <br><br>
    ℹ️ <a href='https://groq.com/privacy-policy/' target='_blank' style='color:#4a9eff;'>Groq Privacy Policy</a>
    </div>
    """, unsafe_allow_html=True)


# ── MAIN ──────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center; font-size:2.5rem;'>🕉️ Bhagavad Gita AI Therapist</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ffd700; font-size:17px;'>Share your struggles. Receive ancient wisdom. Find modern clarity.</p>", unsafe_allow_html=True)

show_image("krishna_arjuna", "Krishna imparting wisdom to Arjuna on the battlefield of Kurukshetra")
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("📜 Shlokas", len(SHLOKAS))
c2.metric("📖 Chapters", 18)
c3.metric("🎭 Themes", "100+")
c4.metric("💬 Turns", len(st.session_state.chat_history))
st.markdown("---")

col_a, col_b = st.columns(2)
with col_a:
    show_image("kurukshetra", "⚔️ The Battle of Kurukshetra")
with col_b:
    show_image("gita_teaching", "🕉️ Krishna's Divine Teaching")
st.markdown("---")

# ── Chat history display ────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation History")
    for idx, entry in enumerate(st.session_state.chat_history):
        fb      = entry.get("feedback")
        fb_icon = " 👍" if fb == 1 else (" 👎" if fb == -1 else "")
        with st.expander(f"Turn {idx + 1}{fb_icon}  —  \"{entry['input'][:55]}...\"  ({entry['ts']})", expanded=False):
            st.markdown(f"**You asked:** {entry['input']}")
            for s in entry["shlokas"]:
                chapter_name = CHAPTER_NAMES.get(s["chapter"], "")
                # ── English meaning only ──
                st.markdown(f"""
                <div class='shloka-box' style='padding:14px;'>
                    <b style='color:#ffd700;'>🕉️ Ch {s['chapter']}, Verse {s['verse']}</b>
                    <span style='color:#888; font-size:12px;'> — {chapter_name}</span><br><br>
                    <span style='color:#f0e6d3;'>{s['meaning']}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class='guidance-box' style='padding:14px;'>
                <p style='color:#e0e0e0; font-size:14px; margin:0;'>{entry['guidance'].replace(chr(10), '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")

# ── Input section ────────────────────────────────────────────────────────────
st.markdown("### 💛 How are you feeling right now?")
st.caption("Tap a feeling or type your own below ⬇️")

EMOTIONS = {
    "😟 Anxious":     "I am feeling very anxious and stressed about my future, work, and results",
    "💔 Heartbroken": "I am heartbroken and sad after a painful loss or breakup",
    "😞 Demotivated": "I feel demotivated, lazy and like giving up on everything",
    "😠 Angry":       "I am feeling very angry, full of ego and pride",
    "😨 Fearful":     "I am overwhelmed with fear and guilt about my mistakes",
    "🤔 Lost":        "I feel completely lost and confused about my purpose and meaning of life",
    "🧐 Self-Doubt":  "I have severe self-doubt and very low confidence in myself",
    "🎯 Distracted":  "I am very distracted and unable to focus or concentrate on anything",
    "🙏 Lonely":      "I feel very lonely and like nobody truly understands me",
    "🙊 Jealous":     "I am feeling jealous and always comparing myself to others",
    "😫 Burnout":     "I am completely burned out, exhausted, and overwhelmed",
    "💥 Rage":        "I have uncontrolled anger and rage that I cannot manage",
}

cols = st.columns(4)
for i, (label, val) in enumerate(EMOTIONS.items()):
    if cols[i % 4].button(label, use_container_width=True):
        st.session_state.preset = val
        st.session_state.result = None
        st.session_state.voice_audio = {}

st.markdown("### ✏️ Describe your situation")
user_input = st.text_area(
    "",
    value=st.session_state.preset,
    placeholder="E.g. I am stressed about my exams and fear of failure is stopping me from studying...",
    height=130,
    label_visibility="collapsed",
)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    seek = st.button("🕉️ Seek Krishna's Guidance", use_container_width=True)

if seek:
    if not user_input.strip():
        st.warning("⚠️ Please describe your situation or tap a feeling above.")
    else:
        with st.spinner("🕉️ Seeking wisdom from the Bhagavad Gita..."):
            st.session_state.result = get_gita_guidance(user_input)
        st.session_state.voice_audio = {}
        st.session_state.chat_history.append({
            "input":    user_input,
            "shlokas":  st.session_state.result["shlokas"],
            "guidance": st.session_state.result["guidance"],
            "feedback": None,
            "ts":       datetime.now().strftime("%I:%M %p"),
        })
        st.session_state.preset = ""

# ── Current result ────────────────────────────────────────────────────────────
if st.session_state.result:
    result   = st.session_state.result
    turn_idx = len(st.session_state.chat_history) - 1

    st.markdown("---")
    show_image("krishna_arjuna", "🕉️ Krishna & Arjuna — Bhagavad Gita")
    st.markdown("### 📜 Shlokas for Your Situation")

    for i, s in enumerate(result["shlokas"]):
        chapter_name = CHAPTER_NAMES.get(s["chapter"], "")
        # ── English meaning only ──
        st.markdown(f"""
        <div class='shloka-box'>
            <h4 style='color:#ffd700; margin-top:0;'>
                🕉️ Chapter {s['chapter']}, Verse {s['verse']}
                <span style='color:#888; font-size:13px; font-weight:normal;'>&nbsp;— {chapter_name}</span>
            </h4>
            <p style='color:#f0e6d3; font-size:16px; line-height:1.9;'>{s['meaning']}</p>
        </div>
        """, unsafe_allow_html=True)

        vkey = f"s_{s['chapter']}_{s['verse']}"
        if vkey not in st.session_state.voice_audio:
            with st.spinner(f"🕉️ Loading recitation for Ch {s['chapter']}, Verse {s['verse']}..."):
                audio = get_shloka_audio(s)
            if audio:
                st.session_state.voice_audio[vkey] = audio
        if vkey in st.session_state.voice_audio:
            st.markdown(f"<p style='color:#ffd700; font-size:13px; margin:8px 0 2px 0;'>🕉️ Verse Recitation — Ch {s['chapter']}, Verse {s['verse']}</p>", unsafe_allow_html=True)
            st.audio(st.session_state.voice_audio[vkey], format="audio/mp3")
        else:
            st.caption("⚠️ Audio unavailable for this verse.")

    st.markdown("### 🧘 Krishna's Guidance for You")
    guidance_text = result["guidance"]
    st.markdown(f"""
    <div class='guidance-box'>
        <p style='color:#e0e0e0; line-height:1.9; font-size:15px;'>{guidance_text.replace(chr(10), '<br>')}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔊 Hear Krishna's Guidance", key="btn_guidance"):
        full_script = (
            f"O Arjuna. {guidance_text} "
            "This is the eternal truth. Go forward with courage. "
            "Surrender to the divine will. Tat Tvam Asi."
        )
        with st.spinner("🕉️ Generating voice..."):
            audio = make_guidance_voice(full_script)
        if audio:
            st.session_state.voice_audio["guidance"] = audio
        else:
            st.error("❌ Voice generation failed. Please try again.")

    if "guidance" in st.session_state.voice_audio:
        st.audio(st.session_state.voice_audio["guidance"], format="audio/mp3")

    # ── Feedback row ───────────────────────────────────────────────────────
    current_fb = st.session_state.chat_history[turn_idx].get("feedback") if st.session_state.chat_history else None
    st.markdown("<p style='color:#888; font-size:13px; margin-top:18px;'>Was this guidance helpful?</p>", unsafe_allow_html=True)
    fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 6])
    with fb_col1:
        thumb_up_label = "👍 Helpful" if current_fb != 1 else "✅ Helpful"
        if st.button(thumb_up_label, key=f"fb_up_{turn_idx}"):
            st.session_state.chat_history[turn_idx]["feedback"] = 1
            st.toast("👍 Thank you! Glad this was helpful.", icon="✅")
            st.rerun()
    with fb_col2:
        thumb_dn_label = "👎 Not helpful" if current_fb != -1 else "❌ Not helpful"
        if st.button(thumb_dn_label, key=f"fb_dn_{turn_idx}"):
            st.session_state.chat_history[turn_idx]["feedback"] = -1
            st.toast("🙏 Thank you for the feedback. We'll aim to do better.", icon="🔄")
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#ffd700; font-size:16px;'>✨ <i>Tat Tvam Asi — Thou Art That</i> ✨</p>", unsafe_allow_html=True)

# ── Export section ──────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 📄 Export Your Session")
    st.caption("Download your conversation with shlokas and guidance for personal reflection.")
    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        txt_data = build_text_export(st.session_state.chat_history)
        st.download_button(
            label="📝 Download as Text (.txt)",
            data=txt_data,
            file_name=f"gita_session_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with exp_col2:
        try:
            pdf_data = build_pdf_export(st.session_state.chat_history)
            st.download_button(
                label="📅 Download as PDF",
                data=pdf_data,
                file_name=f"gita_session_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except RuntimeError as e:
            st.info(f"ℹ️ PDF export unavailable: {e}")

# ── Bottom disclaimer & privacy ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div class='disclaimer-box'>
    <p style='color:#ffaa80; font-size:13px; margin:0; line-height:1.7;'>
    ⚠️ <b style='color:#ff6b35;'>Important Disclaimer:</b>
    This app offers <b>spiritual reflection and emotional support</b> inspired by the Bhagavad Gita.
    It is <b>not a substitute</b> for professional psychological, psychiatric, or medical advice.
    If you are in crisis or experiencing thoughts of self-harm, please contact a mental health professional immediately.
    <br>
    🇮🇳 <b>iCall (India):</b> 9152987821 &nbsp;|
    🇮🇳 <b>Vandrevala Foundation:</b> 1860-2662-345 (24/7) &nbsp;|
    🇺🇸 <b>988 Lifeline (USA):</b> Call/text 988
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='privacy-box'>
    <p style='color:#a8e6c1; font-size:12px; margin:0; line-height:1.6;'>
    🔒 <b style='color:#2ecc71;'>Privacy Notice:</b>
    Your inputs are sent to <a href='https://groq.com/privacy-policy/' target='_blank' style='color:#4a9eff;'>Groq AI</a> for inference only.
    <b>No data is stored</b> by this app. No personal information is collected. Session data is cleared when you close the tab.
    Avoid sharing sensitive personal details — keep inputs general (e.g. "I feel anxious").
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; color:#555; font-size:12px; line-height:1.8; margin-top:12px;'>
    Built with ❤️ using Streamlit &amp; Groq AI · Inspired by the eternal wisdom of the Bhagavad Gita
</div>
""", unsafe_allow_html=True)
