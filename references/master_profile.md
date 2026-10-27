# Vidya Rani Patil — Master Career Profile

This is the single source of truth for building Vidya's resumes and cover letters. Every fact here is verified — pulled from her existing resumes or stated directly by her. **Only use facts from this file, or facts the user states explicitly in the current conversation.** Never add anything else, no matter how well it would match a job description.

If the user gives you a new true fact about her background during a conversation (a certification, a project detail, an audit she supported, etc.), add it to the right section below before you finish, so future runs have it without re-asking.

## Contact
Vidya Rani Patil
Winter Park, FL
{{CONTACT_PHONE}}
{{CONTACT_EMAIL}}
LinkedIn: https://www.linkedin.com/in/vidyapatilr/
GitHub: https://github.com/vidyapatilr — worth including on resumes for AI/LLM-adjacent QA roles. Two original (non-forked) repos are directly relevant proof points: "agentaudit" (evals, guardrails, and observability for a real LLM agent — Python, OpenAI, Arize Phoenix) [confirmed 2026-10-22: agentaudit includes a golden dataset, guardrail tests, and hallucination tests] and "loop-engineering" (agent-loop debugging with Claude/GPT-4). A third, "ai-agents," includes an API test generator. Most of her other repos are forks of courses/tutorials, not original work — don't cite those as accomplishments.
**Important precision on Arize Phoenix: she learned it in an AI course and used it in the personal "agentaudit" project — she did NOT use Arize at Hitachi Vantara.** Her Hitachi Vantara observability work was a custom monitoring skill she built herself for token/cost/latency tracking (see that job's bullets below) — cite that as the professional-experience observability evidence, and Arize/agentaudit separately as course-learned/personal-project evidence. Don't conflate the two or imply Arize was used on the job.

## Work Experience (reverse chronological)

Each role lists the full pool of real, verified accomplishments. Pick and reword the subset that's relevant to a given JD — using the JD's own terminology where it *honestly* describes what she did — but never invent an accomplishment that isn't in this list, and never claim a tool/standard/methodology she didn't actually use.

### Sr. QA Engineering Specialist – Professional — Hitachi Vantara — Nov 2018 – Jul 2026
Validated the Pentaho ETL platform — a data-integration tool used by enterprise clients — across cloud and on-premises environments (AWS, GCP, Hadoop, Oracle, PostgreSQL). Later led a focused initiative bringing agentic AI into the team's testing practice. **Presentation note: always show this as a single role ending Jul 2026 — do not split out the Leo Group/Pentaho acquisition as a separate entry.**
- Managed a team of 4 software testers: hiring, onboarding, assigning and reviewing their work, and mentoring — genuine people-management experience, not just informal/technical leadership. Use this to speak directly to "team/staff management" requirements in a JD; it's a small team, so don't inflate it into "enterprise QA organization" leadership unless the JD's bar is modest.
- Redesigned the ETL test-case architecture and tightened requirements traceability, cutting the defect escape rate by about 35%.
- Automated Docker-based test-environment provisioning across six-plus database and OS configurations, eliminating 80+ hours of manual setup per month and enabling parallel test execution.
- Led the team's agentic AI strategy: evaluated multiple LLMs (Claude Sonnet, Claude Opus, Gemini Pro, GPT-5.5) before selecting Claude Sonnet 4.6 as the production model for the team's agent workflows.
- Built agents to monitor cluster and database health.
- Built a Text-to-SQL agent that accepted a natural language goal, generated SQL, and queried the MySQL database to retrieve release and build version information on demand.
- Built an agent that used the existing codebase as context to generate Pentaho Spoon jobs and transformations for testing, cutting manual test-prep time. This was specifically for generating ETL test artifacts — not a general-purpose test-case generator and not database-related.
- Built a custom monitoring skill to track token utilization, cost, and latency across agent workflows as part of ongoing model evaluation.
- Designed a multi-agent workflow with constraints and guardrails built in, where a second agent validated the first agent's output using in-script validations. **Precision note (stated by Vidya 2026-10-22): she described it as a deterministic multi-agent workflow. Never call it "non-deterministic" testing. Do not claim golden datasets or scoring rubrics at Hitachi; those are from agentaudit.**
- How the Hitachi agents were built: AI-assisted Python development ("vibe coding"). The AI generated the Python; she reviewed the code and it ran for the team. She did NOT use Langflow for these agents. **Say "built agents through AI-assisted Python development" or similar; never "wrote Python from scratch" or claim strong Python coding.** (Stated by Vidya 2026-10-22.)
- Partnered with development, support, and vendor teams to triage, root-cause, and resolve defects in JIRA, improving mean time-to-resolution by around 40%.
- Implemented TestNG and Maven regression suites within the Jenkins CI/CD pipeline as release-validation quality gates, compressing the release validation window from three weeks to six days. **Precision note (stated by Vidya 2026-10-22): she did NOT write the Java test code. She ran and consumed existing TestNG suites and used them as Jenkins quality gates. Say "ran" or "integrated" TestNG/Maven suites as Jenkins quality gates; never "built", "wrote", or "developed" them, and do not claim Java coding.**
- Used TestRail for test-case management and execution tracking for about 5 years of this role, then transitioned the team to PractiTest for continued test-case management and defect tracking.
- Worked within Agile/Scrum sprint teams at both Hitachi Vantara and LexisNexis — participated in sprint planning, backlog refinement, daily standups, and retrospectives. Comfortable with Agile ceremonies and iterative delivery cadences.
- Tested Pentaho ETL pipelines that connected to Salesforce as a data source — validating data ingestion and transformation from Salesforce into downstream systems. Basic hands-on familiarity with Salesforce in a data integration context; not deep Salesforce admin/configuration knowledge.
- Used Confluence as a system of record alongside JIRA for over 8 years — comfortable, day-to-day proficiency, not a passing exposure.
- Attended go/no-go release meetings and had direct visibility into the release decision process; understands what the criteria and tradeoffs involve, though was not a voting decision-maker on the call. **Precision note: she understood the process and was present — do not phrase this as "drove" or "led" release decisions; say "participated in" or "attended" go/no-go meetings at most.**
- Tested Kafka services as part of Pentaho testing at Hitachi Vantara: set up a Dockerized Kafka environment to produce and consume messages, and connected it to Pentaho to test Kafka integration. **Precision note: limited hands-on exposure in a Pentaho context, not deep Kafka or event-driven architecture expertise. Say "set up a Dockerized Kafka environment to produce and consume messages and tested Pentaho's Kafka integration"; do not claim Kafka administration, event-driven test design, or streaming-platform expertise.** (Added 2026-10-22, stated by Vidya.)
- Tested REST APIs manually with Postman: built and sent requests to service endpoints and checked the responses. **Precision note: hands-on, working-level API testing in Postman, not a deep specialty. Do not claim API test automation frameworks (RestAssured, PyTest API suites, Newman in CI), contract testing, or microservices test architecture. Say "tested REST APIs with Postman" or "manual REST API testing in Postman." Employer attributed to Hitachi Vantara because she confirmed it in answer to a question about her day job; confirm with her if a JD needs a different attribution.** (Added 2026-10-22, stated by Vidya.)
- Tested Pentaho connecting to Azure and AWS cloud environments. On Azure: uploaded test files to Azure Storage, then validated Pentaho connecting to Azure to read and write those files. **Precision note: cloud testing in a Pentaho integration context; do not claim Azure/AWS administration, infrastructure-as-code, or cloud certifications. The Azure service is Azure Storage (file read/write); do not name other Azure services.** (Added 2026-10-22, stated by Vidya.)
- Used OpenTelemetry to capture logs from Pentaho: the Pentaho web app was hosted in a Docker container with OpenTelemetry collecting the logs for each build, so the team could trace errors. **Precision note: log collection with OpenTelemetry for error tracing; do not claim distributed tracing, metrics dashboards, or Datadog.** (Added 2026-10-22, stated by Vidya.)
- Performed security/authentication testing for login systems using LDAP and CAS (Central Authentication Service), including setting up test logins for Pentaho.
- Performed manual performance testing. **Precision needed here: this was manual, not tool-based — she did not use JMeter or a similar automated performance-testing tool. Don't claim "performance testing tools" or name JMeter; say "manual performance testing" specifically.**
- Used SQL as part of ETL testing — querying Oracle, PostgreSQL, and MySQL databases to verify data transformations, validate source-to-target data flow, and confirm data integrity across pipeline stages. Also used for database connectivity verification and test environment configuration. **Precision note: this is ETL/pipeline validation SQL, not analytical/reporting SQL or complex aggregation queries — frame it as data verification for ETL testing, which is accurate.**
Software/Tools: IntelliJ, Maven, TestNG, GitHub, Oracle, PostgreSQL, MySQL, Linux, Hadoop, AWS, Azure, GCP, OpenTelemetry (log capture), Python, JIRA, Confluence, Jenkins, Docker, PractiTest, TestRail, LDAP, CAS, Salesforce (ETL data source), Kafka (Pentaho context, limited), Postman (REST API testing), GitHub Copilot, Langflow, Anthropic Claude, OpenAI

### Sr. Quality Test Engineer — LexisNexis Risk Solutions — Aug 2016 – Nov 2018
Data quality at scale — processing large volumes of records where manual QA couldn't keep pace. Introduced ML-based validation and automated analytics.
- Developed ARIMA and SVM (Support Vector Machine) statistical models to automate data-distribution and accuracy checks — structured, data-driven / risk-based anomaly detection — cutting manual QA effort by about 60%.
- Identified three systemic data-accuracy issues during requirements and integration test analysis, preventing them from becoming high-severity production incidents (root-cause investigation and corrective action).
Software/Tools: HPCC, ECL, Python, R, SQL, Oracle, Linux, HP ALM, JIRA

### Systems Process Analyst — Orlando Health — Nov 2013 – Aug 2016
Worked on the Data Warehousing team at a healthcare system managing clinical data across multiple sites; made the ETL and reporting infrastructure more reliable within a regulated healthcare-data environment.
- Led ICD-9 to ICD-10 migration testing across every clinical system — a federally mandated change touching 100% of patient records — delivered on time with no data-integrity issues.
- Built an Infection Control dashboard in OBIEE with drill-down capability into specific numbers for each kind of infection, replacing manual unit-by-unit monitoring across the whole system and saving 20+ hours a week.
**Note: the old "worked with clinical trials data as part of a regulated, multi-site healthcare system" bullet was cut — it was vague filler (no action, no result) once split out on its own. The Data Warehousing team detail now lives in the intro line instead. Don't re-add a standalone version of that line unless there's a concrete action/result to attach to it.**
Software/Tools: OBIEE, ETL Testing, Data Warehousing, Star Schema, Allscripts Sunrise, SQL, QlikView

### Programmer/Analyst — Population Health Research Institute (PHRI), McMaster University — Jun 2003 – Feb 2008
First hands-on clinical-EDC-system experience, supporting a large clinical-trials organization running multi-center cardiovascular trials on the DataFax platform (conceptually similar to modern EDC systems like Veeva CDMS/Rave).
- Administered the DataFax clinical EDC system across production and test environments, sustaining reliable data capture for international multi-center cardiovascular trials under Good Clinical Practice (GCP) and CFR Part 11 requirements.
- Audited clinical research records for data consistency and regulatory integrity across trial sites.
- Supported FDA and pharmaceutical sponsor audits directly; authored SOPs for quality auditing of clinical research records.
- Earned Certified Clinical Research Associate (CCRA) certification (a 15-credit program) during this role, 2004–2006.
- Sole system administrator for DataFax: responsible for keeping the system up and running, user administration (adding users), and completing system testing (confirmed by Vidya 2026-10-22).
- Personally executed and documented SOP-governed testing under FDA compliance testing protocols, and wrote and signed many SOPs. She cannot recall whether this was formally called CSV, so do not claim CSV, IQ/OQ/PQ, or 'validated GxP systems' by name.
- Implemented the MedDRA dictionary in DataFax by writing a Perl script.
- Was part of the compliance auditing process.
- Number of countries/sites covered during her tenure is unknown; say 'international'. PHRI's current scope (55 countries, many therapeutic areas) is today's, not hers.
Software/Tools: DataFax Clinical EDC, PERL, Shell Scripting, Oracle, PL/SQL, Linux, Good Clinical Practice (GCP) Standards

### Earlier Experience
- **QA Tester — CheckFree i-Solutions** (Jun 2000 – Jul 2002): Tested financial databases for integrity during outage events; rolled out Rational ClearQuest for defect management and regression testing.
- **Programmer/Database Analyst — IDS InfoTech Limited, India** (Jan 1998 – Apr 1999): Y2K consultant for SmithKline Beecham (UK), testing PCs, software, and lab instruments for Year 2000 compliance.

## Projects (personal / hackathon — not employment)
- **FindMyTrial** — built for the Lovable SheBuilds Season 04 Hackathon (Oct 2026), her first Lovable (low-code/no-code) build, in 72 hours. Live app: https://plain-speak-trials.lovable.app/ (include this link whenever the project appears on a resume). Lets people search public ClinicalTrials.gov listings in plain English: enter a condition and ZIP code to see nearby studies with easy-to-read summaries, age and gender filters, contact details, and suggested questions for the care team. Summaries are kept tied to what the official listing says; not medical advice. She plans to take it to production (multi-language, international trials, email alerts). Good evidence for low-code/no-code requirements; weak for hands-on automation-framework/API-testing JDs. Don't claim AI/LLM features in it unless she confirms them.
  - She planned and designed the whole product herself and built it through prompts (prompt-driven development); finishing a deployed product in 72 hours is a key signal to keep. Do not call it 'low code' on resumes (2026-10-22).
  - She is continuing to build FindMyTrial out for real-world public release (stated 2026-10-22); date it 'Oct 2026 – Present'. It is not just a prototype: she is in talks with a few people to publish it as a real product on web and mobile apps. Don't call it 'commercial' unless she confirms.

## Education & Certifications
**On a resume, list these most-recent-first (by completion year) — not grouped by degree-vs-certification, not oldest-first. This has been gotten wrong before; double-check the ordering before saving a resume.**
- AI Evals for Everyone — LevelUp Labs, via Maven, completed 7/4/2026 (Certificate ID 2LALOO-CE000925)
- Building Agentic AI Applications with a Problem-First Approach — LevelUp Labs, via Maven (2026): agentic workflows, RAG, MCP servers, prompt/context engineering, evals, workflow tracing
- Become an Agent-Native Operator — OpenClaw Automation, via LevelUp Labs on Maven (2026)
- M.S. in Data Science — Indiana University, Bloomington (2016–2018); coursework: Hadoop, Python, R, Tableau, Statistics, Visualization, Social Media Mining, Algorithms
- B.S. in Health Informatics & Information Management — University of Central Florida (2013–2015)
- A.A. — Valencia College (2009–2012)
- Certified Clinical Research Associate (CCRA) — McMaster University (2004–2006)

## What she does NOT have (do not claim any of these)
- No degree in chemistry, materials science, chemical engineering, polymer science, or biochemistry — do not position her for materials-characterization/formulation-science roles.
- No hands-on experience with IEC 62304, 21 CFR 820, ISO 13485, ISO 14971, IEC 82304, or EU MDR (medical-device software/QMS regulatory standards). Her regulated-environment experience is Good Clinical Practice (GCP) and CFR Part 11 from clinical-research work at PHRI, which is a genuinely different regulatory pathway than medical-device software — real experience, but do not conflate the two.
- No experience with Software Hazard Analysis (SHA), design FMEA/DFMEA/PFMEA, Design History Files, or literal CAPA within a medical-device quality system.
- No direct experience interacting with FDA or notified bodies as a device manufacturer (her FDA exposure was as a clinical-trials-org employee supporting sponsor/FDA audits, not as device-company QA).
- No ASQ CSQE certification (as of this writing) — she was considering pursuing it; check with her before assuming she has it.

## Standing rules on how to write her resumes/cover letters

These live in full in `SKILL.md` (same directory) and in this session's memory (`vidya_resume_context.md`) — read those for the complete, current rules (fabrication, years-of-experience, gap handling, per-JD rewording, etc.). Don't duplicate them here; a stale copy in a second place is how the old "disclose gaps in the cover letter" rule almost got reintroduced after it was corrected. This file's job is facts, not process rules.
