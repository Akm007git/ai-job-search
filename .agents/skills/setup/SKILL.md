---
name: setup
description: >-
  Onboard and configure your professional candidate profile for the AI Job Search framework.
  Reads documents folder, imports CVs, or runs an interactive interview.
  Triggers on: /setup, setup profile, build profile, configure profile, update profile.
---

# /setup - Candidate Profile Onboarding

You are running the onboarding setup for the AI Job Search framework inside **Google Antigravity** powered by **Google Gemini**. Your goal is to collect the user's professional information and populate all profile files so the `/apply` and `/scrape` workflows work out of the box.

There are three paths into setup. Step 0 picks the right one; all three converge on Step 3 (file generation) and Step 4 (confirmation).

---

## Step 0: Welcome & Choose Path

If arguments contain `--section <name>`, skip directly to that section in Path C for an update-only flow.

Otherwise:
1. Scan the `documents/` folder (`documents/**/*`) and count files per subfolder (`cv/`, `linkedin/`, `diplomas/`, `references/`, `projects/`, `applications/`).
2. Welcome the user with a single message offering the three paths:
   - **Path A: Documents folder** (Recommended if documents are present) - Reads `documents/`, cross-references materials for consistency, and extracts profile data.
   - **Path B: Single CV import** - Paste or @-mention a single CV/resume. Extracts it and asks targeted follow-ups for any missing fields.
   - **Path C: Interview mode** - Walks through structured questions section by section. Ideal when starting from scratch.

---

## Step 1: Data Collection

Collect information across:
1. **Identity & Location**: Full name, contact email, phone, location (city, country), commute/relocation preferences, languages spoken and proficiency levels, and preferred CV language.
2. **Education**: Degrees, institutions, graduation years, thesis topics, honors.
3. **Professional Experience**: Roles, companies, dates, key responsibilities, quantifiable achievements (metrics, scale, impact).
4. **Technical Skills**: Primary skills (core stack), secondary skills, domain expertise, tools & software.
5. **Certifications, Publications & Awards**: Formal credentials, papers, hackathons.
6. **Behavioral Profile**: Work style, thriving environments, team collaboration, decision-making style.
7. **Career Goals & Preferences**: Target roles, industries, exciting topics, deal-breakers, salary expectations.
8. **Job Search Configuration**: Role titles for `/scrape`, distinctive keywords, geographic scope, and enabled job portals.

---

## Step 2: Generate & Synchronize Profile Files

When data collection is complete, update:
1. **`GEMINI.md`**: Replace all `[PLACEHOLDER]` tokens with the candidate's actual profile data.
2. **`CLAUDE.md`**: Keep in sync with `GEMINI.md` so the profile is portable across runtimes.
3. **`.claude/skills/job-application-assistant/01-candidate-profile.md`**: Full structured profile.
4. **`.claude/skills/job-application-assistant/02-behavioral-profile.md`**: Behavioral profile.
5. **`.claude/skills/job-application-assistant/04-job-evaluation.md`**: Match criteria and evaluation rules.
6. **`.claude/skills/job-application-assistant/05-cv-templates.md`**: Role-specific profile statements and contact info.
7. **`.claude/skills/job-application-assistant/06-cover-letter-templates.md`**: Personal contact line and signature.
8. **`.claude/skills/job-application-assistant/07-interview-prep.md`**: STAR examples.
9. **`cv/main_example.tex`**: Personalize with real name and contact details.
10. **`.claude/skills/job-scraper/search-queries.md`**: Personalized search queries for `/scrape`.

---

## Step 3: Confirm & Next Steps

Summarize the updated files and suggest next steps:
- Run `/scrape` to discover open jobs matching the newly configured profile.
- Run `/apply <url>` to test the fit evaluation, CV tailoring, and cover letter generation pipeline.
