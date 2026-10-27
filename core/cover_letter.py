"""Tailored cover letter: prompt for build_cover_letter() content, check it, build the .docx."""

import io
import json

from core.ai_client import ask_json
from core.output import slug
from core.rules import WRITING_RULES, check_cover_letter
from build_docx import build_cover_letter

SYSTEM = f"""You write tailored cover letters for Vidya Rani Patil from her master profile.

{WRITING_RULES}

COVER LETTER RULES:
- Written in first person as Vidya ("I"). Plain, confident tone. No explicit years of experience.
- 3 to 4 paragraphs of 60 to 120 words each. Open with the role and why she fits, give two or three concrete proof points from the profile tied to the JD, and make the last paragraph the ask.
- Do not put phone, email, or links in the body; the header already has them.
- Do not include a greeting, a "Thank you" line, or a sign off; code adds those.
- Re: line format: "Re: <Job Title>", adding " (<Location>)" and ", Job ID <ID>" only when the JD states them. No dashes.

Return JSON with exactly these keys:
{{"company": "hiring company name from the JD", "position": "job title from the JD", "re_line": "", "paragraphs": ["", "", ""]}}"""


def _user_prompt(profile, jd, fit, problems):
    parts = [f"MASTER PROFILE:\n{profile}", f"JOB DESCRIPTION:\n{jd}"]
    if fit:
        slim = {k: fit.get(k) for k in ("company", "position", "strengths", "summary")}
        parts.append(f"FIT REVIEW RESULT:\n{json.dumps(slim, indent=2)}")
    if problems:
        parts.append("YOUR PREVIOUS DRAFT BROKE THESE RULES. Fix every one:\n- " + "\n- ".join(problems))
    return "\n\n".join(parts)


def generate(profile, jd, fit=None, temperature=0.4):
    problems = []
    for _ in range(2):
        data = ask_json(SYSTEM, _user_prompt(profile, jd, fit, problems), temperature=temperature)
        problems = check_cover_letter(data)
        if not problems:
            break
    return data, problems


def to_docx(data, company):
    buf = io.BytesIO()
    build_cover_letter(path=buf, company=company, re_line=data["re_line"], paragraphs=data["paragraphs"])
    return buf.getvalue()


def filename(company, position):
    return f"VidyaPatil_CoverLetter_{slug(company, 'Company')}_{slug(position, 'Role')}.docx"
