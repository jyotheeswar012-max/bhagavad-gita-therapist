"""
Central configuration for Bhagavad Gita AI Therapist.
All hardcoded values live here — change once, reflects everywhere.
"""

# ── Audio ────────────────────────────────────────────────────────────────

# Local cache directory for generated .mp3 files
# Set to None to disable caching (always generate on demand)
AUDIO_CACHE_DIR = "/tmp/gita_audio"

# Maximum number of cached .mp3 files before oldest are evicted
# Prevents unbounded disk usage on long-running deployments
AUDIO_CACHE_MAX_FILES = 50

# ElevenLabs voice IDs (deep, gravelly, resonant male — guru-style)
# Tried in order; falls back to Edge TTS then gTTS if all fail
ELEVENLABS_VOICES = [
    "N2lVS1w4EtoT3dr4eOWO",  # Callum
    "JBFqnCBsd6RMkjVDRZzb",  # George
    "onwK4e9ZLuTAKqWW03F9",  # Daniel
]

# Edge TTS voice for shloka recitation
EDGE_TTS_SHLOKA_VOICE  = "en-IN-PrabhatNeural"
EDGE_TTS_SHLOKA_RATE   = "-25%"
EDGE_TTS_SHLOKA_PITCH  = "-10Hz"

# Edge TTS voice for guidance narration
EDGE_TTS_GUIDANCE_VOICE = "en-IN-PrabhatNeural"
EDGE_TTS_GUIDANCE_RATE  = "-20%"
EDGE_TTS_GUIDANCE_PITCH = "-8Hz"

# Font paths for PIL placeholder images (tried in order)
FONT_PATHS_BOLD   = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_PATHS_REGULAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]

# ── Groq AI ────────────────────────────────────────────────────────────────

# Groq models tried in order (first available wins)
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
]

# Guidance response token limit
GROQ_MAX_TOKENS = 400

# Creativity level (0.0 = deterministic, 1.0 = very creative)
GROQ_TEMPERATURE = 0.7

# ── Shloka Matching ───────────────────────────────────────────────────────────

# Number of shlokas to return per query
TOP_N_SHLOKAS = 2

# Fallback shloka indices (0-based) used when no themes match
FALLBACK_SHLOKA_INDICES = [4, 0]   # Ch2:47 (karma), Ch1:1 (context)

# ── User-Friendly Error Messages ──────────────────────────────────────────────

ERRORS = {
    "no_api_key": (
        "🔑 **API key not configured.**\n\n"
        "To enable AI guidance, add your `GROQ_API_KEY` in:\n"
        "- **Streamlit Cloud:** App Settings → Secrets\n"
        "- **Local:** Create a `.env` file with `GROQ_API_KEY=your_key`\n\n"
        "Get a free key at [console.groq.com](https://console.groq.com)"
    ),
    "rate_limit": (
        "⏳ **Groq API rate limit reached.**\n\n"
        "The free tier has usage limits. Please wait a moment and try again, "
        "or check your quota at [console.groq.com](https://console.groq.com/usage)."
    ),
    "all_models_down": (
        "⚠️ **All AI models are temporarily unavailable.**\n\n"
        "Groq's servers may be under load. Please try again in 1–2 minutes. "
        "The shlokas above are still available for your reflection."
    ),
    "generic": (
        "❌ **Something went wrong while generating guidance.**\n\n"
        "The shlokas above are still available for your reflection. "
        "Please try again or refresh the page."
    ),
}
