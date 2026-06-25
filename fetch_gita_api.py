"""
fetch_gita_api.py  -  One-time script to populate gita_data.py with all 700 shlokas.

Usage (run locally, NOT on Streamlit Cloud):
    pip install requests
    python fetch_gita_api.py

This writes a fresh gita_data.py in the project root.
Commit it and redeploy - no other code changes needed.

API used: https://bhagavadgita.io/api  (free, no key required)
Fallback: https://vedicscriptures.github.io/slok/<ch>/<v>/  (also free)

Shloka schema produced (matches existing gita_data.py exactly):
    {
      "id":              int          e.g. 247  (chapter*100 + verse)
      "chapter":         int          1-18
      "verse":           int          1-N
      "sanskrit":        str          Devanagari text
      "transliteration": str          Roman transliteration
      "meaning":         str          English translation
      "themes":          list[str]    auto-generated from keywords
    }

Auto-theme generation:
    Each verse meaning is scanned against a keyword -> theme map.
    This gives reasonable theme coverage across all 700 verses;
    you can refine manually for important verses.
"""

import json
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Install requests first:  pip install requests")


# ---------------------------------------------------------------------------
# Chapter metadata (unchanged from existing gita_data.py)
# ---------------------------------------------------------------------------

CHAPTER_NAMES = {
    1:  "Arjuna Visada Yoga - The Grief of Arjuna",
    2:  "Sankhya Yoga - The Eternal Reality",
    3:  "Karma Yoga - The Path of Action",
    4:  "Jnana Yoga - The Path of Knowledge",
    5:  "Karma Sanyasa Yoga - Renunciation of Action",
    6:  "Dhyana Yoga - The Path of Meditation",
    7:  "Jnana Vijnana Yoga - Knowledge and Wisdom",
    8:  "Aksara Brahma Yoga - The Imperishable Absolute",
    9:  "Raja Vidya Yoga - The Royal Science",
    10: "Vibhuti Yoga - Divine Manifestations",
    11: "Visvarupa Yoga - The Cosmic Form",
    12: "Bhakti Yoga - The Path of Devotion",
    13: "Ksetra Yoga - The Field and Its Knower",
    14: "Gunatraya Yoga - The Three Modes of Nature",
    15: "Purushottama Yoga - The Supreme Person",
    16: "Daiva Yoga - Divine and Demoniac Natures",
    17: "Sraddhatraya Yoga - The Three Divisions of Faith",
    18: "Moksha Yoga - Liberation Through Renunciation",
}

# Number of verses per chapter (standard count)
CHAPTER_VERSE_COUNTS = {
    1: 47, 2: 72, 3: 43, 4: 42, 5: 29, 6: 47,
    7: 30, 8: 28, 9: 34, 10: 42, 11: 55, 12: 20,
    13: 35, 14: 27, 15: 20, 16: 24, 17: 28, 18: 78,
}


# ---------------------------------------------------------------------------
# Keyword -> theme map for auto-tagging
# ---------------------------------------------------------------------------

KEYWORD_THEMES: list[tuple[list[str], list[str]]] = [
    (["anxious", "anxiety", "worry", "stress", "worried", "tension", "restless"],
     ["anxiety", "stress", "overthinking", "worry"]),

    (["grief", "sorrow", "mourn", "lament", "weep", "tears", "cry", "wept"],
     ["grief", "sadness", "loss", "heartbreak", "depression"]),

    (["fear", "afraid", "terrified", "dread", "fright", "scared"],
     ["fear", "courage", "fearlessness"]),

    (["anger", "wrath", "rage", "furious", "irritat"],
     ["anger", "ego", "self-control"]),

    (["desire", "lust", "greed", "crav", "tempt", "want"],
     ["desire", "attachment", "greed", "addiction"]),

    (["duty", "dharma", "righteous", "obligat", "prescribed"],
     ["duty", "purpose", "karma"]),

    (["action", "karma", "perform", "deed", "work", "act "],
     ["work", "action", "karma", "productivity"]),

    (["result", "fruit", "outcome", "reward", "attach"],
     ["attachment", "results", "detachment"]),

    (["knowledge", "wisdom", "learn", "understand", "intellect"],
     ["knowledge", "wisdom", "learning", "education"]),

    (["soul", "atman", "spirit", "eternal", "immortal", "self"],
     ["soul", "spiritual", "eternal", "identity"]),

    (["death", "die", "mortal", "slain", "perish", "kill"],
     ["death", "impermanence", "existential"]),

    (["peace", "tranquil", "calm", "serenity", "equanim"],
     ["peace", "inner peace", "calm", "equanimity"]),

    (["faith", "devot", "worship", "prayer", "bhakti"],
     ["faith", "devotion", "god", "spiritual"]),

    (["surrender", "refuge", "seek me", "come to me"],
     ["surrender", "trust", "hope", "faith"]),

    (["mind", "thought", "mental", "contemplate", "meditat"],
     ["focus", "meditation", "mind control", "distraction"]),

    (["ego", "pride", "arrogance", "vanity", "conceit"],
     ["ego", "pride", "humility"]),

    (["compassion", "kind", "friend", "love", "care"],
     ["compassion", "relationships", "kindness"]),

    (["forgiv", "sin", "guilt", "mistake", "repent"],
     ["forgiveness", "guilt", "past mistakes", "regret"]),

    (["liberation", "freedom", "moksha", "release", "transcend"],
     ["liberation", "freedom", "moksha", "spiritual liberation"]),

    (["purpose", "meaning", "direct", "lost", "confus"],
     ["purpose", "meaning of life", "direction", "lost"]),

    (["lazy", "inaction", "sloth", "idle", "procrastinat"],
     ["laziness", "procrastination", "motivation", "discipline"]),

    (["comparison", "jealous", "envy", "others"],
     ["jealousy", "comparison", "self-doubt"]),

    (["health", "body", "sleep", "food", "diet", "eat"],
     ["health", "self-care", "wellness", "burnout"]),

    (["change", "impermanent", "temporary", "transient"],
     ["impermanence", "change", "acceptance"]),

    (["lonely", "alone", "isolat", "abandon"],
     ["loneliness", "lonely", "support"]),

    (["confidence", "self-doubt", "doubt yourself", "courage", "weak"],
     ["self-doubt", "low confidence", "motivation", "courage"]),

    (["balance", "moderat", "regul", "discipline"],
     ["balance", "discipline", "self-control"]),
]


