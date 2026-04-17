import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    print("Creating Chrome driver...")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 🔥 анти-детект
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    # убираем selenium detection
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


def random_delay(a=1, b=3):
    t = random.uniform(a, b)
    print(f"Sleeping {t:.2f}s")
    time.sleep(t)


def run_account(login, password):
    print(f"\n=== START ACCOUNT: {login} ===")

    driver = create_driver()

    try:
        print("Opening login page...")
        driver.get("https://loliland.ru/ru/login")

        wait = WebDriverWait(driver, 25)

        print("Waiting page load...")
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        time.sleep(5)

        print("Page source length:", len(driver.page_source))

        # 🔥 fallback поиск input
        print("Finding inputs (fallback)...")
        inputs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))

        print(f"Found {len(inputs)} inputs")

        login_input = None
        password_input = None

        for inp in inputs:
            t = inp.get_attribute("type")
            if t == "text" and not login_input:
                login_input = inp
            elif t == "password":
                password_input = inp

        if not login_input or not password_input:
            raise Exception("Inputs not found")

        print("Typing credentials...")

        login_input.clear()
        login_input.send_keys(login)

        password_input.clear()
        password_input.send_keys(password)

        random_delay(1, 2)

        # 🔥 поиск кнопки
        print("Finding login button...")

        buttons = driver.find_elements(By.TAG_NAME, "button")

        login_button = None
        for btn in buttons:
            if "Войти" in btn.text:
                login_button = btn
                break

        if not login_button:
            raise Exception("Login button not found")

        login_button.click()

        print("Clicked login")

        time.sleep(6)

        print("Login attempt finished")

    except Exception as e:
        print(f"ERROR for {login}: {str(e)}")

        driver.save_screenshot("error.png")
        print("Screenshot saved")

    finally:
        driver.quit()
        print("Driver closed")


def main():
    print("=== BOT STARTED ===")

    accounts = []

    i = 1
    while True:
        login = os.getenv(f"LOGIN_{i}")
        password = os.getenv(f"PASSWORD_{i}")

        if not login or not password:
            break

        accounts.append((login, password))
        i += 1

    print(f"Found {len(accounts)} accounts")

    if not accounts:
        print("No accounts found. Exiting.")
        return

    for login, password in accounts:
        run_account(login, password)

    print("=== BOT FINISHED ===")


if __name__ == "__main__":
    main()
