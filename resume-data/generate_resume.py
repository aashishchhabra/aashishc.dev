#!/usr/bin/env python3
"""Generate the country-specific résumés (PDF + Word) from resume-data/facts.yaml.

facts.yaml is the single source of truth for content: edit it, then re-run this
script. Do not hand-edit the generated files.

Usage:
    python3 resume-data/generate_resume.py

Requires: pyyaml, reportlab, python-docx

Each country is a genuinely different document (length, sections, order), per
the conventions researched for that market:
    India        2 pages  short summary, dense key-skills block, tools per role
    Australia    3 pages  work rights up front, key achievements, full role
                          detail, referees line
    UK & Europe  2 pages  titled as a CV, personal profile, tight bullets,
                          sponsorship stated

All output is single-column, table-free, real text with contact details in the
body (not a page header/footer), which is what applicant tracking systems parse
most reliably.
"""
from pathlib import Path

import yaml
from docx import Document
from docx.enum.text import WD_BREAK  # noqa: F401  (kept for manual page-break tweaks)
from docx.shared import Mm, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent.parent
FACTS_PATH = Path(__file__).resolve().parent / "facts.yaml"

ACCENT_HEX, TEXT_HEX, MUTED_HEX = "0B6E8A", "101826", "4A5B6E"

COUNTRIES = {
    "india": {
        "label": "India",
        "basename": "Aashish-Chhabra-Resume-India",
        "phones": ["phone_india"],
        "max_tier": 2,
        "expected_pages": 2,
        "sections": ["summary", "key_skills", "experience", "credentials", "awards", "education"],
        "summary_heading": "PROFESSIONAL SUMMARY",
        "show_tools": True,
        "font_scale": 0.97,
    },
    "australia": {
        "label": "Australia",
        "basename": "Aashish-Chhabra-Resume-Australia",
        "phones": ["phone_australia", "phone_india"],
        "max_tier": 3,
        "expected_pages": 3,
        "sections": ["summary", "key_achievements", "skills", "experience", "credentials", "awards", "education", "referees"],
        "summary_heading": "EXECUTIVE SUMMARY",
        "show_tools": True,
        "font_scale": 1.06,
    },
    "uk_europe": {
        "label": "UK & Europe",
        "basename": "Aashish-Chhabra-CV-UK-Europe",
        "phones": ["phone_india"],
        "max_tier": 2,
        "expected_pages": 2,
        "sections": ["summary", "experience", "skills", "credentials", "education"],
        "summary_heading": "PERSONAL PROFILE",
        "show_tools": False,
        "font_scale": 1.04,
    },
}


