---
name: scrape
description: >-
  Search installed job portals (LinkedIn, regional job boards, and custom portals) matching
  your configured candidate profile. Deduplicates across runs and highlights fit scores.
  Triggers on: /scrape, scrape, scrape jobs, find jobs, search jobs, new jobs, job search.
---

# /scrape - Automated Job Portal Search

Searches job portals using the **installed portal-search CLIs** in `.agents/skills/` (and WebSearch as fallback), matching roles against your candidate profile configured in `GEMINI.md`.

---

## Invocation

Trigger phrases:
- `/scrape`
- `/scrape data science` (focus area)
- `/scrape broad` (run all search categories)
- `/scrape health` (probe installed portal CLIs without scraping)

---

## Workflow Steps

### Step 0: Load Profile & Search Queries
1. Read `.claude/skills/job-scraper/search-queries.md` for prioritized queries and location filters.
2. Deduplication is handled via `.venv/bin/python tools/scrape_state.py`; do not dump large raw tracker files into conversation context.

### Step 1: Run Portal CLIs
Run portal searches using `bun`:
- **LinkedIn Search** (global / country-agnostic):
  ```bash
  bun run .agents/skills/linkedin-search/cli/src/cli.ts search --location "<your_location>" --query "<query>" --jobage 14 --format json
  ```
- **Freehire Search**:
  ```bash
  bun run .agents/skills/freehire-search/cli/src/cli.ts search [flags]
  ```
- Any regional portals enabled in `.agents/skills/<portal>/SKILL.md` (e.g. `jobindex-search`, `jobnet-search`, etc.).

If `bun` is unavailable or for portals without CLIs, fall back to WebSearch queries.

### Step 2: Deduplication & Integrity
1. Pass raw hits through `tools/job_key.py` and `tools/scrape_state.py` to filter out previously seen postings in `job_scraper/seen_jobs.json` or tracked applications in `job_search_tracker.csv`.
2. Verify URLs and check deadline dates.

### Step 3: Present Matches
Format newly discovered jobs in a clean Markdown table:
- **Title & Company**
- **Portal / Location**
- **Quick Fit Estimate** (Strong / Moderate / Borderline)
- **Posting URL**

Offer immediate handoff:
- *"Say `/apply <url>` on any of these positions to evaluate fit and generate your tailored CV and cover letter, or `/rank` to batch-score the entire shortlist."*
