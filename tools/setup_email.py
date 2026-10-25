#!/usr/bin/env python3
"""Interactive & Automated Gmail SMTP Setup for Anup Kumar Mahata.

Configures Gmail for automated daily job search delivery:
- Only ONE Gmail address is required (it sends the email to itself).
- Tests the connection to smtp.gmail.com:587.
- Sends a live test email to verify credentials.
- Saves the working credentials to .env safely (gitignored).

Usage:
  python tools/setup_email.py [--email user@gmail.com] [--password "xxxx xxxx xxxx xxxx"]
"""

import argparse
import getpass
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"

def print_google_instructions():
    print("""
======================================================================
How to get your 16-character Google App Password (takes 1 minute):
======================================================================
1. Open Google Account Security:
   👉 https://myaccount.google.com/security

2. Ensure "2-Step Verification" is turned ON.

3. Under 2-Step Verification or by searching the search bar for "App passwords":
   👉 Direct Link: https://myaccount.google.com/apppasswords

4. Enter an App Name (e.g. "Job Search") and click "Create".

5. Google will show a 16-character code (e.g. "abcd efgh ijkl mnop").
   Copy this code! That is your GMAIL_APP_PASSWORD.
======================================================================
""")

def verify_and_save(email_addr: str, app_password: str) -> bool:
    email_addr = email_addr.strip()
    app_password = app_password.strip().replace(" ", "")

    print(f"\n[1/3] Testing SMTP connection to smtp.gmail.com:587 as {email_addr}...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email_addr, app_password)
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n[FAIL] Authentication failed: {e}", file=sys.stderr)
        print("Please verify:")
        print("1. Did you enter the 16-character Google App Password (not regular password)?")
        print("2. Is 2-Step Verification enabled on this Google account?")
        return False
    except Exception as e:
        print(f"\n[FAIL] Connection error: {e}", file=sys.stderr)
        return False

    print("\n[2/3] Sending live verification email to your inbox...")
    msg = MIMEMultipart()
    msg["Subject"] = "🎉 Success! Your AI Job Search Email Delivery is Configured"
    msg["From"] = email_addr
    msg["To"] = email_addr

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; padding: 24px; color: #1E293B; background-color: #F8FAFC;">
      <div style="max-width: 580px; margin: 0 auto; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 28px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
        <h2 style="color: #059669; margin-top: 0; font-size: 22px;">🎉 Gmail Setup Complete!</h2>
        <p style="font-size: 15px; line-height: 1.5; color: #334155;">
          Congratulations! Your Google SMTP connection has been verified and is ready to deliver your daily 24-hour job search digests.
        </p>
        <div style="background-color: #F1F5F9; border-radius: 8px; padding: 16px; margin: 20px 0; font-size: 14px; line-height: 1.6;">
          <div><strong>Configured Email:</strong> {email_addr}</div>
          <div><strong>Role Focus:</strong> AI Engineer, Gen AI Engineer, Software Engineer, Software Developer</div>
          <div><strong>Target Locations:</strong> Bangalore &amp; Kolkata (Hybrid, Onsite, Remote)</div>
          <div><strong>Experience Bar:</strong> 2+ Years</div>
        </div>
        <p style="font-size: 14px; color: #475569;">
          From now on, every daily digest will arrive in this inbox with direct 1-click apply buttons and the full Excel spreadsheet attached.
        </p>
        <div style="font-size: 12px; color: #94A3B8; margin-top: 24px; border-top: 1px solid #E2E8F0; padding-top: 12px; text-align: center;">
          Google Antigravity &amp; Gemini AI Job Search Assistant
        </div>
      </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        server.sendmail(email_addr, [email_addr], msg.as_string())
        server.quit()
        print(f"[OK] Live test email sent to {email_addr}! Check your Gmail inbox.")
    except Exception as e:
        print(f"[FAIL] Failed to dispatch test email: {e}", file=sys.stderr)
        return False

    print("\n[3/3] Saving working configuration to .env...")
    env_content = f"""# Gmail SMTP Configuration for AI Job Search
GMAIL_ADDRESS={email_addr}
GMAIL_APP_PASSWORD={app_password}
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL={email_addr}
RECEIVER_EMAIL={email_addr}
"""
    ENV_PATH.write_text(env_content, encoding="utf-8")
    print(f"[OK] Configuration saved securely to: {ENV_PATH}")
    print("\nAll set! You can now:")
    print("  1. Send full daily digest anytime: python tools/send_daily_job_email.py --run-scraper")
    print("  2. Activate daily morning schedule: python tools/setup_daily_schedule.py --time 09:00")
    return True

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--email", help="Your Gmail address (e.g. yourname@gmail.com)")
    parser.add_argument("--password", help="Your 16-character Google App Password")
    args = parser.parse_args()

    print("=" * 70)
    print("Gmail SMTP Setup Wizard for Daily Job Reports")
    print("=" * 70)

    email_addr = args.email
    password = args.password

    if not email_addr or not password:
        print_google_instructions()

    if not email_addr:
        try:
            email_addr = input("Enter your Gmail address: ").strip()
        except EOFError:
            print("Error: No email provided.", file=sys.stderr)
            return 1

    if not password:
        try:
            password = getpass.getpass("Enter your 16-character Google App Password: ").strip()
        except EOFError:
            print("Error: No password provided.", file=sys.stderr)
            return 1

    if not email_addr or not password:
        print("Error: Both Gmail address and App Password are required.", file=sys.stderr)
        return 1

    success = verify_and_save(email_addr, password)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
