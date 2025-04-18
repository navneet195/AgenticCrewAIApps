import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class Driver:
    def __init__(self, url, cookie=None, browser="chrome"):
        self.driver = self._create_driver(url, cookie, browser)

    def navigate(self, url, wait=3):
        self.driver.get(url)
        time.sleep(wait)

    def scroll_to_bottom(self, wait=3):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait)

    def get_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def get_elements(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    def fill_text_field(self, selector, text):
        element = self.get_element(selector)
        element.clear()
        element.send_keys(text)

    def click_button(self, selector):
        element = self.get_element(selector)
        element.click()

    def _create_driver(self, url, cookie, browser):
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--headless")  # Uncomment if you want headless Chrome
            driver = webdriver.Chrome(executable_path='/opt/homebrew/bin/chromedriver', options=options)
        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")  # Uncomment if you want headless Firefox
            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.get(url)
        if cookie:
            driver.add_cookie(cookie)
        return driver

    def close(self):
        self.driver.close()
