"""Shared Streamlit helpers: page setup, theme CSS, and the profile/JD panels."""

from pathlib import Path

import streamlit as st

from core import profile as profile_store
from core.jd_fetcher import read_upload

CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "style.css"


def setup(title, icon="🎨"):
    st.set_page_config(page_title=f"{title} · CareerCanvas", page_icon=icon, layout="centered")
    st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)


def profile_panel():
    """Show the profile status line and return the profile text, or None."""
    text, name, updated = profile_store.load()
    if text:
        st.caption(profile_store.status_line(name, updated))
    else:
        st.warning("No master profile loaded yet.")
        st.page_link("pages/4_Profile.py", label="Upload your master profile", icon="📄")
    return text


def jd_panel(key):
    """Reuse the job description already entered elsewhere, otherwise offer paste or upload."""
    if st.session_state.get("jd"):
        fit = st.session_state.get("fit") or {}
        who = " at ".join(x for x in (fit.get("position"), fit.get("company")) if x)
        st.caption(f"Using the job description you already entered{': ' + who if who else ''}.")
        with st.expander("View job description"):
            st.text(st.session_state["jd"])
        if st.button("Use a different job description", key=f"{key}_clear"):
            st.session_state.pop("jd", None)
            for k in ("fit", "resume", "cover"):
                st.session_state.pop(k, None)
            st.rerun()
        return st.session_state["jd"], st.session_state.get("fit")

    pasted = st.text_area("Paste the job description", height=220, key=f"{key}_paste")
    uploaded = st.file_uploader("Or upload it", type=["txt", "pdf", "docx"], key=f"{key}_upload")
    jd = pasted.strip()
    if uploaded and not jd:
        jd = read_upload(uploaded).strip()
    if jd:
        # Share it immediately so other pages don't ask for it again.
        st.session_state["jd"] = jd
    return jd, None
