import streamlit as st

from core import profile as profile_store
from core import ui

ui.setup("Profile", "📄")
st.title("Master Profile")

text, name, updated = profile_store.load()
if text:
    st.caption(profile_store.status_line(name, updated))
else:
    st.info("No profile yet. Add your details below, or upload a master_profile.md file.")

st.markdown("#### Edit")
st.caption(
    "Add or change anything here, a new job, a certification, a correction, and save. "
    "Keep `{{CONTACT_PHONE}}` and `{{CONTACT_EMAIL}}` as they are; those are filled in from your .env."
)

# Bumping this forces the text area to remount with a fresh value, since Streamlit
# won't otherwise refresh a textarea's on-screen text after the user has typed in it.
st.session_state.setdefault("profile_edit_version", 0)
edit_key = f"profile_edit_{st.session_state['profile_edit_version']}"

edited = st.text_area(
    "Profile source",
    value=profile_store.load_raw(),
    height=500,
    key=edit_key,
    label_visibility="collapsed",
)
saved_text = profile_store.load_raw()
has_changes = edited != saved_text
c1, c2 = st.columns(2)
if c1.button("Save changes", type="primary", disabled=not (has_changes and edited.strip()), use_container_width=True):
    profile_store.save(edited)
    st.success("Profile saved.")
    st.rerun()
if c2.button("Cancel changes", disabled=not has_changes, use_container_width=True):
    st.session_state["profile_edit_version"] += 1
    st.rerun()

with st.expander("Preview (contact info filled in)"):
    with st.container(height=400, border=True):
        st.markdown(profile_store.load()[0] or "")

st.divider()
st.markdown("#### Or replace the whole file")
uploaded = st.file_uploader("Upload a new master_profile.md (replaces the current one)", type=["md"])
if uploaded and st.session_state.get("profile_uploaded") != uploaded.file_id:
    profile_store.save(uploaded.getvalue().decode("utf-8"))
    st.session_state["profile_uploaded"] = uploaded.file_id
    st.session_state["profile_edit_version"] += 1
    st.success(f"Saved {uploaded.name} as your master profile.")
    st.rerun()
