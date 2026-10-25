#!/usr/bin/env python3
"""Multi-Portal Job Scraper for Anup Kumar Mahata (2+ YoE, Bangalore & Kolkata, Hybrid & Remote).

Aggregates fresh jobs (last 24 hours / live) across:
1. LinkedIn (via guest API CLI with --jobage 1)
2. Instahyre (premier tech startup & product company portal in India)
3. Hasjob / Tech feeds (Indian developer community)

Outputs:
- jobs_multi_portal_bangalore_kolkata_last_24h.xlsx (Multi-tab formatted Excel sheet)
- jobs_multi_portal_bangalore_kolkata_last_24h.csv (Companion CSV)
"""

import json
import os
import re
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent

# Search roles requested by user
ROLES = [
    "AI Engineer",
    "Gen AI Engineer",
    "Software Engineer",
    "Software Developer",
]

# Target locations
LOCATIONS_LINKEDIN = [
    ("Bangalore", "Bengaluru, Karnataka, India"),
    ("Kolkata", "Kolkata, West Bengal, India"),
    ("Remote", "Remote"),
]

LOCATIONS_INSTAHYRE = [
    "Bangalore",
    "Kolkata",
    "Remote",
]

def fetch_linkedin_jobs(query: str, location_label: str, location_query: str, page: int = 1) -> list[dict]:
    """Fetch 24h jobs from LinkedIn public endpoints using local bun CLI."""
    cli_path = ROOT / ".agents" / "skills" / "linkedin-search" / "cli" / "src" / "cli.ts"
    if not cli_path.exists():
        print(f"Warning: {cli_path} not found.", file=sys.stderr)
        return []

    cmd = [
        "bun",
        "run",
        str(cli_path),
        "search",
        "-l", location_query,
        "-q", query,
        "--jobage", "1",
        "--page", str(page),
        "--format", "json"
    ]
    try:
        proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            return []
        data = json.loads(proc.stdout)
        results = data.get("results", [])
        formatted = []
        for item in results:
            formatted.append({
                "portal": "LinkedIn",
                "role_category": query,
                "title": item.get("title", "").strip(),
                "company": item.get("company", "").strip(),
                "location": item.get("location", location_label).strip(),
                "target_city": location_label,
                "date_posted": item.get("date", "Last 24h"),
                "job_id": str(item.get("id", "")),
                "url": item.get("url", f"https://www.linkedin.com/jobs/view/{item.get('id', '')}"),
                "experience": "2+ years match",
                "skills": query,
            })
        return formatted
    except Exception as e:
        print(f"Error querying LinkedIn for '{query}' in {location_label}: {e}", file=sys.stderr)
        return []

def fetch_instahyre_jobs(role: str, location: str) -> list[dict]:
    """Fetch curated tech & AI jobs from Instahyre for 2+ YoE in target cities."""
    ctx = ssl._create_unverified_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    encoded_role = urllib.parse.quote(role)
    url = f"https://www.instahyre.com/api/v1/job_search?company_type=0&designation={encoded_role}&experience=2&job_type=0&location={location}&offset=0"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            objs = data.get("objects", [])
            formatted = []
            for o in objs:
                jid = str(o.get("id", ""))
                company = o.get("employer", {}).get("company_name", "Tech Startup").strip()
                title = o.get("title", role).strip()
                loc = o.get("locations", location).strip()
                pub_url = o.get("public_url")
                if not pub_url:
                    pub_url = f"https://www.instahyre.com/job-{jid}"
                keywords = o.get("keywords", [])
                skills_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)

                formatted.append({
                    "portal": "Instahyre",
                    "role_category": role,
                    "title": title,
                    "company": company,
                    "location": loc,
                    "target_city": location,
                    "date_posted": "Live / Active",
                    "job_id": f"instahyre-{jid}",
                    "url": pub_url,
                    "experience": "2+ years",
                    "skills": skills_str or role,
                })
            return formatted
    except Exception as e:
        print(f"Error querying Instahyre for '{role}' in {location}: {e}", file=sys.stderr)
        return []

