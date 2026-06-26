# 🕉️ Contributing to Bhagavad Gita AI Therapist

Thank you for your interest in contributing! Every shloka, bug fix, and feature helps bring ancient wisdom to more people. 🙏

---

## 🚀 Quick Start

```bash
git clone https://github.com/jyotheeswar012-max/bhagavad-gita-therapist
cd bhagavad-gita-therapist
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

---

## 📜 Adding Shlokas (Easy — Great First Contribution!)

1. Open `gita_data.py`
2. Add to the `SHLOKAS` list following this structure:

```python
{
    "chapter": 2,
    "verse": 47,
    "sanskrit": "कर्मण्येवाधिकारस्ते।",
    "transliteration": "Karmany evadhikaras te",
    "meaning": "You have the right to perform your duties...",
    "themes": ["anxiety", "stress", "career", "action"],
    "source": "Swami Prabhupada"
}
```

3. Use the [📜 Add Shloka](.github/ISSUE_TEMPLATE/shloka_addition.md) issue template
4. Always cite your source

---

## 🌐 Multilingual Contributions

We're adding Hindi and Telugu support! Contributions welcome for:
- Translating UI labels to Hindi / Telugu
- Adding meanings in Hindi / Telugu to existing shlokas
- Testing the language switcher

---

## 🐛 Reporting Bugs

Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template.

## ✨ Requesting Features

Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template.

---

## 📋 Code Style

- Python: follow PEP 8
- Keep CSS inside `app.py` `st.markdown()` blocks
- No hardcoded API keys ever
- Run `pytest tests/ -v` before submitting a PR

---

## 🏷️ Difficulty Labels

| Label | Difficulty | Examples |
|---|---|---|
| `good first issue` | Easy | Adding shlokas, fixing typos |
| `help wanted` | Medium | New features, language support |
| `enhancement` | Medium-Hard | New UI sections, analytics |
| `bug` | Varies | Any broken functionality |

---

*"The soul is eternal. So is good code."* 🕉️
