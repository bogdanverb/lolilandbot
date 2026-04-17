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
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    return driver


def wait_and_find(driver, by, selector, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )


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

        wait = WebDriverWait(driver, 20)

        print("Waiting page load...")
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        time.sleep(3)

        print("Finding login input...")

        login_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@placeholder='Игровой никнейм']"
        )))

        password_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@placeholder='Пароль']"
        )))

        print("Typing credentials...")

        login_input.send_keys(login)
        password_input.send_keys(password)

        time.sleep(2)

        print("Finding login button...")

        login_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(., 'Войти')]"
        )))

        login_button.click()

        print("Clicked login")

        time.sleep(5)

        print("Login attempt finished")

    except Exception as e:
        print(f"ERROR for {login}: {str(e)}")

        # 🔥 ВАЖНО: скриншот при ошибке
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
