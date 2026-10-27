"""Master profile storage: data/master_profile.md, seeded from references/ on first run."""

import datetime
import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = ROOT / "data" / "master_profile.md"
SEED_PATH = ROOT / "references" / "master_profile.md"

# Contact details live in .env, not in the profile file.
PLACEHOLDERS = ("CONTACT_EMAIL", "CONTACT_PHONE")


def _fill_placeholders(text):
    for key in PLACEHOLDERS:
        text = text.replace("{{" + key + "}}", os.getenv(key, ""))
    return text


def _ensure():
    if not PROFILE_PATH.exists() and SEED_PATH.exists():
        PROFILE_PATH.parent.mkdir(exist_ok=True)
        shutil.copy(SEED_PATH, PROFILE_PATH)


def load():
    """Return (text, filename, updated datetime) or (None, None, None)."""
    _ensure()
    if not PROFILE_PATH.exists():
        return None, None, None
    updated = datetime.datetime.fromtimestamp(PROFILE_PATH.stat().st_mtime)
    text = _fill_placeholders(PROFILE_PATH.read_text(encoding="utf-8"))
    return text, PROFILE_PATH.name, updated


def load_raw():
    """Return the profile source as stored on disk, with {{CONTACT_...}} placeholders
    left intact, so editing it in the app doesn't bake in real contact info."""
    _ensure()
    if not PROFILE_PATH.exists():
        return ""
    return PROFILE_PATH.read_text(encoding="utf-8")


def save(text):
    PROFILE_PATH.parent.mkdir(exist_ok=True)
    PROFILE_PATH.write_text(text, encoding="utf-8")


def status_line(filename, updated):
    stamp = updated.strftime("%b %d, %Y %I:%M %p").replace(" 0", " ")
    return f"Master profile loaded: {filename}, updated {stamp}"
