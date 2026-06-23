import os
import google.generativeai as genai
from gita_data import SHLOKAS
from dotenv import load_dotenv

load_dotenv()


def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key and api_key != "your_gemini_api_key_here":
        genai.configure(api_key=api_key)
        return True
    return False


def find_relevant_shlokas(user_input: str, top_n: int = 2) -> list:
    """Keyword-based shloka matcher."""
    user_lower = user_input.lower()
    scores = {}
    for shloka in SHLOKAS:
        score = sum(1 for theme in shloka["themes"] if theme in user_lower)
        if score > 0:
            scores[shloka["id"]] = score
    sorted_ids = sorted(scores, key=scores.get, reverse=True)[:top_n]
    matched = [s for s in SHLOKAS if s["id"] in sorted_ids]
    if not matched:
        matched = [SHLOKAS[0], SHLOKAS[2]]  # Default: karma + self-elevation
    return matched


def get_gita_guidance(user_input: str) -> dict:
    """Get AI-powered Gita guidance for the user's problem."""
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

    gemini_available = configure_gemini()
    ai_response = ""

    if gemini_available:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            ai_response = response.text
        except Exception:
            ai_response = _fallback_response()
    else:
        ai_response = _fallback_response()

    return {"shlokas": shlokas, "guidance": ai_response}


def _fallback_response() -> str:
    return (
        "The Bhagavad Gita offers timeless wisdom for moments like these.\n\n"
        "What you're feeling is deeply human — and Krishna's teachings remind us "
        "that every challenge carries within it the seed of growth.\n\n"
        "Reflect on these shlokas and let them guide you toward:\n"
        "1. ✅ Focusing on your actions, not the outcomes\n"
        "2. ✅ Accepting impermanence with grace\n"
        "3. ✅ Trusting the process of life\n\n"
        "To unlock AI-powered guidance, add your free Gemini API key in the sidebar. 🕉️"
    )
