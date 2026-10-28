import streamlit as st

from core import cover_letter, resume_builder, ui
from core.ai_client import AIError
from core.output import save_copy

ui.setup("Resume & Cover Letter", "📝")
st.title("Resume & Cover Letter")

profile = ui.profile_panel()
jd, fit = ui.jd_panel("doc")

st.markdown("#### Build")
col1, col2 = st.columns(2)

with col1:
    resume_feedback = ""
    if "resume" in st.session_state:
        resume_feedback = st.text_area(
            "Anything to fix or change? (optional)",
            key="resume_feedback",
            placeholder="e.g. Lead with the TestNG bullet, trim the summary, emphasize Python more",
            height=80,
        )
    label = "Regenerate Resume" if "resume" in st.session_state else "Build Resume"
    if st.button(label, type="primary", use_container_width=True, disabled=not (jd and profile)):
        with st.spinner("Writing your resume..."):
            try:
                data, problems = resume_builder.generate(profile, jd, fit, feedback=resume_feedback.strip() or None)
                company = (fit or {}).get("company") or data.get("company", "")
                position = (fit or {}).get("position") or data.get("position", "")
                docx = resume_builder.to_docx(data)
                name = resume_builder.filename(company, position)
                saved = save_copy(company, name, docx)
                st.session_state["resume"] = dict(
                    data=data, problems=problems, docx=docx, name=name, saved=str(saved)
                )
            except (AIError, KeyError) as e:
                st.error(f"Generation failed: {e}")

with col2:
    cover_feedback = ""
    if "cover" in st.session_state:
        cover_feedback = st.text_area(
            "Anything to fix or change? (optional)",
            key="cover_feedback",
            placeholder="e.g. Make the opening paragraph punchier, drop the FindMyTrial mention",
            height=80,
        )
    label = "Regenerate Cover Letter" if "cover" in st.session_state else "Build Cover Letter"
    if st.button(label, type="primary", use_container_width=True, disabled=not (jd and profile)):
        with st.spinner("Writing your cover letter..."):
            try:
                data, problems = cover_letter.generate(profile, jd, fit, feedback=cover_feedback.strip() or None)
                company = (fit or {}).get("company") or data.get("company", "")
                position = (fit or {}).get("position") or data.get("position", "")
                docx = cover_letter.to_docx(data, company or "Hiring")
                name = cover_letter.filename(company, position)
                saved = save_copy(company, name, docx)
                st.session_state["cover"] = dict(
                    data=data, problems=problems, docx=docx, name=name, saved=str(saved)
                )
            except (AIError, KeyError) as e:
                st.error(f"Generation failed: {e}")

res_col, cover_col = st.columns(2)

with res_col:
    res = st.session_state.get("resume")
    if res:
        data = res["data"]
        st.markdown("##### Resume")
        for p in res["problems"]:
            st.warning(f"Rule check: {p}")
        st.download_button(
            "Download .docx",
            res["docx"],
            file_name=res["name"],
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            key="resume_dl",
        )
        st.caption(f"Also saved to {res['saved']}")
        st.caption("CCRA included" if data.get("is_healthcare") else "CCRA left out (not a healthcare role)")
        with st.expander("Preview", expanded=False):
            st.markdown("**Summary**")
            st.write(data.get("summary", ""))
            st.markdown("**Core competencies**")
            st.markdown("\n".join(f"- {c}" for c in data.get("competencies", [])))
            for job in data.get("jobs", []):
                st.markdown(f"**{job['title']}**  \n{job['dates']}")
                st.markdown("\n".join(f"- {b}" for b in job.get("bullets", [])))
            for proj in data.get("projects") or []:
                st.markdown(f"**{proj['title']}**  \n{proj['date']}")
                st.markdown(f"- {proj['description']}")

with cover_col:
    res = st.session_state.get("cover")
    if res:
        st.markdown("##### Cover Letter")
        for p in res["problems"]:
            st.warning(f"Rule check: {p}")
        st.download_button(
            "Download .docx",
            res["docx"],
            file_name=res["name"],
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            key="cover_dl",
        )
        st.caption(f"Also saved to {res['saved']}")
        with st.expander("Preview", expanded=False):
            st.markdown(f"**{res['data']['re_line']}**")
            for para in res["data"]["paragraphs"]:
                st.write(para)
