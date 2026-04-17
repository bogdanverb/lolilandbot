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

        random_delay()

        print("Waiting for login input...")
        login_input = wait_and_find(
            driver, By.XPATH, "//input[contains(@placeholder, 'никнейм')]"
        )

        password_input = wait_and_find(
            driver, By.XPATH, "//input[contains(@placeholder, 'Пароль')]"
        )

        print("Typing credentials...")
        login_input.clear()
        login_input.send_keys(login)

        password_input.clear()
        password_input.send_keys(password)

        random_delay()

        print("Clicking login button...")
        login_button = wait_and_find(
            driver, By.XPATH, "//button[contains(text(), 'Войти')]"
        )
        login_button.click()

        random_delay(3, 5)

        print("Login attempt finished")

        # 👉 ТУТ ПОТОМ ДОБАВИМ БОНУС
        print("Trying to find bonus button (not implemented yet)...")

        print("Finished account")

    except Exception as e:
        print(f"ERROR for {login}: {str(e)}")

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
