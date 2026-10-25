#!/usr/bin/env python3
"""Daily Job Email Dispatcher for Anup Kumar Mahata.

Sends a daily executive email digest with:
1. Top high-priority jobs from the last 24 hours (with direct 1-click Apply buttons).
2. Naukri 24-Hour Live Search Hub (instant 1-click filters for Bangalore & Kolkata).
3. The complete formatted Excel workbook attached directly to the email.

Usage:
  python tools/send_daily_job_email.py [--run-scraper] [--dry-run] [--preview]
"""

import argparse
import datetime
import os
import smtplib
import subprocess
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load local environment variables from .env if present
def load_env():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("\"'"))

load_env()

user_email = (
    os.environ.get("GMAIL_ADDRESS")
    or os.environ.get("EMAIL")
    or os.environ.get("RECEIVER_EMAIL")
    or os.environ.get("SENDER_EMAIL")
    or "anupkumarmahata2022@outlook.com"
)
EMAIL_FROM = os.environ.get("SENDER_EMAIL") or user_email
EMAIL_TO = os.environ.get("RECEIVER_EMAIL") or user_email

# Auto-detect Gmail or Outlook
if "@gmail.com" in EMAIL_FROM.lower() or "@gmail.com" in EMAIL_TO.lower():
    default_host = "smtp.gmail.com"
else:
    default_host = "smtp-mail.outlook.com"

SMTP_HOST = os.environ.get("SMTP_HOST", default_host)
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("SMTP_PASSWORD") or ""

NAUKRI_LINKS = [
    ("AI Engineer - Bangalore (2+ YoE, 24h)", "https://www.naukri.com/ai-engineer-jobs-in-bangalore?experience=2&jobAge=1"),
    ("Generative AI Engineer - Bangalore (2+ YoE, 24h)", "https://www.naukri.com/generative-ai-engineer-jobs-in-bangalore?experience=2&jobAge=1"),
    ("Software Engineer - Bangalore (2+ YoE, 24h)", "https://www.naukri.com/software-engineer-jobs-in-bangalore?experience=2&jobAge=1"),
    ("AI Engineer - Kolkata (2+ YoE, 24h)", "https://www.naukri.com/ai-engineer-jobs-in-kolkata?experience=2&jobAge=1"),
    ("Software Engineer - Kolkata (2+ YoE, 24h)", "https://www.naukri.com/software-engineer-jobs-in-kolkata?experience=2&jobAge=1"),
    ("Backend Developer - Bangalore (2+ YoE, 24h)", "https://www.naukri.com/backend-developer-jobs-in-bangalore?experience=2&jobAge=1"),
]

def load_jobs_from_workbook():
    import openpyxl
    wb_path = ROOT / "jobs_multi_portal_bangalore_kolkata_last_24h.xlsx"
    if not wb_path.exists():
        return [], 0, 0, 0, 0

    wb = openpyxl.load_workbook(wb_path)
    ws = wb["All_Portals_Consolidated"]
    jobs = []

    blr_count = 0
    ccu_count = 0
    ai_count = 0

    for r in range(2, ws.max_row + 1):
        portal = ws.cell(row=r, column=2).value or ""
        cat = ws.cell(row=r, column=3).value or ""
        title = ws.cell(row=r, column=4).value or ""
        company = ws.cell(row=r, column=5).value or ""
        loc = ws.cell(row=r, column=6).value or ""
        exp = ws.cell(row=r, column=7).value or ""
        date = ws.cell(row=r, column=8).value or ""
        link = ws.cell(row=r, column=9).hyperlink.target if ws.cell(row=r, column=9).hyperlink else ws.cell(row=r, column=9).value or ""
        fit = ws.cell(row=r, column=10).value or ""
        skills = ws.cell(row=r, column=11).value or ""

        loc_lower = str(loc).lower()
        if "bangalore" in loc_lower or "bengaluru" in loc_lower or "remote" in loc_lower:
            blr_count += 1
        if "kolkata" in loc_lower or "calcutta" in loc_lower or "remote" in loc_lower:
            ccu_count += 1
        if "ai" in str(fit).lower() or "genai" in str(fit).lower():
            ai_count += 1

        jobs.append({
            "portal": portal,
            "category": cat,
            "title": title,
            "company": company,
            "location": loc,
            "exp": exp,
            "date": date,
            "url": link,
            "fit": fit,
            "skills": skills
        })

    total = len(jobs)
    return jobs, total, blr_count, ccu_count, ai_count

