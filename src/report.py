"""Generates the downloadable PDF "Movie Taste Report" (ReportLab)."""
import io
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ACCENT = colors.HexColor("#E50914")


def _table(rows, widths):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F4F4")]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def _genre_chart(top_genres) -> Image:
    fig, ax = plt.subplots(figsize=(6, 2.6))
    names = [g["genre"] for g in top_genres][::-1]
    ax.barh(names, [g["count"] for g in top_genres][::-1], color="#E50914")
    ax.set_xlabel("Movies rated")
    ax.set_title("Top genres")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return Image(buf, width=15 * cm, height=6.5 * cm)


def build_pdf(user: dict, profile: dict, recs: list, ai_text: str) -> bytes:
    styles = getSampleStyleSheet()
    styles["Title"].textColor = ACCENT
    cell = styles["BodyText"].clone("cell", fontSize=9, leading=11)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                            title="Movie Taste Report")
    story = [
        Paragraph("Movie Taste Report", styles["Title"]),
        Paragraph(f"AI Based Movie Recommendation System &middot; generated {datetime.now():%d %b %Y, %H:%M}",
                  styles["Italic"]),
        Spacer(1, 12),
        _table([
            ["User", "Movies rated", "Average rating", "Liked (>= 4 stars)"],
            [f"{user.get('full_name') or user['username']} (#{user['user_id']})", profile["num_ratings"],
             profile["avg_rating"], f"{profile.get('liked_pct', 0)}%"],
        ], [6 * cm, 3.5 * cm, 3.5 * cm, 4 * cm]),
        Spacer(1, 14),
        Paragraph("AI Analysis", styles["Heading2"]),
    ]
    for line in ai_text.splitlines():
        if line.strip():
            story.append(Paragraph(line.strip().replace("&", "&amp;").replace("<", "&lt;"), styles["BodyText"]))
            story.append(Spacer(1, 4))

    if profile["top_genres"]:
        story += [Spacer(1, 8), _genre_chart(profile["top_genres"])]

    if profile["favourite_movies"]:
        story += [Paragraph("Favourite Movies", styles["Heading2"]),
                  _table([["Title", "Your rating"]] +
                         [[Paragraph(m["title"], cell), f"{m['rating']} / 5"] for m in profile["favourite_movies"]],
                         [13 * cm, 4 * cm])]

    if recs:
        story += [Paragraph("Top AI Recommendations", styles["Heading2"]),
                  _table([["#", "Title", "Genres", "Match"]] +
                         [[i + 1, Paragraph(r["title"], cell), Paragraph(r["genres"].replace("|", ", "), cell),
                           f"{r['score'] * 100:.0f}%"] for i, r in enumerate(recs)],
                         [1 * cm, 7.5 * cm, 6.5 * cm, 2 * cm])]

    story += [Spacer(1, 16), Paragraph(
        "Match % is the like-probability predicted by the Keras ANN model. "
        "AI Analysis is written by an open-source LLM (Ollama) using prompt engineering.", styles["Italic"])]
    doc.build(story)
    return buf.getvalue()
