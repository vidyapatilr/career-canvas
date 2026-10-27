"""Shared helpers for naming and saving generated documents."""

import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# Resumes also get saved here, one folder per employer.
OUTPUT_DIR = Path(os.path.expanduser(os.getenv("RESUME_OUTPUT_DIR", "~/Resume")))


def slug(text, fallback):
    words = re.findall(r"[A-Za-z0-9]+", text or "")
    cleaned = "".join(w[0].upper() + w[1:] for w in words)
    return cleaned[:40] or fallback


def folder_name(company):
    name = re.sub(r'[\\/:*?"<>|]+', "", (company or "").strip())
    return name or "Unknown Employer"


def save_copy(company, filename, data):
    """Write the .docx bytes into OUTPUT_DIR/<Company>/ and return the path."""
    folder = OUTPUT_DIR / folder_name(company)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    path.write_bytes(data)
    return path
