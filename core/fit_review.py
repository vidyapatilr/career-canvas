"""Fit scoring: the model scores each rubric part, code adds them up and picks the label."""

from core.ai_client import ask_json

WEIGHTS = {"skills": 35, "domain": 20, "seniority": 20, "education": 15, "nice_to_have": 10}

SYSTEM = f"""You are an honest career coach and technical recruiter reviewing how well Vidya Patil fits a job.
Judge fit only from the master profile. Do not inflate scores. Distinguish phrasing gaps (she did it, but the profile words it differently) from real gaps (she has not done it). Respect every precision note and the "What she does NOT have" section in the profile.

Score each rubric part as an integer from 0 up to its maximum:
- skills (max 35): core technical skills and tools match
- domain (max 20): domain match (healthcare, clinical, finance, data)
- seniority (max 20): seniority and scope match
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
