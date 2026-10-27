import html

import streamlit as st

from core import ui
from core.ai_client import AIError
from core.fit_review import LABEL_HELP, WEIGHTS, review
from core.jd_fetcher import fetch_jd

ui.setup("Fit Review", "🎯")
st.title("Fit Review")

legend_rows = "".join(
    f"<div style='margin-bottom:0.35rem'><span class='cc-badge {label}' style='font-size:0.75rem;padding:0.15rem 0.6rem'>{label}</span> "
    f"<span class='cc-muted' style='font-size:0.78rem'>{html.escape(help_text)}</span></div>"
    for label, help_text in LABEL_HELP.items()
)
st.markdown(
    f"<div class='cc-legend'><div style='font-weight:700;margin-bottom:0.4rem;color:var(--cc-primary)'>"
    f"What do the scores mean?</div>{legend_rows}</div>",
    unsafe_allow_html=True,
)

profile = ui.profile_panel()

url = st.text_input("Job posting URL (optional)")
if st.button("Fetch from URL", disabled=not url.strip()):
    text = fetch_jd(url.strip())
    if text:
        st.session_state["fit_paste"] = text
        st.success("Fetched the page. Check the text below and trim anything that isn't the JD.")
    else:
        st.error("Could not read this page. Please paste the JD text.")

jd = st.text_area("Job description", height=260, key="fit_paste").strip()

if st.button("Review Fit", type="primary", disabled=not (jd and profile)):
    with st.spinner("Reviewing fit..."):
        try:
            st.session_state["fit"] = review(profile, jd)
            st.session_state["jd"] = jd
            st.session_state.pop("resume", None)
            st.session_state.pop("cover", None)
        except AIError as e:
            st.error(str(e))

fit = st.session_state.get("fit")
if fit and st.session_state.get("jd"):
    e = html.escape
    who = " at ".join(e(x) for x in (fit.get("position"), fit.get("company")) if x)
    strengths = "".join(f"<li>{e(s)}</li>" for s in fit.get("strengths", []))
    gaps = "".join(
        f"<li>{e(g.get('text', ''))} <span class='cc-muted'>({e(g.get('type', ''))} gap)</span></li>"
        for g in fit.get("gaps", [])
    )
    subs = " · ".join(f"{k.replace('_', ' ').title()} {fit['subscores'][k]}/{cap}" for k, cap in WEIGHTS.items())
    label_help = e(LABEL_HELP.get(fit["label"], ""))
    st.markdown(
        f"""<div class='cc-card'>
        <div class='cc-score'><span class='cc-score-num'>{fit['score']}</span>
        <span class='cc-badge {fit['label']}'>{fit['label']}</span></div>
        <p class='cc-muted'>{label_help}</p>
        <div><b>{who}</b>{' · ' + e(fit['pay_range']) if fit.get('pay_range') else ''}</div>
        <p class='cc-muted'>Score breakdown: {subs}</p>
        <p>{e(fit.get('summary', ''))}</p>
        <b>Strengths</b><ul>{strengths}</ul>
        <b>Gaps</b><ul>{gaps}</ul>
        </div>""",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    if c1.button("Build Resume / Cover Letter", use_container_width=True):
        st.switch_page("pages/2_Resume_and_Cover_Letter.py")
    if c2.button("Add to Tracker", use_container_width=True):
        st.switch_page("pages/5_Job_Tracker.py")
