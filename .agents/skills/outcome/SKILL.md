---
name: outcome
description: >-
  Record application status updates (interviews, offers, rejections) and manage follow-ups.
  Triggers on: /outcome, outcome, record outcome, interview status, follow up, application status.
---

# /outcome - Application Status Tracking & Follow-up

Updates application status in `job_search_tracker.csv` and `outcome.md`, drafts personalized follow-up emails, and feeds calibration back into the evaluation framework.

---

## Subcommands & Options

- **`/outcome <company>`**: Update stage (e.g. `screening`, `technical_round`, `hired`, `rejected`).
- **`/outcome followup`**: Scan open applications that have been quiet for 10+ days and draft concise, professional check-in notes.
