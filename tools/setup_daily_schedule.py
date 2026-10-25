#!/usr/bin/env python3
"""Daily Job Search Schedule Setup for macOS & Linux.

Configures an automated background job that runs every day at specified times:
- Morning Dispatch: 10:00 AM (Scrapes latest 24-hour jobs, generates Excel, sends digest)
- Evening Reminder: 8:00 PM (20:00) (Scrapes latest afternoon updates, delivers evening reminder)

Usage:
  python tools/setup_daily_schedule.py [--times 10:00,20:00] [--method launchd|cron] [--status] [--uninstall]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYTHON_BIN = ROOT / ".venv" / "bin" / "python"
DISPATCHER = ROOT / "tools" / "send_daily_job_email.py"
PLIST_LABEL = "com.aijobsearch.dailyreport"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_LABEL}.plist"
LOG_DIR = Path.home() / "Library" / "Logs"
LOG_FILE = LOG_DIR / "aijobsearch_daily.log"


def parse_times(times_str: str) -> list[tuple[int, int]]:
    """Parse comma-separated HH:MM strings into list of (hour, minute) tuples."""
    parsed = []
    for part in times_str.split(","):
        part = part.strip()
        if not part:
            continue
        sub = part.split(":")
        if len(sub) != 2:
            raise ValueError(f"Invalid time format '{part}'. Expected HH:MM (e.g. 10:00 or 20:00)")
        h, m = int(sub[0]), int(sub[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError(f"Time out of range: '{part}'")
        parsed.append((h, m))
    if not parsed:
        raise ValueError("No valid times provided.")
    return parsed


def format_time_display(hour: int, minute: int) -> str:
    """Format hour and minute into human-readable 12h and 24h string."""
    period = "AM" if hour < 12 else "PM"
    h12 = hour if 1 <= hour <= 12 else (hour - 12 if hour > 12 else 12)
    return f"{h12:02d}:{minute:02d} {period} ({hour:02d}:{minute:02d})"


def get_launchd_plist_content(time_list: list[tuple[int, int]]) -> str:
    path_env = f"/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:{Path.home()}/.bun/bin:{Path.home()}/Library/TinyTeX/bin/universal-darwin"
    
    intervals_xml = []
    for h, m in time_list:
        intervals_xml.append(f"""        <dict>
            <key>Hour</key>
            <integer>{h}</integer>
            <key>Minute</key>
            <integer>{m}</integer>
        </dict>""")
    intervals_block = "\n".join(intervals_xml)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{PYTHON_BIN}</string>
        <string>{DISPATCHER}</string>
        <string>--run-scraper</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>{path_env}</string>
    </dict>
    <key>WorkingDirectory</key>
    <string>{ROOT}</string>
    <key>StartCalendarInterval</key>
    <array>
{intervals_block}
    </array>
    <key>StandardOutPath</key>
    <string>{LOG_FILE}</string>
    <key>StandardErrorPath</key>
    <string>{LOG_FILE}</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
"""


def install_launchd(time_list: list[tuple[int, int]]):
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Unload existing if loaded
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)], capture_output=True)

    # Write plist
    PLIST_PATH.write_text(get_launchd_plist_content(time_list), encoding="utf-8")
    print(f"[OK] Created LaunchAgent definition at: {PLIST_PATH}")

    # Load agent
    res = subprocess.run(["launchctl", "load", str(PLIST_PATH)], capture_output=True, text=True)
    if res.returncode == 0:
        times_desc = ", ".join(format_time_display(h, m) for h, m in time_list)
        print(f"[OK] Successfully scheduled daily job automation via macOS launchd!")
        print(f"     Execution times: {times_desc}")
        print(f"     Logs will be written to: {LOG_FILE}")
    else:
        print(f"[FAIL] Could not load launchd plist: {res.stderr}", file=sys.stderr)


def uninstall_launchd():
    if PLIST_PATH.exists():
        subprocess.run(["launchctl", "unload", str(PLIST_PATH)], capture_output=True)
        PLIST_PATH.unlink()
        print(f"[OK] Uninstalled daily LaunchAgent: {PLIST_LABEL}")
    else:
        print(f"No LaunchAgent found at {PLIST_PATH}")


def check_status():
    print("Checking Daily Job Automation Status...")
    res = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
    loaded = PLIST_LABEL in res.stdout
    print(f"  LaunchAgent status: {'ACTIVE & LOADED' if loaded else 'NOT LOADED'}")
    if PLIST_PATH.exists():
        print(f"  Plist file exists: {PLIST_PATH}")
    else:
        print("  Plist file does not exist.")

    # Check crontab
    cron_res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if "send_daily_job_email" in cron_res.stdout:
        print("  Crontab: ACTIVE")
        for line in cron_res.stdout.splitlines():
            if "send_daily_job_email" in line:
                print(f"    {line}")
    else:
        print("  Crontab: None")

    if LOG_FILE.exists():
        print(f"  Recent log lines ({LOG_FILE}):")
        lines = LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
        for l in lines[-5:]:
            print(f"    {l}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--times", "--time", default="10:00,20:00",
                        help="Comma-separated times to run (HH:MM in 24h format, default: 10:00,20:00)")
    parser.add_argument("--method", choices=["launchd", "cron"], default="launchd",
                        help="Scheduling system (default: launchd)")
    parser.add_argument("--status", action="store_true", help="Check current schedule status")
    parser.add_argument("--uninstall", action="store_true", help="Remove scheduled job")
    args = parser.parse_args()

    if args.status:
        check_status()
        return 0

    if args.uninstall:
        uninstall_launchd()
        return 0

    try:
        time_list = parse_times(args.times)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.method == "launchd":
        install_launchd(time_list)
    elif args.method == "cron":
        cron_lines = []
        for h, m in time_list:
            cron_lines.append(f"{m} {h} * * * cd {ROOT} && {PYTHON_BIN} {DISPATCHER} --run-scraper >> {LOG_FILE} 2>&1")
        
        # read existing
        existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
        cleaned = "\n".join(l for l in existing.splitlines() if "send_daily_job_email" not in l)
        combined = (cleaned.strip() + "\n" + "\n".join(cron_lines) + "\n").lstrip()
        
        p = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        p.communicate(input=combined)
        times_desc = ", ".join(format_time_display(h, m) for h, m in time_list)
        print(f"[OK] Added crontab entries for: {times_desc}")

    print("\nTarget Configuration Summary:")
    print("  - Morning Job Digest: 10:00 AM IST")
    print("  - Evening Application Reminder: 8:00 PM (20:00) IST")
    print(f"  - Recipient: anupkumar.mahata.ai@gmail.com")
    print(f"  - Attached: jobs_multi_portal_bangalore_kolkata_last_24h.xlsx")


if __name__ == "__main__":
    sys.exit(main())
