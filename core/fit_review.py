"""Fit scoring: the model scores each rubric part, code adds them up and picks the label."""

from core.ai_client import ask_json

WEIGHTS = {"skills": 35, "domain": 20, "seniority": 20, "education": 15, "nice_to_have": 10}

SYSTEM = f"""You are an honest career coach and technical recruiter reviewing how well Vidya Patil fits a job.
Judge fit only from the master profile. Do not inflate scores. Distinguish phrasing gaps (she did it, but the profile words it differently) from real gaps (she has not done it). Respect every precision note and the "What she does NOT have" section in the profile.

Score each rubric part as an integer from 0 up to its maximum:
- skills (max 35): core technical skills and tools match
- domain (max 20): domain match (healthcare, clinical, finance, data)
- seniority (max 20): seniority and scope match. Judge this from the actual responsibilities, years required, and reporting structure described in the JD, not from the job title word alone. Titles are not standardized across industries: in banking and finance (e.g. Vice President, Assistant Vice President), the ladder usually runs Analyst, Associate, Vice President, Director, Managing Director, so "Vice President" there is typically a mid-career or senior individual-contributor level, not executive leadership. Don't penalize seniority just because a title sounds senior in a generic sense; check what the JD actually asks the person to own and how many years it requires.
- education (max 15): required degree or certification met
- nice_to_have (max 10): nice-to-have skills

Return JSON with exactly these keys:
{{
  "company": "hiring company name, or empty string",
  "position": "job title, or empty string",
  "pay_range": "pay range exactly as stated in the JD, or empty string",
  "is_healthcare": true or false (true when the employer or role is in healthcare, clinical research, pharma, life sciences, or medical devices),
  "subscores": {{"skills": 0, "domain": 0, "seniority": 0, "education": 0, "nice_to_have": 0}},
  "strengths": ["2 to 3 short strengths"],
  "gaps": [{{"text": "short gap", "type": "phrasing or real"}}],
  "summary": "4 to 5 sentences of honest breakdown, full sentences"
}}
Write in full sentences. Never use em dashes or hyphens as sentence connectors."""


def label_for(score):
    if score >= 85:
        return "Perfect"
    if score >= 65:
        return "Good"
    if score >= 45:
        return "Stretch"
    return "Skip"


LABEL_HELP = {
    "Perfect": "85 to 100. A strong, ready-to-apply match on skills, domain, seniority, and education.",
    "Good": "65 to 84. A solid match overall, with only small or phrasing-level gaps. Worth applying to.",
    "Stretch": "45 to 64. Real gaps on some must-haves (often seniority, domain, or a specific skill). "
    "Still worth applying if you want to grow into the role, but expect to be a longer shot.",
    "Skip": "Below 45. Significant mismatch on the core requirements. Unlikely to be shortlisted.",
}


def review(profile, jd):
    user = f"MASTER PROFILE:\n{profile}\n\nJOB DESCRIPTION:\n{jd}"
    result = ask_json(SYSTEM, user, temperature=0)
    subs = result.get("subscores", {})
    total = 0
    for key, cap in WEIGHTS.items():
        val = max(0, min(cap, int(subs.get(key, 0) or 0)))
        subs[key] = val
        total += val
    result["subscores"] = subs
    result["score"] = total
    result["label"] = label_for(total)
    return result
