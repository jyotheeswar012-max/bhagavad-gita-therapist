import streamlit as st
from therapist import get_gita_guidance
from gita_data import SHLOKAS
import os

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
    .stButton > button:hover { opacity: 0.9; transform: scale(1.02); }
    div[data-testid="stSidebar"] { background-color: #1a0800 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center; font-size:2.5rem;'>🕉️ Bhagavad Gita AI Therapist</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#ffd700; font-size:17px;'>"
    "Share your struggles. Receive ancient wisdom. Find modern clarity."
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔐 Gemini API Key")
    api_key_input = st.text_input("Enter your key", type="password",
                                  placeholder="AIza...")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        st.success("✅ API Key saved!")
    st.markdown("[Get free key →](https://aistudio.google.com/)")
    st.markdown("---")
    st.markdown("## 📚 About")
    st.markdown(
        "This app maps your emotions to Bhagavad Gita shlokas and "
        "delivers warm, non-preachy guidance.\n\n"
        f"**Shlokas loaded:** {len(SHLOKAS)}  \n"
        "**Themes covered:** 50+"
    )
    st.markdown("---")
    st.markdown("## 📜 Shlokas Reference")
    for s in SHLOKAS:
        st.markdown(f"- Ch {s['chapter']}.{s['verse']} — *{', '.join(s['themes'][:3])}...*")

# ── Emotion Quick-Select ──────────────────────────────────────────────
st.markdown("### 💛 How are you feeling right now?")
st.caption("Tap a feeling or type your own below ⬇️")

EMOTIONS = {
    "😟 Anxious": "I am feeling very anxious and stressed about my future, work, and results",
    "💔 Heartbroken": "I am heartbroken and sad after a painful loss or breakup",
    "😞 Demotivated": "I feel demotivated, lazy and like giving up on everything",
    "😠 Angry": "I am feeling very angry, full of ego and pride",
    "😨 Fearful": "I am overwhelmed with fear and guilt about my mistakes",
    "🤔 Lost": "I feel completely lost and confused about my purpose and meaning of life",
    "🧐 Self-Doubt": "I have severe self-doubt and very low confidence in myself",
    "🎯 Distracted": "I am very distracted and unable to focus or concentrate on anything",
}

if "preset" not in st.session_state:
    st.session_state.preset = ""

cols = st.columns(4)
for i, (label, val) in enumerate(EMOTIONS.items()):
    if cols[i % 4].button(label, use_container_width=True):
        st.session_state.preset = val

# ── Text Input ────────────────────────────────────────────────────────
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

# ── Results ───────────────────────────────────────────────────────────
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
                <h4 style='color:#ffd700; margin-top:0;'>🕉️ Chapter {s['chapter']}, Verse {s['verse']}</h4>
                <p style='color:#ff8c00; font-size:17px; font-family:serif; line-height:1.8;'>{s['sanskrit']}</p>
                <p style='color:#aaa; font-style:italic; font-size:14px;'>{s['transliteration']}</p>
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

# ── Footer ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#555; font-size:12px;'>"
    "Built with ❤️ using Streamlit & Gemini AI · "
    "Inspired by the eternal wisdom of the Bhagavad Gita"
    "</p>",
    unsafe_allow_html=True,
)
