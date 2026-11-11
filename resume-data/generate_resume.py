#!/usr/bin/env python3
"""Generate the 3 country-localized résumé PDFs from resume-data/facts.yaml.

facts.yaml is the single source of truth for résumé content — edit it, then
re-run this script. Do not hand-edit the generated PDFs; that drift (a résumé
maintained by hand, separately from the site) is exactly what caused the
previous résumé to carry stale and incorrect claims.

Usage:
    python3 resume-data/generate_resume.py

Requires: pyyaml, reportlab (pip install pyyaml reportlab)

Outputs (at the repo root, alongside index.html):
    Aashish-Chhabra-Resume-India.pdf
    Aashish-Chhabra-Resume-Australia.pdf
    Aashish-Chhabra-Resume-UK-Europe.pdf
"""
import yaml
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent.parent
FACTS_PATH = Path(__file__).resolve().parent / "facts.yaml"

ACCENT = colors.HexColor("#0089AD")
TEXT = colors.HexColor("#101826")
MUTED = colors.HexColor("#54677D")
RULE = colors.HexColor("#D8E3EF")

# Country-specific rendering rules. Everything else (wording, role framing,
# ordering) is shared across all 3 variants by design — one role framing
# ("Platform Engineering & Architecture Leader"), not a role x country matrix.
COUNTRIES = {
    "india": {
        "label": "India",
        "filename": "Aashish-Chhabra-Resume-India.pdf",
        "phone_keys": ["phone_india"],
        "bullet_priorities": {1, 2},
        "show_au_status": False,
    },
    "australia": {
        "label": "Australia",
        "filename": "Aashish-Chhabra-Resume-Australia.pdf",
        # Published fully per the site owner's explicit decision — same
        # treatment as the India number (visible, not withheld).
        "phone_keys": ["phone_india", "phone_australia"],
        "bullet_priorities": {1, 2},
        "show_au_status": True,
    },
    "uk_europe": {
        "label": "UK & Europe",
        "filename": "Aashish-Chhabra-Resume-UK-Europe.pdf",
        "phone_keys": ["phone_india"],
        # Trimmed to priority-1 bullets to respect the tighter 2-page UK/EU
        # convention; India and Australia keep the fuller priority-2 set.
        "bullet_priorities": {1},
        "show_au_status": False,
    },
}


def esc(text):
    """Escape raw fact text for reportlab's Paragraph markup (a small XML-like
    dialect) — needed because facts.yaml has plain ampersands (e.g. "AT&T",
    "Platform & Big Data") that would otherwise be parsed as malformed entity
    references and silently corrupt the rendered text."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_facts():
    with open(FACTS_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="NameHeader", fontName="Helvetica-Bold", fontSize=20, textColor=TEXT, leading=24, spaceAfter=4))
    styles.add(ParagraphStyle(name="RoleHeader", fontName="Helvetica", fontSize=12, textColor=ACCENT, spaceAfter=8))
    styles.add(ParagraphStyle(name="ContactLine", fontName="Helvetica", fontSize=9, textColor=MUTED, spaceAfter=6))
    styles.add(ParagraphStyle(name="AUStatus", fontName="Helvetica-Bold", fontSize=9.5, textColor=ACCENT, spaceAfter=8))
    styles.add(ParagraphStyle(name="SectionHead", fontName="Helvetica-Bold", fontSize=11, textColor=ACCENT, spaceBefore=10, spaceAfter=4))
    styles.add(ParagraphStyle(name="JobTitle", fontName="Helvetica-Bold", fontSize=10.3, textColor=TEXT, spaceAfter=0))
    styles.add(ParagraphStyle(name="JobMeta", fontName="Helvetica-Oblique", fontSize=8.8, textColor=MUTED, spaceAfter=3))
    styles.add(ParagraphStyle(name="JobBullet", fontName="Helvetica", fontSize=9.2, textColor=TEXT, leading=12.2, leftIndent=12, spaceAfter=2.5))
    styles.add(ParagraphStyle(name="BodyText2", fontName="Helvetica", fontSize=9.2, textColor=TEXT, leading=12.6, spaceAfter=5))
    return styles


def contact_line(facts, cfg):
    c = facts["contact"]
    parts = [c["email"]]
    for key in cfg["phone_keys"]:
        parts.append(c[key]["display"])
    parts.append(c["linkedin_display"])
    parts.append(c["portfolio_display"])
    parts.append(c["location"])
    return " &nbsp;·&nbsp; ".join(esc(p) for p in parts)


def build_pdf(country_key, facts):
    cfg = COUNTRIES[country_key]
    styles = build_styles()
    c = facts["contact"]
    out_path = ROOT / cfg["filename"]

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        title=f"Aashish Chhabra — Resume ({cfg['label']})",
        author=c["name"],
    )

    story = [
        Paragraph(esc(c["name"]), styles["NameHeader"]),
        Paragraph(esc(facts["role_framing"]), styles["RoleHeader"]),
        Paragraph(contact_line(facts, cfg), styles["ContactLine"]),
    ]

    if cfg["show_au_status"]:
        story.append(Paragraph(esc(c["au_status"]["text"]), styles["AUStatus"]))

    story.append(HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=8))

    story.append(Paragraph("SUMMARY", styles["SectionHead"]))
    story.append(Paragraph(esc(facts["summary"]["text"]), styles["BodyText2"]))

    story.append(Paragraph("EXPERIENCE", styles["SectionHead"]))
    for job in facts["experience"]:
        story.append(Paragraph(f'<b>{esc(job["title"])}</b> — {esc(job["employer"])}', styles["JobTitle"]))
        story.append(Paragraph(f'{esc(job["location"])} &nbsp;·&nbsp; {esc(job["period"])}', styles["JobMeta"]))
        for b in job["bullets"]:
            if b.get("priority", 1) in cfg["bullet_priorities"]:
                story.append(Paragraph(f'• {esc(b["text"])}', styles["JobBullet"]))
        story.append(Spacer(1, 5))

    story.append(Paragraph("TECHNICAL SKILLS", styles["SectionHead"]))
    for group in facts["skills"]:
        items = ", ".join(esc(i) for i in group["items"])
        story.append(Paragraph(f'<b>{esc(group["category"])}:</b> {items}', styles["BodyText2"]))

    story.append(Paragraph("CREDENTIALS", styles["SectionHead"]))
    story.append(Paragraph(
        "; ".join(f'{esc(cred["name"])} ({esc(cred["year"])})' for cred in facts["credentials"]),
        styles["BodyText2"],
    ))

    story.append(Paragraph("EDUCATION", styles["SectionHead"]))
    for e in facts["education"]:
        story.append(Paragraph(
            f'{esc(e["degree"])} — {esc(e["institution"])} ({esc(e["period"])})',
            styles["BodyText2"],
        ))

    doc.build(story)
    return out_path


def main():
    facts = load_facts()
    for key in COUNTRIES:
        path = build_pdf(key, facts)
        print(f"Generated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
