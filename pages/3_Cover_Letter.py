import streamlit as st

from core import cover_letter, ui
from core.ai_client import AIError
from core.output import save_copy

ui.setup("Cover Letter", "✉️")
st.title("Cover Letter")

profile = ui.profile_panel()
jd, fit = ui.jd_panel("cover")

label = "Regenerate" if "cover" in st.session_state else "Generate Cover Letter"
if st.button(label, type="primary", disabled=not (jd and profile)):
    with st.spinner("Writing your cover letter..."):
        try:
            data, problems = cover_letter.generate(profile, jd, fit)
            company = (fit or {}).get("company") or data.get("company", "")
            position = (fit or {}).get("position") or data.get("position", "")
            docx = cover_letter.to_docx(data, company or "Hiring")
            name = cover_letter.filename(company, position)
            saved = save_copy(company, name, docx)
            st.session_state["cover"] = dict(data=data, problems=problems, docx=docx, name=name, saved=str(saved))
        except (AIError, KeyError) as e:
            st.error(f"Generation failed: {e}")

res = st.session_state.get("cover")
if res:
    for p in res["problems"]:
        st.warning(f"Rule check: {p}")
    st.download_button(
        "Download .docx",
        res["docx"],
        file_name=res["name"],
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary",
    )
    st.caption(f"Also saved to {res['saved']}")
    st.markdown(f"**{res['data']['re_line']}**")
    for para in res["data"]["paragraphs"]:
        st.write(para)
