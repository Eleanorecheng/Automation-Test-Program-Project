import pytest

from api_objects.create_product_api import CreateProductsAPI
from api_objects.delete_product_api import DeleteProductAPI
from utils.common_handler import APICommonHandler
from utils.database_utils import DatabaseUtil

from test_data.test_data_from_excel import TestData
import allure

test_data = TestData()


@allure.story("Scenario: Test Create Product Success")
@pytest.mark.parametrize('product_data', test_data.read_data('API Create Product Success'))
def test_create_product_success(session, db_cursor, default_api_login, product_data, request):
    create_product_api = CreateProductsAPI(session)
    delete_product_api = DeleteProductAPI(session)
    api_command_handlr = APICommonHandler()
    database_utils = DatabaseUtil()

    with allure.step("Send create product API request and check status = 200"):
        info = create_product_api.create_product(product_data)
        api_command_handlr.assertion(info.response.status_code, 200)

    with allure.step("Get Product_id"):
        product_id = info.get_json('data')['product_id']
        assert product_id

    with allure.step("Verify response is correct by comparing with DB"):
        db_data = database_utils.get_product_info_by_id_from_db(db_cursor, product_id)
        # 因為 db 撈不到缺 other_images 的情況，所以把 '' 拿掉比對
        payload = create_product_api.arrange_payload(product_data)
        if '' in payload['other_images']:
            payload['other_images'].remove('')
        assert db_data == payload

    def delete_product_finalizer():
        with allure.step("Delete product and check delete alert"):
            delete_product_api.delete_product(product_id)

    request.addfinalizer(delete_product_finalizer)


@allure.story("Scenario: Test Create Product Fail")
@pytest.mark.parametrize('product_data', test_data.read_data('API Create Product Failed'))
def test_create_product_fail(session, db_cursor, default_api_login, product_data, request):
    create_product_api = CreateProductsAPI(session)
    delete_product_api = DeleteProductAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send create product API request and check status code"):
        info = create_product_api.create_product(product_data)
        api_command_handlr.assertion(info.response.status_code, 400)
        api_command_handlr.assertion(info.get_json('errorMsg'), product_data['Error Msg'])

    with allure.step("Delete product if product_id exists"):
        try:
            product_id = info.get_json('data')['product_id']
            def delete_product_finalizer():
                with allure.step("Delete product and check delete alert"):
                    delete_product_api.delete_product(product_id)

            request.addfinalizer(delete_product_finalizer)
        except:
            pass

@allure.story("Scenario: Test Create Product Without Login")
@pytest.mark.parametrize('product_data', test_data.read_data('API Create Product Success'))
@pytest.mark.parametrize('authorization_data', test_data.read_data('API Invalid Authorization'))

def test_create_product_with_invalid_access(session, product_data, authorization_data, request):
    create_product_api = CreateProductsAPI(session)
    delete_product_api = DeleteProductAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Set token to invalid"):
        session.headers["Authorization"] = authorization_data['authorization']

    with allure.step("Send create product API request and check status code"):
        info = create_product_api.create_product(product_data)
        api_command_handlr.assertion(info.response.status_code, authorization_data['status_code'])
        api_command_handlr.assertion(info.get_json('errorMsg'), authorization_data['err_msg'])

    with allure.step("Delete product if product_id exists"):
        try:
            product_id = info.get_json('data')['product_id']
            def delete_product_finalizer():
                with allure.step("Delete product and check delete alert"):
                    delete_product_api.delete_product(product_id)

            request.addfinalizer(delete_product_finalizer)
        except:
            pass