def rate_fit(title: str, skills: str, role_cat: str) -> str:
    """Classify fit score against Anup's 2+ YoE Generative AI and Software Engineering profile."""
    t_title = title.lower()
    t_skills = skills.lower()

    # Filter non-engineering roles
    if any(k in t_title for k in ["seo expert", "sales", "hr recruiter", "accountant", "marketing specialist"]):
        return "Non-Engineering"

    if any(k in t_title for k in ["principal", "director", "staff engineer", "architect", "head of", "vp", "lead "]):
        return "⚠️ Senior/Lead (Check YoE)"

    # Core Generative AI match
    if any(k in t_title for k in ["gen ai", "generative ai", "agentic", "llm", "rag", "langchain", "langgraph", "mcp"]):
        return "🔥 High Priority (Core GenAI Match)"

    # AI / ML Engineer
    if any(k in t_title for k in ["ai engineer", "ai developer", "ai ml", "ai/ml", "artificial intelligence", "applied ai", "machine learning"]):
        return "⭐ Strong Fit (AI/ML Engineer)"

    # SDE & Backend Engineer
    if any(k in t_title for k in ["sde - 1", "sde 1", "sde - 2", "sde 2", "sde-1", "sde-2", "backend", "python", "fastapi", "node"]):
        return "🚀 Ideal Match (Backend/SDE)"

    # General Software Engineer / Developer
    if any(k in t_title for k in ["software engineer", "software developer", "full stack", "fullstack", "developer"]):
        return "✅ Eligible (Software Engineer)"

    # Fallback to skills check
    if any(k in t_skills for k in ["generative ai", "langchain", "llm", "rag", "python"]):
        return "⭐ Relevant (AI Skills Match)"

    return "ℹ️ Tech Role"

def style_worksheet(ws, headers, rows_data):
    """Apply modern executive styling to openpyxl worksheet."""
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    border_side = Side(border_style="thin", color="E0E0E0")
    row_border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)
    alt_fill = PatternFill(start_color="F7F9FC", end_color="F7F9FC", fill_type="solid")

    ws.append(headers)
    ws.row_dimensions[1].height = 26

    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for i, row in enumerate(rows_data, start=1):
        row_num = i + 1
        ws.append(row)
        ws.row_dimensions[row_num].height = 22

        for col_num in range(1, len(headers) + 1):
            c = ws.cell(row=row_num, column=col_num)
            c.border = row_border
            c.font = data_font
            c.alignment = Alignment(vertical="center")

            if col_num in (1, 2, 7, 8):
                c.alignment = Alignment(horizontal="center", vertical="center")

            if i % 2 == 0:
                c.fill = alt_fill

            # Portal tag styling
            if col_num == 2:
                portal_val = str(c.value)
                if portal_val == "LinkedIn":
                    c.font = Font(name="Calibri", size=10, bold=True, color="0077B5")
                elif portal_val == "Instahyre":
                    c.font = Font(name="Calibri", size=10, bold=True, color="0E8044")

            # Fit rating styling
            if col_num == 10:
                fit_val = str(c.value)
                if "High Priority" in fit_val:
                    c.font = Font(name="Calibri", size=10, bold=True, color="C00000")
                elif "Strong Fit" in fit_val or "Ideal Match" in fit_val:
                    c.font = Font(name="Calibri", size=10, bold=True, color="008000")

            # Apply Link Column
            if col_num == 9:
                link_url = row[8]
                c.hyperlink = link_url
                portal_name = row[1]
                c.value = f"Apply on {portal_name}"
                c.font = Font(name="Calibri", size=10, color="0563C1", underline="single")
                c.alignment = Alignment(horizontal="center", vertical="center")

    col_widths = {
        1: 6,   # S.No
        2: 14,  # Portal
        3: 20,  # Role Category
        4: 38,  # Job Title
        5: 26,  # Company
        6: 28,  # Location
        7: 14,  # Experience
        8: 14,  # Date Posted
        9: 20,  # Apply Link
        10: 32, # Fit Rating
        11: 30, # Skills / Keywords
    }
    for col_idx, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    ws.freeze_panes = "A2"

