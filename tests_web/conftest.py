from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import allure
from allure_commons.types import AttachmentType
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture()
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(os.getenv("DOMAIN"))
    yield driver
    allure.attach(driver.get_screenshot_as_png(), name="Logo_Screenshot", attachment_type=AttachmentType.PNG)
    driver.quit()


@pytest.fixture()
def db_cursor():
    db = mysql.connector.connect(
        host=os.getenv("DBHOST"),
        port=os.getenv("DBPORT"),
        user=os.getenv("DBUSER"),
        passwd=os.getenv("DBPASSWD"),
        database=os.getenv("DBDATABASE")
    )
    cursor = db.cursor(dictionary=True)
    yield cursor
    cursor.close()
    db.close()



