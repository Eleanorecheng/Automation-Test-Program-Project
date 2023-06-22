import os
import pytest
from api_objects.order_api import OrderAPI
from utils.common_handler import APICommonHandler
from utils.database_utils import DatabaseUtil

from test_data.test_data_from_excel import TestData
import allure

test_data = TestData()


@allure.story("Scenario: Test Order Success")
@pytest.mark.parametrize('order_data', test_data.read_data('API Checkout with Valid Value'))
def test_order_success(session, default_api_login, order_data):
    order_api = OrderAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send order API request and check status = 200"):
        info = order_api.order(order_data)
        api_command_handlr.assertion(info.response.status_code, 200)
        assert info.get_json("data")['number']


@allure.story("Scenario: Test Order Fail With Invalid Data")
@pytest.mark.parametrize('order_data', test_data.read_data('API Checkout with Invalid Value'))
def test_order_fail_with_invalid_data(session, default_api_login, order_data):
    order_api = OrderAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send order API request and check status = 400"):
        info = order_api.order(order_data)
        api_command_handlr.assertion(info.response.status_code, 400)
        api_command_handlr.assertion(info.get_json('errorMsg'), order_data["Alert Msg"])


@allure.story("Scenario: Test Order Fail Without Login")
@pytest.mark.parametrize('order_data', test_data.read_data('API Checkout with Valid Value'))
def test_order_fail_without_login(session, order_data):
    order_api = OrderAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send order API request and check status = 401"):
        info = order_api.order(order_data)
        api_command_handlr.assertion(info.response.status_code, 401)
        api_command_handlr.assertion(info.get_json('errorMsg'), "Unauthorized")


@allure.story("Scenario: Test Get Order Success")
@pytest.mark.parametrize('order_data', test_data.read_data('API Checkout with Valid Value'))
def test_get_order_success(session, default_api_login, order_data):
    order_api = OrderAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send order API request and check status = 200"):
        info = order_api.order(order_data)
        api_command_handlr.assertion(info.response.status_code, 200)

    with allure.step("Get order info by order_id and check status = 200"):
        order_id = info.get_json("data")['number']
        order_info = order_api.get_order_info(order_id)
        api_command_handlr.assertion(order_info.response.status_code, 200)

    with allure.step("Verify order details"):
        # 驗證 number, details[list], details[freight, payment shipping], details[recipient]
        order_number = order_info.get_json("data")['number']
        order_details_list = order_info.get_json("data")['details']['list'][0]
        order_details = order_info.get_json("data")['details']
        order_details_recipient = order_info.get_json("data")['details']['recipient']

        api_command_handlr.assertion(order_number, order_id)
        api_command_handlr.assertion(order_details_list['id'], order_data["Id"])
        api_command_handlr.assertion(order_details_list['qty'], int(order_data["Qty"]))
        api_command_handlr.assertion(order_details_list['name'], order_data["Name"])
        api_command_handlr.assertion(order_details_list['size'], order_data["Size"])
        api_command_handlr.assertion(order_details_list['color'], eval(order_data["Color"]))
        api_command_handlr.assertion(order_details_list['price'], int(order_data["Price"]))

        api_command_handlr.assertion(order_details['total'], int(order_data["Total"]))
        api_command_handlr.assertion(order_details['freight'], int(order_data["Freight"]))
        api_command_handlr.assertion(order_details['payment'], order_data["Payment"])
        api_command_handlr.assertion(order_details['shipping'], order_data["Shipping"])
        api_command_handlr.assertion(order_details['subtotal'], int(order_data["Subtotal"]))

        api_command_handlr.assertion(order_details_recipient['name'], order_data["Receiver"])
        api_command_handlr.assertion(order_details_recipient['time'], order_data["Deliver Time"])
        api_command_handlr.assertion(order_details_recipient['email'], order_data["Email"])
        api_command_handlr.assertion(order_details_recipient['phone'], order_data["Mobile"])
        api_command_handlr.assertion(order_details_recipient['address'], order_data["Address"])


@allure.story("Scenario: Test Get Order Failed")
@pytest.mark.parametrize("invalid_order_id, status_code, err_msg",
                         [(123, 400, "Order Not Found."), (-1, 400, "Please input correct id format."),
                          ("abc", 400, "Please input correct id format.")])
def test_get_order_fail(session, default_api_login, invalid_order_id, status_code, err_msg):
    order_api = OrderAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Get order info by order_id and check status"):
        info = order_api.get_order_info(invalid_order_id)
        api_command_handlr.assertion(info.response.status_code, status_code)
        api_command_handlr.assertion(info.get_json('errorMsg'), err_msg)

@allure.story("Scenario: Test Get Order Fail Without Login")
def test_get_order_fail_without_login(session):
    order_api = OrderAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Get order info by order_id and check status"):
        info = order_api.get_order_info(314562783901)
        api_command_handlr.assertion(info.response.status_code, 401)
        api_command_handlr.assertion(info.get_json('errorMsg'), "Unauthorized")