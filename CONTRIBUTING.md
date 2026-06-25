# 🕉️ Contributing to Bhagavad Gita AI Therapist

First of all, **thank you** for taking the time to contribute! This project aims to bring the timeless wisdom of the Bhagavad Gita to people through modern AI — every contribution, big or small, is deeply appreciated. 🙏

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Areas We Need Help With](#areas-we-need-help-with)

---

## 🤝 Code of Conduct

This project follows a simple principle inspired by the Gita itself:

> *"Let your acts be your motivation, not the fruit that comes from them."* — Bhagavad Gita 2.47

- Be respectful and inclusive to all contributors
- Welcome beginners and first-time contributors warmly
- Keep discussions focused and constructive
- Respect the sacred nature of the content in this project

---

## 💡 How Can I Contribute?

### 🐛 Reporting Bugs
- Check [existing issues](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/issues) first
- Open a new issue with a clear title and description
- Include steps to reproduce, expected vs actual behavior
- Add screenshots if helpful

### ✨ Suggesting Features
- Open an issue with the label `enhancement`
- Describe the feature and why it would benefit users
- Examples: new emotion categories, better UI, multilingual support

### 📜 Adding / Improving Shlokas
- The shloka data lives in `gita_data.py`
- You can add missing verses, fix Sanskrit text, improve transliterations or meanings
- Always cite your source (e.g. Swami Prabhupada, Swami Chinmayananda, etc.)

### 🌐 Translations
- Help translate guidance text or shloka meanings into other languages
- Telugu, Hindi, Tamil, Kannada, Malayalam — all welcome!

### 🎨 UI/UX Improvements
- Better themes, layouts, accessibility improvements
- Mobile responsiveness fixes

---

## 🚀 Getting Started

### 1. Fork the repository
Click the **Fork** button at the top right of the [repo page](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist).

### 2. Clone your fork
```bash
git clone https://github.com/YOUR-USERNAME/bhagavad-gita-therapist.git
cd bhagavad-gita-therapist
```

### 3. Set up environment
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 5. Run the app locally
```bash
streamlit run app.py
```

---

## 🔄 Development Workflow

### Create a branch for your change
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### Make your changes, then commit
```bash
git add .
git commit -m "feat: add Telugu shloka translations"
# or
git commit -m "fix: correct Sanskrit for Chapter 2 Verse 47"
```

### Push and open a Pull Request
```bash
git push origin feature/your-feature-name
```
Then open a PR on GitHub against the `main` branch.

---

## ✅ Pull Request Process

1. **One PR per feature/fix** — keep PRs small and focused
2. **Describe your changes** clearly in the PR description
3. **Test locally** before submitting — make sure `streamlit run app.py` works
4. **Link related issues** using `Closes #issue-number` in your PR description
5. PRs will be reviewed within **2–3 days**
6. At least **1 approval** is required before merging

---

## 🎨 Style Guidelines

### Python
- Follow **PEP 8** conventions
- Use descriptive variable names
- Add comments for complex logic
- Keep functions small and focused

### Commit Messages
Use conventional commit format:
```
feat: add new feature
fix: fix a bug
docs: update documentation
style: formatting changes
refactor: code restructure
chore: maintenance tasks
```

### Shloka Data Format (`gita_data.py`)
Each shloka entry must follow this structure:
```python
{
    "chapter": 2,
    "verse": 47,
    "sanskrit": "कर्मण्येवाधिकारस्ते...",
    "transliteration": "karmanye vadhikaraste...",
    "meaning": "You have a right to perform your duties...",
    "themes": ["duty", "action", "detachment"]
}
```

---

## 🙏 Areas We Need Help With

| Area | Difficulty | Description |
|------|-----------|-------------|
| 📜 More Shlokas | Easy | Add remaining verses from all 18 chapters |
| 🌐 Hindi UI | Easy | Translate UI labels to Hindi |
| 🎙️ Better TTS | Medium | Improve Sanskrit pronunciation in audio |
| 📱 Mobile UI | Medium | Improve layout on mobile screens |
| 🧪 Tests | Medium | Add unit tests for `therapist.py` and `gita_data.py` |
| 🤖 Better AI | Hard | Improve Groq prompt for more accurate shloka matching |
| 🗣️ Regional Languages | Hard | Add Tamil, Telugu, Kannada shloka meanings |

---

## 📬 Questions?

Feel free to open a [GitHub Discussion](https://github.com/jyotheeswar012-max/bhagavad-gita-therapist/discussions) or reach out via issues.

---

<p align="center">
  <i>"Yoga is the journey of the self, through the self, to the self."</i><br>
  — Bhagavad Gita 6.20
</p>
