"""Tailored resume: prompt the model for build_resume() content, check it, build the .docx."""

import io
import json

from core.ai_client import ask_json
from core.output import slug
from core.rules import WRITING_RULES, check_resume
from build_docx import EARLIER_EXPERIENCE_DEFAULT, EDUCATION_DEFAULT, build_resume

EARLIER_KEYS = ("CheckFree", "IDS InfoTech")

SYSTEM = f"""You write tailored, ATS-friendly resumes for Vidya Rani Patil from her master profile.

{WRITING_RULES}

RESUME RULES:
- Write every bullet as Action + Context + Result. Keep results and numbers exactly as stated in the profile.
- Write a new summary for this JD: one paragraph, 3 to 4 sentences, no years of experience. Use implied first person: no name, no "she", no "I" (for example "QA engineering specialist who...").
- Competencies: 5 to 6 short lines drawn from the profile that match the JD.
- Include every role in the profile's Work Experience section (not the Earlier Experience entries, CheckFree and IDS InfoTech, which code adds), most recent first, using the exact title, company, and dates from the profile, formatted as "<Title> — <Company>" with dates like "Nov 2018 – Jul 2026". Show Hitachi Vantara as a single role.
- Give the most recent role 6 to 7 bullets. Give older roles up to 7 bullets, but only as many as the profile honestly supports. Never pad.
- For each role, a "software" line listing the profile's tools for that role that are relevant to the JD, comma separated.
- Include FindMyTrial in "projects" only when it helps for this JD. Its title is "FindMyTrial (https://plain-speak-trials.lovable.app/)" and its date is "Oct 2026 – Present".
- The whole resume must fit on 2 pages, so keep bullets to one or two lines each.
- Do not include earlier experience or education; code adds those.

Return JSON with exactly these keys:
{{
  "company": "hiring company name from the JD",
  "position": "job title from the JD",
  "is_healthcare": true or false,
  "summary": "",
  "competencies": [""],
  "jobs": [{{"title": "", "dates": "", "bullets": [""], "software": ""}}],
  "projects": [{{"title": "", "date": "", "description": ""}}]
}}"""


def education_for(is_healthcare):
    if is_healthcare:
        return list(EDUCATION_DEFAULT)
    return [e for e in EDUCATION_DEFAULT if "CCRA" not in e]


def _user_prompt(profile, jd, fit, problems):
    parts = [f"MASTER PROFILE:\n{profile}", f"JOB DESCRIPTION:\n{jd}"]
    if fit:
        slim = {k: fit.get(k) for k in ("company", "position", "is_healthcare", "strengths", "gaps", "summary")}
        parts.append(f"FIT REVIEW RESULT:\n{json.dumps(slim, indent=2)}")
    if problems:
        parts.append(
            "YOUR PREVIOUS DRAFT BROKE THESE RULES. Fix every one:\n- " + "\n- ".join(problems)
        )
    return "\n\n".join(parts)


def generate(profile, jd, fit=None, temperature=0.4):
    """Return (content dict, problems list). Retries once if the checks fail."""
    problems = []
    for _ in range(2):
        data = ask_json(SYSTEM, _user_prompt(profile, jd, fit, problems), temperature=temperature, max_tokens=6000)
        if fit and "is_healthcare" in fit:
            data["is_healthcare"] = bool(fit["is_healthcare"])
        data["jobs"] = [j for j in data.get("jobs", []) if not any(x in j.get("title", "") for x in EARLIER_KEYS)]
        data["education"] = education_for(data.get("is_healthcare"))
        problems = check_resume(data, EARLIER_EXPERIENCE_DEFAULT, data["education"])
        if not problems:
            break
    return data, problems


def to_docx(data):
    buf = io.BytesIO()
    build_resume(
        path=buf,
        summary=data["summary"],
        competencies=data["competencies"],
        jobs=data["jobs"],
        projects=data.get("projects") or None,
        education=data["education"],
    )
    return buf.getvalue()


def filename(company, position):
    return f"VidyaPatil_Resume_{slug(company, 'Company')}_{slug(position, 'Role')}.docx"
