import streamlit as st

from core import resume_builder, ui
from core.ai_client import AIError
from core.output import save_copy

ui.setup("Resume Builder", "📝")
st.title("Resume Builder")

profile = ui.profile_panel()
jd, fit = ui.jd_panel("resume")

has_result = "resume" in st.session_state
label = "Regenerate" if has_result else "Generate Resume"
if st.button(label, type="primary", disabled=not (jd and profile)):
    with st.spinner("Writing your resume..."):
        try:
            data, problems = resume_builder.generate(profile, jd, fit)
            company = (fit or {}).get("company") or data.get("company", "")
            position = (fit or {}).get("position") or data.get("position", "")
            docx = resume_builder.to_docx(data)
            name = resume_builder.filename(company, position)
            saved = save_copy(company, name, docx)
            st.session_state["resume"] = dict(data=data, problems=problems, docx=docx, name=name, saved=str(saved))
        except (AIError, KeyError) as e:
            st.error(f"Generation failed: {e}")

res = st.session_state.get("resume")
if res:
    data = res["data"]
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
    st.caption("CCRA included" if data.get("is_healthcare") else "CCRA left out (not a healthcare role)")
    st.markdown("#### Summary")
    st.write(data.get("summary", ""))
    st.markdown("#### Core competencies")
    st.markdown("\n".join(f"- {c}" for c in data.get("competencies", [])))
    for job in data.get("jobs", []):
        st.markdown(f"**{job['title']}**  \n{job['dates']}")
        st.markdown("\n".join(f"- {b}" for b in job.get("bullets", [])))
    for proj in data.get("projects") or []:
        st.markdown(f"**{proj['title']}**  \n{proj['date']}")
        st.markdown(f"- {proj['description']}")
