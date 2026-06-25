"""
therapist.py — Shloka matching and Groq AI guidance engine.

Matching strategy (layered, best-first):
  1. TF-IDF cosine similarity between user input and shloka theme+meaning text
  2. Keyword overlap score (theme substring match) as tiebreaker
  3. Hard fallback to canonical shlokas if nothing matches
"""

import os
import math
import re
from collections import Counter

import streamlit as st
from groq import Groq

from gita_data import SHLOKAS
from config import (
    GROQ_MODELS, GROQ_MAX_TOKENS, GROQ_TEMPERATURE,
    TOP_N_SHLOKAS, FALLBACK_SHLOKA_INDICES, ERRORS
)


# ── Groq client ───────────────────────────────────────────────────────────────

def get_groq_client():
    """Return (Groq client, None) or (None, error_message)."""
    for source in [
        lambda: st.secrets.get("GROQ_API_KEY", ""),
        lambda: os.getenv("GROQ_API_KEY", ""),
    ]:
        try:
            key = source()
            if key:
                return Groq(api_key=key), None
        except Exception:
            pass
    return None, ERRORS["no_api_key"]


# ── TF-IDF semantic matching ──────────────────────────────────────────────────

_STOP_WORDS = {
    "i", "me", "my", "am", "is", "are", "was", "be", "been", "the", "a", "an",
    "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "it",
    "this", "that", "so", "do", "not", "no", "very", "feel", "feeling", "about",
    "have", "has", "just", "like", "from", "can", "cant", "cannot",
}


def _tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, remove stop words."""
    tokens = re.findall(r"[a-z]+", text.lower())
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 2]


def _build_shloka_docs() -> list[str]:
    """Build one rich text document per shloka (themes + meaning)."""
    docs = []
    for s in SHLOKAS:
        theme_text  = " ".join(s["themes"]).replace("-", " ")
        meaning_text = s.get("meaning", "")
        docs.append(f"{theme_text} {meaning_text}")
    return docs


def _tfidf_scores(query: str, docs: list[str]) -> list[float]:
    """Compute cosine TF-IDF similarity between query and each doc."""
    N = len(docs)
    all_docs_tokens = [_tokenize(d) for d in docs]
    query_tokens    = _tokenize(query)

    if not query_tokens:
        return [0.0] * N

    # IDF: log(N / df) for each term
    df: dict[str, int] = {}
    for tokens in all_docs_tokens:
        for term in set(tokens):
            df[term] = df.get(term, 0) + 1

    def idf(term: str) -> float:
        return math.log((N + 1) / (df.get(term, 0) + 1)) + 1.0

    def tfidf_vec(tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        return {t: (count / len(tokens)) * idf(t) for t, count in tf.items()}

    query_vec = tfidf_vec(query_tokens)

    scores = []
    for tokens in all_docs_tokens:
        doc_vec = tfidf_vec(tokens)
        # Cosine similarity
        dot    = sum(query_vec.get(t, 0) * doc_vec.get(t, 0) for t in query_vec)
        norm_q = math.sqrt(sum(v**2 for v in query_vec.values()))
        norm_d = math.sqrt(sum(v**2 for v in doc_vec.values()))
        scores.append(dot / (norm_q * norm_d) if norm_q and norm_d else 0.0)

    return scores


# Pre-build shloka documents once at import time (not on every call)
_SHLOKA_DOCS = _build_shloka_docs()


def _keyword_score(user_lower: str, shloka: dict) -> int:
    """Secondary score: exact theme keyword matches in user text."""
    return sum(1 for theme in shloka["themes"] if theme in user_lower)


def find_relevant_shlokas(user_input: str, top_n: int = TOP_N_SHLOKAS) -> list:
    """
    Find the most relevant shlokas for a given user input.

    Strategy:
      - Primary:   TF-IDF cosine similarity (semantic)
      - Secondary: Keyword overlap (exact theme match) as tiebreaker
      - Fallback:  Return canonical shlokas if combined score is zero
    """
    user_lower  = user_input.lower()
    tfidf       = _tfidf_scores(user_input, _SHLOKA_DOCS)
    kw_scores   = [_keyword_score(user_lower, s) for s in SHLOKAS]

    # Combined score: TF-IDF (weighted 70%) + keyword overlap (30%)
    max_kw      = max(kw_scores) or 1
    combined    = [
        0.7 * tfidf[i] + 0.3 * (kw_scores[i] / max_kw)
        for i in range(len(SHLOKAS))
    ]

    # Pick top_n by combined score
    ranked_indices = sorted(range(len(SHLOKAS)), key=lambda i: combined[i], reverse=True)
    top_indices    = ranked_indices[:top_n]

    # If all scores are effectively zero, use canonical fallbacks
    if all(combined[i] < 0.01 for i in top_indices):
        return [SHLOKAS[i] for i in FALLBACK_SHLOKA_INDICES]

    return [SHLOKAS[i] for i in top_indices]


# ── Guidance generation ──────────────────────────────────────────────────────────

def get_gita_guidance(user_input: str) -> dict:
    """Return dict with 'shlokas' (list) and 'guidance' (str)."""
    shlokas = find_relevant_shlokas(user_input)

    shloka_context = "".join(
        f"\nChapter {s['chapter']}, Verse {s['verse']}:\n"
        f"Sanskrit: {s['sanskrit']}\nMeaning: {s['meaning']}\n"
        for s in shlokas
    )

    prompt = f"""You are a compassionate Bhagavad Gita AI therapist. A person has shared their feelings:

\"{user_input}\"

Here are relevant shlokas from the Bhagavad Gita:
{shloka_context}
Provide a warm, empathetic response that:
1. Acknowledges their feelings with compassion (2-3 sentences)
2. Explains how these shlokas apply to their situation in simple modern language
3. Gives 3 practical daily life action points inspired by the Gita's wisdom
4. Ends with a short motivational closing line

Tone: Warm, wise, non-preachy. Like a wise friend, not a lecture.
Language: Simple English. No jargon. Max 300 words."""

    client, error = get_groq_client()
    if not client:
        return {"shlokas": shlokas, "guidance": error}

    for model_name in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a compassionate Bhagavad Gita AI therapist."},
                    {"role": "user",   "content": prompt},
                ],
                model=model_name,
                max_tokens=GROQ_MAX_TOKENS,
                temperature=GROQ_TEMPERATURE,
            )
            return {"shlokas": shlokas, "guidance": response.choices[0].message.content}

        except Exception as e:
            err_str = str(e)
            if "decommissioned" in err_str or "model_not_found" in err_str:
                continue   # try next model
            if "429" in err_str or "rate_limit" in err_str.lower():
                return {"shlokas": shlokas, "guidance": ERRORS["rate_limit"]}
            # Unexpected error — don't silently swallow it
            return {"shlokas": shlokas, "guidance": ERRORS["generic"]}

    return {"shlokas": shlokas, "guidance": ERRORS["all_models_down"]}
