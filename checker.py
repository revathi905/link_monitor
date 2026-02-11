import requests
from datetime import datetime
import pytz
from playwright.sync_api import sync_playwright

# ===== HARD CODED LINKS =====
URLS = [
    "https://www.publichealthworldconference.com/",
    "https://www.diabetesworldconference.com/",
    "https://www.internationalobesityconference.com/",
    "https://www.gynecologyworldconference.com/",
    "https://www.womenshealthconferences.com/",
    "https://www.infectiousworldconference.com/",
    "https://www.vaccine-rnd.com/",
    "https://www.preventivemedicineconference.com/",
    "https://www.pharmadrugresearchconference.com/",
    "https://www.cosmetologyworldconference.com/",
    "https://www.plasticsurgeryworldconference.com/",
    "https://www.plantandmolecularconference.com/",
    "https://www.agricultureworldconference.com/",
    "https://www.cellgenetherapyconference.com/",
    "https://www.publichealthmidwifery.com/",
    "https://www.dementiaworldconference.com/",
    "https://www.addictionworldconference.com/",
    "https://www.cancerglobalconference.com/",
    "https://www.internationalneurologyconference.com/",
    "https://www.psychiatryworldconference.com/",
    "https://www.mental-healthconferences.precisionglobalcon.com/",
    "https://www.pediatricsconferences.precisionglobalcon.com/",
    "https://www.neonatalconference.precisionglobalcon.com/",
    "https://www.cardiologyconferences.precisionglobalcon.com/",
    "https://www.heartconferences.precisionglobalcon.com/",
    "https://www.traditional-medicineconferences.precisionglobalcon.com/",
    "https://www.natural-therapiesconferences.precisionglobalcon.com/",
    "https://www.nanotechnologyconferences.precisionglobalcon.com/",
    "https://www.materials-scienceconferences.precisionglobalcon.com/",
    "https://www.globalnursingconference.com/",
    "https://www.neurologyworldconference.com/",
    "https://www.worldnursingresearchconference.com/",
    "https://www.precisionbusinessinsights.com/",
]

def get_links():
    return URLS

# ===== TELEGRAM CONFIG =====
BOT_TOKEN = "8347404520:AAEeTkAPPKsMH-7DN5gJMqk7NFVapaok_aA"
CHAT_ID = "-1003625299691"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


# ===== CHECK LOGIC =====
def check_url(page, url):
    try:
        page.goto(
            url,
            timeout=45000,
            wait_until="load"
        )
        return True
    except Exception:
        return False


def check_with_retry(page, url, retries=2):
    for attempt in range(retries):
        if check_url(page, url):
            return True
        print(f"Retrying {url} ({attempt + 1}/{retries})")
    return False


# ===== MAIN EXECUTION FUNCTION =====
def run_checker():
    working = []
    failed = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        for url in URLS:
            page = browser.new_page()
            try:
                if check_with_retry(page, url):
                    working.append(url)
                else:
                    failed.append(url)
            finally:
                page.close()

        browser.close()

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist).strftime("%d-%m-%Y %I:%M %p IST")

    if failed:
        message = (
            "❌ SUMMARY REPORT\n"
            f"Checked at: {now}\n\n"
            "Down websites:\n"
            + "\n".join(failed)
        )
    else:
        message = (
            "✅ SUMMARY REPORT\n"
            f"Checked at: {now}\n\n"
            f"All {len(working)} websites are working fine"
        )

    send_telegram(message)


# ===== IMPORTANT MAIN GUARD =====
if __name__ == "__main__":
    run_checker()









