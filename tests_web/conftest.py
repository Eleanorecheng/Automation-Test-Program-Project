from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import logging
import allure
from allure_commons.types import AttachmentType


@pytest.fixture()
def driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('http://54.201.140.239/')
    yield driver
    allure.attach(driver.get_screenshot_as_png(), name="Logo_Screenshot", attachment_type=AttachmentType.PNG)
    driver.quit()

    def scroll_to_load_all_product(self):
        current_num = 0
        while True:
            self.scroll_down()
            elem = self.find_element(
                (By.XPATH, f"//div[@class='products' and count(a) > {current_num}]"),
            )
            current_product_list = self.find_elements(self.result_product_title_list)
            if elem is None:
                return current_product_list
            else:
                current_num = len(current_product_list)