def auto_themes(meaning: str) -> list[str]:
    """Generate theme tags from the English meaning of a verse."""
    m_lower = meaning.lower()
    themes: list[str] = []
    for keywords, tags in KEYWORD_THEMES:
        if any(kw in m_lower for kw in keywords):
            themes.extend(t for t in tags if t not in themes)
    return themes or ["spiritual", "wisdom"]  # always at least one tag


# ---------------------------------------------------------------------------
# API fetchers  (two sources, tried in order)
# ---------------------------------------------------------------------------

API_A = "https://bhagavadgita.io/api/v1"      # bhagavadgita.io  (needs RapidAPI key optionally)
API_B = "https://vedicscriptures.github.io"    # vedicscriptures (no key needed)


def _fetch_verse_vedic(chapter: int, verse: int) -> dict | None:
    """
    Fetch a single verse from vedicscriptures.github.io.
    Returns a normalised dict or None on failure.
    """
    url = f"{API_B}/slok/{chapter}/{verse}/"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        # API response fields
        sanskrit = data.get("slok", "").strip()
        roman    = ""
        english  = ""
        # Try multiple translators in order of preference
        for author in ["chinmay", "siva", "purohit", "gambirananda", "sankaracharya",
                       "tej", "ms", "rk", "abhinav", "adi"]:
            entry = data.get(author, {})
            if not entry:
                continue
            if not roman and entry.get("et"):
                roman = entry["et"].strip()
            if not english and entry.get("ec"):
                english = entry["ec"].strip()
            if roman and english:
                break
        if not sanskrit:
            return None
        return {
            "id":              chapter * 100 + verse,
            "chapter":         chapter,
            "verse":           verse,
            "sanskrit":        sanskrit,
            "transliteration": roman or f"Chapter {chapter}, Verse {verse}",
            "meaning":         english or "See Bhagavad Gita for translation.",
            "themes":          auto_themes(english),
        }
    except Exception as e:
        print(f"    [warn] vedicscriptures {chapter}:{verse} -> {e}")
        return None


