
<div align="center">

```
        ॐ
   कर्मण्येवाधिकारस्ते
  You have a right to act —
   never to the fruits.
      — Gita 2.47
```

---

# 🕉️ Bhagavad Gita AI Therapist

### *5,000 years of wisdom. One conversation. Your peace.*

> **Arjuna sat on the battlefield, paralysed by grief, confusion, and fear.**
> **Krishna spoke. The world changed forever.**
>
> *Now — whenever you feel lost, anxious, heartbroken, or afraid —*
> *Krishna listens again.*

<br/>

[![Live — Talk to Krishna](https://img.shields.io/badge/🌐%20Live%20App-Talk%20to%20Krishna-FF6B00?style=for-the-badge&labelColor=1a0800)](https://bhagavad-gita-therapist.streamlit.app/)

<br/>

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bhagavad-gita-therapist.streamlit.app/)
[![CI](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/actions/workflows/ci.yml/badge.svg)](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/jyotheeswar012-max/bhagavad-gita-therapist?style=social)](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/jyotheeswar012-max/bhagavad-gita-therapist?color=brightgreen)](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/commits/main)

</div>

---

<div align="center">

## ✦ What Is This? ✦

</div>

You open the app. You type what's hurting — maybe it's anxiety about the future, a heartbreak that won't heal, rage you can't explain, or a hollow feeling of being completely lost.

The app reads your words. A **TF-IDF engine** silently searches through **700+ Bhagavad Gita shlokas**, each mapped to dozens of emotional themes. It surfaces the verses that speak directly to *your* pain.

Then **Groq AI** — powered by LLaMA 3.3-70B — channels those shlokas into warm, practical, non-preachy guidance. Not a lecture. Not a sermon. A wise friend, fluent in 5,000-year-old truth.

The words arrive in **English, हिंदी, or తెలుగు**. A deep voice recites the Sanskrit. The flute plays softly in the background.

*You exhale.*

---

<div align="center">

## ✦ The Journey ✦

```
You type your pain
        |
        ▼
┌─────────────────────────────┐
│  🧠  TF-IDF Shloka Matcher  │ ◄─── 700+ shlokas, 100+ themes
│   cosine similarity engine  │      (gita_data.py)
└──────────────┬──────────────┘
               │  top 2 most relevant shlokas
               ▼
┌─────────────────────────────┐
│  🤖  Groq AI  (LLaMA 3.3)  │ ◄─── model config + prompts
│   compassionate guidance    │      (config.py + therapist.py)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  🎨  Streamlit UI (app.py)  │
│                             │
│  Sanskrit verse  +  audio   │ ◄─── ElevenLabs / Edge TTS / gTTS
│  AI guidance in your lang   │ ◄─── i18n.py (EN / HI / TE)
│  Save ❤️  Export 📥  Share  │ ◄─── export_utils.py
│  Background music 🎵        │ ◄─── music.py
│  Analytics 📊 (PIN-gated)   │ ◄─── analytics.py
└─────────────────────────────┘
               │
               ▼
         You find peace.
```

</div>

---

<div align="center">

## ✦ Features ✦

</div>

| | Feature | What It Does |
|--|---------|-------------|
| 🌐 | **Trilingual** | Full UI + AI responses in English, हिंदी & తెలుగు — live switch |
| 💛 | **12 Emotion Chips** | Tap Anxious / Heartbroken / Lost / Rage — or type freely |
| 🧠 | **Smart Shloka Matching** | TF-IDF cosine similarity across 700+ shlokas, 100+ themes |
| 🤖 | **Groq AI Guidance** | LLaMA 3.3-70B — warm, empathetic, actionable wisdom |
| 🎙️ | **Sanskrit Voice** | ElevenLabs guru voice → Edge TTS → gTTS (triple fallback) |
| ❤️ | **Save Favourites** | Bookmark verses, export them as `.json` anytime |
| 📚 | **Chapter Browser** | Read all 18 chapters from the sidebar |
| 💬 | **Session Memory** | All turns saved with timestamps, language, feedback |
| 📥 | **Export** | Download full session as `.txt` or styled `.pdf` |
| 🎵 | **Ambient Music** | Om chanting, flute, bells, rain — your choice |
| 📊 | **Owner Analytics** | PIN-gated: top themes, daily stats, language breakdown |
| 🔒 | **Zero Tracking** | No login. No storage. No trackers. Ever. |

---

<div align="center">

## ✦ Shlokas for Every Storm ✦

</div>

> *नैनं छिन्दन्ति शस्त्राणि नैनं दहति पावकः*
> *"Weapons cannot cut the soul; fire cannot burn it."*
> — Gita 2.23

| Chapter | Verse | When You Feel... |
|:-------:|:-----:|-----------------|
| 2 | 47 | Anxious about results, work, exams |
| 2 | 14 | Heartbroken, grieving, depressed |
| 2 | 20 | Lost after a death, existential fear |
| 2 | 23 | Fragile, afraid, like you might break |
| 3 | 27 | Angry, egotistic, jealous |
| 4 | 7  | Morally lost, watching injustice |
| 6 | 5  | Full of self-doubt, low confidence |
| 6 | 35 | Distracted, unfocused, restless |
| 9 | 22 | Hopeless, needing faith |
| 18 | 66 | Overwhelmed, guilty, surrendering |

