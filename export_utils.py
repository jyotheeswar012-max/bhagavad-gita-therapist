"""
export_utils.py - Session export helpers.

Provides:
  - build_text_export()  -> plain-text string (always available)
  - build_pdf_export()   -> bytes of a styled PDF (requires fpdf2)

PDF Note: fpdf2 with core fonts (Helvetica) is Latin-1 only.
All text passed to pdf.cell() / pdf.multi_cell() must be ASCII-safe.
Use _safe() to sanitise any string before rendering.
"""

from datetime import datetime
import unicodedata
import re


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe(text: str) -> str:
    """
    Convert a Unicode string to a Latin-1-safe string for fpdf2 core fonts.

    Strategy (in order):
      1. Replace common Unicode punctuation with ASCII equivalents.
      2. Normalise to NFKD and drop combining characters.
      3. Encode to latin-1, replacing anything still un-encodable with '?'.
    """
    # Common replacements
    replacements = {
        "\u2014": "-",   # em dash
        "\u2013": "-",   # en dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
        "\u00a0": " ",   # non-breaking space
        "\u2022": "*",   # bullet
        "\u2122": "(TM)",
        "\u00ae": "(R)",
    }
    for uni, asc in replacements.items():
        text = text.replace(uni, asc)

    # Strip emoji and other symbols (anything outside Basic Latin + Latin-1 Supplement)
    text = re.sub(r"[^\x00-\xff]", "", text)

    # NFKD normalise + drop combining marks
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    # Final safety net
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _ts() -> str:
    return datetime.now().strftime("%d %B %Y, %I:%M %p")


# ---------------------------------------------------------------------------
# Text export
# ---------------------------------------------------------------------------

def build_text_export(history: list[dict]) -> str:
    """
    Convert session chat history to a plain-text string.

    Each history entry:
      {
        "input":    str,
        "shlokas":  list[shloka_dict],
        "guidance": str,
        "feedback": int | None   # 1=helpful, -1=not helpful, None=no vote
      }
    """
    lines = [
        "Om  Bhagavad Gita AI Therapist -- Session Export",
        f"    Generated: {_ts()}",
        "=" * 60,
        "",
    ]
    for i, entry in enumerate(history, 1):
        lines.append(f"--- Turn {i} ---")
        lines.append(f"You: {entry['input']}")
        lines.append("")
        for s in entry["shlokas"]:
            lines.append(f"  [Shloka] Chapter {s['chapter']}, Verse {s['verse']}")
            lines.append(f"     {s['sanskrit']}")
            lines.append(f"     [{s['transliteration']}]")
            lines.append(f"     Meaning: {s['meaning']}")
            lines.append("")
        lines.append("Krishna's Guidance:")
        lines.append(entry["guidance"])
        if entry.get("feedback") == 1:
            lines.append("  [Thumbs Up] Marked as helpful")
        elif entry.get("feedback") == -1:
            lines.append("  [Thumbs Down] Marked as not helpful")
        lines.append("")
        lines.append("=" * 60)
        lines.append("")
    lines.append("Note: This is a spiritual reflection session, not medical advice.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# PDF export
# ---------------------------------------------------------------------------

def build_pdf_export(history: list[dict]) -> bytes:
    """
    Build a styled PDF of the session and return it as bytes.
    Raises RuntimeError if fpdf2 is not installed.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        raise RuntimeError("fpdf2 is not installed. Run: pip install fpdf2")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # -- Title block -----------------------------------------------------------
    pdf.set_fill_color(26, 8, 0)
    pdf.rect(0, 0, 210, 40, "F")
    pdf.set_text_color(255, 215, 0)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(10, 8)
    pdf.cell(190, 10, "Bhagavad Gita AI Therapist", align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(10, 22)
    pdf.cell(190, 8, _safe(f"Session Export  -  {_ts()}"), align="C")
    pdf.ln(20)

    pdf.set_text_color(30, 30, 30)

    for i, entry in enumerate(history, 1):
        # Turn header
        pdf.set_fill_color(240, 230, 200)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(139, 69, 19)
        pdf.cell(0, 8, f"  Turn {i}", fill=True, ln=True)
        pdf.ln(2)

        # User input
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(20, 6, "You:", ln=False)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, _safe(entry["input"]))
        pdf.ln(3)

        # Shlokas
        for s in entry["shlokas"]:
            pdf.set_fill_color(255, 248, 220)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(180, 80, 0)
            pdf.cell(
                0, 7,
                _safe(f"  Shloka: Chapter {s['chapter']}, Verse {s['verse']}"),
                fill=True, ln=True,
            )
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(100, 60, 0)
            pdf.multi_cell(0, 5, _safe(s["transliteration"]))
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, _safe("Meaning: " + s["meaning"]))
            pdf.ln(2)

        # Guidance
        pdf.set_fill_color(230, 240, 255)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 80, 160)
        pdf.cell(0, 7, "  Krishna's Guidance", fill=True, ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, _safe(entry["guidance"]))

        # Feedback badge
        if entry.get("feedback") == 1:
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(0, 130, 0)
            pdf.cell(0, 6, "  [Helpful] Thank you for the feedback", ln=True)
        elif entry.get("feedback") == -1:
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(180, 0, 0)
            pdf.cell(0, 6, "  [Not helpful] Thank you for the feedback", ln=True)

        pdf.ln(5)
        pdf.set_draw_color(200, 180, 140)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

    # Disclaimer footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0, 5,
        "This document is a personal spiritual reflection session. "
        "It is not a substitute for professional psychological or medical advice.",
    )

    return bytes(pdf.output())
