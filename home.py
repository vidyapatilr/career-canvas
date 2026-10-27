import streamlit as st

from core import ui

ui.setup("Home")

st.markdown(
    """<div class='cc-hero'>
    <h1>CareerCanvas</h1>
    <p>Turn a job description into an honest fit review, a tailored resume, and a cover letter, all grounded in your master profile.</p>
    </div>""",
    unsafe_allow_html=True,
)

ui.profile_panel()

fit = st.session_state.get("fit")
if fit:
    st.markdown(
        f"<div class='cc-card'><b>Last review:</b> {fit.get('position') or 'Role'} at "
        f"{fit.get('company') or 'Company'} &middot; {fit['score']} ({fit['label']})</div>",
        unsafe_allow_html=True,
    )

st.markdown("#### Where to start")

TILES = [
    ("🎯", "Fit Review", "Score a JD against your profile.", "pages/1_Fit_Review.py"),
    ("📝", "Resume & Cover Letter", "Paste one JD, build both .docx files.", "pages/2_Resume_and_Cover_Letter.py"),
    ("📄", "Profile", "View or replace your master profile.", "pages/4_Profile.py"),
    ("📋", "Job Tracker", "Track every application.", "pages/5_Job_Tracker.py"),
]

cols = st.columns(2)
for i, (icon, title, desc, target) in enumerate(TILES):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"<div class='cc-tile-icon'>{icon}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='cc-tile-title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='cc-tile-desc'>{desc}</div>", unsafe_allow_html=True)
            st.page_link(target, label="Open →")
