import os
import streamlit as st
from groq import Groq
from gita_data import SHLOKAS


def get_groq_client():
    # 1. Try Streamlit secrets
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        if api_key:
            return Groq(api_key=api_key), None
    except Exception:
        pass

    # 2. Try environment variable
    api_key = os.getenv("GROQ_API_KEY", "")
    if api_key:
        return Groq(api_key=api_key), None

    return None, "GROQ_API_KEY not found in Streamlit Secrets."


def find_relevant_shlokas(user_input: str, top_n: int = 2) -> list:
    user_lower = user_input.lower()
    scores = {}
    for shloka in SHLOKAS:
        score = sum(1 for theme in shloka["themes"] if theme in user_lower)
        if score > 0:
            scores[shloka["id"]] = score
    sorted_ids = sorted(scores, key=scores.get, reverse=True)[:top_n]
    matched = [s for s in SHLOKAS if s["id"] in sorted_ids]
    if not matched:
        matched = [SHLOKAS[0], SHLOKAS[2]]
    return matched


def get_gita_guidance(user_input: str) -> dict:
    shlokas = find_relevant_shlokas(user_input)

    shloka_context = ""
    for s in shlokas:
        shloka_context += f"""
        Chapter {s['chapter']}, Verse {s['verse']}:
        Sanskrit: {s['sanskrit']}
        Meaning: {s['meaning']}
        """

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
        return {"shlokas": shlokas, "guidance": f"❌ {error}"}

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a compassionate Bhagavad Gita AI therapist."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            max_tokens=400,
            temperature=0.7,
        )
        ai_response = chat_completion.choices[0].message.content
    except Exception as e:
        ai_response = f"❌ Groq API Error: {str(e)}"

    return {"shlokas": shlokas, "guidance": ai_response}
