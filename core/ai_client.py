"""Thin OpenRouter wrapper. Every call asks for a JSON object back."""

import json
import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4.6")


class AIError(RuntimeError):
    pass


def _extract_json(text):
    """Pull the first JSON object out of a model reply, tolerating code fences."""
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise AIError("The model did not return JSON.")
    return json.loads(text[start : end + 1])


def ask_json(system, user, temperature=0.0, max_tokens=4000):
    """Send one system + user prompt and return the parsed JSON reply."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise AIError("OPENROUTER_API_KEY is missing from .env.")
    resp = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "X-Title": "CareerCanvas",
        },
        json={
            "model": MODEL,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system + "\n\nRespond with a single JSON object and nothing else."},
                {"role": "user", "content": user},
            ],
        },
        timeout=180,
    )
    if resp.status_code != 200:
        raise AIError(f"OpenRouter error {resp.status_code}: {resp.text[:300]}")
    content = resp.json()["choices"][0]["message"]["content"]
    try:
        return _extract_json(content)
    except json.JSONDecodeError as e:
        raise AIError(f"Could not parse the model's JSON: {e}") from e
