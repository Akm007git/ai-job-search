---
name: apply
description: >-
  Evaluate job fit and generate tailored CV and cover letter in LaTeX for a specific job posting.
  Runs security integrity checks, fit scoring, two-pass review, PDF compilation, and ATS text extraction.
  Triggers on: /apply, apply, apply to job, tailor CV, draft cover letter.
---

# /apply - End-to-End Job Application Workflow

Orchestrates the fit evaluation, CV tailoring, and cover letter generation pipeline for a specific job posting (URL or pasted text) inside **Google Antigravity** using **Google Gemini**.

---

## Step 0: Input Parsing & Security Integrity
1. **URL input**:
   - Check if the URL belongs to an installed portal CLI in `.agents/skills/*-search/` (e.g. LinkedIn). If so, fetch via:
     ```bash
     bun run .agents/skills/<portal>/cli/src/cli.ts detail "<url>" --format plain
     ```
   - Otherwise, fetch via WebFetch or `.venv/bin/python tools/fetch_page.py "<url>"`.
2. **Text input**:
   - Save text to scratchpad and run `.venv/bin/python tools/posting_guard.py --in <scratchpad>/posting.txt --text --json`.
3. Extract: Company name, job title, department, location, application deadline, and required skills.

---

## Step 1: Fit Evaluation
Evaluate posting against candidate profile in `GEMINI.md` and `.claude/skills/job-application-assistant/04-job-evaluation.md`:
- **Skills Match**: Core GenAI / Agentic stack (LangChain, LangGraph, RAG, MCP, Vector DBs, Python, Full-Stack) vs requirements.
- **Experience Match**: Real achievements from `GEMINI.md` and `01-candidate-profile.md`.
- **Behavioral & Culture Match**: Team dynamics, autonomy, system design approach.
- **Overall Score**: Strong / Moderate / Borderline fit.

Present the evaluation to the user before drafting.

---

## Step 2: Draft Tailored CV & Cover Letter
1. **CV (`cv/main_<company>_<role>.tex`)**:
   - Adapt `cv/main_example.tex` using the `moderncv` banking template.
   - Tailor the professional summary to highlight relevance to this specific role.
   - Highlight the most relevant experience and projects (e.g. Enterprise RAG, MCP AI Agents, LangGraph workflows).
   - Ensure strictly truthful claims grounded in `GEMINI.md` (no fabricated metrics or tools).
2. **Cover Letter (`cover_letters/cover_<company>_<role>.tex`)**:
   - Adapt `cover_letters/cover.cls` template.
   - Address to Hiring Manager / Recruiter.
   - Structure: Opening hook -> Why this company & role -> Proven relevant impact -> Forward-looking alignment -> Call to action.

---

## Step 3: Reviewer Audit
Audit drafts against:
- **Factual Grounding**: Every skill, tool, company, and achievement exists in candidate profile.
- **Targeting**: Specifically addresses the posting's core requirements.
- **Format**: CV is exactly 2 pages; cover letter is exactly 1 page.
- **AI Tooling Reference**: References **Google Gemini** / **Antigravity** when discussing agentic workflows and AI pair programming.

---

## Step 4: PDF Compilation & ATS Verification
1. **Compile**:
   ```bash
   export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
   cd cv && lualatex -interaction=nonstopmode -halt-on-error main_<company>_<role>.tex
   cd ../cover_letters && xelatex -interaction=nonstopmode -halt-on-error cover_<company>_<role>.tex
   ```
2. **ATS Text Extraction**:
   ```bash
   .venv/bin/python tools/verify_pdf.py cv/main_<company>_<role>.pdf --dump-text cv/main_<company>_<role>.txt
   ```
   Verify contact info, reading order, and keyword presence.

---

## Step 5: Archive & Update Tracker
1. Archive application files into `documents/applications/<company>_<role>/`.
2. Append a record to `job_search_tracker.csv` with status `applied`.
