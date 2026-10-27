import streamlit as st

from core import profile as profile_store
from core import ui

ui.setup("Profile", "📄")
st.title("Master Profile")

uploaded = st.file_uploader("Upload a new master_profile.md (replaces the current one)", type=["md"])
if uploaded and st.session_state.get("profile_uploaded") != uploaded.file_id:
    profile_store.save(uploaded.getvalue().decode("utf-8"))
    st.session_state["profile_uploaded"] = uploaded.file_id
    st.success(f"Saved {uploaded.name} as your master profile.")

text, name, updated = profile_store.load()
if text:
    st.caption(profile_store.status_line(name, updated))
    with st.container(height=600, border=True):
        st.markdown(text)
else:
    st.info("No profile yet. Upload your master_profile.md above.")
