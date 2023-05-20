# When go to stylish website.
# Then stylish logo should be shown.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import allure
from allure_commons.types import AttachmentType

import logging

# 創立 logger 記錄器，指定級別
logger = logging.getLogger()
logger.setLevel(logging.INFO)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)


@allure.step("Check whether logo element shows: ")
def test_logo_is_shown():
    # Chromedriver in Headless Mode (為了截圖先拿掉了)
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get('http://54.201.140.239/')
        logo_shows = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[@class='header__logo']")
        )).is_displayed()
        assert logo_shows, f'Logo does not display'
        # 印出 log information 在 allure report
        logger.info('Logged INFO message')
        allure.attach(driver.get_screenshot_as_png(), name="Logo_Screenshot", attachment_type=AttachmentType.PNG)
    except:
        logger.error('Logged ERROR message')
    finally:
        driver.quit()
