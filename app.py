import streamlit as st
from therapist import get_gita_guidance
from gita_data import SHLOKAS, CHAPTER_NAMES
import os
import base64

st.set_page_config(
    page_title="Bhagavad Gita AI Therapist",
    page_icon="🕉️",
    layout="centered",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
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
    .chapter-card {
        background: rgba(255,140,0,0.08);
        border: 1px solid #ff8c0044;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 4px 0;
        font-size: 13px;
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
    .stSelectbox select { background-color: #2d1200 !important; color: #fff !important; }
    .stSlider { color: #ffd700; }
</style>
""", unsafe_allow_html=True)

# ── Background Music via HTML Audio ───────────────────────────────────────────
MUSIC_URLS = {
    "🕉️ Om Chanting (Peaceful)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "🎵 Flute Meditation": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "🕔 Temple Bells": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "🌿 Nature & Birds": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    "🔇 No Music": "",
}

with st.sidebar:
    st.markdown("## 🎶 Background Music")
    selected_music = st.selectbox("Choose ambient sound:", list(MUSIC_URLS.keys()), index=0)
    music_volume = st.slider("Volume", 0, 100, 30, step=5)
    music_url = MUSIC_URLS[selected_music]

    if music_url:
        st.markdown(f"""
        <audio id="bgMusic" autoplay loop style="display:none">
            <source src="{music_url}" type="audio/mpeg">
        </audio>
        <script>
            var audio = document.getElementById('bgMusic');
            if (audio) {{
                audio.volume = {music_volume / 100};
                audio.play().catch(e => console.log('Autoplay blocked:', e));
            }}
        </script>
        <p style='color:#ffd700; font-size:13px;'>Now playing: {selected_music}</p>
        <p style='color:#888; font-size:11px;'>Note: Click anywhere on the page if music doesn't start (browser autoplay policy).</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#888; font-size:13px;'>Music is off.</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🔐 Gemini API Key")
    api_key_input = st.text_input("Enter your key", type="password", placeholder="AIza...")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        st.success("✅ API Key saved!")
    st.markdown("[Get free key →](https://aistudio.google.com/)")

    st.markdown("---")
    st.markdown("## 📚 Browse All 18 Chapters")
    selected_chapter = st.selectbox(
        "Jump to chapter:",
        options=[""] + list(CHAPTER_NAMES.keys()),
        format_func=lambda x: "Select a chapter..." if x == "" else f"Ch {x}: {CHAPTER_NAMES[x].split(' — ')[0]}"
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

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center; font-size:2.5rem;'>🕉️ Bhagavad Gita AI Therapist</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#ffd700; font-size:17px;'>"
    "Share your struggles. Receive ancient wisdom. Find modern clarity."
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ── Stats Bar ──────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("📜 Shlokas", len(SHLOKAS))
col2.metric("📖 Chapters", 18)
col3.metric("🎭 Themes", "100+")
col4.metric("🌐 Live", "Yes")

st.markdown("---")

# ── Emotion Quick-Select ───────────────────────────────────────────────────────
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
    "💥 Angry/Rage":  "I have uncontrolled anger and lust that I cannot manage",
}

if "preset" not in st.session_state:
    st.session_state.preset = ""

cols = st.columns(4)
for i, (label, val) in enumerate(EMOTIONS.items()):
    if cols[i % 4].button(label, use_container_width=True):
        st.session_state.preset = val

# ── Text Input ─────────────────────────────────────────────────────────────────
st.markdown("### ✏️ Describe your situation in detail")
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

# ── Results ────────────────────────────────────────────────────────────────────
if seek:
    if not user_input.strip():
        st.warning("⚠️ Please describe your situation or tap a feeling above.")
    else:
        with st.spinner("🕉️ Seeking wisdom from the Bhagavad Gita..."):
            result = get_gita_guidance(user_input)

        st.markdown("---")
        st.markdown("### 📜 Shlokas for Your Situation")
        for s in result["shlokas"]:
            st.markdown(f"""
            <div class='shloka-box'>
                <h4 style='color:#ffd700; margin-top:0;'>
                    🕉️ Chapter {s['chapter']}, Verse {s['verse']}
                    <span style='color:#888; font-size:13px; font-weight:normal;'>
                        &nbsp;— {CHAPTER_NAMES.get(s['chapter'], '')}
                    </span>
                </h4>
                <p style='color:#ff8c00; font-size:18px; font-family:serif; line-height:1.9;'>{s['sanskrit']}</p>
                <p style='color:#aaa; font-style:italic; font-size:13px;'>{s['transliteration']}</p>
                <hr style='border-color:#4a1e00;'/>
                <p style='color:#f0e6d3;'><b>Meaning:</b> {s['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🧘 Krishna's Guidance for You")
        st.markdown(f"""
        <div class='guidance-box'>
            <p style='color:#e0e0e0; line-height:1.9; font-size:15px;'>
                {result['guidance'].replace(chr(10), '<br>')}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(
            "<p style='text-align:center; color:#ffd700; font-size:16px;'>"
            "✨ <i>Tat Tvam Asi — Thou Art That</i> ✨"
            "</p>",
            unsafe_allow_html=True,
        )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#555; font-size:12px;'>"
    "Built with ❤️ using Streamlit & Gemini AI · "
    "Inspired by the eternal wisdom of the Bhagavad Gita"
    "</p>",
    unsafe_allow_html=True,
)
