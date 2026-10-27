"""
Reusable docx builder for Vidya Patil's resumes and cover letters.

Why this exists: this environment has no Node.js, pandoc, or LibreOffice —
only python-docx. Don't waste a turn rediscovering that; import this module
directly.

Usage pattern (see SKILL.md for the full workflow):

    import sys
    sys.path.insert(0, "/Users/vidyapatil/Resume/.claude/skills/resume-tailor/scripts")
    from build_docx import build_resume, build_cover_letter, EDUCATION_DEFAULT

    build_resume(
        path="/Users/vidyapatil/Resume/<Company>/VidyaPatil_Resume_<Company>_<Role>.docx",
        summary="...",                     # one paragraph, no explicit years-of-experience
        competencies=["...", "..."],        # 5-6 short bullet lines
        jobs=[
            {
                "title": "Sr. QA Engineering Specialist – Professional — Hitachi Vantara",
                "dates": "Nov 2018 – Jun 2026",
                "bullets": ["...", "..."],
                "software": "AWS, GCP, ...",   # optional
            },
            ...
        ],
        earlier_experience=[  # optional, defaults to her standard two early roles
            "QA Tester, CheckFree i-Solutions (Jun 2000 – Jul 2002) — ...",
        ],
        education=EDUCATION_DEFAULT,        # or a custom list of strings
    )

    build_cover_letter(
        path="/Users/vidyapatil/Resume/<Company>/VidyaPatil_CoverLetter_<Company>_<Role>.docx",
        company="<Company>",
        re_line="Re: <Job Title> (<Location>) — Job ID <ID>",
        paragraphs=["...", "...", "..."],   # 3-4 paragraphs; last one is the ask
        date_str="September 22, 2026",      # optional, defaults to today
    )

Both functions save a US-Letter, single-column, ATS-friendly .docx: no
tables, columns, text boxes, or images; standard Calibri font; bullets via
Word's built-in 'List Bullet' style (not literal "•" characters); job
title/dates on one line via a right-aligned tab stop, not a table.
"""

import datetime
import os

from dotenv import load_dotenv
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

load_dotenv()
EMAIL = os.getenv("CONTACT_EMAIL", "")
PHONE = os.getenv("CONTACT_PHONE", "")

NAVY = RGBColor(0x1F, 0x38, 0x64)
DARK = RGBColor(0x22, 0x22, 0x22)
GRAY = RGBColor(0x55, 0x55, 0x55)

EDUCATION_DEFAULT = [
    # Most-recent-first (by completion year) — do not reorder to group by degree vs.
    # certification; the ordering IS the point.
    "AI Evals for Everyone — LevelUp Labs, via Maven (2026)",
    "Building Agentic AI Applications with a Problem-First Approach — LevelUp Labs, via Maven (2026)",
    "Become an Agent-Native Operator — OpenClaw Automation, via LevelUp Labs on Maven (2026)",
    "M.S. in Data Science — Indiana University, Bloomington (2016–2018)",
    "B.S. in Health Informatics & Information Management — University of Central Florida (2013–2015)",
    "A.A. — Valencia College (2009–2012)",
    "Certified Clinical Research Associate (CCRA) — McMaster University (2004–2006)",
]

EARLIER_EXPERIENCE_DEFAULT = [
    "QA Tester, CheckFree i-Solutions (Jun 2000 – Jul 2002) — Tested financial databases for integrity during outage events; rolled out Rational ClearQuest for defect management.",
    "Programmer/Database Analyst, IDS InfoTech Limited, India (Jan 1998 – Apr 1999) — Y2K consultant for SmithKline Beecham (UK).",
]

CONTACT_LINE = (
    f"Winter Park, FL   |   {PHONE}   |   {EMAIL}   |   "
    "https://linkedin.com/in/vidyapatilr   |   https://github.com/vidyapatilr"
)


def _set_margins(doc):
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    sec.left_margin = Inches(0.625)
    sec.right_margin = Inches(0.625)
    sec.top_margin = Inches(0.43)
    sec.bottom_margin = Inches(0.35)


