from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import allure
from allure_commons.types import AttachmentType
import mysql.connector
import os
from dotenv import load_dotenv
from page_objects.login_page import LoginPage

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

    login_page = LoginPage(driver)
    # request 為固定寫法，用於接收 parametrize 中傳入的數值, 即為 {"email": os.environ.get('EMAIL'), "password": os.environ.get('PASSWORD')}
    email = request.param.get("email")
    password = request.param.get("password")

    with allure.step("Input email and password to login"):
        login_page.input_email_and_password_to_login(email, password)

@pytest.fixture()
def login_in_parallel(driver, worker_id):
    driver.get(f"{os.getenv('DOMAIN')}/login.html")
    login_page = LoginPage(driver)

    worker_id = os.environ.get('PYTEST_XDIST_WORKER')
    if worker_id == 'gw0':
        email = os.environ.get('EMAIL_1')
        password = os.environ.get('PASSWORD_1')
    elif worker_id == 'gw1':
        email = os.environ.get('EMAIL_2')
        password = os.environ.get('PASSWORD_2')
    else:
        email = os.environ.get('EMAIL')
        password = os.environ.get('PASSWORD')

    with allure.step("Input email and password to login"):
        login_page.input_email_and_password_to_login(email, password)
        get_alert = login_page.get_alert_message()
        assert get_alert == "Login Success", f'Wrong alert message'
        login_page.accept_alert()