def _fetch_verse_rapidapi(chapter: int, verse: int, api_key: str) -> dict | None:
    """
    Fetch a single verse from bhagavad-gita.p.rapidapi.com (requires free RapidAPI key).
    """
    url = f"https://bhagavad-gita3.p.rapidapi.com/v2/chapters/{chapter}/verses/{verse}/"
    headers = {
        "X-RapidAPI-Key":  api_key,
        "X-RapidAPI-Host": "bhagavad-gita3.p.rapidapi.com",
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        sanskrit = data.get("text", "").strip()
        roman    = data.get("transliteration", "").strip()
        english  = ""
        for t in data.get("translations", []):
            if t.get("language") == "english":
                english = t.get("description", "").strip()
                break
        if not sanskrit:
            return None
        return {
            "id":              chapter * 100 + verse,
            "chapter":         chapter,
            "verse":           verse,
            "sanskrit":        sanskrit,
            "transliteration": roman or f"Chapter {chapter}, Verse {verse}",
            "meaning":         english or "See Bhagavad Gita for translation.",
            "themes":          auto_themes(english),
        }
    except Exception as e:
        print(f"    [warn] rapidapi {chapter}:{verse} -> {e}")
        return None


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------

SHLOKA_REPR_TEMPLATE = '''\
    {{"id": {id}, "chapter": {chapter}, "verse": {verse},
     "sanskrit": {sanskrit},
     "transliteration": {transliteration},
     "meaning": {meaning},
     "themes": {themes}}},
'''


def _repr(val) -> str:
    """Python repr that uses double-quoted strings."""
    if isinstance(val, str):
        # Escape backslashes and double quotes, then wrap
        escaped = val.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(val, list):
        inner = ", ".join(f'"{v}"' for v in val)
        return f"[{inner}]"
    return repr(val)


def write_gita_data(shlokas: list[dict], out_path: Path) -> None:
    lines = [
        "# gita_data.py  -  Auto-generated by fetch_gita_api.py",
        f"# Total shlokas: {len(shlokas)} across 18 chapters",
        "# Schema: id, chapter, verse, sanskrit, transliteration, meaning, themes",
        "",
        "SHLOKAS = [",
    ]
    current_chapter = None
    for s in shlokas:
        if s["chapter"] != current_chapter:
            current_chapter = s["chapter"]
            lines.append(f"")
            lines.append(f"    # -- Chapter {current_chapter}: {CHAPTER_NAMES.get(current_chapter, '')} --")
        lines.append(
            SHLOKA_REPR_TEMPLATE.format(
                id             = s["id"],
                chapter        = s["chapter"],
                verse          = s["verse"],
                sanskrit       = _repr(s["sanskrit"]),
                transliteration= _repr(s["transliteration"]),
                meaning        = _repr(s["meaning"]),
                themes         = _repr(s["themes"]),
            ).rstrip()
        )
    lines.append("]")
    lines.append("")

    # Paste the lookup maps / utility section verbatim (same as original)
    lines += [
        "",
        "# -- Lookup Maps --",
        "",
        "THEME_MAP = {",
        "    theme: shloka",
        "    for shloka in SHLOKAS",
        "    for theme in shloka[\"themes\"]",
        "}",
        "",
        "VERSE_MAP = {",
        "    (s[\"chapter\"], s[\"verse\"]): s",
        "    for s in SHLOKAS",
        "}",
        "",
        "CHAPTER_MAP = {}",
        "for s in SHLOKAS:",
        "    CHAPTER_MAP.setdefault(s[\"chapter\"], []).append(s)",
        "",
        "CHAPTER_NAMES = " + repr(CHAPTER_NAMES),
        "",
        "",
        "def get_shloka(chapter: int, verse: int):",
        "    return VERSE_MAP.get((chapter, verse))",
        "",
        "def get_chapter(chapter_number: int):",
        "    return CHAPTER_MAP.get(chapter_number, [])",
        "",
        "def search_by_theme(keyword: str):",
        "    keyword = keyword.lower().strip()",
        "    return [s for s in SHLOKAS if any(keyword in t.lower() for t in s[\"themes\"])]",
        "",
    ]

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[ok] Written {len(shlokas)} shlokas to {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fetch all Gita shlokas and write gita_data.py")
    parser.add_argument(
        "--api-key", default="",
        help="RapidAPI key for bhagavad-gita3.p.rapidapi.com (optional; falls back to vedicscriptures)",
    )
    parser.add_argument(
        "--out", default="gita_data.py",
        help="Output file path (default: gita_data.py)",
    )
    parser.add_argument(
        "--delay", type=float, default=0.25,
        help="Seconds to sleep between API calls to avoid rate-limiting (default: 0.25)",
    )
    args = parser.parse_args()

    out_path  = Path(args.out)
    api_key   = args.api_key.strip()
    shlokas: list[dict] = []
    failures: list[tuple] = []

    total = sum(CHAPTER_VERSE_COUNTS.values())
    fetched = 0

    for ch, verse_count in CHAPTER_VERSE_COUNTS.items():
        print(f"Chapter {ch:2d} ({CHAPTER_NAMES[ch].split(' - ')[0]})  -  {verse_count} verses")
        for v in range(1, verse_count + 1):
            shloka = None
            # Try RapidAPI first if key provided
            if api_key:
                shloka = _fetch_verse_rapidapi(ch, v, api_key)
            # Fallback to vedicscriptures
            if not shloka:
                shloka = _fetch_verse_vedic(ch, v)
            if shloka:
                shlokas.append(shloka)
                fetched += 1
                print(f"  [{fetched:3d}/{total}] Ch {ch}:{v}  ok", end="\r")
            else:
                failures.append((ch, v))
                print(f"  [FAIL] Ch {ch}:{v}")
            time.sleep(args.delay)
        print()  # newline after chapter

    print(f"\nFetched: {fetched}/{total}  |  Failed: {len(failures)}")
    if failures:
        print("Failed verses:", failures)

    if not shlokas:
        sys.exit("[error] No shlokas fetched. Check your internet connection.")

    write_gita_data(shlokas, out_path)
    print("\nDone! Commit gita_data.py and redeploy your Streamlit app.")
    print("No other code changes required.")


if __name__ == "__main__":
    main()
