"""
export_utils.py — Session export helpers.

Provides:
  - build_text_export()  → plain-text string (always available)
  - build_pdf_export()   → bytes of a styled PDF (requires fpdf2)
"""

from datetime import datetime


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
        "🕉️  Bhagavad Gita AI Therapist — Session Export",
        f"    Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        "=" * 60,
        "",
    ]
    for i, entry in enumerate(history, 1):
        lines.append(f"--- Turn {i} ---")
        lines.append(f"You: {entry['input']}")
        lines.append("")
        for s in entry["shlokas"]:
            lines.append(f"  📜 Chapter {s['chapter']}, Verse {s['verse']}")
            lines.append(f"     {s['sanskrit']}")
            lines.append(f"     [{s['transliteration']}]")
            lines.append(f"     Meaning: {s['meaning']}")
            lines.append("")
        lines.append("Krishna's Guidance:")
        lines.append(entry["guidance"])
        if entry.get("feedback") == 1:
            lines.append("  👍 Marked as helpful")
        elif entry.get("feedback") == -1:
            lines.append("  👎 Marked as not helpful")
        lines.append("")
        lines.append("=" * 60)
        lines.append("")
    lines.append("⚠️  This is a spiritual reflection session, not medical advice.")
    return "\n".join(lines)


def build_pdf_export(history: list[dict]) -> bytes:
    """
    Build a styled PDF of the session and return it as bytes.
    Falls back gracefully if fpdf2 is not installed.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        raise RuntimeError(
            "fpdf2 is not installed. Run: pip install fpdf2"
        )

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── Title block ────────────────────────────────────────────────────────
    pdf.set_fill_color(26, 8, 0)          # dark saffron background
    pdf.rect(0, 0, 210, 40, "F")
    pdf.set_text_color(255, 215, 0)       # gold
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(10, 8)
    pdf.cell(190, 10, "Bhagavad Gita AI Therapist", align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(10, 22)
    pdf.cell(190, 8, "Session Export  —  " + datetime.now().strftime("%d %B %Y, %I:%M %p"), align="C")
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
        pdf.multi_cell(0, 6, entry["input"])
        pdf.ln(3)

        # Shlokas
        for s in entry["shlokas"]:
            pdf.set_fill_color(255, 248, 220)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(180, 80, 0)
            pdf.cell(
                0, 7,
                f"  Shloka: Chapter {s['chapter']}, Verse {s['verse']}",
                fill=True, ln=True
            )
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(100, 60, 0)
            pdf.multi_cell(0, 5, s["transliteration"])
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, "Meaning: " + s["meaning"])
            pdf.ln(2)

        # Guidance
        pdf.set_fill_color(230, 240, 255)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 80, 160)
        pdf.cell(0, 7, "  Krishna's Guidance", fill=True, ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, entry["guidance"])

        # Feedback badge
        if entry.get("feedback") == 1:
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(0, 130, 0)
            pdf.cell(0, 6, "  Marked as helpful", ln=True)
        elif entry.get("feedback") == -1:
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(180, 0, 0)
            pdf.cell(0, 6, "  Marked as not helpful", ln=True)

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
        "It is not a substitute for professional psychological or medical advice."
    )

    return bytes(pdf.output())
