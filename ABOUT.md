<div align="center">

```
        ॐ
दुःखेष्वनुद्विग्नमनाः सुखेषु विगतस्पृहः
 One who is not disturbed by sorrow,
  not elated by happiness —
   that person has found peace.
        — Gita 2.56
```

# About This Project

### *Why we built a therapist out of a 5,000-year-old battlefield conversation*

</div>

---

## The Moment It Started

It was 2 AM. The kind of night where the ceiling feels too close and the thoughts feel too loud.

A search bar. *"why do I feel so empty."* Millions of results. None of them felt like they were written for *this* moment.

But somewhere in a dusty PDF, a verse appeared:

> *"वासांसि जीर्णानि यथा विहाय नवानि गृह्णाति नरो‍’पराणि"*
> *Just as a person puts on new garments, giving up old ones,*
> *similarly, the soul accepts new bodies, giving up the old ones.*
> — Gita 2.22

Something shifted.

Not because it solved anything. But because it had been said before — to someone on a battlefield, paralysed by the same feeling of not knowing how to keep going.

**This project is that moment, turned into a product.**

---

## Who It's For

This app was built for the person who:

- Feels anxious about exams, career, or an uncertain future — and needs to be reminded that outcomes are never fully in our hands
- Is heartbroken after a loss, a breakup, or a death — and needs to know that grief is not weakness, it is love with nowhere to go
- Feels completely lost — no purpose, no direction — and needs to hear that confusion is the beginning of clarity
- Is burning with anger or jealousy — and needs to understand where it truly comes from
- Feels like giving up — and needs Arjuna's moment: the moment *he* wanted to give up, and what happened next

This is **not** for people in clinical crisis. That requires a human professional, not an app. The helplines in the README exist for a reason.

This is for the vast middle ground — the everyday weight that most people carry silently because no one taught them how to put it down.

---

## Why the Bhagavad Gita?

The Gita is not a religious text. It is a **psychological manual**.

It was spoken on a battlefield — not in a temple. To a warrior in the middle of a panic attack — not to a saint in meditation. It addresses:

- **Anxiety** (Arjuna's shaking hands, Chapter 1)
- **Identity crisis** ("Who am I really?" Chapter 2)
- **Paralysis by overthinking** (Chapter 3)
- **The ego and its destruction** (Chapters 3–6)
- **Fear of failure and death** (Chapters 2, 8)
- **The search for meaning** (Chapters 9–12)
- **How to act in a broken world** (Chapter 18)

Every emotion a human being feels in 2026 was felt by Arjuna in 3000 BCE. Krishna's answers did not expire.

---

## The Philosophy of the Product

**Non-preachy by design.**
The AI is instructed never to lecture. Never to say "you should." It speaks like a wise friend who has read the Gita, not like a priest reciting it.

**Language as respect.**
The Gita was originally in Sanskrit. Many who need it most think in Hindi or Telugu — not English. The trilingual support is not a feature. It is a statement: *ancient wisdom belongs to everyone, in their own tongue.*

**Privacy as a value, not a checkbox.**
No accounts. No stored conversations. No analytics on individuals. The moment you close the tab, the session is gone. Your pain is yours.

**Voice as a bridge.**
Reading a verse is one experience. *Hearing it* in Sanskrit — that deep, resonant sound that has been chanted for millennia — is something else entirely. The voice layer exists because some truths land differently when spoken aloud.

---

## The Technical Choices (and Why)

| Choice | Why |
|--------|-----|
| **Streamlit** | Zero frontend overhead. The idea, not the framework, should be the focus. |
| **Groq + LLaMA 3.3** | Speed matters when someone is in distress. Sub-second inference keeps the experience human. |
| **TF-IDF over embeddings** | No API dependency for matching. Works offline. Explainable. Fast. |
| **Triple voice fallback** | ElevenLabs sounds best but costs money. Edge TTS is free and good. gTTS always works. Nobody should hit a silent error when they needed to hear that verse. |
| **fpdf2 for PDF** | Sessions should be exportable as keepsakes. A beautifully formatted PDF of your conversation with the Gita is worth saving. |
| **No database** | Every database is a liability — a breach waiting to happen, a GDPR obligation, a maintenance burden. The best database for a mental health app is no database. |

---

## What This Is Not

- **Not a replacement for therapy.** If you need a therapist, please find one.
- **Not a religious conversion tool.** The Gita belongs to humanity. You do not need to be Hindu to benefit from Stoicism. You do not need to be Hindu to benefit from the Gita.
- **Not a chatbot that pretends to be Krishna.** The AI is a *guide* speaking from the wisdom of the Gita — not a deity roleplay.
- **Not a finished product.** It is a living project. 700 shlokas today. All 700 verses of all 18 chapters eventually. More languages. Better voice. Richer guidance.

---

## The Vision

```
Phase 1  ✓  Core app — match, guide, speak              [DONE]
Phase 2  ✓  Multilingual — English, Hindi, Telugu       [DONE]
Phase 3  ✓  Voice, music, export, history               [DONE]
Phase 4  ~  All 700 Gita verses fully mapped            [IN PROGRESS]
Phase 5  ~  Kannada, Tamil, Malayalam support
Phase 6  ~  Personalised shloka journeys (7-day paths)
Phase 7  ~  Offline PWA (no internet needed at 2 AM)
```

---

## For Contributors

If you found this project and feel pulled to contribute — that instinct is the project working.

The best contributions are not code. They are:
- A shloka you know that belongs here
- A translation that feels more alive than the current one
- A language that your grandmother speaks and deserves to hear this in
- A bug you found because you were actually *using* the app

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get started.

---

## Creator

Built by **[Jyotheeswar Reddy](https://github.com/jyotheeswar012-max)** — a developer who believes that the most important software is the software that helps people feel less alone.

---

<div align="center">

```
तत्त्वमसि

Thou Art That.

The one who is reading this,
the one who built this,
the one who needed this at 2 AM —
are not so different.
```

*— Chandogya Upanishad 6.8.7*

</div>
