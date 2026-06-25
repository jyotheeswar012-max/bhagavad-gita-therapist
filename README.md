# 🕉️ Bhagavad Gita AI Therapist

> *Share your struggles. Receive ancient wisdom. Find modern clarity.*

An AI-powered Streamlit app that listens to your emotional struggles and responds with relevant Bhagavad Gita shlokas + warm, practical guidance powered by **Groq AI**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bhagavad-gita-therapist.streamlit.app/)
[![CI](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/actions/workflows/ci.yml/badge.svg)](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/actions/workflows/ci.yml)

🌐 **Live Demo:** [bhagavad-gita-therapist.streamlit.app](https://bhagavad-gita-therapist.streamlit.app/)

---

## ⚠️ Mental Health Disclaimer

> **This app is not a substitute for professional psychological, psychiatric, or medical advice, diagnosis, or treatment.**
>
> The Bhagavad Gita guidance provided here is meant for **spiritual reflection and general emotional support only**. If you are experiencing a mental health crisis, severe depression, thoughts of self-harm, or any psychiatric emergency, please seek immediate help from a licensed professional.
>
> **Crisis Resources:**
> - 🇮🇳 **iCall (India):** 9152987821
> - 🇮🇳 **Vandrevala Foundation:** 1860-2662-345 (24/7)
> - 🌍 **International Association for Suicide Prevention:** https://www.iasp.info/resources/Crisis_Centres/
> - 🇺🇸 **988 Suicide & Crisis Lifeline (USA):** Call or text **988**

---

## 🔒 Privacy Policy

Your privacy is important. Here is exactly what this app does and does **not** do with your data:

| What | Policy |
|------|--------|
| **User inputs (your text)** | Sent to Groq API for AI inference only. **Not stored** by this app. |
| **Groq API data handling** | Subject to [Groq's Privacy Policy](https://groq.com/privacy-policy/). Groq does not use API inputs for model training by default. |
| **Session data** | Stored temporarily in your browser session only. Cleared when you close the tab. |
| **No user accounts** | This app collects no personal information — no name, email, or login required. |
| **No analytics tracking** | No third-party analytics (e.g. Google Analytics) are used. |
| **Audio generation** | Text is sent to ElevenLabs / Edge TTS for voice synthesis only, not stored. |

> If you are concerned about sharing sensitive personal information, we recommend keeping your inputs general (e.g. "I feel anxious" rather than personally identifying details).

---

## ✨ Features

- 💛 **12 quick-emotion buttons** — Anxious, Heartbroken, Demotivated, Angry, Fearful, Lost, Self-doubt, Distracted, Lonely, Jealous, Burnout, Rage
- 📜 **Smart Shloka Matcher** — Finds the most relevant shlokas for your situation from 100+ mapped themes
- 🤖 **Groq AI Guidance** — Warm, empathetic, non-preachy modern interpretations
- 🎭 **Sanskrit + Transliteration + Meaning** — Full shloka display
- 🎨 **Beautiful dark UI** — Saffron & gold themed, inspired by Indian aesthetics
- ⚡ **Works without API key** — Graceful fallback responses built-in
- 🔊 **Voice recitation** — ElevenLabs / Edge TTS / gTTS fallback chain
- 📚 **Browse all 18 chapters** — Sidebar chapter explorer

---

## 🚀 Quick Start

```bash
git clone https://github.com/jyotheeswar012-max/bhagavad-gita-therapist
cd bhagavad-gita-therapist
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY to .env
streamlit run app.py
```

---

## 🔐 Get Your Free Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Sign in → Click **API Keys** → **Create API Key**
3. Paste it in the app sidebar or `.env` file

---

## 🧪 Testing & CI/CD

This project uses **pytest** and **GitHub Actions** for automated testing.

```bash
# Run tests locally
pip install pytest
pytest tests/ -v
```

Tests cover:
- ✅ All 18 chapters present in the database
- ✅ Every shloka has required fields (sanskrit, meaning, themes, etc.)
- ✅ `get_shloka()`, `get_chapter()`, `search_by_theme()` lookup functions
- ✅ Image fallback logic (PIL placeholder generation)
- ✅ Network failure graceful degradation

CI runs automatically on every push and pull request.

---

## 📚 Shlokas Covered

| Chapter | Verse | Themes |
|:---:|:---:|:---|
| 2 | 47 | Anxiety, Stress, Career, Exam pressure |
| 2 | 14 | Sadness, Grief, Heartbreak, Depression |
| 6 | 5  | Self-doubt, Low confidence, Mindset |
| 18 | 66 | Fear, Guilt, Overwhelm, Helplessness |
| 2 | 20 | Loss, Death, Existential questions |
| 3 | 27 | Ego, Anger, Jealousy, Attachment |
| 6 | 35 | Distraction, Focus, Discipline, Study |
| 4 | 7  | Injustice, Moral dilemma, Ethics |
| 9 | 22 | Faith, Hope, Spiritual support |
| 2 | 3  | Weakness, Giving up, Courage |

*...and 40+ more shlokas across all 18 chapters.*

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Groq AI](https://img.shields.io/badge/Groq_AI-F55036?style=flat-square&logo=groq&logoColor=white)

---

## 📄 License

MIT License © 2026 Jyotheeswar Reddy

---

<div align='center'>

*"✨ Tat Tvam Asi — Thou Art That ✨"*

</div>
