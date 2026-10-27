"""CareerCanvas entry point. Run with: uv run streamlit run app.py"""

import streamlit as st

nav = st.navigation(
    [
        st.Page("home.py", title="Home", icon="🎨", default=True),
        st.Page("pages/1_Fit_Review.py", title="Fit Review", icon="🎯"),
        st.Page("pages/2_Resume_and_Cover_Letter.py", title="Resume & Cover Letter", icon="📝"),
        st.Page("pages/4_Profile.py", title="Profile", icon="📄"),
        st.Page("pages/5_Job_Tracker.py", title="Job Tracker", icon="📋"),
    ]
)
nav.run()
