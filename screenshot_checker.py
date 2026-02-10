from playwright.sync_api import sync_playwright, TimeoutError
import os
import time
import requests
import traceback
import sys
from datetime import datetime
import pytz
from checker import get_links

# ================= TELEGRAM CONFIG =================
BOT_TOKEN = "8347404520:AAEeTkAPPKsMH-7DN5gJMqk7NFVapaok_aA"
GROUP_CHAT_ID = -5171687843  # supergroup ID

send_message("🟢 screenshot_checker.py VERSION: 2026-02-10 FIXED")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(
            url,
            json={"chat_id": GROUP_CHAT_ID, "text": text},
            timeout=15
        )
        print("Telegram:", r.status_code, r.text)
    except Exception as e:
        print("Telegram ERROR:", e)

def send_photo(path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(path, "rb") as f:
            requests.post(
                url,
                files={"photo": f},
                data={"chat_id": GROUP_CHAT_ID, "caption": caption},
                timeout=30
            )
    except Exception as e:
        print("Photo send ERROR:", e)

# ================= START DEBUG =================
send_message("🚀 DEBUG: screenshot_checker.py started")

# ================= PATHS =================
SCREENSHOT_DIR = "/app/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ================= LINKS =================
URLS = get_links()

# ================= TIME =================
ist = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(ist).strftime("%d-%m-%Y %I:%M %p IST")

# ================= MAIN LOGIC =================
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process",
                "--disable-setuid-sandbox"
            ]
        )

        page = browser.new_page()
        results = []

        send_message("🟢 Browser launched successfully")

        for idx, url in enumerate(URLS, start=1):
            send_message(f"🔍 Checking {idx}/{len(URLS)}")

            status = "NO"
            try:
                page.goto(url, timeout=45000, wait_until="domcontentloaded")
                status = "YES"
            except Exception as e:
                print("Navigation failed:", e)

            path = f"{SCREENSHOT_DIR}/{idx:02d}.png"
            screenshot_taken = False
            try:
                page.screenshot(path=path, timeout=10000)
                screenshot_taken = True
            except Exception as e:
                print("screenshot failed:", e)
            if screenshot_taken:
                send_photo(
                    path,
                    f"{idx}. {url}\nStatus: {status}\nChecked: {now_ist}"
                )
            else:
                send_message(
                    f"Screenshot failed\n{idx}. {url}\nStatus: {status}\nChecked: {now_ist}"
                )
            results.append((url, status))
            time.sleep(3)

        browser.close()


except Exception as e:
    send_message("❌ SCRIPT CRASHED")
    send_message(str(e))
    send_message(traceback.format_exc())
    sys.exit(1)

