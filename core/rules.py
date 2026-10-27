"""Writing rules shared by every generation prompt, plus code checks run after generation."""

import math
import re

WRITING_RULES = """WRITING RULES (follow every one):
1. Never fabricate. Every claim must trace to the master profile. Never add a tool, standard, metric, or accomplishment that is not in the profile, however well it would match the JD.
2. Never use em dashes, en dashes, or hyphens as sentence connectors. Write full sentences or use commas and periods instead. Hyphenated compound words (for example "Docker-based") are fine.
3. Never use the phrase "low code" or "low-code" anywhere.
4. Never state Vidya's total years of experience (no "20+ years", "two decades", "decades of experience").
5. Python agents at Hitachi Vantara were built through AI-assisted Python development. Never say she wrote Python from scratch or claim strong Python coding.
6. TestNG and Maven suites: she "ran" or "integrated" existing suites as Jenkins quality gates. Never say she built, wrote, or developed them, and never claim Java coding.
7. The roughly 35% defect escape reduction came from redesigning the ETL test-case architecture and tightening requirements traceability. Never attribute it to Jenkins gates or TestNG.
8. Clinical data experience comes from PHRI (McMaster) and Orlando Health. CheckFree was financial databases, not clinical.
9. FindMyTrial, when used, must say she planned and designed it, built it on Lovable in 72 hours, and is in discussions with partners to launch it on web and mobile.
10. The Hitachi multi-agent workflow was deterministic. Never call it non-deterministic. No golden datasets or scoring rubrics at Hitachi (those belong to the personal agentaudit project).
11. Arize Phoenix was used only in the personal agentaudit project, never at Hitachi Vantara.
12. Never list gaps, missing skills, or weaknesses inside a resume or cover letter.
13. Use the JD's own terminology only where it honestly describes what she did. Never borrow the JD's responsibility verbs ("owned", "led", "drove", "architected") unless the profile uses that verb for that work.
14. No hype about her own work ("goes well beyond", "production-level", "rare", "world-class"). Let the facts and numbers carry it."""

DASH_CONNECTOR = re.compile(r"\s[—–-]\s|—|–")
YEARS = re.compile(r"\b\d+\s*\+\s*years|\b\d+\s+years of (?:experience|expertise)|\bdecades?\b", re.I)
BANNED = [
    (re.compile(r"low[\s-]?code", re.I), 'uses the phrase "low code"'),
    (re.compile(r"from scratch", re.I), 'says "from scratch" (agents were AI-assisted)'),
    (re.compile(r"\bnon[\s-]?deterministic", re.I), 'calls the Hitachi workflow "non-deterministic"'),
    (re.compile(r"\b(?:wrote|coded|programmed) (?:the )?python", re.I), "claims she wrote Python directly"),
    (re.compile(r"\b(?:built|wrote|developed|authored|created|designed)\b[^.]{0,40}\bTestNG", re.I), 'says TestNG was built or written (should be "ran")'),
]


def _prose_violations(texts):
    found = []
    for t in texts:
        if not t:
            continue
        snippet = t[:70] + ("..." if len(t) > 70 else "")
        if DASH_CONNECTOR.search(t):
            found.append(f"Dash used as a connector: \"{snippet}\"")
        if YEARS.search(t):
            found.append(f"States years of experience: \"{snippet}\"")
        for pat, why in BANNED:
            if pat.search(t):
                found.append(f"{why.capitalize()}: \"{snippet}\"")
        if "findmytrial" in t.lower() and not ("lovable" in t.lower() and "72 hours" in t.lower()):
            found.append(f"FindMyTrial mentioned without \"Lovable\" and \"72 hours\": \"{snippet}\"")
    return found


def resume_prose(data):
    texts = [data.get("summary", "")] + list(data.get("competencies", []))
    for job in data.get("jobs", []):
        texts += job.get("bullets", [])
    for proj in data.get("projects", []) or []:
        texts.append(proj.get("description", ""))
    return texts


def estimate_resume_lines(data, earlier, education):
    """Rough line count at 10.5 pt Calibri on a 7.25 inch line (about 115 characters)."""
    wrap = lambda s: max(1, math.ceil(len(s) / 115))
    lines = 2 + 5 * 2  # name, contact, and section headings with spacing
    lines += wrap(data.get("summary", ""))
    lines += sum(wrap(c) for c in data.get("competencies", []))
    for job in data.get("jobs", []):
        lines += 1.5 + sum(wrap(b) for b in job.get("bullets", []))
        if job.get("software"):
            lines += wrap("Software: " + job["software"])
    for proj in data.get("projects", []) or []:
        lines += 1.5 + wrap(proj.get("description", ""))
    lines += sum(wrap(e) for e in earlier) + sum(wrap(e) for e in education)
    return lines


MAX_LINES = 112  # about two pages with this script's margins and spacing


def check_resume(data, earlier, education):
    problems = _prose_violations(resume_prose(data))
    jobs = data.get("jobs", [])
    for i, job in enumerate(jobs):
        n = len(job.get("bullets", []))
        if n > 7:
            problems.append(f"{job.get('title', 'A role')} has {n} bullets (max 7).")
        if i == 0 and n < 6:
            problems.append(f"{job.get('title', 'The most recent role')} has {n} bullets (needs 6 to 7).")
    if estimate_resume_lines(data, earlier, education) > MAX_LINES:
        problems.append("Resume is likely longer than 2 pages. Trim bullets or the summary.")
    return problems


def check_cover_letter(data):
    texts = [data.get("re_line", "")] + list(data.get("paragraphs", []))
    problems = _prose_violations(texts[1:])
    # The Re: line may not use dashes either, but job IDs like "Job ID 123" are fine.
    if DASH_CONNECTOR.search(texts[0]):
        problems.append(f"Dash used in the Re: line: \"{texts[0]}\"")
    n = len(data.get("paragraphs", []))
    if not 3 <= n <= 4:
        problems.append(f"Cover letter has {n} paragraphs (needs 3 to 4).")
    return problems
