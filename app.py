import streamlit as st
from therapist import get_gita_guidance
from gita_data import SHLOKAS, CHAPTER_NAMES
from music import MUSIC_TRACKS
import asyncio
import edge_tts
import os
import tempfile
import requests
from gtts import gTTS
import io

st.set_page_config(
    page_title="Bhagavad Gita AI Therapist",
    page_icon="🕉️",
    layout="centered",
)

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1a0800 0%, #2d1200 50%, #1a0800 100%); }
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
    h1, h2, h3 { color: #ffd700 !important; }
    p { color: #f0e6d3; }
    .stTextArea textarea {
        background-color: #2d1200 !important;
        color: #fff !important;
        border: 1px solid #ff8c00 !important;
        border-radius: 10px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #ff6b00, #ffd700) !important;
        color: #1a0800 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 16px !important;
    }
    div[data-testid="stSidebar"] { background-color: #1a0800 !important; }
</style>
""", unsafe_allow_html=True)

CACHE_DIR = "/tmp/gita_audio"
os.makedirs(CACHE_DIR, exist_ok=True)


def is_valid_mp3(data: bytes) -> bool:
    """Check if bytes are a real MP3 (starts with ID3 tag or MPEG sync word)."""
    if len(data) < 4:
        return False
    # ID3 header
    if data[:3] == b'ID3':
        return True
    # MPEG sync word (0xFF 0xE0-0xFF)
    if data[0] == 0xFF and (data[1] & 0xE0) == 0xE0:
        return True
    return False


def get_shloka_audio(shloka: dict) -> bytes | None:
    """
    Fetch real human Sanskrit chanting for the exact chapter+verse.
    Sources tried in order:
      1. archive.org - Srimad Bhagavad Gita by T.S. Ranganathan (verified direct MP3)
      2. vedicscriptures.net direct MP3
      3. gTTS Hindi slow (fallback — always works, reads the exact transliteration)
    Cached in /tmp per chapter_verse.
    """
    ch = shloka["chapter"]
    v  = shloka["verse"]
    cache_file = os.path.join(CACHE_DIR, f"{ch}_{v}.mp3")

    if os.path.exists(cache_file):
        data = open(cache_file, "rb").read()
        if is_valid_mp3(data):
            return data
        os.remove(cache_file)  # stale/bad cache

    headers = {"User-Agent": "Mozilla/5.0"}

    urls = [
        # archive.org — T.S. Ranganathan classical chanting, verified file structure
        f"https://archive.org/download/SrimadBhagavadGita_201712/Ch{ch:02d}_V{v:02d}.mp3",
        f"https://archive.org/download/SrimadBhagavadGita_201712/Ch{ch}_V{v}.mp3",
        f"https://archive.org/download/SrimadBhagavadGita_201712/BG{ch:02d}{v:02d}.mp3",
        # vedicscriptures.net
        f"https://www.vedicscriptures.net/audio/gita/ch{ch}/{ch}_{v:02d}.mp3",
        f"https://www.vedicscriptures.net/audio/gita/ch{ch:02d}/ch{ch:02d}_{v:02d}.mp3",
    ]

    for url in urls:
        try:
            r = requests.get(url, timeout=8, headers=headers)
            if r.status_code == 200 and is_valid_mp3(r.content):
                with open(cache_file, "wb") as f:
                    f.write(r.content)
                return r.content
        except Exception:
            continue

    # Final fallback: gTTS reads the exact transliteration — always correct verse
    try:
        tts = gTTS(text=shloka["transliteration"], lang="hi", slow=True)
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
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        async def _gen():
            communicate = edge_tts.Communicate(
                script, "en-IN-NeerjaNeural", rate="-15%", pitch="-5Hz"
            )
            await communicate.save(tmp_path)
        asyncio.run(_gen())
        with open(tmp_path, "rb") as f:
            data = f.read()
        os.unlink(tmp_path)
        return data
    except Exception:
        return None


for key in ["preset", "result", "voice_audio"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key == "preset" else (None if key == "result" else {})


with st.sidebar:
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
                st.markdown(f"**Sanskrit:** {s['sanskrit']}")
                st.markdown(f"*{s['transliteration']}*")
                st.markdown(f"**Meaning:** {s['meaning']}")
    st.markdown("---")
    st.markdown(f"**Total Shlokas:** {len(SHLOKAS)} across 18 chapters  \n**Themes:** 100+")


st.markdown("<h1 style='text-align:center; font-size:2.5rem;'>🕉️ Bhagavad Gita AI Therapist</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ffd700; font-size:17px;'>Share your struggles. Receive ancient wisdom. Find modern clarity.</p>", unsafe_allow_html=True)
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("📜 Shlokas", len(SHLOKAS))
c2.metric("📖 Chapters", 18)
c3.metric("🎭 Themes", "100+")
c4.metric("🌐 Live", "Yes")
st.markdown("---")

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
    "🎯 Distracted": "I am very distracted and unable to focus or concentrate on anything",
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
    "", value=st.session_state.preset,
    placeholder="E.g. I am stressed about my exams and fear of failure is stopping me from studying...",
    height=130, label_visibility="collapsed",
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

if st.session_state.result:
    result = st.session_state.result
    st.markdown("---")
    st.markdown("### 📜 Shlokas for Your Situation")

    for i, s in enumerate(result["shlokas"]):
        chapter_name = CHAPTER_NAMES.get(s['chapter'], '')
        st.markdown(f"""
        <div class='shloka-box'>
            <h4 style='color:#ffd700; margin-top:0;'>
                🕉️ Chapter {s['chapter']}, Verse {s['verse']}
                <span style='color:#888; font-size:13px; font-weight:normal;'>&nbsp;— {chapter_name}</span>
            </h4>
            <p style='color:#ff8c00; font-size:18px; font-family:serif; line-height:1.9;'>{s['sanskrit']}</p>
            <p style='color:#aaa; font-style:italic; font-size:13px;'>{s['transliteration']}</p>
            <hr style='border-color:#4a1e00;'/>
            <p style='color:#f0e6d3;'><b>Meaning:</b> {s['meaning']}</p>
        </div>
        """, unsafe_allow_html=True)

        vkey = f"s_{s['chapter']}_{s['verse']}"
        if vkey not in st.session_state.voice_audio:
            with st.spinner(f"🕉️ Loading chanting for Ch {s['chapter']}, Verse {s['verse']}..."):
                audio = get_shloka_audio(s)
            if audio:
                st.session_state.voice_audio[vkey] = audio

        if vkey in st.session_state.voice_audio:
            st.markdown(
                f"<p style='color:#ffd700; font-size:13px; margin:8px 0 2px 0;'>"
                f"🕉️ Shloka Chanting — Ch {s['chapter']}, Verse {s['verse']}</p>",
                unsafe_allow_html=True
            )
            st.audio(st.session_state.voice_audio[vkey], format="audio/mp3")
        else:
            st.caption("⚠️ Audio unavailable for this verse.")

    st.markdown("### 🧘 Krishna's Guidance for You")
    guidance_text = result['guidance']
    st.markdown(f"""
    <div class='guidance-box'>
        <p style='color:#e0e0e0; line-height:1.9; font-size:15px;'>
            {guidance_text.replace(chr(10), '<br>')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔊 Hear Krishna's Guidance", key="btn_guidance"):
        full_script = f"O Arjuna, {guidance_text}. Go forward with courage, and surrender to the divine."
        with st.spinner("🕉️ Generating voice..."):
            audio = make_guidance_voice(full_script)
        if audio:
            st.session_state.voice_audio["guidance"] = audio
        else:
            st.error("❌ Voice generation failed.")

    if "guidance" in st.session_state.voice_audio:
        st.audio(st.session_state.voice_audio["guidance"], format="audio/mp3")

    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#ffd700; font-size:16px;'>✨ <i>Tat Tvam Asi — Thou Art That</i> ✨</p>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#555; font-size:12px;'>Built with ❤️ using Streamlit & Groq AI · Inspired by the eternal wisdom of the Bhagavad Gita</p>", unsafe_allow_html=True)