def _set_base_style(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = DARK
    normal.paragraph_format.space_after = Pt(0)


def _add_name(doc, name):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(name)
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = NAVY
    r.font.name = "Calibri"
    return p


def _add_contact(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    r.font.size = Pt(10.5)
    r.font.color.rgb = DARK
    return p


def _add_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = NAVY
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), "1F3864")
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def _add_body(doc, text, size=10.5, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.color.rgb = DARK
    return p


def _add_job_title(doc, title_co, dates):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(7.25), alignment=2)  # right-aligned
    r1 = p.add_run(title_co)
    r1.bold = True
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = DARK
    r2 = p.add_run("\t" + dates)
    r2.bold = True
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = NAVY
    return p


def _add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.28)
    r = p.add_run(text)
    r.font.size = Pt(10.5)
    r.font.color.rgb = DARK
    r.font.name = "Calibri"
    return p


def _add_software_line(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run("Software: ")
    r1.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = GRAY
    r2 = p.add_run(text)
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = GRAY
    return p


def build_resume(path, summary, competencies, jobs, earlier_experience=None, education=None, projects=None):
    """Build an ATS-friendly single-column resume .docx and save it to `path`.

    `projects` is an optional list of dicts: {title, date, description}.
    If provided, a PROJECTS section is inserted between EXPERIENCE and EARLIER EXPERIENCE.
    """
    earlier_experience = earlier_experience or EARLIER_EXPERIENCE_DEFAULT
    education = education or EDUCATION_DEFAULT

    doc = Document()
    _set_margins(doc)
    _set_base_style(doc)

    _add_name(doc, "VIDYA RANI PATIL")
    _add_contact(doc, CONTACT_LINE)

    _add_heading(doc, "SUMMARY")
    _add_body(doc, summary)

    _add_heading(doc, "CORE COMPETENCIES")
    for c in competencies:
        _add_bullet(doc, c)

    _add_heading(doc, "EXPERIENCE")
    for job in jobs:
        _add_job_title(doc, job["title"], job["dates"])
        for b in job["bullets"]:
            _add_bullet(doc, b)
        if job.get("software"):
            _add_software_line(doc, job["software"])

    if projects:
        _add_heading(doc, "PROJECTS")
        for proj in projects:
            _add_job_title(doc, proj["title"], proj["date"])
            _add_bullet(doc, proj["description"])

    _add_heading(doc, "EARLIER EXPERIENCE")
    for e in earlier_experience:
        _add_bullet(doc, e)

    _add_heading(doc, "EDUCATION & CERTIFICATIONS")
    for e in education:
        _add_bullet(doc, e)

    doc.save(path)
    return path


def _add_empty(doc):
    """Add a blank paragraph spacer (matches Vidya's preferred cover-letter style)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    return p


def build_cover_letter(path, company, re_line, paragraphs, date_str=None):
    """Build a cover letter .docx and save it to `path`.

    Format (per Vidya's preferred style):
      - Header: name + "Winter Park, FL" only (no full contact line)
      - Empty blank-paragraph spacers between every element
      - Re: line is bold
      - 2-3 body paragraphs; last one is the closing ask
      - "Thank you" / "Sincerely" closing added automatically

    `company` is the hiring company name used in the addressee line.
    Do not include the closing in `paragraphs` — it's added automatically.
    """
    date_str = date_str or datetime.date.today().strftime("%B %d, %Y")

    cl = Document()
    _set_margins(cl)
    _set_base_style(cl)

    # Header: name, location, phone and email
    _add_name(cl, "Vidya Rani Patil")
    _add_body(cl, f"Winter Park, FL   |   {PHONE}   |   {EMAIL}", space_after=0)
    _add_empty(cl)

    _add_body(cl, date_str, space_after=0)
    _add_empty(cl)

    _add_body(cl, f"{company} Hiring Team", space_after=0)
    _add_empty(cl)

    # Re: line — bold
    p = cl.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(re_line)
    r.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = DARK
    _add_empty(cl)

    _add_body(cl, "Dear Hiring Team,", space_after=0)
    _add_empty(cl)

    for para in paragraphs:
        _add_body(cl, para, space_after=0)
        _add_empty(cl)

    _add_body(cl, "Thank you for your consideration.", space_after=0)
    _add_empty(cl)
    _add_body(cl, "Sincerely,", space_after=0)
    _add_body(cl, "Vidya Rani Patil", space_after=0)

    cl.save(path)
    return path
