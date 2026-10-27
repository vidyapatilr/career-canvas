# CareerCanvas

A personal Streamlit app that turns a job description into an honest fit review, a tailored resume, and a tailored cover letter, all grounded in the master profile. It also tracks applications in a local SQLite database.

## Run it

```bash
uv sync
uv run streamlit run app.py
```

Then open http://localhost:8501.

## Configuration (.env)

| Key | Purpose |
|---|---|
| `OPENROUTER_API_KEY` | Required. OpenRouter key for the AI calls. |
| `CONTACT_EMAIL`, `CONTACT_PHONE` | Used in the resume and cover letter headers. |
| `OPENROUTER_MODEL` | Optional. Defaults to `anthropic/claude-sonnet-4.6`. |
| `RESUME_OUTPUT_DIR` | Optional. Where a copy of each .docx is saved, one folder per employer. Defaults to `~/Resume`. |

## Pages

1. **Fit Review**: paste a JD (or fetch it from a URL) and get a 0 to 100 score with strengths and gaps.
2. **Resume Builder**: generates a tailored .docx resume with `scripts/build_docx.py`.
3. **Cover Letter**: generates a tailored .docx cover letter.
4. **Profile**: view or replace the master profile (stored at `data/master_profile.md`, seeded from `references/` on first run).
5. **Job Tracker**: add, edit, delete, and export applications (`data/tracker.db`).

Writing rules are in `core/rules.py`. They go into every prompt and are checked in code after generation; a failed check triggers one retry, then a warning in the app.

## Tests

```bash
uv run pytest
```
