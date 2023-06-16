import os
import pytest
from api_objects.login_api import LoginAPI
from api_objects.logout_api import LogoutAPI
from api_objects.profile_api import ProfileAPI
from utils.common_handler import APICommonHandler
from utils.database_utils import DatabaseUtil

from test_data.test_data_from_excel import TestData
import allure

test_data = TestData()


@allure.story("Scenario: Test Login Success")
def test_login_success(session, db_cursor):
    login_api = LoginAPI(session)
    api_command_handlr = APICommonHandler()
    database_utils = DatabaseUtil()

    with allure.step("Send Login API request and check status = 200"):
        info = login_api.login('native', os.getenv("EMAIL"), os.getenv("PASSWORD"))
        response_json = info.get_json("data")
        assert info.response.status_code == 200, api_command_handlr.assert_message(info.response.status_code, 200)

    with allure.step("Get DB data"):
        db_response = database_utils.get_user_result_from_db(db_cursor, os.getenv("EMAIL"))

    with allure.step("Verify response is correct"):
        assert response_json['access_token'] == db_response['access_token'], api_command_handlr.assert_message(
            response_json['access_token'], db_response['access_token'])
        # assert user_api.parse_datetime(response['login_at']) == db_response['login_at'] # 時間 parse 後秒數有誤差無法比對
        assert response_json['user']['id'] == db_response['id']
        assert response_json['user']['provider'] == db_response['provider']
        assert response_json['user']['name'] == db_response['name']
        assert response_json['user']['email'] == db_response['email']
        assert response_json['user']['picture'] == db_response['picture']


@allure.story("Scenario: Test Login Failed")
@pytest.mark.parametrize('invalid_login_data', test_data.read_data('API Login with Invalid Value'))
def test_login_fail(session, invalid_login_data):
    login_api = LoginAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send Login API request"):
        Info = login_api.login(invalid_login_data['Provider'], invalid_login_data['Email'],
                               invalid_login_data['Password'])

    with allure.step("Verify status code = 400 and error msg"):
        assert Info.response.status_code == 400, api_command_handlr.assert_message(Info.response.status_code, 400)
        assert Info.get_json('errorMsg') == invalid_login_data['Message'], api_command_handlr.assert_message(
            Info.get_json('errorMsg'), invalid_login_data['Message'])


@allure.story("Scenario: Test Logout Success")
def test_logout_success(session, default_api_login):
    logout_api = LogoutAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send Logout API request"):
        request = logout_api.logout()

    with allure.step("Verify status code = 200"):
        assert request.response.status_code == 200, api_command_handlr.assert_message(request.response.status_code, 200)
        assert request.get_json('message') == 'Logout Success', api_command_handlr.assert_message(
            request.get_json('message'),
            'Logout Success')


@allure.story("Scenario: Test Logout Failed")
@pytest.mark.parametrize("invalid_token, status_code, err_msg", [("", 401, "Unauthorized"), ("123", 403, "Forbidden")])
def test_logout_fail(session, default_api_login, invalid_token, status_code, err_msg):
    logout_api = LogoutAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Set token to invalid"):
        session.headers["Authorization"] = invalid_token

    with allure.step("Send Logout API request"):
        request = logout_api.logout()

    with allure.step("Verify status code = 401/403"):
        assert request.response.status_code == status_code, api_command_handlr.assert_message(
            request.response.status_code,
            status_code)
        assert request.get_json('errorMsg') == err_msg, api_command_handlr.assert_message(request.get_json('errorMsg'),
                                                                                          err_msg)


@allure.story("Scenario: Test Profile Success")
def test_profile_success(session, default_api_login, db_cursor):
    profile_api = ProfileAPI(session)
    api_command_handlr = APICommonHandler()
    database_utils = DatabaseUtil()

    email = default_api_login["email"]  # default_api_login 回傳 payload, 其中的 email 作為查詢 db 用

    with allure.step("Send profile API request and check status = 200"):
        info = profile_api.profile()
        response_json = info.get_json("data")
        assert info.response.status_code == 200, api_command_handlr.assert_message(info.response.status_code, 200)

    with allure.step("Get DB data"):
        db_response = database_utils.get_user_result_from_db(db_cursor, email)

    with allure.step("Verify response is correct"):
        assert response_json['provider'] == db_response['provider']
        assert response_json['name'] == db_response['name']
        assert response_json['email'] == db_response['email']
        assert response_json['picture'] == db_response['picture']


@allure.story("Scenario: Test Profile Fail")
@pytest.mark.parametrize("Invalid_token, Status_code, Err_msg", [("", 401, "Unauthorized"), ("123", 403, "Forbidden")])
def test_profile_fail(session, default_api_login, Invalid_token, Status_code, Err_msg):
    profile_api = ProfileAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Set token to invalid"):
        session.headers["Authorization"] = Invalid_token

    with allure.step("Send Profile API request"):
        request = profile_api.profile()

    with allure.step("Verify status code = 401/403"):
        assert request.response.status_code == Status_code, api_command_handlr.assert_message(
            request.response.status_code,
            Status_code)
        assert request.get_json('errorMsg') == Err_msg, api_command_handlr.assert_message(request.get_json('errorMsg'),
                                                                                          Err_msg)
