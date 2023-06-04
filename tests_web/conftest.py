import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import allure
from allure_commons.types import AttachmentType
import mysql.connector
import os
from dotenv import load_dotenv
from page_objects.loginout_page import LoginoutPage

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
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

@pytest.fixture()
def login(driver, request):
    driver.get(f"{os.getenv('DOMAIN')}/login.html")

    loginout_page = LoginoutPage(driver)
    # request 為固定寫法，用於接收 parametrize 中傳入的數值, 即為 {"email": os.environ.get('EMAIL'), "password": os.environ.get('PASSWORD')}
    email = request.param.get("email")
    password = request.param.get("password")

    with allure.step("Input email and password to login"):
        loginout_page.input_email_and_password_to_login(email, password)
        time.sleep(1) # 不放的話抓不到 alert message --> "error":"no such alert"

