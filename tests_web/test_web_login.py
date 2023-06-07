import os
import pytest
from page_objects.login_page import LoginPage
import allure
import logging
logger = logging.getLogger()


@allure.story("Scenario: Login and Logout Success")
@pytest.mark.parametrize("login", [{"email": os.environ.get('EMAIL'), "password": os.environ.get('PASSWORD')}],
                         indirect=True)  # indirect=True 代表 pytest 惠譽找相對應的 fixture 名稱使用
def test_login_out_success(driver, login, db_cursor):
    login_page = LoginPage(driver)

    with allure.step("Check login success alert and redirect to profile page"):
        get_alert = login_page.get_alert_message()
        assert get_alert == "Login Success", f'Wrong alert message: {get_alert}'
        login_page.accept_alert()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/profile.html"

    with allure.step("Check jwt token exists"):
        assert login_page.get_local_storage("jwtToken") != None, f'Cannot find jwt token'

    with allure.step("Logout in /profile.html"):
        login_page.click_logout_btn()

    with allure.step("Check logout success alert"):
        get_alert = login_page.get_alert_message()
        assert get_alert == "Logout Success", f'Wrong alert message: {get_alert}'
        login_page.accept_alert()

    with allure.step("Check jwt token is removed from both local storage and db"):
        assert login_page.get_local_storage("jwtToken") == None, f'Show jwt token in local storage: {login_page.get_jwt_token("jwtToken")}'
        assert login_page.get_access_token_from_db(
            db_cursor) == "", f'jwt token in db: {login_page.get_access_token_from_db(db_cursor)}'


@allure.story("Scenario: Login Failed with incorrect email or password")
@pytest.mark.parametrize("login", [{"email": "echeng@netbase.com", "password": "12345"}],
                         indirect=True)  # indirect=True 代表 pytest 惠譽找相對應的 fixture 名稱使用
def test_login_fail_incorrect_email_psd(driver, login):
    login_page = LoginPage(driver)

    with allure.step("Check login fail alert"):
        get_alert = login_page.get_alert_message()
        assert get_alert == "Login Failed", f'Wrong alert message: {get_alert}'
        login_page.accept_alert()


@allure.story("Scenario: Login with invalid access token")
@pytest.mark.parametrize("login", [{"email": os.environ.get('EMAIL'), "password": os.environ.get('PASSWORD')}],
                         indirect=True)  # indirect=True 代表 pytest 惠譽找相對應的 fixture 名稱使用
def test_login_fail_invalid_token(driver, login):
    login_page = LoginPage(driver)

    with allure.step("Successfully Login"):
        login_page.get_alert_message()
        login_page.accept_alert()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/profile.html"

    with allure.step("Get jwt token in local storage"):
        jwtToken = login_page.get_local_storage("jwtToken")

    with allure.step("Successfully Logout"):
        login_page.click_logout_btn()
        login_page.get_alert_message()
        login_page.accept_alert()

    with allure.step("Use jwt token to access /profile.html"):
        driver.get(f"{os.getenv('DOMAIN')}/login.html")
        login_page.set_local_storage("jwtToken", jwtToken)
        driver.get(f"{os.getenv('DOMAIN')}/profile.html")

    with allure.step("Show Invalid Access Token alert"):
        get_alert = login_page.get_alert_message()
        assert get_alert == "Invalid Access Token", f'Wrong alert message: {get_alert}'
        login_page.accept_alert()