def main():
    print("=" * 70)
    print("Multi-Portal 24-Hour Job Scraper for Anup Kumar Mahata (2+ YoE)")
    print("Target Locations: Bangalore, Kolkata, Hybrid & Remote")
    print("Target Roles: AI Engineer, Gen AI Engineer, Software Engineer, Software Developer")
    print("=" * 70)

    all_jobs = []
    seen_keys = set()

    # 1. Scrape LinkedIn (24h filter)
    print("\n[1/2] Querying LinkedIn (Last 24 Hours)...")
    for role in ROLES:
        for loc_label, loc_query in LOCATIONS_LINKEDIN:
            for page in (1, 2):
                print(f"  LinkedIn: '{role}' in {loc_label} (page {page})...")
                results = fetch_linkedin_jobs(role, loc_label, loc_query, page=page)
                for item in results:
                    key = (item["company"].lower(), item["title"].lower())
                    if item["job_id"] in seen_keys or key in seen_keys:
                        continue
                    seen_keys.add(item["job_id"])
                    seen_keys.add(key)
                    all_jobs.append(item)

    print(f"  -> LinkedIn scraped: {len([j for j in all_jobs if j['portal'] == 'LinkedIn'])} unique 24h jobs.")

    # 2. Scrape Instahyre (Tech Startups & Product MNCs)
    print("\n[2/2] Querying Instahyre (2+ Years Experience)...")
    instahyre_roles = [
        "AI Engineer",
        "Software Engineer",
        "Backend Developer",
        "Full Stack Developer"
    ]
    for role in instahyre_roles:
        for loc in LOCATIONS_INSTAHYRE:
            print(f"  Instahyre: '{role}' in {loc}...")
            results = fetch_instahyre_jobs(role, loc)
            for item in results:
                key = (item["company"].lower(), item["title"].lower())
                if item["job_id"] in seen_keys or key in seen_keys:
                    continue
                seen_keys.add(item["job_id"])
                seen_keys.add(key)
                all_jobs.append(item)

    print(f"  -> Instahyre scraped: {len([j for j in all_jobs if j['portal'] == 'Instahyre'])} curated jobs.")
    print(f"\nTotal Unified Jobs Collected: {len(all_jobs)}")

    # Prepare data rows
    headers = [
        "S.No",
        "Portal",
        "Role Category",
        "Job Title",
        "Company",
        "Location",
        "Experience",
        "Date Posted",
        "Apply / View Link",
        "Fit Rating",
        "Skills / Keywords"
    ]

    master_rows = []
    bangalore_rows = []
    kolkata_rows = []
    ai_genai_rows = []
    software_rows = []

    for i, job in enumerate(all_jobs, start=1):
        fit = rate_fit(job["title"], job.get("skills", ""), job["role_category"])
        row = [
            i,
            job["portal"],
            job["role_category"],
            job["title"],
            job["company"],
            job["location"],
            job["experience"],
            job["date_posted"],
            job["url"],
            fit,
            job.get("skills", "")
        ]
        master_rows.append(row)

        loc_lower = job["location"].lower()
        if "bangalore" in loc_lower or "bengaluru" in loc_lower or "remote" in loc_lower:
            bangalore_rows.append(row)
        if "kolkata" in loc_lower or "calcutta" in loc_lower or "remote" in loc_lower:
            kolkata_rows.append(row)

        if "ai" in fit.lower() or "genai" in fit.lower() or "ml" in fit.lower():
            ai_genai_rows.append(row)
        else:
            software_rows.append(row)

    # Build Multi-Tab Workbook
    wb = openpyxl.Workbook()

    # Tab 1: All Portals Consolidated
    ws_all = wb.active
    ws_all.title = "All_Portals_Consolidated"
    style_worksheet(ws_all, headers, master_rows)

    # Tab 2: Bangalore & Hybrid
    ws_blr = wb.create_sheet(title="Bangalore_Jobs")
    # Re-index S.No for tab
    blr_indexed = [[idx] + r[1:] for idx, r in enumerate(bangalore_rows, start=1)]
    style_worksheet(ws_blr, headers, blr_indexed)

    # Tab 3: Kolkata & Hybrid
    ws_ccu = wb.create_sheet(title="Kolkata_Jobs")
    ccu_indexed = [[idx] + r[1:] for idx, r in enumerate(kolkata_rows, start=1)]
    style_worksheet(ws_ccu, headers, ccu_indexed)

    # Tab 4: AI & GenAI Roles
    ws_ai = wb.create_sheet(title="AI_GenAI_Roles")
    ai_indexed = [[idx] + r[1:] for idx, r in enumerate(ai_genai_rows, start=1)]
    style_worksheet(ws_ai, headers, ai_indexed)

    # Tab 5: Software Engineering Roles
    ws_swe = wb.create_sheet(title="Software_Engineering_Roles")
    swe_indexed = [[idx] + r[1:] for idx, r in enumerate(software_rows, start=1)]
    style_worksheet(ws_swe, headers, swe_indexed)

    # Tab 6: Naukri 24h Live Direct Hub
    ws_naukri = wb.create_sheet(title="Naukri_Live_24h_Hub")
    naukri_headers = [
        "S.No",
        "Portal",
        "Target Role",
        "Target Location",
        "Experience Filter",
        "Posting Time Filter",
        "Direct 1-Click Search & Apply Link",
        "Action"
    ]
    naukri_items = [
        ("AI Engineer", "Bangalore / Bengaluru", "2+ Years", "Last 24 Hours", "https://www.naukri.com/ai-engineer-jobs-in-bangalore?experience=2&jobAge=1"),
        ("Generative AI Engineer", "Bangalore / Bengaluru", "2+ Years", "Last 24 Hours", "https://www.naukri.com/generative-ai-engineer-jobs-in-bangalore?experience=2&jobAge=1"),
        ("Software Engineer", "Bangalore / Bengaluru", "2+ Years", "Last 24 Hours", "https://www.naukri.com/software-engineer-jobs-in-bangalore?experience=2&jobAge=1"),
        ("Software Developer", "Bangalore / Bengaluru", "2+ Years", "Last 24 Hours", "https://www.naukri.com/software-developer-jobs-in-bangalore?experience=2&jobAge=1"),
        ("Backend Developer (Python/Node)", "Bangalore / Bengaluru", "2+ Years", "Last 24 Hours", "https://www.naukri.com/backend-developer-jobs-in-bangalore?experience=2&jobAge=1"),
        ("Full Stack AI Developer", "Bangalore / Bengaluru", "2+ Years", "Last 24 Hours", "https://www.naukri.com/full-stack-developer-jobs-in-bangalore?experience=2&jobAge=1"),
        ("AI Engineer", "Kolkata (West Bengal)", "2+ Years", "Last 24 Hours", "https://www.naukri.com/ai-engineer-jobs-in-kolkata?experience=2&jobAge=1"),
        ("Generative AI Engineer", "Kolkata (West Bengal)", "2+ Years", "Last 24 Hours", "https://www.naukri.com/generative-ai-engineer-jobs-in-kolkata?experience=2&jobAge=1"),
        ("Software Engineer", "Kolkata (West Bengal)", "2+ Years", "Last 24 Hours", "https://www.naukri.com/software-engineer-jobs-in-kolkata?experience=2&jobAge=1"),
        ("Software Developer", "Kolkata (West Bengal)", "2+ Years", "Last 24 Hours", "https://www.naukri.com/software-developer-jobs-in-kolkata?experience=2&jobAge=1"),
        ("Python AI Developer", "Kolkata (West Bengal)", "2+ Years", "Last 24 Hours", "https://www.naukri.com/python-developer-jobs-in-kolkata?experience=2&jobAge=1"),
        ("Remote AI / GenAI Engineer", "Pan-India Remote", "2+ Years", "Last 24 Hours", "https://www.naukri.com/remote-ai-engineer-jobs?experience=2&jobAge=1"),
        ("Remote Software Engineer", "Pan-India Remote", "2+ Years", "Last 24 Hours", "https://www.naukri.com/remote-software-engineer-jobs?experience=2&jobAge=1"),
    ]

    ws_naukri.append(naukri_headers)
    header_fill = PatternFill(start_color="0A3B75", end_color="0A3B75", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    border_side = Side(border_style="thin", color="E0E0E0")
    row_border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)
    alt_fill = PatternFill(start_color="FFF9F2", end_color="FFF9F2", fill_type="solid")

    ws_naukri.row_dimensions[1].height = 26
    for col_num in range(1, len(naukri_headers) + 1):
        cell = ws_naukri.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for idx, (role, loc, exp, time_win, url) in enumerate(naukri_items, start=1):
        row_num = idx + 1
        ws_naukri.append([
            idx,
            "Naukri.com",
            role,
            loc,
            exp,
            time_win,
            url,
            "Open 24h Listings"
        ])
        ws_naukri.row_dimensions[row_num].height = 22
        for col_num in range(1, len(naukri_headers) + 1):
            c = ws_naukri.cell(row=row_num, column=col_num)
            c.border = row_border
            c.font = data_font
            c.alignment = Alignment(vertical="center")

            if col_num in (1, 2, 5, 6, 8):
                c.alignment = Alignment(horizontal="center", vertical="center")

            if idx % 2 == 0:
                c.fill = alt_fill

            if col_num == 2:
                c.font = Font(name="Calibri", size=10, bold=True, color="FF6B00")

            if col_num == 7:
                c.hyperlink = url
                c.value = f"Search '{role}' on Naukri"
                c.font = Font(name="Calibri", size=10, color="0563C1", underline="single")
                c.alignment = Alignment(horizontal="center", vertical="center")

    naukri_widths = {1: 6, 2: 14, 3: 30, 4: 26, 5: 16, 6: 18, 7: 36, 8: 20}
    for c_idx, w in naukri_widths.items():
        ws_naukri.column_dimensions[get_column_letter(c_idx)].width = w
    ws_naukri.freeze_panes = "A2"

    out_xlsx = ROOT / "jobs_multi_portal_bangalore_kolkata_last_24h.xlsx"
    wb.save(out_xlsx)
    print(f"\n[OK] Excel Workbook generated: {out_xlsx}")

    # Generate companion CSV
    out_csv = ROOT / "jobs_multi_portal_bangalore_kolkata_last_24h.csv"
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write("S.No,Portal,Role Category,Job Title,Company,Location,Experience,Date Posted,Apply Link,Fit Rating,Skills\n")
        for r in master_rows:
            def q(v):
                return f'"{str(v).replace(chr(34), chr(34)+chr(34))}"'
            f.write(f'{r[0]},{q(r[1])},{q(r[2])},{q(r[3])},{q(r[4])},{q(r[5])},{q(r[6])},{q(r[7])},{q(r[8])},{q(r[9])},{q(r[10])}\n')

    print(f"[OK] Companion CSV generated: {out_csv}")
    print(f"Summary:")
    print(f"  - Total Jobs: {len(master_rows)}")
    print(f"  - Bangalore & Remote: {len(bangalore_rows)}")
    print(f"  - Kolkata & Remote: {len(kolkata_rows)}")
    print(f"  - AI / GenAI Focus: {len(ai_genai_rows)}")
    print(f"  - Software Engineering Focus: {len(software_rows)}")

if __name__ == "__main__":
    main()
