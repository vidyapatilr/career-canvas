"""
Mechanical check: for each job, how many of the profile's available bullets
made it into a built resume? Run this after building every resume, before
calling it done — this exists because "remember to check the full pool" as
prose guidance alone has failed twice already.

Usage:
    python3 check_bullet_coverage.py <path-to-resume.docx>

Reads company names from master_profile.md (relative to this script's
../references/ directory) and counts bullets per job in both the profile
and the resume, matching jobs by a short company key (substring match on
the job heading). Prints a table; flags any job using fewer bullets than
are available in the profile as something to consciously confirm, not an
error to silence.

This is a coverage check, not a taste check: it can't tell you whether the
unused bullets were *irrelevant* to this JD (a legitimate reason to skip
them) — it can only tell you they exist and weren't used, so you look and
decide. A flagged job with a good reason to have fewer bullets is fine;
a flagged job nobody looked at is the bug this script exists to catch.
"""

import re
import sys
import os

import docx

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(SCRIPT_DIR, "..", "references", "master_profile.md")

# Short keys to match job headings in both the profile and the resume.
# Add a new key here if a new job is ever added to the profile.
JOB_KEYS = [
    "Pentaho (Leo Group)",
    "Hitachi Vantara",
    "LexisNexis",
    "Orlando Health",
    "Population Health Research Institute",
]


def count_profile_bullets():
    with open(PROFILE_PATH, "r") as f:
        text = f.read()

    counts = {}
    # Split on job headings (### ...) to isolate each job's block.
    sections = re.split(r"^### ", text, flags=re.MULTILINE)[1:]
    for section in sections:
        heading = section.splitlines()[0]
        for key in JOB_KEYS:
            if key in heading:
                # Count lines starting with "- " up to the "Software/Tools:" line,
                # excluding any bracketed **Note:**-style meta lines that aren't
                # real accomplishment bullets (those don't start with "- " anyway).
                body = section.split("Software/Tools:")[0]
                bullet_lines = [l for l in body.splitlines() if l.strip().startswith("- ")]
                counts[key] = len(bullet_lines)
                break
    return counts


SECTION_HEADERS = {
    "SUMMARY", "CORE COMPETENCIES", "EXPERIENCE", "EARLIER EXPERIENCE",
    "EDUCATION & CERTIFICATIONS",
}


def count_resume_bullets(resume_path):
    d = docx.Document(resume_path)
    counts = {}
    current_key = None
    bullet_count = 0

    def flush():
        if current_key is not None:
            counts[current_key] = bullet_count

    for p in d.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        if text in SECTION_HEADERS:
            # A section boundary — stop attributing bullets to the last job.
            # (EXPERIENCE itself isn't a job, but seeing it also means any
            # prior job's bullet run has ended.)
            flush()
            current_key = None
            continue
        matched_key = None
        for key in JOB_KEYS:
            if key in text and p.runs and p.runs[0].bold:
                matched_key = key
                break
        if matched_key:
            flush()
            current_key = matched_key
            bullet_count = 0
            continue
        if text.startswith("Software:"):
            continue
        if p.style.name == "List Bullet" and current_key is not None:
            bullet_count += 1
    flush()
    return counts


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_bullet_coverage.py <path-to-resume.docx>")
        sys.exit(1)

    resume_path = sys.argv[1]
    profile_counts = count_profile_bullets()
    resume_counts = count_resume_bullets(resume_path)

    MIN_BULLETS = 2  # Vidya's stated floor: every job should show 2-3 bullets on a resume.

    print(f"{'Job':<45} {'Available':>10} {'Used':>6} {'Flag':>6}")
    print("-" * 70)
    any_flag = False
    for key in JOB_KEYS:
        available = profile_counts.get(key, 0)
        used = resume_counts.get(key, 0)
        under_pool = available > used
        under_floor = used < MIN_BULLETS and available >= MIN_BULLETS
        flag = "<--" if (under_pool or under_floor) else ""
        if flag:
            any_flag = True
        print(f"{key:<45} {available:>10} {used:>6} {flag:>6}")

    print()
    if any_flag:
        print(f"Flagged: either fewer than {MIN_BULLETS} bullets used while {MIN_BULLETS}+ exist in the")
        print("profile, or the resume didn't use everything available. Look at what's")
        print("unused and decide deliberately whether it fits this JD — don't just pad")
        print("with irrelevant bullets to silence the flag, and don't fabricate a bullet")
        print("that isn't in the profile to hit the floor. If the profile itself only has")
        print("1 bullet for a job, that's a sign to enrich the profile, not the resume.")
    else:
        print("No jobs are under-using their available bullet pool or below the 2-bullet floor.")


if __name__ == "__main__":
    main()
