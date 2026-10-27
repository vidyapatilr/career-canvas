"""Turn a job posting URL, or an uploaded file, into plain text."""

import io

import requests
from bs4 import BeautifulSoup

MIN_CHARS = 400
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    )
}

# Sites known to serve a sign-in wall to anonymous/non-browser requests instead
# of the posting itself. Skip the network call and fail clearly instead of
# fetching a login page.
BLOCKED_DOMAINS = ("linkedin.com",)

# Phrases that show up near the top of a sign-in-wall page rather than a real
# job posting. Catches login walls on sites not explicitly listed above too.
LOGIN_WALL_SIGNALS = ("sign in to", "join now to", "welcome back", "forgot password", "sign in with")


def _looks_like_login_wall(text):
    head = text[:500].lower()
    return any(signal in head for signal in LOGIN_WALL_SIGNALS)


def fetch_jd(url):
    """Return the page text, or None when the page can't be read, is too thin,
    or is a sign-in wall instead of the actual posting."""
    if any(domain in url.lower() for domain in BLOCKED_DOMAINS):
        return None
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except requests.RequestException:
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "noscript", "svg", "form"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    lines = [ln.strip() for ln in main.get_text("\n").splitlines()]
    text = "\n".join(ln for ln in lines if ln)
    if len(text) < MIN_CHARS or _looks_like_login_wall(text):
        return None
    return text


def read_upload(uploaded):
    """Extract text from a Streamlit UploadedFile (.txt, .pdf, .docx)."""
    name = uploaded.name.lower()
    data = uploaded.getvalue()
    if name.endswith(".pdf"):
        from pypdf import PdfReader

        return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    if name.endswith(".docx"):
        from docx import Document

        return "\n".join(p.text for p in Document(io.BytesIO(data)).paragraphs)
    return data.decode("utf-8", errors="ignore")
