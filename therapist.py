import os
import streamlit as st
import google.generativeai as genai
from gita_data import SHLOKAS


def configure_gemini():
    # 1. Try Streamlit secrets
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        if api_key:
            genai.configure(api_key=api_key)
            return True, None
    except Exception:
        pass

    # 2. Try environment variable
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key and api_key != "your_gemini_api_key_here":
        genai.configure(api_key=api_key)
        return True, None

    return False, "GEMINI_API_KEY not found in Streamlit Secrets."


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

    gemini_available, config_error = configure_gemini()

    if not gemini_available:
        return {"shlokas": shlokas, "guidance": f"❌ API Key Error: {config_error}"}

    # Try models in order from most to least quota-friendly
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.0-pro",
    ]

    last_error = ""
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return {"shlokas": shlokas, "guidance": response.text}
        except Exception as e:
            last_error = str(e)
            if "429" in str(e):
                continue  # Try next model
            else:
                break  # Non-quota error, stop trying

    return {
        "shlokas": shlokas,
        "guidance": (
            "⚠️ Daily AI quota reached for today.\n\n"
            "The shlokas above still carry deep wisdom for you. "
            "Please come back tomorrow for a fresh AI response, "
            "or the app owner can upgrade to a paid Gemini plan for unlimited access.\n\n"
            "🕉️ Reflect on the shlokas shown above — they are chosen specifically for your situation."
        )
    }
