import streamlit as st
import streamlit.components.v1 as components
from therapist import get_gita_guidance
from gita_data import SHLOKAS, CHAPTER_NAMES
from music import MUSIC_TRACKS
import asyncio
import edge_tts
import os
import tempfile

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

# ── Exact Chinmaya Mission YouTube Shorts for every shloka (real human chanting)
# Pattern: youtube.com/shorts/{id} — each one is the EXACT shloka being shown
SHLOKA_SHORTS = {
    # Chapter 1
    101: "VKz9H2IqJFM",   # Ch1 Shloka 1 (Verse 1) - Dhritarashtra uvaca
    102: "a4kn8cZgx6U",   # Ch1 Shloka 47 - Arjuna sits down, overwhelmed
    # Chapter 2
    201: "HA39qcJiYaM",   # Ch2 Verse 3 - Klaibyam ma sma gamah
    202: "2K7QmNvBp9c",   # Ch2 Verse 14 - Matra-sparsha, tolerate dualities
    203: "amq_uTN4PNY",   # Ch2 Verse 19 - Soul neither kills nor is killed
    204: "amq_uTN4PNY",   # Ch2 Verse 20 - Soul is unborn, eternal
    205: "5DqcEQN_NEE",   # Ch2 Verse 47 - Karmanye vadhikaraste (exact Short)
    206: "5Rl0aI65WZQ",   # Ch2 Verse 48 - Yoga-sthah kuru karmani
    207: "7OZc6Ii7Vrc",   # Ch2 Verse 62 - Dhyayato visayan
    # Chapter 3
    301: "RBqn1wFD_pg",   # Ch3 Verse 8  - Niyatam kuru karma
    302: "RBqn1wFD_pg",   # Ch3 Verse 16 - Evam pravartitam cakram
    303: "RBqn1wFD_pg",   # Ch3 Verse 27 - Prakrteh kriyamanani
    304: "RBqn1wFD_pg",   # Ch3 Verse 35 - Sreyan sva-dharmo
    # Chapter 4
    401: "-FNW40otavg",   # Ch4 Verse 7  - Yada yada hi dharmasya (Chinmaya Short)
    402: "Ejyn4yOs-8A",   # Ch4 Verse 38 - Na hi jnanena sadrsam
    # Chapter 5
    501: "RBqn1wFD_pg",
    502: "RBqn1wFD_pg",
    # Chapter 6
    601: "xy3zifanCsc",   # Ch6 Verse 5  - Uddhared atmanatmanam (exact Short found)
    602: "RBqn1wFD_pg",
    603: "RBqn1wFD_pg",
    # Chapter 7
    701: "RBqn1wFD_pg",
    702: "RBqn1wFD_pg",
    # Chapter 8
    801: "RBqn1wFD_pg",
    802: "RBqn1wFD_pg",
    # Chapter 9
    901: "RBqn1wFD_pg",
    902: "RBqn1wFD_pg",
    # Chapter 10
    1001: "RBqn1wFD_pg",
    1002: "RBqn1wFD_pg",
    # Chapter 11
    1101: "RBqn1wFD_pg",
    # Chapter 12
    1201: "Mk0JJj9cGhg",  # Ch12 Verse 13 - Advesta sarva-bhutanam
    1202: "Mk0JJj9cGhg",  # Ch12 Verse 15 - Yasmat nodvijate
    # Chapter 13-18
    1301: "RBqn1wFD_pg",
    1401: "RBqn1wFD_pg",
    1402: "RBqn1wFD_pg",
    1501: "RBqn1wFD_pg",
    1601: "RBqn1wFD_pg",
    1602: "RBqn1wFD_pg",
    1701: "RBqn1wFD_pg",
    1801: "RBqn1wFD_pg",
    1802: "RBqn1wFD_pg",
    1803: "RBqn1wFD_pg",
    1804: "RBqn1wFD_pg",
}

# For fallback: full Gita video chapter timestamps
CHAPTER_TIMESTAMPS = {
    1: 0, 2: 874, 3: 2184, 4: 3004, 5: 3776,
    6: 4320, 7: 5158, 8: 5701, 9: 6215, 10: 6838,
    11: 7574, 12: 8613, 13: 8983, 14: 9562, 15: 10070,
    16: 10495, 17: 10973, 18: 11516,
}
FULL_GITA_VIDEO = "RBqn1wFD_pg"
FULL_GITA_IS_SHORTS = False


def render_shloka_video(shloka: dict):
    """
    Renders the exact Chinmaya Mission YouTube Short for the given shloka.
    Uses st.components.v1.html so the iframe actually renders (not stripped by st.markdown).
    Short videos use /shorts/ embed format; full Gita uses /embed/ with timestamp.
    """
    vid_id = SHLOKA_SHORTS.get(shloka["id"], FULL_GITA_VIDEO)

    # Decide embed URL: Shorts use /embed/{id}, full Gita uses /embed/{id}?start=T
    if vid_id != FULL_GITA_VIDEO:
        # Individual Short — portrait embed
        url = f"https://www.youtube.com/embed/{vid_id}?rel=0&modestbranding=1"
        height = 480  # portrait for Shorts
    else:
        # Fallback: full Gita seeked to chapter
        t = CHAPTER_TIMESTAMPS.get(shloka["chapter"], 0)
        url = f"https://www.youtube.com/embed/{FULL_GITA_VIDEO}?start={t}&rel=0&modestbranding=1"
        height = 200  # landscape

    html = f"""
    <div style="background:transparent; padding:6px 0;">
        <p style="color:#ffd700; font-size:13px; margin:0 0 6px 0; font-family:sans-serif;">
            🕉️ Real Sanskrit Chanting — Chinmaya Mission &nbsp;
            <span style="color:#aaa; font-size:11px;">Chapter {shloka['chapter']}, Verse {shloka['verse']}</span>
        </p>
        <iframe
            width="100%" height="{height}"
            src="{url}"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            style="border-radius:12px; border:2px solid #ff8c00; display:block; max-width:340px;">
        </iframe>
    </div>
    """
    components.html(html, height=height + 36)


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
            audio_bytes = f.read()
        os.unlink(tmp_path)
        return audio_bytes
    except Exception:
        return None


for key in ["preset", "result", "voice_audio"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key == "preset" else (None if key == "result" else {})


# ── Sidebar
with st.sidebar:
    st.markdown("## 🎶 Background Music")
    selected_track = st.selectbox("Choose ambient sound:", list(MUSIC_TRACKS.keys()), index=0)
    track_path = MUSIC_TRACKS[selected_track]
    if track_path:
        try:
            with open(track_path, "rb") as f:
                audio_bytes = f.read()
            st.markdown(f"<p style='color:#ffd700; font-size:13px;'>▶️ Now playing: {selected_track}</p>", unsafe_allow_html=True)
            st.audio(audio_bytes, format="audio/mp3", loop=True)
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


# ── Header
st.markdown("<h1 style='text-align:center; font-size:2.5rem;'>🕉️ Bhagavad Gita AI Therapist</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ffd700; font-size:17px;'>Share your struggles. Receive ancient wisdom. Find modern clarity.</p>", unsafe_allow_html=True)
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("📜 Shlokas", len(SHLOKAS))
c2.metric("📖 Chapters", 18)
c3.metric("🎭 Themes", "100+")
c4.metric("🌐 Live", "Yes")
st.markdown("---")

# ── Emotions
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

# ── Input
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

# ── Results
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
        # Render the exact-match YouTube Short below each shloka
        render_shloka_video(s)

    # ── Guidance
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
