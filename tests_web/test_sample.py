# When go to stylish website.
# Then stylish logo should be shown.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import allure

import logging

# 創立 logger 記錄器，指定級別
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 截圖
import pyautogui


@allure.step("Check whether logo element shows: ")
def set_driver():
    # Chromedriver in Headless Mode (為了截圖先拿掉了)
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)
    return driver, wait


def element_shown(path):
    driver, wait = set_driver()
    try:
        driver.get('http://54.201.140.239/')
        logo_shows = wait.until(EC.presence_of_element_located(
            (By.XPATH, path)
        ))
        # 設想是在logo出現後driver quit前做截圖，但放在這邊是不是有點怪..
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(r'../screenshot.png')
        # 印出 log information 在 allure report
        logger.info('Logged INFO message')
    finally:
        driver.quit()


def test_logo():
    path = "//*[@class='header__logo']"
    element_shown(path)
