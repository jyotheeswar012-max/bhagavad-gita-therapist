# 🕉️ Bhagavad Gita AI Therapist

> *Share your struggles. Receive ancient wisdom. Find modern clarity.*

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bhagavad-gita-therapist.streamlit.app/)
[![CI](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/actions/workflows/ci.yml/badge.svg)](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red)](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist)

</div>

---

🌐 **Live Demo:** [bhagavad-gita-therapist.streamlit.app](https://bhagavad-gita-therapist.streamlit.app/)

An AI-powered Streamlit app that listens to your emotional struggles and responds with relevant Bhagavad Gita shlokas + warm, practical guidance powered by **Groq AI** — now in **English, हिंदी & తెలుగు**.

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

## ✨ Features

| Feature | Details |
|---|---|
| 🌐 **Multilingual** | Full UI + AI responses in English, हिंदी, తెలుగు |
| 💛 **12 Emotion Chips** | Anxious, Heartbroken, Angry, Lost, Lonely & more — in all 3 languages |
| 📜 **Smart Shloka Matcher** | TF-IDF cosine similarity across 100+ mapped themes |
| 🤖 **Groq AI Guidance** | Warm, empathetic, non-preachy modern interpretations |
| ❤️ **Favourite Shlokas** | Save, view & export your favourite verses |
| 📊 **Owner Analytics** | PIN-gated usage stats: top themes, languages, daily queries |
| 🎙️ **Voice Recitation** | ElevenLabs → Edge TTS → gTTS fallback chain |
| 📚 **Chapter Browser** | Explore all 18 chapters from the sidebar |
| 💬 **Session History** | All turns logged with feedback & timestamps |
| 📥 **Export** | Download session as Text or PDF |
| 🎵 **Background Music** | Ambient spiritual audio while you reflect |

---

## 🌐 Multilingual Support

The app fully supports 3 languages — switchable live from the sidebar:

```
🌐 English  |  🇮🇳 हिंदी  |  🌺 తెలుగు
```

All UI labels, emotion chips, buttons, headings, and **AI responses** switch to the chosen language instantly.

---

## ❤️ Favourite Shlokas

Click **❤️ Save Shloka** on any displayed verse to save it. View and export all favourites from the sidebar as a `.json` file anytime.

---

## 📊 Owner Analytics (Privacy-First)

No third-party trackers. No user data stored. Only aggregate counts logged locally:

- 🔥 Top requested themes
- 🌐 Language usage breakdown
- 📅 Daily query counts (last 7 days)
- 💭 Most common emotions

**Access:** Enter your `OWNER_PIN` secret in the sidebar Analytics section.
Set it in Streamlit Cloud: `Settings → Secrets → OWNER_PIN = "yourpin"`

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

## 🔒 Privacy Policy

| What | Policy |
|------|--------|
| **User inputs** | Sent to Groq API for inference only. **Not stored** by this app. |
| **Groq API** | Subject to [Groq's Privacy Policy](https://groq.com/privacy-policy/). Does not train on API inputs by default. |
| **Session data** | Browser session only. Cleared when tab closes. |
| **Analytics** | Only aggregate theme/language counts. Zero personal data. |
| **No accounts** | No name, email, or login required. |

---

## 🧪 Testing & CI/CD

```bash
pip install pytest
pytest tests/ -v
```

CI runs automatically on every push and pull request via GitHub Actions.

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
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-000000?style=flat-square&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- 📜 **Add shlokas** — great first contribution!
- 🌐 **Add languages** — Kannada, Tamil, Malayalam welcome
- 🐛 **Report bugs** — use the [Bug Report template](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/issues/new?template=bug_report.md)
- ✨ **Request features** — use the [Feature Request template](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/issues/new?template=feature_request.md)

---

## ⭐ Show Your Support

If this project helped you or someone you know, please consider giving it a ⭐ star on GitHub — it helps more people discover ancient wisdom through modern technology. 🙏

[![Star this repo](https://img.shields.io/github/stars/jyotheeswar012-max/bhagavad-gita-therapist?style=for-the-badge&logo=github)](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/stargazers)

---

## 📄 License

MIT License © 2026 Jyotheeswar Reddy

---

<div align='center'>

*"✨ Tat Tvam Asi — Thou Art That ✨"*

</div>
