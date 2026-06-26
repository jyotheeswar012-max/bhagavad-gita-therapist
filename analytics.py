"""
analytics.py — Privacy-first, owner-only usage analytics.
No external trackers. No user data stored. Only theme counts.
"""

import json
import os
from datetime import datetime

STATS_FILE = "/tmp/gita_stats.json"


def _load() -> dict:
    try:
        if os.path.exists(STATS_FILE):
            return json.loads(open(STATS_FILE).read())
    except Exception:
        pass
    return {"themes": {}, "total_queries": 0, "languages": {}, "daily": {}, "emotions": {}}


def _save(stats: dict):
    try:
        open(STATS_FILE, "w").write(json.dumps(stats, ensure_ascii=False))
    except Exception:
        pass


def log_query(themes: list, language: str = "English", emotion: str = ""):
    """Log a query. Called after every guidance request."""
    stats = _load()
    stats["total_queries"] = stats.get("total_queries", 0) + 1

    for theme in themes:
        stats["themes"][theme] = stats["themes"].get(theme, 0) + 1

    stats["languages"][language] = stats["languages"].get(language, 0) + 1

    today = datetime.now().strftime("%Y-%m-%d")
    stats["daily"][today] = stats["daily"].get(today, 0) + 1

    if emotion:
        stats["emotions"][emotion] = stats["emotions"].get(emotion, 0) + 1

    _save(stats)


def get_stats() -> dict:
    return _load()


def render_analytics(st, lang: str = "English"):
    """Render analytics dashboard in Streamlit sidebar. Owner-PIN gated."""
    import streamlit as st_inner

    st_inner.markdown("---")
    st_inner.markdown("## 📊 Usage Analytics")

    try:
        correct_pin = st_inner.secrets.get("OWNER_PIN", "gita2025")
    except Exception:
        correct_pin = "gita2025"

    pin = st_inner.text_input("🔐 Owner PIN", type="password", key="owner_pin")
    if pin != correct_pin:
        st_inner.caption("Enter PIN to view analytics.")
        return

    stats = get_stats()
    total = stats.get("total_queries", 0)
    st_inner.success(f"✅ Total queries: **{total}**")

    themes = stats.get("themes", {})
    if themes:
        st_inner.markdown("**🔥 Top Themes Requested**")
        top = sorted(themes.items(), key=lambda x: x[1], reverse=True)[:8]
        for theme, count in top:
            bar = "█" * min(count, 20)
            st_inner.markdown(f"`{theme}` {bar} {count}")

    langs = stats.get("languages", {})
    if langs:
        st_inner.markdown("**🌐 Languages Used**")
        for lng, cnt in sorted(langs.items(), key=lambda x: x[1], reverse=True):
            st_inner.markdown(f"- {lng}: **{cnt}**")

    daily = stats.get("daily", {})
    if daily:
        st_inner.markdown("**📅 Daily Queries (last 7 days)**")
        recent = sorted(daily.items())[-7:]
        for day, cnt in recent:
            st_inner.markdown(f"- {day}: **{cnt}**")

    emotions = stats.get("emotions", {})
    if emotions:
        st_inner.markdown("**💭 Top Emotions**")
        top_e = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:5]
        for emo, cnt in top_e:
            st_inner.markdown(f"- {emo}: **{cnt}**")
