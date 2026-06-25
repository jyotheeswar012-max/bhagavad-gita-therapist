"""
fetch_gita_api.py  -  One-time script to populate gita_data.py with all 700 shlokas.

Usage (run locally, NOT on Streamlit Cloud):
    pip install requests
    python fetch_gita_api.py

This writes a fresh gita_data.py in the project root.
Commit it and redeploy - no other code changes needed.

APIs used (both free, no key required):
    Primary fallback : https://vedicscriptures.github.io/slok/<ch>/<v>/
    Optional better  : https://bhagavad-gita3.p.rapidapi.com/  (free RapidAPI key)
        python fetch_gita_api.py --api-key YOUR_KEY

Why json.dumps() for string fields?
    Sanskrit text contains Devanagari, pipe characters (।), newlines, and
    backslashes that break hand-rolled string escaping.  json.dumps() is
    specified to produce valid JSON string literals, which are also valid
    Python string literals - making SyntaxError impossible.
"""

import json
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Install requests first:  pip install requests")


# ---------------------------------------------------------------------------
# Chapter metadata
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

CHAPTER_VERSE_COUNTS = {
    1: 47, 2: 72, 3: 43, 4: 42, 5: 29, 6: 47,
    7: 30, 8: 28, 9: 34, 10: 42, 11: 55, 12: 20,
    13: 35, 14: 27, 15: 20, 16: 24, 17: 28, 18: 78,
}


# ---------------------------------------------------------------------------
# Auto-theme generation
# ---------------------------------------------------------------------------

