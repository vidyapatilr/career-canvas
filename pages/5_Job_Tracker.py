import datetime

import pandas as pd
import streamlit as st

from core import tracker_db, ui

ui.setup("Job Tracker", "📋")
st.title("Job Tracker")

fit = st.session_state.get("fit") or {}
with st.expander("Add application", expanded=bool(fit)):
    with st.form("add_app", clear_on_submit=True):
        c1, c2 = st.columns(2)
        company = c1.text_input("Company", value=fit.get("company", ""))
        position = c2.text_input("Position", value=fit.get("position", ""))
        c3, c4, c5 = st.columns(3)
        date_applied = c3.date_input("Date applied", value=datetime.date.today())
        pay = c4.text_input("Pay range", value=fit.get("pay_range", ""))
        status = c5.selectbox("Status", tracker_db.STATUSES)
        notes = st.text_area("Notes", height=80)
        if st.form_submit_button("Add", type="primary"):
            if company.strip() and position.strip():
                tracker_db.add(company.strip(), position.strip(), date_applied.isoformat(), pay.strip(), status, notes.strip())
                st.success(f"Added {position} at {company}.")
            else:
                st.error("Company and position are required.")

rows = tracker_db.list_all()
if not rows:
    st.info("No applications yet.")
    st.stop()

df = pd.DataFrame(rows)
df["date_applied"] = pd.to_datetime(df["date_applied"]).dt.date
df.insert(0, "delete", False)
ids = df["id"].tolist()


def save_edits():
    """Write each inline edit to SQLite as soon as it happens."""
    for idx, changes in st.session_state["tracker_editor"]["edited_rows"].items():
        fields = {k: ("" if v is None else str(v)) for k, v in changes.items() if k != "delete"}
        if fields:
            tracker_db.update(ids[int(idx)], **fields)


st.caption("Edits save automatically. Tick Delete and click Delete selected to remove rows.")
edited = st.data_editor(
    df,
    hide_index=True,
    use_container_width=True,
    disabled=["id"],
    column_config={
        "delete": st.column_config.CheckboxColumn("Delete", width="small"),
        "id": None,
        "company": "Company",
        "position": "Position",
        "date_applied": st.column_config.DateColumn("Date Applied"),
        "pay_range": "Pay Range",
        "status": st.column_config.SelectboxColumn("Status", options=tracker_db.STATUSES, required=True),
        "notes": st.column_config.TextColumn("Notes", width="large"),
    },
    key="tracker_editor",
    on_change=save_edits,
)

c1, c2, _ = st.columns([1, 1, 2])
to_delete = edited.loc[edited["delete"], "id"].tolist()
if c1.button("Delete selected", disabled=not to_delete):
    for rid in to_delete:
        tracker_db.delete(int(rid))
    st.session_state.pop("tracker_editor", None)
    st.rerun()

csv = pd.DataFrame(tracker_db.list_all()).drop(columns=["id"]).to_csv(index=False).encode("utf-8")
c2.download_button("Export CSV", csv, file_name=f"career_canvas_tracker_{datetime.date.today()}.csv", mime="text/csv")
