"""Tests for gita_data.py — shloka database and lookup functions."""
import pytest
from gita_data import (
    SHLOKAS, THEME_MAP, VERSE_MAP, CHAPTER_MAP, CHAPTER_NAMES,
    get_shloka, get_chapter, search_by_theme
)


# ── Database integrity ─────────────────────────────────────────────────────

def test_shlokas_not_empty():
    assert len(SHLOKAS) > 0, "SHLOKAS list must not be empty"

def test_all_18_chapters_present():
    chapters_in_db = {s["chapter"] for s in SHLOKAS}
    for ch in range(1, 19):
        assert ch in chapters_in_db, f"Chapter {ch} missing from database"

def test_every_shloka_has_required_fields():
    required = {"id", "chapter", "verse", "sanskrit", "transliteration", "meaning", "themes"}
    for s in SHLOKAS:
        missing = required - s.keys()
        assert not missing, f"Shloka id={s.get('id')} missing fields: {missing}"

def test_themes_are_non_empty_lists():
    for s in SHLOKAS:
        assert isinstance(s["themes"], list), f"Shloka {s['id']} themes must be a list"
        assert len(s["themes"]) > 0, f"Shloka {s['id']} has no themes"

def test_no_duplicate_ids():
    ids = [s["id"] for s in SHLOKAS]
    assert len(ids) == len(set(ids)), "Duplicate shloka IDs found"

def test_chapter_names_all_18():
    assert len(CHAPTER_NAMES) == 18
    for i in range(1, 19):
        assert i in CHAPTER_NAMES, f"CHAPTER_NAMES missing chapter {i}"


# ── get_shloka() ───────────────────────────────────────────────────────────

def test_get_shloka_known_verse():
    """The most famous shloka — Chapter 2, Verse 47."""
    s = get_shloka(2, 47)
    assert s is not None, "get_shloka(2, 47) returned None"
    assert s["chapter"] == 2
    assert s["verse"] == 47
    assert "karma" in s["meaning"].lower() or "duty" in s["meaning"].lower()

def test_get_shloka_returns_none_for_missing():
    assert get_shloka(99, 99) is None
    assert get_shloka(0, 0) is None

def test_get_shloka_chapter_18_verse_66():
    """Surrender verse — one of the most important in the Gita."""
    s = get_shloka(18, 66)
    assert s is not None
    assert "surrender" in s["meaning"].lower() or "fear" in s["meaning"].lower()


# ── get_chapter() ─────────────────────────────────────────────────────────

def test_get_chapter_returns_list():
    result = get_chapter(2)
    assert isinstance(result, list)
    assert len(result) > 0

def test_get_chapter_all_belong_to_chapter():
    for ch_num in range(1, 19):
        shlokas = get_chapter(ch_num)
        for s in shlokas:
            assert s["chapter"] == ch_num

def test_get_chapter_invalid_returns_empty():
    assert get_chapter(99) == []
    assert get_chapter(0) == []


# ── search_by_theme() ─────────────────────────────────────────────────────

def test_search_by_theme_anxiety():
    results = search_by_theme("anxiety")
    assert len(results) > 0, "Should find shlokas for 'anxiety'"

def test_search_by_theme_grief():
    results = search_by_theme("grief")
    assert len(results) > 0

def test_search_by_theme_case_insensitive():
    lower = search_by_theme("anger")
    upper = search_by_theme("ANGER")
    assert lower == upper

def test_search_by_theme_nonexistent_returns_empty():
    results = search_by_theme("zzznomatch999")
    assert results == []

def test_search_by_theme_returns_list_of_dicts():
    results = search_by_theme("fear")
    for r in results:
        assert isinstance(r, dict)
        assert "meaning" in r


# ── THEME_MAP and VERSE_MAP integrity ────────────────────────────────────

def test_theme_map_populated():
    assert len(THEME_MAP) > 0

def test_verse_map_keys_are_tuples():
    for key in VERSE_MAP:
        assert isinstance(key, tuple) and len(key) == 2

def test_critical_themes_in_theme_map():
    critical = ["anxiety", "grief", "anger", "fear", "duty", "faith", "peace"]
    for theme in critical:
        assert theme in THEME_MAP, f"Critical theme '{theme}' missing from THEME_MAP"
