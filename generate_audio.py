"""
Run this ONCE locally or in CI to pre-generate all shloka audio files.

Usage:
    pip install gtts
    python generate_audio.py

Output: static/audio/{shloka_id}.mp3  (e.g. static/audio/205.mp3)
"""

import os
import re
from gtts import gTTS
from gita_data import SHLOKAS

OUTPUT_DIR = os.path.join("static", "audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_sanskrit(text: str) -> str:
    """Remove verse markers like ||47|| | from Devanagari text."""
    text = re.sub(r'\|+\s*\d*\s*\|*', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


for shloka in SHLOKAS:
    sid = shloka["id"]
    out_path = os.path.join(OUTPUT_DIR, f"{sid}.mp3")
    if os.path.exists(out_path):
        print(f"[SKIP] {sid}.mp3 already exists")
        continue
    try:
        clean = clean_sanskrit(shloka["sanskrit"])
        tts = gTTS(text=clean, lang='hi', slow=True)
        tts.save(out_path)
        print(f"[OK]   {sid}.mp3  — Ch {shloka['chapter']} v{shloka['verse']}")
    except Exception as e:
        print(f"[FAIL] {sid}.mp3 — {e}")

print(f"\nDone. Audio files saved to: {OUTPUT_DIR}/")
