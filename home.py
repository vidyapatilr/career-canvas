import streamlit as st

from core import ui

ui.setup("Home")

st.title("CareerCanvas")
st.markdown("Turn a job description into an honest fit review, a tailored resume, and a cover letter, all grounded in your master profile.")

ui.profile_panel()

st.markdown("#### Where to start")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Fit_Review.py", label="Fit Review", icon="🎯")
    st.caption("Score a JD against your profile.")
    st.page_link("pages/2_Resume_Builder.py", label="Resume Builder", icon="📝")
    st.caption("Generate a tailored .docx resume.")
    st.page_link("pages/3_Cover_Letter.py", label="Cover Letter", icon="✉️")
    st.caption("Generate a tailored .docx cover letter.")
with col2:
    st.page_link("pages/4_Profile.py", label="Profile", icon="📄")
    st.caption("View or replace your master profile.")
    st.page_link("pages/5_Job_Tracker.py", label="Job Tracker", icon="📋")
    st.caption("Track every application.")

fit = st.session_state.get("fit")
if fit:
    st.markdown(
        f"<div class='cc-card'><b>Last review:</b> {fit.get('position') or 'Role'} at "
        f"{fit.get('company') or 'Company'} · {fit['score']} ({fit['label']})</div>",
        unsafe_allow_html=True,
    )
