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
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('http://54.201.140.239/')
    yield driver
    driver.close()

@pytest.fixture()
def logger():
    logger = logging.getLogger()
    return logger

@pytest.fixture()
def allure_screenshot():
    allure.attach(driver.get_screenshot_as_png(), name="Logo_Screenshot", attachment_type=AttachmentType.PNG)