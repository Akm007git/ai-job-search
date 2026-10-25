---
name: rank
description: >-
  Batch-score newly scraped job postings against the candidate fit framework to produce
  a prioritized shortlist. Identifies strengths, gaps, deal-breakers, and deadlines.
  Triggers on: /rank, rank, rank jobs, score postings, shortlist jobs.
---

# /rank - Batch Job Scoring & Shortlisting

Bridges `/scrape` and `/apply` by evaluating all newly discovered job postings against your profile in `GEMINI.md`.

---

## Workflow

1. **Load Unscored Postings**:
   Read unseen postings from `job_scraper/seen_jobs.json` via `tools/rank_state.py`.
2. **Evaluate Fit Dimensions**:
   For each posting, evaluate:
   - Skills Match (GenAI, RAG, LangChain/LangGraph, Python, System Design)
   - Experience Match
   - Location & Work Mode (Bangalore / Remote / Hybrid)
   - Deal-breakers & Urgency / Deadline
3. **Generate Ranked Table**:
   Present ranked results with rank number, title, company, location, fit score, deadline, and key strengths/gaps.
4. **Handoff**:
   Prompt the user to select any role by number to trigger `/apply`.