KEYWORD_THEMES = [
    (["anxious", "anxiety", "worry", "stress", "worried", "tension", "restless"],
     ["anxiety", "stress", "overthinking", "worry"]),
    (["grief", "sorrow", "mourn", "lament", "weep", "tears", "cry", "wept"],
     ["grief", "sadness", "loss", "heartbreak", "depression"]),
    (["fear", "afraid", "terrified", "dread", "fright", "scared"],
     ["fear", "courage", "fearlessness"]),
    (["anger", "wrath", "rage", "furious", "irritat"],
     ["anger", "ego", "self-control"]),
    (["desire", "lust", "greed", "crav", "tempt"],
     ["desire", "attachment", "greed", "addiction"]),
    (["duty", "dharma", "righteous", "obligat", "prescribed"],
     ["duty", "purpose", "karma"]),
    (["action", "karma", "perform", "deed", "work"],
     ["work", "action", "karma", "productivity"]),
    (["result", "fruit", "outcome", "reward", "attach"],
     ["attachment", "results", "detachment"]),
    (["knowledge", "wisdom", "learn", "understand", "intellect"],
     ["knowledge", "wisdom", "learning", "education"]),
    (["soul", "atman", "spirit", "eternal", "immortal"],
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
    (["comparison", "jealous", "envy"],
     ["jealousy", "comparison", "self-doubt"]),
    (["health", "body", "sleep", "food", "diet", "eat"],
     ["health", "self-care", "wellness", "burnout"]),
    (["change", "impermanent", "temporary", "transient"],
     ["impermanence", "change", "acceptance"]),
    (["lonely", "alone", "isolat", "abandon"],
     ["loneliness", "lonely", "support"]),
    (["confidence", "self-doubt", "weak", "courage"],
     ["self-doubt", "low confidence", "motivation", "courage"]),
    (["balance", "moderat", "regul", "discipline"],
     ["balance", "discipline", "self-control"]),
]


def auto_themes(meaning: str) -> list:
    m = meaning.lower()
    themes = []
    for keywords, tags in KEYWORD_THEMES:
        if any(kw in m for kw in keywords):
            themes.extend(t for t in tags if t not in themes)
    return themes or ["spiritual", "wisdom"]


# ---------------------------------------------------------------------------
# API fetchers
# ---------------------------------------------------------------------------

def _fetch_vedic(chapter: int, verse: int) -> dict | None:
    """Free, no key: vedicscriptures.github.io"""
    try:
        r = requests.get(
            f"https://vedicscriptures.github.io/slok/{chapter}/{verse}/",
            timeout=10,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        sanskrit = (data.get("slok") or "").strip()
        if not sanskrit:
            return None
        roman, english = "", ""
        for author in ["chinmay", "siva", "purohit", "gambirananda",
                       "sankaracharya", "tej", "ms", "rk", "abhinav", "adi"]:
            entry = data.get(author) or {}
            if not roman   and entry.get("et"): roman   = entry["et"].strip()
            if not english and entry.get("ec"): english = entry["ec"].strip()
            if roman and english:
                break
        return {
            "id":              chapter * 100 + verse,
            "chapter":         chapter,
            "verse":           verse,
            "sanskrit":        sanskrit,
            "transliteration": roman    or f"Chapter {chapter}, Verse {verse}",
            "meaning":         english  or "Refer to Bhagavad Gita for translation.",
            "themes":          auto_themes(english),
        }
    except Exception as e:
        print(f"    [warn] vedic {chapter}:{verse} -> {e}")
        return None


def _fetch_rapidapi(chapter: int, verse: int, api_key: str) -> dict | None:
    """Optional: bhagavad-gita3.p.rapidapi.com (free RapidAPI key)"""
    try:
        r = requests.get(
            f"https://bhagavad-gita3.p.rapidapi.com/v2/chapters/{chapter}/verses/{verse}/",
            headers={
                "X-RapidAPI-Key":  api_key,
                "X-RapidAPI-Host": "bhagavad-gita3.p.rapidapi.com",
            },
            timeout=10,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        sanskrit = (data.get("text") or "").strip()
        if not sanskrit:
            return None
        roman   = (data.get("transliteration") or "").strip()
        english = ""
        for t in data.get("translations") or []:
            if t.get("language") == "english":
                english = (t.get("description") or "").strip()
                break
        return {
            "id":              chapter * 100 + verse,
            "chapter":         chapter,
            "verse":           verse,
            "sanskrit":        sanskrit,
            "transliteration": roman    or f"Chapter {chapter}, Verse {verse}",
            "meaning":         english  or "Refer to Bhagavad Gita for translation.",
            "themes":          auto_themes(english),
        }
    except Exception as e:
        print(f"    [warn] rapidapi {chapter}:{verse} -> {e}")
        return None


# ---------------------------------------------------------------------------
# Writer — json.dumps() for every string/list: SyntaxError is impossible
# ---------------------------------------------------------------------------

def write_gita_data(shlokas: list, out_path: Path) -> None:
    """
    Serialise shlokas into a valid Python source file.

    Every string/list value is serialised with json.dumps() which:
      - Escapes backslashes, double-quotes, newlines, tabs correctly
      - Preserves Devanagari and all Unicode (ensure_ascii=False)
      - Produces output that is simultaneously valid JSON and valid Python
    This makes it impossible to generate a SyntaxError regardless of the
    content returned by the API.
    """
    lines = [
        "# gita_data.py  -  Auto-generated by fetch_gita_api.py",
        f"# Total shlokas: {len(shlokas)} across 18 chapters",
        "",
        "SHLOKAS = [",
    ]

    current_chapter = None
    for s in shlokas:
        if s["chapter"] != current_chapter:
            current_chapter = s["chapter"]
            lines.append("")
            lines.append(
                f"    # -- Chapter {current_chapter}: "
                f"{CHAPTER_NAMES.get(current_chapter, '')} --"
            )

        # json.dumps handles ALL edge cases safely
        sk = json.dumps(s["sanskrit"],        ensure_ascii=False)
        tr = json.dumps(s["transliteration"], ensure_ascii=False)
        me = json.dumps(s["meaning"],         ensure_ascii=False)
        th = json.dumps(s["themes"],          ensure_ascii=False)

        lines.append(
            f'    {{"id": {s["id"]}, "chapter": {s["chapter"]}, "verse": {s["verse"]},'
        )
        lines.append(f'     "sanskrit": {sk},')
        lines.append(f'     "transliteration": {tr},')
        lines.append(f'     "meaning": {me},')
        lines.append(f'     "themes": {th}}},')

    lines += [
        "]",
        "",
        "",
        "# -- Lookup Maps --",
        "",
        'THEME_MAP = {theme: s for s in SHLOKAS for theme in s["themes"]}',
        'VERSE_MAP = {(s["chapter"], s["verse"]): s for s in SHLOKAS}',
        "CHAPTER_MAP = {}",
        "for s in SHLOKAS:",
        '    CHAPTER_MAP.setdefault(s["chapter"], []).append(s)',
        "",
        f"CHAPTER_NAMES = {repr(CHAPTER_NAMES)}",
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
        '    return [s for s in SHLOKAS if any(keyword in t.lower() for t in s["themes"])]',
        "",
    ]

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[ok] Written {len(shlokas)} shlokas to {out_path}")

    # Self-verify: import the file and confirm it loads cleanly
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_gita_check", out_path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print(f"[verified] {len(mod.SHLOKAS)} shlokas imported without errors.")
    except SyntaxError as e:
        print(f"[ERROR] SyntaxError in generated file at line {e.lineno}: {e.msg}")
        print("This should never happen with json.dumps writer — please report.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Fetch all Bhagavad Gita shlokas and write gita_data.py"
    )
    parser.add_argument("--api-key", default="",
                        help="Optional RapidAPI key for better translations")
    parser.add_argument("--out",     default="gita_data.py",
                        help="Output file (default: gita_data.py)")
    parser.add_argument("--delay",   type=float, default=0.25,
                        help="Seconds between API calls (default: 0.25)")
    args = parser.parse_args()

    out_path = Path(args.out)
    api_key  = args.api_key.strip()
    shlokas, failures = [], []
    total   = sum(CHAPTER_VERSE_COUNTS.values())
    fetched = 0

    for ch, verse_count in CHAPTER_VERSE_COUNTS.items():
        print(f"\nChapter {ch:2d}: {CHAPTER_NAMES[ch].split(' - ')[0]}  ({verse_count} verses)")
        for v in range(1, verse_count + 1):
            shloka = None
            if api_key:
                shloka = _fetch_rapidapi(ch, v, api_key)
            if not shloka:
                shloka = _fetch_vedic(ch, v)
            if shloka:
                shlokas.append(shloka)
                fetched += 1
                print(f"  [{fetched:3d}/{total}] Ch{ch}:{v} ok", end="\r")
            else:
                failures.append((ch, v))
                print(f"  [FAIL] Ch{ch}:{v}")
            time.sleep(args.delay)

    print(f"\n\nFetched: {fetched}/{total}  |  Failed: {len(failures)}")
    if failures:
        print("Failed verses:", failures)
    if not shlokas:
        sys.exit("[error] No shlokas fetched. Check your internet connection.")

    write_gita_data(shlokas, out_path)

    print("\nNext steps:")
    print("  git add gita_data.py")
    print('  git commit -m "data: full 700-shloka Bhagavad Gita"')
    print("  git push")


if __name__ == "__main__":
    main()
