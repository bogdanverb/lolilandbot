import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def run_bot(login, password):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://loliland.ru")

        time.sleep(3)

        print(f"Login: {login}")
        # тут потом добавим реальные действия

    finally:
        driver.quit()


def main():
    i = 1
    while True:
        login = os.getenv(f"LOGIN_{i}")
        password = os.getenv(f"PASSWORD_{i}")

        if not login or not password:
            break

        run_bot(login, password)
        i += 1


if __name__ == "__main__":
    main()
