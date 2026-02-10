'''from playwright.sync_api import sync_playwright, TimeoutError
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
GROUP_CHAT_ID = -1003625299691   # supergroup ID

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
                "--disable-gpu"
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
    sys.exit(1)'''

from playwright.sync_api import sync_playwright, TimeoutError
import os
import time
import requests
from datetime import datetime
import pytz
from datetime import date
from datetime import timedelta

ACCOMMODATION_TYPES = [
    ("Single Occupancy", "accomm_single"),
    ("Double Occupancy", "accomm_double"),
    ("Triple Occupancy", "accomm_triple"),
]

DAY_INDEX = date.today().toordinal()
TODAY_ACCOMMODATION_NAME, TODAY_ACCOMMODATION_ID = (
    ACCOMMODATION_TYPES[DAY_INDEX % len(ACCOMMODATION_TYPES)]
)

# ================= TELEGRAM =================
BOT_TOKEN = "8347404520:AAEeTkAPPKsMH-7DN5gJMqk7NFVapaok_aA"
GROUP_CHAT_ID = "-5171687843"
#CAPTCHA_API_KEY = "dff02cab134c92646c704071d815d12b"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": GROUP_CHAT_ID, "text": text}, timeout=15)

def send_photo(path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(path, "rb") as f:
        requests.post(
            url,
            files={"photo": f},
            data={"chat_id": GROUP_CHAT_ID, "caption": caption},
            timeout=30
        )

# ================= CONFIG =================
TEST_URL = [
    #----DAY A----
    "https://www.publichealthworldconference.com", "https://www.diabetesworldconference.com", "https://www.internationalobesityconference.com",  "https://www.gynecologyworldconference.com", 
    "https://www.womenshealthconferences.com", "https://www.infectiousworldconference.com",  "https://www.vaccine-rnd.com",  "https://www.preventivemedicineconference.com",
    "https://www.pharmadrugresearchconference.com", "https://www.cosmetologyworldconference.com", "https://www.plasticsurgeryworldconference.com", "https://www.plantandmolecularconference.com", 
    "https://www.agricultureworldconference.com", "https://www.cellgenetherapyconference.com", "https://www.publichealthmidwifery.com", "https://www.dementiaworldconference.com",
    #----DAY B ----
    "https://www.addictionworldconference.com", "https://www.cancerglobalconference.com", "https://www.internationalneurologyconference.com", "https://www.psychiatryworldconference.com",
    "https://www.mental-healthconferences.precisionglobalcon.com", "https://www.pediatricsconferences.precisionglobalcon.com", "https://www.neonatalconference.precisionglobalcon.com", "https://www.cardiologyconferences.precisionglobalcon.com",
    "https://www.heartconferences.precisionglobalcon.com", "https://www.traditional-medicineconferences.precisionglobalcon.com",  "https://www.natural-therapiesconferences.precisionglobalcon.com",  "https://www.nanotechnologyconferences.precisionglobalcon.com",
    "https://www.materials-scienceconferences.precisionglobalcon.com", "https://www.globalnursingconference.com", "https://www.neurologyworldconference.com", "https://www.worldnursingresearchconference.com",
]

FALLBACK_ROLE_URLS = {
    "https://www.cancerglobalconference.com/registration",
    "https://www.pharmadrugresearchconference.com/registration",
    "https://www.cellgenetherapyconference.com/registration",
}

VACCINE_SPECIAL_URL = "https://www.vaccine-rnd.com/registration"

ROLE_OPTIONS_DEFAULT = [
    "Oral Presenter (In-Person)",
    "Oral Presenter (Virtual)",
    "Poster Presenter (In-Person)",
    "Poster Presenter (Virtual)",
    "Listener (In-Person)",
    "Listener (Virtual)",
    "Exhibitor/Sponsor (In-Person)",
    "Exhibitor/Sponsor (Virtual)",
]

ROLE_OPTIONS_FALLBACK = [
    "Academic",
    "Industry",
    "Student",
    "Government Agency",
    "Non-Profit",
    "Researcher",
    "Exhibitor/Sponsor (In-Person)",
    "Exhibitor/Sponsor (Virtual)",
    "Listener",
]
ROLE_OPTIONS_VACCINE = [
    "Academic",
    "Industry",
    "Student",
    "Government Agency",
    "Non-Profit",
    "Researcher",
    "Exhibitor/Sponsor (In-Person)",
    "Exhibitor/Sponsor (Virtual)",
    "Delegate / Listener",
]

 
today_index = date.today().toordinal()

if today_index % 2 == 0:
    DAILY_URLS = TEST_URL[:16]
    DAY_LABEL = "DAY A (links 1–16)"
else:
    DAILY_URLS = TEST_URL[16:]
    DAY_LABEL = "DAY B (links 17–32)"

import sys

SLOT = sys.argv[1] if len(sys.argv) > 1 else "slot1"

SLOT_MAP = {
    "slot1": DAILY_URLS[0:4],    # 9:00 AM
    "slot2": DAILY_URLS[4:8],    # 1:30 PM
    "slot3": DAILY_URLS[8:12],   # 5:30 PM
    "slot4": DAILY_URLS[12:16],  # 9:30 PM
}

URLS_TO_CHECK = SLOT_MAP.get(SLOT)
if not URLS_TO_CHECK:
    raise ValueError("Invalid slot")


print(f"📅 Running {DAY_LABEL}") 
SCREENSHOT_DIR = "/app/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

ist = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(ist).strftime("%d-%m-%Y %I:%M %p IST")

# ================= MAIN =================
def run_checker(TEST_URL):

    # IMPORTANT: reset summary PER URL
    summary = {
        "register_button": None,
        "pricing_option": None,
        "accommodation": None,
        "check_in": None,
        "check_out": None,
    }
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,   # MUST BE TRUE IN DOCKER
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()
        send_message("🧪 TEST MODE: Starting single-site registration flow")

        print("Opening site...")
        page.goto(TEST_URL, timeout=60000, wait_until="domcontentloaded")

        # ---------- STEP 1: CLICK REGISTER ----------

        clicked = False
   
        register_selectors = [
            "a:has-text('Register')",
            "button:has-text('Register')",
            "a:has-text('Buy Ticket')",
            "button:has-text('Buy Ticket')"
        ]

        for sel in register_selectors:
            try:
                page.locator(sel).first.scroll_into_view_if_needed()
                page.locator(sel).first.click(timeout=5000)
                page.wait_for_url("**registration**", timeout=20000)
                if "Buy Ticket" in sel:
                    summary["register_button"] = "BUY_TICKET"
                elif "button" in sel:
                    summary["register_button"] = "BUTTON_REGISTER"
                else:
                    summary["register_button"] = "LINK_REGISTER"
                print(f"Clicked register using selector: {sel}")
                clicked = True
                break
            except:
                continue
        if not clicked:
            send_message("❌ Register button not found")
            browser.close()
            exit(1)

        print("STEP 1.5: Waiting for registration form to appear")

        # Trigger lazy load
        for _ in range(5):
            page.mouse.wheel(0, 800)
            time.sleep(1)

        # Stable indicator
        page.wait_for_selector("text=Online Registration", timeout=30000)

        print("Registration form detected")
        
        # ================= STEP 2: Fill full basic form =================
        print("STEP 2: Filling basic registration form (SAFE SELECTORS)")

        # Wait until form is really visible
        page.wait_for_selector("input[placeholder='Name']", timeout=30000)

        # Name
        page.fill("input[placeholder='Name']", "PGC sites monitoring")

        # Email
        page.fill("input[placeholder='Email']", "sathya_prabhu90@outlook.com")

        # Alternative Email
        page.fill("input[placeholder='Alternative Email']", "sathya_prabhu90@outlook.com")

        # Phone
        page.fill("input[placeholder='Phone']", "9456781233")

        # WhatsApp
        page.fill("input[placeholder='WhatsApp Number']", "9456781233")

        # Country
        country_select = page.locator("select[name='country']")

        # Wait until the <select> exists and is visible
        country_select.wait_for(state="visible", timeout=30000)

        # Select the country by visible text
        country_select.select_option(label="India")  # use the exact visible country name

        # Debug: check value
        selected_country = page.eval_on_selector("select[name='country']", "el => el.value")
        print("✅ Country selected:", selected_country)


        # Fill Institution (autocomplete)

        inst_input = page.locator("input[name='institution']")

        inst_input.wait_for(state="attached", timeout=30000)
        inst_input.wait_for(state="visible", timeout=30000)


        # Fill the value
        inst_input.fill("pbi")


        # Trigger input/change events to ensure site registers it
        inst_input.evaluate("""
        el => {
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
        """)

        # Debug: check value
        inst_value = page.eval_on_selector(
            "input[name='institution']",
            "el => el.value"
        )
        print("✅ Institution entered:", inst_value)

        print("✅ STEP 2 OK – Basic registration form filled")
        print(f"URL: {TEST_URL}")
        print(f"Checked: {now_ist}")

        # ===========================================================
        # ================= STEP 3: Select Role =================

        print("STEP 3: Selecting pricing role (radio button)")

        from datetime import date

        # 🔀 Choose correct role list
        if TEST_URL == VACCINE_SPECIAL_URL:
            ROLE_OPTIONS = ROLE_OPTIONS_VACCINE
            print("Using VACCINE-SPECIFIC role list")
        elif TEST_URL in FALLBACK_ROLE_URLS:
            ROLE_OPTIONS = ROLE_OPTIONS_FALLBACK
            print("Using FALLBACK role list")
        else:
            ROLE_OPTIONS = ROLE_OPTIONS_DEFAULT
            print("Using DEFAULT role list")

        today_index = date.today().toordinal()
        ROLE_TEXT = ROLE_OPTIONS[today_index % len(ROLE_OPTIONS)]

        print(f"Today's pricing role: {ROLE_TEXT}")

        # Scroll to pricing section
        page.locator("text=Early Bird Registration").scroll_into_view_if_needed()
        time.sleep(1)

        label = page.locator(
            "section:has-text('Early Bird') label",
            has_text=ROLE_TEXT
        )

        if label.count() == 0:
            raise Exception(
                f"Pricing role '{ROLE_TEXT}' not found on page for {TEST_URL}"
            )

        label.first.click()
        summary["pricing_option"] = ROLE_TEXT

        print("Pricing role selected:", ROLE_TEXT)
            
        # ===================== STEP 4: Select Accommodation =====================

        print("STEP 4: Selecting accommodation")
        # -------------------------------
        # Pick accommodation automatically
        # -------------------------------

        today_index = date.today().toordinal()
        ACC_TEXT, ACC_RADIO_ID = ACCOMMODATION_TYPES[
            today_index % len(ACCOMMODATION_TYPES)
        ]
        print(f"Today's accommodation: {ACC_TEXT}")

        # Scroll to section
        acc_header = page.locator("text=Looking for Accommodation")
        acc_header.scroll_into_view_if_needed()
        time.sleep(1)
        acc_header.click()
        time.sleep(1)

        # -------------------------------
        # Click accommodation via label
        # -------------------------------
        print(f"Resolved radio id: {ACC_RADIO_ID}")

        page.evaluate("""
        (radioId) => {
          const label = document.querySelector(`label[for='${radioId}']`);
          if (!label) throw new Error("Accommodation label not found");
          label.scrollIntoView({ behavior: "smooth", block: "center" });
          label.click();
        }
        """, ACC_RADIO_ID)

        # -------------------------------
        # Wait until accommodation is checked
        # -------------------------------
        page.wait_for_function("""
        () => document.querySelector("input[name='accomm']:checked") !== null 
        """, timeout=10000)

        # -------------------------------
        # Read back selected accommodation (truth source)
        # -------------------------------
        acc_selected = page.locator("input[name='accomm']:checked")
        selected_id = acc_selected.first.get_attribute("id")

        selected_label = page.locator(
            f"label[for='{selected_id}']"
        ).inner_text().strip()

        summary["accommodation"] = selected_label.split("-")[0].strip()

        print("Accommodation selected successfully:", summary["accommodation"])

        time.sleep(1)
        print("Accommodation selected successfully")
        # ---- Accommodation dates ----
        print("📅 Selecting accommodation dates automatically")

        # --- Wait until check-in options are available ---
        page.wait_for_function("""
        () => {
            const el = document.querySelector('#checkin');
            return el && el.options && el.options.length > 1;
        }
        """, timeout=20000)

        checkin_value = page.locator("#checkin option").nth(1).get_attribute("value")

        # --- Force select check-in via JS ---
        page.evaluate("""
        (value) => {
            const el = document.querySelector('#checkin');
            el.value = value;
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
        """, checkin_value)

        print("✅ Check-in selected (JS):", checkin_value)

        # --- Wait for checkout options to populate ---
        page.wait_for_timeout(500)

        page.wait_for_function("""
        () => {
            const el = document.querySelector('#checkout');
            return el && el.options && el.options.length > 1;
        }
        """, timeout=20000)

        checkout_value = page.locator("#checkout option").nth(1).get_attribute("value")

        # --- Force select check-out via JS --- 
        page.evaluate("""
        (value) => {
            const el = document.querySelector('#checkout');
            el.value = value;
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
        """, checkout_value)

        print("✅ Check-out selected (JS):", checkout_value)
        summary["check_in"] = checkin_value
        summary["check_out"] = checkout_value

        print("✅ STEP 4 OK – Accommodation selected")
        print(f"Check-in: {checkin_value}") 
        print(f"Check-out: {checkout_value}")
        print(f"URL: {TEST_URL}")
        print(f"Checked: {now_ist}")

        # STEP 5: Solve CAPTCHA (FINAL)
  
        print("STEP 5: Checking for TEXT CAPTCHA")
 
        captcha_text_el = page.locator("span.input-group-addon")
        captcha_input = page.locator("#captcha-input")

        if captcha_text_el.count() > 0 and captcha_input.count() > 0:
            captcha_text = captcha_text_el.inner_text().strip()
            print("🔐 CAPTCHA text found:", captcha_text)

            captcha_input.wait_for(state="visible", timeout=5000)
            captcha_input.fill("")
            captcha_input.type(captcha_text, delay=120)

            captcha_input.evaluate("""
            el => {
                el.focus();
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.dispatchEvent(new Event('blur', { bubbles: true }));
            }
            """)


            page.wait_for_timeout(500)

            print("✅ CAPTCHA filled successfully")
        else:
            print("ℹ️ No CAPTCHA present on page")

        print("STEP 6: Clicking Proceed button")

        page.locator("button:has-text('Proceed To Register')").click()

        # ================= STEP 7: Click Pay Now & Screenshot NEXT page =================
        print("STEP 7: Clicking Pay Now and capturing NEXT page")

        print(">>> ENTERED STEP 7")

        pay_now = page.locator("span#buttonText")

        # Wait until Pay Now is visible
        pay_now.wait_for(state="visible", timeout=30000)
        print("Clicking Pay Now")

        # Click Pay Now (DO NOT wait for networkidle)
        pay_now.click()

        # 🔑 Instead, wait for DOM change or short settle time
        time.sleep(4)  # allow iframe / redirect / JS render

        # Optional: wait for URL change (non-blocking)
        try:
            page.wait_for_url("**", timeout=5000)
        except:
            pass

        print("Capturing payment page screenshot")

        final_path = f"{SCREENSHOT_DIR}/final_payment_page.png"
        page.screenshot(path=final_path, full_page=True)

        send_photo(
            final_path,
            f"✅ PAYMENT PAGE REACHED\n{TEST_URL}\nChecked: {now_ist}"
        )
   
        def build_summary_text():
            return f"""
        🧾 DAILY REGISTRATION SUMMARY

        🔘 Register Button:
       {summary['register_button']}

       🎟  Pricing Option:
       {summary['pricing_option']}
 
        🏨 Accommodation:
       {summary['accommodation']}
       Check-in: {summary['check_in']}
       Check-out: {summary['check_out']}
       """.strip()
  
        # ---- DAILY SUMMARY ----
        summary_text = build_summary_text()
        print(summary_text)
        send_message(summary_text)

        browser.close()

if __name__ == "__main__":
    for TEST_URL in URLS_TO_CHECK:
        print(f"🔍 Checking URL: {TEST_URL}")
        run_checker(TEST_URL)
