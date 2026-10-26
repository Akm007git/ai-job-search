<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Pip, the courier bird" width="200">
</p>

# AI Job Search & Application Assistant

*The intelligent, autonomous job application framework that runs locally on your machine.*



An enterprise-grade, agentic job application assistant built natively for **[Google Antigravity](https://github.com/google)** and powered by **Google Gemini** (with multi-agent support for Claude Code). 

> **100% Free & Open-Source**: You do **not** need a paid Claude Code subscription to use this repository! Anyone on GitHub can clone this workspace, connect it freely to **Google Gemini** inside the **Google Antigravity IDE**, and automate their entire job search pipeline:
> - **24-Hour Multi-Portal Job Scraping** (LinkedIn, Instahyre, Naukri 24h Live Hub)
> - **Automated Daily Morning Email Delivery** with formatted Excel spreadsheets attached directly to your personal Gmail
> - **Autonomous 1-Command Job Tailoring (`/apply`)**: Fit scoring, 2-page LaTeX CV, 1-page Cover Letter, and ATS verification
> - **Salary Benchmarking & Offer Hike Analysis** (`salary_lookup.py`)
> - **Stage-Specific Interview Preparation Packages** (`/interview`)

---

## Table of Contents
1. [Core Capabilities & Features](#core-capabilities--features)
2. [Prerequisites](#prerequisites)
3. [Quick Start & Installation Guide](#quick-start--installation-guide)
4. [Setting Up Daily Gmail Automation](#setting-up-daily-gmail-automation)
5. [Core Workflows & How to Use Them](#core-workflows--how-to-use-them)
6. [Salary Benchmark & Offer Analysis](#salary-benchmark--offer-analysis)
7. [Repository Folder & File Structure](#repository-folder--file-structure)
8. [Troubleshooting & FAQ](#troubleshooting--faq)
9. [License & Acknowledgements](#license--acknowledgements)

---

## Core Capabilities & Features

```
+-----------------------------------------------------------------------------------+
|                            AI JOB SEARCH PIPELINE                                 |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ 1. Multi-Portal Scraping ]          [ 2. Daily Email Automation ]              |
|   LinkedIn + Instahyre + Naukri  --->   Twice Daily: 10:00 AM & 8:00 PM to Gmail   |
|   Last 24 hours, Bangalore & Kolkata    HTML Digest + Multi-Tab Excel Workbook     |
|                                                                                   |
|  [ 3. Job Evaluation & Ranking ]       [ 4. 1-Command Tailoring (/apply) ]        |
|   0-100 Fit Scoring across 5 dims --->  Tailored 2-Page CV (LaTeX moderncv)       |
|   Eligibility & Language Gates          Tailored 1-Page Cover Letter (LaTeX)      |
|                                         Reviewer Audit + ATS Keyword Verification |
|                                                                                   |
|  [ 5. Salary Benchmarking ]            [ 6. Interview Preparation (/interview) ]  |
|   Baseline: 11 LPA | Target: 17-18+ LPA Company Research, STAR Stories,          |
|   Instant offer hike calculator         Technical talking points, Mock Interview   |
+-----------------------------------------------------------------------------------+
```

### 1. 24-Hour Multi-Portal Job Scraper
- **Target Roles**: AI Engineer, Generative AI Engineer, Software Engineer, Software Developer.
- **Locations**: Bangalore, Kolkata (Hybrid, Onsite, Remote).
- **LinkedIn Engine**: Scrapes guest job feeds posted in the last 24 hours using the zero-dependency `linkedin-search` CLI tool.
- **Instahyre Engine**: Queries real-time Indian tech postings with curated skill tags.
- **Naukri 24h Live Hub**: Generates direct 1-click pre-filtered search queries for all target roles and cities that bypass aggressive Akamai bot protection.
- **Multi-Tab Excel Spreadsheet**: Generates formatted `.xlsx` and `.csv` files with urgency flags, category tabs, and direct apply links.

### 2. Automated Daily Gmail Dispatch
- Automatically runs the scraper every morning and dispatches an executive email to your personal Gmail.
- Displays the **Top 10 High-Priority Postings** with instant 1-click **Apply on LinkedIn** buttons.
- Features interactive **Naukri 24h Live Hub** buttons to open live searches in one click.
- Attaches the complete `jobs_multi_portal_bangalore_kolkata_last_24h.xlsx` workbook directly to your inbox so you can review and apply on the go from your phone or desktop.
- Runs twice daily (**10:00 AM Morning Digest** and **8:00 PM Evening Application Reminder**) either via **GitHub Actions in the cloud (runs even when your computer is off, 100% free)** or via local background services.

### 3. Autonomous 1-Command Tailoring (`/apply <url-or-text>`)
- Paste any job URL or raw text description.
- **Integrity Gate**: Scans for prompt injections, hidden instructions, or malicious payloads in the job posting.
- **Fit Scoring**: Evaluates the role against your profile across 5 dimensions: Technical Skills, Experience Match, Cultural Fit, Location/Logistics, and Career Motivation.
- **LaTeX ModernCV Generation**: Generates an exact 2-page, ATS-optimized CV (`moderncv` banking style).
- **LaTeX Cover Letter Generation**: Generates a compelling, forward-looking 1-page cover letter (`cover.cls`).
- **Autonomous Reviewer Agent**: Spawns a secondary agent to research the company, verify facts, critique phrasing, and eliminate hallucinations.
- **ATS & PDF Verification**: Runs `verify_pdf.py` to confirm exact page counts, readable text layers, and ATS keyword extraction.
- **Automatic Archival**: Saves final PDFs and records into `documents/applications/<company>_<role>/` and logs the application into `job_search_tracker.csv`.

### 4. Salary Benchmark & Offer Hike Calculator
- Pre-calibrated for Indian Tech & Generative AI benchmarks (Bangalore & Kolkata).
- **Candidate Baseline**: Current CTC: ** <LPA>** (Specialist Programmer – GenAI at Infosys).
- **Target Expectations**: Expected CTC: **18.0 – 200+ LPA** (+54.5% to +63.6% hike).
- Run `python salary_lookup.py "<Company>"` to view salary distributions.
- Run `python salary_lookup.py --calc <offered_LPA>` to get an instant hike breakdown, monthly gross delta, and negotiation verdict.

### 5. Interview Prep Package (`/interview`)
- Automatically generates interview cheat sheets, STAR-method behavioral stories, company recent news analysis, and technical talking points.
- Features an interactive mock interview roleplay simulator.

---

## Prerequisites

To run this repository locally, you only need:

1. **Operating System**: macOS, Linux, or Windows (WSL recommended on Windows).
2. **Python 3.10+**: For runner tools and data processing.
3. **[Bun](https://bun.sh)** (or Node.js 18+): Fast JavaScript/TypeScript runtime for job board CLIs.
4. **LaTeX Distribution**: To compile high-quality PDF CVs and cover letters.
   - Recommended: **TinyTeX** (lightweight, ~150MB, fast).
   - Alternatively: MacTeX (macOS) or TeX Live (Linux/Windows).
5. **AI Runner**:
   - **[Google Antigravity IDE](https://github.com/google)** (Free, native support for Google Gemini).
   - *Optional*: Claude Code CLI if you already have an Anthropic subscription.

---

## Quick Start & Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/anupkumarmahata123/ai-job-search.git
cd ai-job-search
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS / Linux:
source .venv/bin/activate
# On Windows (cmd/PowerShell):
# .venv\Scripts\activate

# Install required Python packages
pip install --upgrade pip
pip install openpyxl pyyaml pypdf pytest
```

### Step 3: Install Bun (for Job Search CLIs)

If you don't have Bun installed:
```bash
# On macOS / Linux:
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc  # or source ~/.zshrc

# Verify installation:
bun --version
```

Install the portal search dependencies:
```bash
python3 tools/install_portal_clis.py
```

### Step 4: Install TinyTeX (LaTeX PDF Compiler)

TinyTeX provides `lualatex` and `xelatex` needed to compile beautiful CVs and cover letters:

```bash
# On macOS / Linux:
curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh

# Add to PATH (or reopen terminal):
export PATH="$HOME/bin:$PATH"

# Verify LaTeX is available:
lualatex --version
xelatex --version
```

### Step 5: Verify Your Installation

Run the built-in integrity check:
```bash
python3 tools/lint_skills.py
python3 tools/security_guards.py
```
If both output `OK`, your environment is 100% ready!

---

## Setting Up Daily Gmail Automation

You can have the scraper run automatically every morning and send a clean job report directly to your personal email with the Excel attachment.

### 1. Configure `.env` File

Copy the example file:
```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in your details:
```env
# Personal Gmail Configuration
GMAIL_ADDRESS="your.email@gmail.com"
GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
RECEIVER_EMAIL="your.email@gmail.com"

# SMTP Settings (Defaults to Gmail)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
```

> **How to generate a Gmail App Password (Takes 1 minute)**:
> 1. Go to your [Google Account Security Settings](https://myaccount.google.com/security).
> 2. Ensure **2-Step Verification** is turned ON.
> 3. Search for **App passwords** (or go to [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)).
> 4. Create a new App Password named `AI Job Search`.
> 5. Copy the 16-character code into `GMAIL_APP_PASSWORD` in your `.env` file (spaces don't matter).

### 2. Test Your Email Setup

Verify that SMTP authentication works and sends a test email:
```bash
python3 tools/setup_email.py
```
You will receive a confirmation email in your inbox!

### 3. Run the Daily Scraper & Email Dispatcher On Demand

To scrape jobs from the last 24 hours and send the daily digest with the Excel attachment right now:
```bash
python3 tools/send_daily_job_email.py --run-scraper
```

### 4. Enable Daily Automated Schedule (10:00 AM & 8:00 PM Every Day)

You can run your daily job search automation in two ways:

#### Option A: Cloud Automation via GitHub Actions (Recommended — Runs Even If Laptop is Switched Off)
A built-in GitHub Actions workflow (`.github/workflows/daily_job_search.yml`) runs automatically at **10:00 AM IST** (morning digest) and **8:00 PM IST** (evening reminder). It scrapes the portals, generates the Excel workbook, and delivers the email completely in the cloud for free ($0).

1. Go to your repository on GitHub: **Settings > Secrets and variables > Actions**.
2. Click **New repository secret** and add:
   - `GMAIL_ADDRESS`: Your personal Gmail address (e.g. `your.email@gmail.com`)
   - `GMAIL_APP_PASSWORD`: Your 16-character Google App Password (from [Google App Passwords](https://myaccount.google.com/apppasswords))
   - `RECEIVER_EMAIL`: Your personal recipient email (e.g. `your.email@gmail.com`)
3. Done! GitHub Actions will run on schedule twice daily. You can also trigger it manually at any time under the **Actions** tab by selecting **Daily Job Search & Email Dispatch** and clicking **Run workflow**.

#### Option B: Local Background Scheduling (Runs when Mac/PC is awake)
If you prefer running it locally on your computer:
```bash
python3 tools/setup_daily_schedule.py --times 10:00,20:00
```
- On **macOS**, this installs a native `launchd` background job (`com.aijobsearch.dailyreport.plist`) that fires at **10:00 AM** and **8:00 PM**.
- On **Linux**, this installs standard `cron` entries (`0 10,20 * * *`).

---

## Core Workflows & How to Use Them

### Workflow 1: Multi-Portal 24h Job Scraping
Fetch fresh jobs from LinkedIn, Instahyre, and generate the Naukri Live Hub:
```bash
python3 tools/scrape_multi_portal_24h_jobs.py
```
**Output**:
- `jobs_multi_portal_bangalore_kolkata_last_24h.xlsx`: Styled Excel sheet with tabs for All Jobs, High Priority, Bangalore, Kolkata, and Naukri Live Search.
- `jobs_multi_portal_bangalore_kolkata_last_24h.csv`: CSV export for programmatic analysis.

### Workflow 2: Applying to a Job (`/apply`)
In the Google Antigravity chat (or Claude Code), simply type:
```text
/apply https://www.linkedin.com/jobs/view/4473857692/
```
Or paste raw text:
```text
/apply
Role: Gen AI Engineer at Acme AI
Requirements: 2+ years experience in LangChain, RAG pipelines, FastAPI, Vector DBs...
```

**What the AI does autonomously**:
1. Checks the posting for integrity & prompt injections.
2. Evaluates fit score (0–100) across 5 dimensions against [`01-candidate-profile.md`](.claude/skills/job-application-assistant/01-candidate-profile.md).
3. Pulls company salary benchmarks from `salary_lookup.py`.
4. Drafts a tailored CV in `cv/main_<company>_<role>.tex`.
5. Drafts a tailored cover letter in `cover_letters/cover_<company>_<role>.tex`.
6. Spawns an autonomous Reviewer Agent to verify all claims and research company recent news.
7. Compiles the LaTeX code into clean PDFs (`lualatex` and `xelatex`).
8. Verifies PDF layout using `verify_pdf.py` (CV must be exactly 2 pages, cover letter exactly 1 page).
9. Runs ATS keyword analysis on the PDF text layer.
10. Archives the application in `documents/applications/<company>_<role>/` and updates `job_search_tracker.csv`.

### Workflow 3: Interview Preparation (`/interview`)
When you land an interview, prepare in minutes:
```text
/interview Infosys Gen AI Engineer
```
The AI builds:
- Company research breakdown and recent initiatives.
- 5 tailored STAR-method behavioral stories highlighting your actual experience.
- Technical talking points covering system design, RAG, agentic workflows, and vector databases.
- An interactive mock interview simulator.

---

## Salary Benchmark & Offer Analysis

The workspace comes with a salary lookup tool calibrated for the Indian IT / AI market (Bangalore & Kolkata):

```bash
# 1. View candidate compensation profile
python3 salary_lookup.py --profile

# 2. Look up salary benchmarks for a target employer
python3 salary_lookup.py "Infosys"
python3 salary_lookup.py "Google" --city "Bangalore"

# 3. Analyze an offer CTC vs Current CTC (11 LPA) & Target Band (17-18+ LPA)
python3 salary_lookup.py --calc 18.5
```

**Example Offer Analysis Output**:
```text
============================================================
  Salary Offer & Hike Analysis
============================================================
  Current CTC:         11.0 LPA (₹91,666 / month gross)
  Target Band:         17.0 – 18.0+ LPA (+54.5% to +63.6%)
  Offered CTC:         18.5 LPA (₹154,166 / month gross)
  Absolute Difference: +7.5 LPA (+₹62,500 / month gross)
  Hike Percentage:     +68.2%
  Evaluation:          [EXCELLENT] EXCEEDS OPTIMAL TARGET (18.0+ LPA) - Strong Acceptance Range
============================================================
```

---

## Repository Folder & File Structure

Here is a complete breakdown of every file and directory in this workspace:

```
ai-job-search/
├── .github/workflows/
│   └── daily_job_search.yml           # GitHub Actions automated cloud workflow (10 AM & 8 PM IST)
├── GEMINI.md                          # Master candidate profile & workflow rules for Google Antigravity & Gemini
├── AGENTS.md                          # Multi-agent thin-pointer architecture definition
├── CLAUDE.md                          # Compatibility runner profile for Claude Code
├── README.md                          # Comprehensive project documentation
├── .env.example                       # Template for email & credentials configuration
├── .gitignore                         # Protects personal documents, compiled PDFs, and credentials
│
├── .agents/skills/                    # Native Google Antigravity workspace skills
│   ├── apply/                         # Skill definition for /apply pipeline
│   ├── scrape/                        # Skill definition for /scrape portal search
│   ├── rank/                          # Skill definition for batch job fit scoring
│   ├── interview/                     # Skill definition for /interview preparation
│   ├── outcome/                       # Skill definition for tracking application outcomes & follow-ups
│   ├── upskill/                       # Skill definition for analyzing profile skill gaps
│   ├── html-report/                   # Skill definition for offline HTML dashboard generation
│   ├── setup/                         # Skill definition for onboarding interview
│   ├── linkedin-search/               # Zero-dependency LinkedIn public job search CLI (global)
│   └── freehire-search/               # Tech job aggregator search CLI
│
├── .claude/skills/job-application-assistant/  # Canonical methodology & evaluation guidelines
│   ├── 01-candidate-profile.md        # Structured candidate profile (Identity, Experience, Education, Skills)
│   ├── 02-behavioral-profile.md       # Behavioral traits, communication style, leadership examples
│   ├── 03-writing-style.md            # Cover letter and CV writing style rules (Honesty & No-Fluff rules)
│   ├── 04-job-evaluation.md           # 5-dimension scoring framework, eligibility gates, and salary benchmark
│   ├── 05-cv-templates.md             # ModernCV LaTeX templates & layout rules
│   ├── 06-cover-letter-templates.md   # Cover letter LaTeX templates & structure rules
│   └── 07-interview-prep.md           # STAR framework and interview prep guidelines
│
├── cv/                                # CV LaTeX source templates and compiled artifacts
│   ├── main_example.tex               # ModernCV banking style reference template
│   ├── main_infosys_gen_ai_engineer.tex # Tailored CV for Infosys application
│   └── main_infosys_gen_ai_engineer.pdf # Exact 2-page compiled CV (ATS-verified)
│
├── cover_letters/                     # Cover letter LaTeX class, fonts, and artifacts
│   ├── cover.cls                      # Custom cover letter LaTeX document class
│   ├── cover_example.tex              # Reference cover letter template
│   ├── cover_infosys_gen_ai_engineer.tex # Tailored cover letter for Infosys
│   ├── cover_infosys_gen_ai_engineer.pdf # Exact 1-page compiled cover letter
│   └── OpenFonts/                     # Embedded Lato and Raleway font files
│
├── documents/                         # Career source files and historical applications
│   ├── applications/                  # Archived applications (<company>_<role>/) with submitted CV & notes
│   ├── cv/                            # Master CV source
│   ├── diplomas/                      # Degree certificates & academic transcripts
│   └── references/                    # Reference letters & certifications
│
├── tools/                             # Automation tools and CI verification scripts
│   ├── scrape_multi_portal_24h_jobs.py# Multi-portal scraper (LinkedIn, Instahyre, Naukri Live Hub) -> Excel
│   ├── send_daily_job_email.py        # Executive daily email dispatcher with Excel attachment
│   ├── setup_email.py                 # Interactive SMTP tester for Gmail & Outlook
│   ├── setup_daily_schedule.py        # Automates 10:00 AM & 8:00 PM execution via launchd or cron
│   ├── verify_pdf.py                  # Validates exact page counts (2-page CV, 1-page Cover Letter) and text extraction
│   ├── verify_layout.py               # Inspects visual PDF layout for orphaned headings and spacing
│   ├── security_guards.py             # Security CI check: validates permissions, hooks, and manifests
│   ├── check_framework_version.py     # CI check: ensures framework_version is bumped on methodology edits
│   ├── lint_skills.py                 # CI linter for skills and command specifications
│   ├── posting_guard.py               # Integrity gate: strips hidden text and prompt injections from job ads
│   ├── fetch_page.py                  # Safe HTTP fetcher with robots.txt enforcement
│   └── install_portal_clis.py         # Installs dependencies for all portal search tools
│
├── salary_lookup.py                   # Salary benchmark lookup & offer hike calculator CLI
├── salary_data.json                   # Market salary benchmark database (Bangalore & Kolkata tech roles)
└── job_search_tracker.csv             # Central CSV tracking spreadsheet for all applications and statuses
```

---

## Troubleshooting & FAQ

### Q1: Do I need a paid Claude Code subscription to use this?
**No!** This repository has been fully adapted for **Google Antigravity** and runs seamlessly using **Google Gemini**. You can run the entire workflow (scraping, emailing, tailoring, interview prep) completely free of charge.

### Q2: What if `lualatex` or `xelatex` command is not found?
Ensure TinyTeX is installed and in your system PATH:
```bash
curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh
export PATH="$HOME/bin:$PATH"
```
On macOS with Homebrew, you can also run: `brew install --cask mactex-no-gui`.

### Q3: Why does Naukri return a bot detection error on direct HTTP scraping?
Naukri uses Akamai Bot Manager which blocks headless scrapers. We solved this with the **Naukri 24h Live Search Hub**:
- Our scraper builds pre-filtered, 1-click URLs for Bangalore & Kolkata with experience (`2+ YoE`) and time (`jobAge=1`) filters already applied.
- These links are embedded into your daily Excel spreadsheet and morning email digest, letting you open and apply directly with zero friction.

### Q4: How do I change the target cities or roles?
Edit `tools/scrape_multi_portal_24h_jobs.py`:
- `ROLES`: Update target job titles (e.g., AI Engineer, Full Stack Developer, Data Scientist).
- `CITIES`: Update target cities (e.g., Bangalore, Kolkata, Hyderabad, Mumbai, Remote).
- `EXPERIENCE_LEVEL`: Adjust years of experience.

---

## Author & Acknowledgements

- **Author & Maintainer**: [Anup Kumar Mahata](https://github.com/Akm007git)
- **Architecture**: Powered natively by **Google Antigravity & Google Gemini**.
- **Inspiration**: Custom-built for automated multi-portal Indian tech career workflows.

---

<p align="center">
  <b>Happy Job Hunting! May your pipeline be full and your offers high. 🚀</b>
</p>