*...and 690+ more across all 18 chapters.*

---

<div align="center">

## ✦ Quick Start ✦

</div>

**Clone & run in 4 steps:**

```bash
# 1. Get the code
git clone https://github.com/jyotheeswar012-max/bhagavad-gita-therapist
cd bhagavad-gita-therapist

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your keys
cp .env.example .env
# Open .env and set: GROQ_API_KEY=your_key_here

# 4. Run
streamlit run app.py
# Open http://localhost:8501
```

**Get your free Groq API key** → [console.groq.com](https://console.groq.com) → API Keys → Create

---

<div align="center">

## ✦ Deploy Free in 60 Seconds ✦

</div>

1. **Fork** this repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → select your fork
3. Main file: `app.py`
4. **Advanced settings → Secrets:**

```toml
GROQ_API_KEY      = "gsk_..."
ELEVENLABS_API_KEY = "..."        # optional — for premium Sanskrit voice
OWNER_PIN          = "yourpin"    # optional — for analytics access
```

5. Click **Deploy** ✅

---

<div align="center">

## ✦ The Codebase ✦

</div>

```
bhagavad-gita-therapist/
│
├── app.py            ← The stage. UI, audio, session, everything visible.
├── therapist.py      ← The mind. TF-IDF matching + Groq AI guidance.
├── gita_data.py      ← The scripture. 700+ shlokas, all 18 chapters.
├── config.py         ← The settings. Voices, models, limits — change once here.
├── i18n.py           ← The tongue. English / हिंदी / తెలుగు translations.
├── analytics.py      ← The memory. Anonymous aggregate stats, PIN-gated.
├── export_utils.py   ← The scribe. Text + PDF session exports.
├── music.py          ← The flute. Background audio track registry.
│
├── assets/           ← Images + music files
├── tests/            ← Pytest suite
├── .github/          ← CI/CD with GitHub Actions
└── .streamlit/       ← Theme + server config
```

---

<div align="center">

## ✦ Tech Behind the Magic ✦

</div>

| Layer | Tool |
|-------|------|
| UI | [Streamlit](https://streamlit.io) |
| AI Brain | [Groq](https://groq.com) — LLaMA 3.3-70B |
| Shloka Matching | Pure Python TF-IDF (no ML deps) |
| Voice #1 | [ElevenLabs](https://elevenlabs.io) — guru-style deep TTS |
| Voice #2 | [Edge TTS](https://github.com/rany2/edge-tts) — en-IN-PrabhatNeural |
| Voice #3 | [gTTS](https://gtts.readthedocs.io/) — Google fallback |
| PDF | [fpdf2](https://pyfpdf.github.io/fpdf2/) |
| Images | [Pillow](https://pillow.readthedocs.io/) |
| CI/CD | GitHub Actions |
| Hosting | Streamlit Community Cloud |

---

<div align="center">

## ✦ Privacy ✦

</div>

| What | How We Handle It |
|------|-----------------|
| Your words | Sent to Groq for inference only — **never stored here** |
| Session data | Lives in your browser tab — gone when you close it |
| Analytics | Aggregate counts only — no names, no IPs, nothing personal |
| Accounts | None. Ever. No email. No login. |

---

<div align="center">

## ✦ Mental Health Note ✦

</div>

> This app offers **spiritual reflection** — not therapy, not diagnosis, not medical advice.
> If you are in crisis, please reach out:

| | |
|-|-|
| 🇮🇳 **iCall (India)** | 9152987821 |
| 🇮🇳 **Vandrevala** | 1860-2662-345 (24/7) |
| 🇺🇸 **988 Lifeline (USA)** | Call or text **988** |
| 🌍 **IASP** | [iasp.info/resources/Crisis_Centres](https://www.iasp.info/resources/Crisis_Centres/) |

---

<div align="center">

## ✦ Contribute ✦

</div>

The Gita was spoken to one person in crisis. This app can reach millions. Help build it:

- 📜 **Add shlokas** — edit `gita_data.py` (best first contribution)
- 🌐 **Add a language** — one new dict in `i18n.py` (Kannada? Tamil? Malayalam?)
- 🎵 **Add music** — drop `.mp3` in `assets/`, register in `music.py`
- 🐛 **Report a bug** — [Bug Report](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/issues/new?template=bug_report.md)
- ✨ **Request a feature** — [Feature Request](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/issues/new?template=feature_request.md)

Read [CONTRIBUTING.md](./CONTRIBUTING.md) before submitting a PR.

---

<div align="center">

## ✦ If This Helped You ✦

Give it a star. Not for vanity — but so the next person searching *"I feel lost"* at 3am finds this instead of nothing.

[![Star](https://img.shields.io/github/stars/jyotheeswar012-max/bhagavad-gita-therapist?style=for-the-badge&logo=github&label=⭐%20Star%20this%20project)](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/stargazers)

---

**MIT License** © 2026 [Jyotheeswar Reddy](https://github.com/jyotheeswar012-max)

<br/>

```
यदा यदा हि धर्मस्य ग्लानिर्भवति भारत।
Whenever righteousness declines —
I manifest myself.
              — Krishna, Gita 4.7
```

*Built with love using Streamlit & Groq AI*
*Inspired by the eternal wisdom of the Bhagavad Gita*

✨ **Tat Tvam Asi — Thou Art That** ✨

</div>