def load_facts():
    with open(FACTS_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_blocks(key, facts):
    """Country-specific document as a flat list of (kind, payload) blocks.

    Both renderers consume this, so the PDF and the Word file can't drift apart.
    """
    cfg = COUNTRIES[key]
    c = facts["contact"]
    contact = [c["email"]] + [c[p] for p in cfg["phones"]] + [c["linkedin_display"], c["portfolio_display"], c["location"]]

    blocks = [("name", c["name"]), ("role", facts["role_framing"]), ("contact", "  |  ".join(contact))]
    status = facts.get("status_line", {}).get(key)
    if status:
        blocks.append(("status", status))
    blocks.append(("rule", None))

    for section in cfg["sections"]:
        if section == "summary":
            blocks += [("h", cfg["summary_heading"]), ("body", (None, facts["summary"][key]))]
        elif section == "key_achievements":
            blocks.append(("h", "KEY ACHIEVEMENTS"))
            blocks += [("bullet", a["text"]) for a in facts["key_achievements"]]
        elif section == "key_skills":
            blocks += [("h", "KEY SKILLS"), ("body", (None, ", ".join(facts["key_skills"])))]
        elif section == "skills":
            blocks.append(("h", "TECHNICAL SKILLS"))
            blocks += [("body", (g["category"] + ": ", ", ".join(g["items"]))) for g in facts["skills"]]
        elif section == "experience":
            blocks.append(("h", "PROFESSIONAL EXPERIENCE"))
            for job in facts["experience"]:
                blocks.append(("job", (job["title"], job["employer"])))
                blocks.append(("meta", job["period"] + "  |  " + job["location"]))
                blocks += [("bullet", b["text"]) for b in job["bullets"] if b["tier"] <= cfg["max_tier"]]
                if cfg["show_tools"]:
                    blocks.append(("tools", ("Tools: ", job["tools"])))
                blocks.append(("gap", None))
        elif section == "credentials":
            blocks += [("h", "CERTIFICATIONS & TRAINING"), ("body", (None, "; ".join(facts["credentials"])))]
        elif section == "awards":
            blocks.append(("h", "AWARDS"))
            blocks += [("body", (None, a)) for a in facts["awards"]]
        elif section == "education":
            blocks.append(("h", "EDUCATION"))
            blocks += [("body", (None, e)) for e in facts["education"]]
        elif section == "referees":
            blocks += [("h", "REFEREES"), ("body", (None, facts["referees"]))]
    return blocks


# ---------------------------------------------------------------- PDF

def esc(text):
    """Escape fact text for reportlab's XML-like Paragraph markup ("AT&T")."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pdf_styles(scale):
    accent, text, muted = (colors.HexColor("#" + h) for h in (ACCENT_HEX, TEXT_HEX, MUTED_HEX))

    def st(name, size, font="Helvetica", color=text, lead=1.36, **kw):
        return ParagraphStyle(name, fontName=font, fontSize=size * scale, leading=size * scale * lead, textColor=color, **kw)

    return {
        "name": st("name", 20, "Helvetica-Bold", lead=1.2, spaceAfter=3),
        "role": st("role", 12, color=accent, spaceAfter=6),
        "contact": st("contact", 9, color=muted, spaceAfter=4),
        "status": st("status", 9.4, "Helvetica-Bold", color=accent, spaceAfter=6),
        "h": st("h", 10.8, "Helvetica-Bold", color=accent, spaceBefore=9, spaceAfter=4),
        "job": st("job", 10.2, "Helvetica-Bold", spaceAfter=1, keepWithNext=1),
        "meta": st("meta", 8.9, "Helvetica-Oblique", color=muted, spaceAfter=3, keepWithNext=1),
        "bullet": st("bullet", 9.2, leftIndent=11, firstLineIndent=-8, spaceAfter=2.5),
        "body": st("body", 9.2, spaceAfter=4),
        "tools": st("tools", 8.7, color=muted, leftIndent=3, spaceAfter=2),
    }


def render_pdf(key, blocks, path):
    cfg = COUNTRIES[key]
    s = pdf_styles(cfg["font_scale"])
    doc = SimpleDocTemplate(
        str(path), pagesize=A4, topMargin=15 * mm, bottomMargin=14 * mm, leftMargin=18 * mm, rightMargin=18 * mm,
        title="Aashish Chhabra - " + ("CV" if "CV" in cfg["basename"] else "Resume") + " (" + cfg["label"] + ")",
        author="Aashish Chhabra",
    )
    story = []
    for kind, payload in blocks:
        if kind == "rule":
            story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#C9D6E2"), spaceAfter=4))
        elif kind == "gap":
            story.append(Spacer(1, 5))
        elif kind == "job":
            story.append(Paragraph("<b>" + esc(payload[0]) + "</b>, " + esc(payload[1]), s["job"]))
        elif kind == "bullet":
            story.append(Paragraph("• " + esc(payload), s["bullet"]))
        elif kind in ("body", "tools"):
            label, text = payload
            story.append(Paragraph(("<b>" + esc(label) + "</b>" if label else "") + esc(text), s[kind]))
        else:
            story.append(Paragraph(esc(payload), s[kind]))
    doc.build(story)
    return doc.page


# ---------------------------------------------------------------- Word

def render_docx(key, blocks, path):
    cfg = COUNTRIES[key]
    scale = cfg["font_scale"]
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.top_margin, sec.bottom_margin = Mm(15), Mm(14)
    sec.left_margin = sec.right_margin = Mm(18)
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(9.2 * scale)
    doc.core_properties.author = "Aashish Chhabra"
    doc.core_properties.title = "Aashish Chhabra (" + cfg["label"] + ")"

    def para(runs, size, color=TEXT_HEX, before=0, after=3, style=None, keep=False):
        p = doc.add_paragraph(style=style)
        pf = p.paragraph_format
        pf.space_before, pf.space_after, pf.keep_with_next = Pt(before), Pt(after), keep
        for text, bold, italic in runs:
            r = p.add_run(text)
            r.bold, r.italic = bold, italic
            r.font.size = Pt(size * scale)
            r.font.color.rgb = RGBColor.from_string(color)
        return p

    for kind, payload in blocks:
        if kind == "name":
            para([(payload, True, False)], 20, after=2)
        elif kind == "role":
            para([(payload, False, False)], 12, ACCENT_HEX, after=4)
        elif kind == "contact":
            para([(payload, False, False)], 9, MUTED_HEX, after=3)
        elif kind == "status":
            para([(payload, True, False)], 9.4, ACCENT_HEX, after=4)
        elif kind in ("rule", "gap"):
            continue
        elif kind == "h":
            para([(payload, True, False)], 10.8, ACCENT_HEX, before=9, after=3, keep=True)
        elif kind == "job":
            para([(payload[0], True, False), (", " + payload[1], False, False)], 10.2, before=5, after=0, keep=True)
        elif kind == "meta":
            para([(payload, False, True)], 8.9, MUTED_HEX, after=2, keep=True)
        elif kind == "bullet":
            para([(payload, False, False)], 9.2, after=2, style="List Bullet")
        elif kind in ("body", "tools"):
            label, text = payload
            runs = ([(label, True, False)] if label else []) + [(text, False, False)]
            para(runs, 8.7 if kind == "tools" else 9.2, MUTED_HEX if kind == "tools" else TEXT_HEX, after=3)
    doc.save(str(path))


def main():
    facts = load_facts()
    for key, cfg in COUNTRIES.items():
        blocks = build_blocks(key, facts)
        pages = render_pdf(key, blocks, ROOT / (cfg["basename"] + ".pdf"))
        render_docx(key, blocks, ROOT / (cfg["basename"] + ".docx"))
        flag = "" if pages == cfg["expected_pages"] else "   <-- expected %d, adjust content or font_scale" % cfg["expected_pages"]
        print("%-12s %s.pdf/.docx  %d page(s)%s" % (cfg["label"], cfg["basename"], pages, flag))


if __name__ == "__main__":
    main()
