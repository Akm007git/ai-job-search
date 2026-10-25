# Changelog

All notable changes to the AI Job Search & Application Assistant (Antigravity & Gemini Edition) are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-25

### Added
- **Google Antigravity & Gemini Engine**: Native workspace support for Google Antigravity IDE and Google Gemini models (`GEMINI.md`, `AGENTS.md`, `.agents/skills/`), fully free and open-source without requiring Claude Code.
- **24-Hour Multi-Portal Job Scraper**: Integrated engine aggregating fresh tech postings across LinkedIn, Instahyre, and direct 1-click Naukri Live Hub for Bangalore and Kolkata (`tools/scrape_multi_portal_24h_jobs.py`).
- **Excel & CSV Deliverables**: Automatically generated multi-tab `.xlsx` workbooks and companion `.csv` with urgency badges and direct apply links.
- **Twice-Daily Email Automation**: Built-in executive HTML digest and Excel attachment dispatcher delivered directly to personal Gmail at **10:00 AM** (morning digest) and **8:00 PM** (evening reminder) (`tools/send_daily_job_email.py`).
- **macOS LaunchAgent & Cron Scheduler**: Background scheduler with zero CPU/RAM overhead while idle (`tools/setup_daily_schedule.py`).
- **Salary Benchmarking & Offer Hike Calculator**: Calibrated for Indian IT / AI market with candidate profile baseline (11.0 LPA) and target expectations (17.0–18.0+ LPA) (`salary_lookup.py`, `salary_data.json`).
- **Autonomous `/apply` Pipeline**: Deterministic integrity gate, 5-dimension quantitative fit scoring, ATS-verified 2-page ModernCV generation, 1-page cover letter generation, autonomous reviewer agent audit, and PDF layout verification (`tools/verify_pdf.py`).
- **Interview Preparation (`/interview`)**: Stage-specific STAR-method stories, technical architecture breakdowns, and interactive mock interview simulator.
- **Central Application Tracker**: Application pipeline management in `job_search_tracker.csv`.
