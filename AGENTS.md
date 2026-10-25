---
framework_version: 1.0.1
---

# Agent Guidelines: AI Job Search

This workspace is structured to manage job search activities, scraper tools, CVs, cover letters, and interview preparation across AI agent runtimes, with primary support for **Google Antigravity / Google Gemini** and **Claude Code**.

## Thin-Pointer Design (Single Source of Truth)

To prevent duplication and configuration drift across different AI agent frameworks (Google Antigravity, Google Gemini, Claude Code, Cursor, Codex, etc.), this workspace uses a unified thin-pointer design:

1. **Personal Candidate Profile:**
   - When running under Google Antigravity / Gemini: defined in [GEMINI.md](GEMINI.md) and the methodology files under [.claude/skills/job-application-assistant/](.claude/skills/job-application-assistant/).
   - When running under Claude Code: defined in [CLAUDE.md](CLAUDE.md). Both files remain synchronized during `/setup`.
2. **Canonical Workflow Specifications:**
   - Antigravity native skills live under [.agents/skills/](.agents/skills/) (e.g. `setup`, `scrape`, `apply`, `rank`, `interview`, `outcome`, `upskill`, `html-report`, `reset`). Antigravity discovers these automatically.
   - Claude Code command markdown files live under [.claude/commands/](.claude/commands/) and [.claude/skills/](.claude/skills/).
3. **Portal Search Skills:**
   - Job-portal search CLIs live under [.agents/skills/*-search/](.agents/skills/) in the portable Agent Skills format (with a `SKILL.md` per portal). Antigravity and other agent engines discover and run these tools via Bun.