def generate_html_email(jobs, total, blr_count, ccu_count, ai_count) -> str:
    now = datetime.datetime.now()
    today_str = now.strftime("%A, %d %B %Y")
    is_evening = now.hour >= 18

    header_tag = "Evening Application Reminder" if is_evening else "Daily Morning Job Digest"
    header_title = "Evening Job Reminder & Matches for Anup" if is_evening else "24-Hour Job Matches for Anup"
    header_subtitle = "Review today's top roles & submit your applications before recruiters close the 24h window!" if is_evening else "Latest roles posted in the last 24 hours across Bangalore & Kolkata."

    # Select top high-priority and ideal match jobs for email preview
    top_jobs = []
    for j in jobs:
        if "High Priority" in j["fit"] or "Ideal Match" in j["fit"] or "Strong Fit" in j["fit"]:
            top_jobs.append(j)
        if len(top_jobs) >= 12:
            break

    job_cards_html = ""
    for j in top_jobs:
        portal_badge_bg = "#0077B5" if j["portal"] == "LinkedIn" else "#0E8044"
        fit_badge_bg = "#C00000" if "High Priority" in j["fit"] else ("#008000" if "Strong Fit" in j["fit"] or "Ideal Match" in j["fit"] else "#1F4E79")

        job_cards_html += f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px 20px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
            <div style="font-size: 16px; font-weight: 700; color: #1E293B;">{j['title']}</div>
            <span style="background-color: {portal_badge_bg}; color: #FFFFFF; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px;">{j['portal']}</span>
          </div>
          <div style="font-size: 14px; color: #475569; margin-bottom: 6px;">
            <strong style="color: #0F172A;">{j['company']}</strong> &bull; 📍 {j['location']}
          </div>
          <div style="margin-bottom: 12px;">
            <span style="background-color: {fit_badge_bg}; color: #FFFFFF; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 12px; display: inline-block;">{j['fit']}</span>
            <span style="background-color: #F1F5F9; color: #334155; font-size: 11px; padding: 2px 8px; border-radius: 12px; margin-left: 6px; display: inline-block;">🗓 {j['date']}</span>
          </div>
          <a href="{j['url']}" style="display: inline-block; background-color: #2563EB; color: #FFFFFF; text-decoration: none; font-size: 13px; font-weight: 600; padding: 8px 18px; border-radius: 6px; box-shadow: 0 1px 2px rgba(37,99,235,0.2);">
            Apply on {j['portal']} &rarr;
          </a>
        </div>
        """

    naukri_buttons_html = ""
    for label, url in NAUKRI_LINKS:
        naukri_buttons_html += f"""
        <a href="{url}" style="display: inline-block; background-color: #FFF7ED; color: #C2410C; border: 1px solid #FFEDD5; text-decoration: none; font-size: 12px; font-weight: 600; padding: 7px 14px; border-radius: 6px; margin: 4px 6px 4px 0;">
          🔍 {label}
        </a>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>{header_title} - {today_str}</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F8FAFC; margin: 0; padding: 24px; color: #1E293B;">
      <div style="max-width: 680px; margin: 0 auto; background-color: #FFFFFF; border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
        
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); padding: 32px 28px; color: #FFFFFF;">
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; color: #93C5FD; margin-bottom: 6px;">{header_tag}</div>
          <h1 style="margin: 0 0 8px 0; font-size: 24px; font-weight: 800; color: #FFFFFF;">{header_title}</h1>
          <div style="font-size: 14px; color: #CBD5E1;">{today_str} &bull; {header_subtitle}</div>
        </div>

        <!-- Metrics Cards -->
        <div style="padding: 20px 28px; background-color: #F1F5F9; border-bottom: 1px solid #E2E8F0;">
          <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr>
              <td align="center" style="padding: 8px;">
                <div style="font-size: 22px; font-weight: 800; color: #1E3A8A;">{total}</div>
                <div style="font-size: 11px; text-transform: uppercase; font-weight: 600; color: #64748B;">Total Jobs</div>
              </td>
              <td align="center" style="padding: 8px; border-left: 1px solid #CBD5E1;">
                <div style="font-size: 22px; font-weight: 800; color: #0284C7;">{blr_count}</div>
                <div style="font-size: 11px; text-transform: uppercase; font-weight: 600; color: #64748B;">Bangalore / Hybrid</div>
              </td>
              <td align="center" style="padding: 8px; border-left: 1px solid #CBD5E1;">
                <div style="font-size: 22px; font-weight: 800; color: #059669;">{ccu_count}</div>
                <div style="font-size: 11px; text-transform: uppercase; font-weight: 600; color: #64748B;">Kolkata / Hybrid</div>
              </td>
              <td align="center" style="padding: 8px; border-left: 1px solid #CBD5E1;">
                <div style="font-size: 22px; font-weight: 800; color: #DC2626;">{ai_count}</div>
                <div style="font-size: 11px; text-transform: uppercase; font-weight: 600; color: #64748B;">AI & GenAI</div>
              </td>
            </tr>
          </table>
        </div>

        <!-- Content Body -->
        <div style="padding: 28px;">
          
          <!-- Attachment Notice -->
          <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 14px 18px; margin-bottom: 24px;">
            <div style="font-size: 14px; font-weight: 700; color: #1E40AF; margin-bottom: 4px;">📎 Complete Excel Spreadsheet Attached</div>
            <div style="font-size: 13px; color: #1E3A8A; line-height: 1.5;">
              The full categorized workbook <strong>jobs_multi_portal_bangalore_kolkata_last_24h.xlsx</strong> with all {total} listings, direct URLs, and custom tabs (Bangalore, Kolkata, AI, Software Engineering) is attached to this email.
            </div>
          </div>

          <!-- Top Priority Matches -->
          <h2 style="font-size: 18px; font-weight: 700; color: #0F172A; margin: 0 0 16px 0;">⭐ Top High-Priority Matches (1-Click Apply)</h2>
          {job_cards_html}

          <!-- Naukri 24h Live Search Hub -->
          <div style="margin-top: 32px; padding: 20px; background-color: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px;">
            <div style="font-size: 15px; font-weight: 700; color: #92400E; margin-bottom: 6px;">🌐 Naukri 24-Hour Live Direct Hub</div>
            <div style="font-size: 13px; color: #78350F; margin-bottom: 12px; line-height: 1.4;">
              Access Naukri's latest postings filtered for your exact profile (2+ YoE, Last 24 Hours) with 1 click:
            </div>
            <div>
              {naukri_buttons_html}
            </div>
          </div>

        </div>

        <!-- Footer -->
        <div style="background-color: #F8FAFC; padding: 20px 28px; border-top: 1px solid #E2E8F0; text-align: center; font-size: 12px; color: #94A3B8;">
          Generated automatically by Google Antigravity &amp; Gemini AI Job Search Assistant for Anup Kumar Mahata.<br>
          Electronics City, Bangalore &bull; Kolkata &bull; anupkumarmahata2022@outlook.com
        </div>

      </div>
    </body>
    </html>
    """
    return html

def send_email(html_content: str, attachment_path: Path) -> bool:
    if not SMTP_PASSWORD:
        print("[!] No SMTP_PASSWORD found in environment or .env file.", file=sys.stderr)
        print("    To send live emails, set SMTP_PASSWORD in .env or environment variables.")
        return False

    msg = MIMEMultipart("mixed")
    now = datetime.datetime.now()
    today_str = now.strftime("%d %b %Y")
    is_evening = now.hour >= 18
    if is_evening:
        msg["Subject"] = f"🔔 Evening Application Reminder & Job Digest ({today_str}) - Bangalore & Kolkata"
    else:
        msg["Subject"] = f"🎯 Daily 24h Job Search Digest ({today_str}) - Bangalore & Kolkata"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    # Attach HTML Body
    msg_alternative = MIMEMultipart("alternative")
    msg_alternative.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(msg_alternative)

    # Attach Excel Spreadsheet
    if attachment_path.exists():
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{attachment_path.name}"')
        msg.attach(part)
        print(f"  -> Attached: {attachment_path.name}")

    print(f"Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT} as {EMAIL_FROM}...")
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_FROM, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        server.quit()
        print(f"[OK] Daily Job Digest successfully sent to {EMAIL_TO}!")
        return True
    except Exception as e:
        print(f"[FAIL] Error sending email: {e}", file=sys.stderr)
        return False

def send_test_email() -> bool:
    """Send a lightweight verification email to test SMTP settings."""
    if not SMTP_PASSWORD:
        print("[!] No SMTP_PASSWORD or GMAIL_APP_PASSWORD found in environment or .env file.", file=sys.stderr)
        print("    See .env.example or run: python tools/setup_email.py")
        return False

    msg = MIMEMultipart()
    msg["Subject"] = "🎉 Job Search Automation: Test Email Successful!"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    body = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; padding: 20px; color: #1E293B;">
      <div style="max-width: 560px; margin: 0 auto; border: 1px solid #E2E8F0; border-radius: 10px; padding: 24px; background-color: #FFFFFF;">
        <h2 style="color: #059669; margin-top: 0;">✅ Your Job Search Email Automation is Working!</h2>
        <p>This is a verification email sent from your AI Job Search workspace.</p>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; margin: 16px 0;">
          <div><strong>Recipient:</strong> {EMAIL_TO}</div>
          <div><strong>Sender:</strong> {EMAIL_FROM}</div>
          <div><strong>SMTP Server:</strong> {SMTP_HOST}:{SMTP_PORT}</div>
          <div><strong>Status:</strong> Authentication Successful</div>
        </div>
        <p>Your daily 24-hour job digests with attached Excel spreadsheets will now be delivered to this inbox automatically.</p>
        <div style="font-size: 12px; color: #94A3B8; margin-top: 20px; border-top: 1px solid #E2E8F0; padding-top: 10px;">
          Generated by Google Antigravity &amp; Gemini AI Job Search Assistant
        </div>
      </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, "html", "utf-8"))

    print(f"Connecting to {SMTP_HOST}:{SMTP_PORT} as {EMAIL_FROM}...")
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_FROM, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        server.quit()
        print(f"\n[SUCCESS] Test email was sent successfully to {EMAIL_TO}!")
        print("          Check your inbox (and Spam/Junk folder just in case).")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n[ERROR] SMTP Authentication failed: {e}", file=sys.stderr)
        if "gmail" in SMTP_HOST.lower():
            print("\n--> For Google / Gmail accounts:")
            print("    1. You cannot use your standard Gmail login password.")
            print("    2. You must generate a 16-character 'App Password' from Google:")
            print("       https://myaccount.google.com/apppasswords")
            print("    3. Ensure 2-Step Verification is turned ON in your Google Account.")
            print("    4. Set GMAIL_APP_PASSWORD=<16_char_password> in your .env file.")
        return False
    except Exception as e:
        print(f"\n[ERROR] Failed to send email: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", action="store_true", help="Send a test verification email to confirm SMTP setup")
    parser.add_argument("--run-scraper", action="store_true", help="Run multi-portal 24h scraper before sending email")
    parser.add_argument("--dry-run", action="store_true", help="Generate HTML email and save preview without sending")
    parser.add_argument("--preview", action="store_true", help="Open generated HTML preview in browser")
    args = parser.parse_args()

    print("=" * 70)
    print("Daily Job Email Digest Dispatcher")
    print(f"Target Email: {EMAIL_TO}")
    print(f"SMTP Host:    {SMTP_HOST}:{SMTP_PORT}")
    print("=" * 70)

    if args.test:
        print("\nSending verification test email...")
        success = send_test_email()
        return 0 if success else 1

    if args.run_scraper:
        print("\n[1/3] Running multi-portal scraper to fetch freshest jobs...")
        proc = subprocess.run([sys.executable, str(ROOT / "tools" / "scrape_multi_portal_24h_jobs.py")], cwd=str(ROOT))
        if proc.returncode != 0:
            print("Warning: scraper completed with errors.", file=sys.stderr)
    else:
        print("\n[1/3] Using latest scraped workbook data...")

    print("\n[2/3] Parsing workbook and generating executive HTML email...")
    jobs, total, blr, ccu, ai = load_jobs_from_workbook()
    print(f"  Total jobs loaded: {total} (Bangalore: {blr}, Kolkata: {ccu}, AI/GenAI: {ai})")

    html_email = generate_html_email(jobs, total, blr, ccu, ai)
    out_html = ROOT / "email_daily_digest.html"
    out_html.write_text(html_email, encoding="utf-8")
    print(f"  -> Saved HTML preview to: {out_html}")

    xlsx_path = ROOT / "jobs_multi_portal_bangalore_kolkata_last_24h.xlsx"

    if args.dry_run or not SMTP_PASSWORD:
        print("\n[3/3] Dry-Run Mode / SMTP Configuration Info:")
        print(f"  HTML digest generated at: {out_html}")
        print(f"  Attachment file: {xlsx_path}")
        print(f"\n  To enable automatic live sending to {EMAIL_TO}:")
        print("  1. Create or edit .env file in workspace root with your Gmail details:")
        print(f"     GMAIL_ADDRESS={EMAIL_TO}")
        print("     GMAIL_APP_PASSWORD=<your_16_character_google_app_password>")
        print("\n  2. Test the connection immediately:")
        print("     python tools/send_daily_job_email.py --test")
        print("\n  3. Send full digest with Excel attachment:")
        print("     python tools/send_daily_job_email.py")
        return 0

    print(f"\n[3/3] Dispatching email to {EMAIL_TO}...")
    success = send_email(html_email, xlsx_path)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

