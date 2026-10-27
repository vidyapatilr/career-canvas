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


def fetch_jd(url):
    """Return the page text, or None when the page can't be read or is too thin."""
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
    return text if len(text) >= MIN_CHARS else None


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
