import os
import pytest
from api_objects.products_api import ProductsAPI
from api_objects.products_details_api import ProductsDetailsAPI
from api_objects.products_search_api import ProductsSearchAPI

from utils.common_handler import APICommonHandler
from utils.database_utils import DatabaseUtil
import allure


@allure.story("Scenario: Test Get Products With Valid Category")
@pytest.mark.parametrize("category, paging",
                         [("women", 0), ("women", 1), ("women", 2), ("men", 0), ("men", 1), ("accessories", 0),
                          ("accessories", 1)])
def test_products_with_valid_category(session, db_cursor, default_api_login, category, paging):
    products_api = ProductsAPI(session)
    api_command_handlr = APICommonHandler()
    database_utils = DatabaseUtil()

    with allure.step("Send products API request and check status = 200"):
        info = products_api.products_by_category(category, paging)
        response_json = info.get_json("data")
        api_command_handlr.assertion(info.response.status_code, 200)

    with allure.step("Get product_id by category in db and check # of products <= 6"):
        db_products_ids = database_utils.get_products_ids_by_category(db_cursor, category, paging)
        if paging != "":
            assert len(db_products_ids) <= 6, f'Expected Result: {len(db_products_ids)}, Actual Result: 6'

    with allure.step("Compare ids from db and response"):
        response_ids = [id.get('id') for id in response_json]
        api_command_handlr.assertion(db_products_ids, response_ids)


    if response_json:
        with allure.step("Verify response is correct by comparing with DB (First data)"):
                # 拿到 first_id 去 db 下 query
                first_id = db_products_ids[0]
                # 用 first_id 去撈 product table
                db_product = database_utils.get_products_result_from_db(db_cursor, first_id)
                db_variants = database_utils.composite_variants(db_cursor, first_id)
                db_colors = database_utils.composite_color(db_cursor, first_id)
                db_sizes = database_utils.composite_size(db_cursor, first_id)
                db_main_image = database_utils.get_products_main_image_from_db(db_cursor, first_id)
                db_images = database_utils.get_products_images_result_from_db(db_cursor, first_id)

                # 拿到 response 的第一筆來根 db 比較
                first_response = response_json[0]
        with allure.step("Verify response of id, category, title, description, price, texture, wash, place, note, story"):
            api_command_handlr.assertion(first_response.get('id'), first_id)
            api_command_handlr.assertion(first_response.get('category'), db_product.get('category'))
            api_command_handlr.assertion(first_response.get('title'), db_product.get('title'))
            api_command_handlr.assertion(first_response.get('description'), db_product.get('description'))
            api_command_handlr.assertion(first_response.get('price'), db_product.get('price'))
            api_command_handlr.assertion(first_response.get('texture'), db_product.get('texture'))
            api_command_handlr.assertion(first_response.get('wash'), db_product.get('wash'))
            api_command_handlr.assertion(first_response.get('place'), db_product.get('place'))
            api_command_handlr.assertion(first_response.get('note'), db_product.get('note'))
            api_command_handlr.assertion(first_response.get('story'), db_product.get('story'))

        with allure.step("Verify response of main_image and images"):
            api_command_handlr.assertion(first_response.get('main_image'), db_main_image)
            api_command_handlr.assertion(first_response.get('images'), db_images)
        #
        with allure.step("Verify response of variants"):
            api_command_handlr.assertion(first_response.get('variants'), db_variants)

        with allure.step("Verify response of colors nad sizes"):
            api_command_handlr.assertion(first_response.get('colors'), db_colors)
            api_command_handlr.assertion(first_response.get('sizes'), db_sizes)

    else:
        api_command_handlr.assertion(response_json, [])

@allure.story("Scenario: Test Get Products With Invalid Category")
@pytest.mark.parametrize("category, paging", [("cats", 0), ("cats", "")])
def test_products_with_invalid_category(session, db_cursor, default_api_login, category, paging):
    products_api = ProductsAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 400"):
        info = products_api.products_by_category(category, paging)
        api_command_handlr.assertion(info.response.status_code, 400)
        api_command_handlr.assertion( info.get_json('errorMsg'), "Invalid Category")


@allure.story("Scenario: Test Get Products With Invalid Paging")
@pytest.mark.parametrize("category, paging", [("women", -1), ("men", "aaaaaaaaa")])
def test_products_with_invalid_paging(session, db_cursor, default_api_login, category, paging):
    products_api = ProductsAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 400"):
        info = products_api.products_by_category(category, paging)
        api_command_handlr.assertion(info.response.status_code, 400)
        api_command_handlr.assertion(info.get_json('errorMsg'), "Invalid Paging Format")

@allure.story("Scenario: Test Get Products Search With Valid Keyword")
@pytest.mark.parametrize("keyword, paging", [("洋裝", 0), ("襯衫", 1), ("二手衣", 0)])
def test_products_search_with_valid_keyword(session, db_cursor, default_api_login, keyword, paging):
    products_search_api = ProductsSearchAPI(session)
    api_command_handlr = APICommonHandler()
    database_utils = DatabaseUtil()

    with allure.step("Send products API request and check status = 200"):
        info = products_search_api.products_by_search(keyword, paging)
        response_json = info.get_json("data")
        api_command_handlr.assertion(info.response.status_code, 200)

    with allure.step("Get product_id by category in db and check # of products <= 6"):
        db_products_ids = database_utils.get_products_ids_by_keyword(db_cursor, keyword, paging)
        if paging != "":
            assert len(db_products_ids) <= 6

    with allure.step("Compare ids from db and response"):
        response_ids = [id.get('id') for id in response_json]
        api_command_handlr.assertion(db_products_ids, response_ids)

    if response_json:
        with allure.step("Verify response is correct by comparing with DB (First data)"):
            # 拿到 first_id 去 db 下 query
            first_id = db_products_ids[0]
            # 用 first_id 去撈 product table
            db_product = database_utils.get_products_result_from_db(db_cursor, first_id)
            db_variants = database_utils.composite_variants(db_cursor, first_id)
            db_colors = database_utils.composite_color(db_cursor, first_id)
            db_sizes = database_utils.composite_size(db_cursor, first_id)
            db_main_image = database_utils.get_products_main_image_from_db(db_cursor, first_id)
            db_images = database_utils.get_products_images_result_from_db(db_cursor, first_id)

            # 拿到 response 的第一筆來根 db 比較
            first_response = response_json[0]
        with allure.step(
                "Verify response of id, category, title, description, price, texture, wash, place, note, story"):
            api_command_handlr.assertion(first_response.get('id'), first_id)
            api_command_handlr.assertion(first_response.get('category'), db_product.get('category'))
            api_command_handlr.assertion(first_response.get('title'), db_product.get('title'))
            api_command_handlr.assertion(first_response.get('description'), db_product.get('description'))
            api_command_handlr.assertion(first_response.get('price'), db_product.get('price'))
            api_command_handlr.assertion(first_response.get('texture'), db_product.get('texture'))
            api_command_handlr.assertion(first_response.get('wash'), db_product.get('wash'))
            api_command_handlr.assertion(first_response.get('place'), db_product.get('place'))
            api_command_handlr.assertion(first_response.get('note'), db_product.get('note'))
            api_command_handlr.assertion(first_response.get('story'), db_product.get('story'))

        with allure.step("Verify response of main_image and images"):
            api_command_handlr.assertion(first_response.get('main_image'), db_main_image)
            api_command_handlr.assertion(first_response.get('images'), db_images)
        #
        with allure.step("Verify response of variants"):
            api_command_handlr.assertion(first_response.get('variants'), db_variants)

        with allure.step("Verify response of colors nad sizes"):
            api_command_handlr.assertion(first_response.get('colors'), db_colors)
            api_command_handlr.assertion(first_response.get('sizes'), db_sizes)

    else:
        api_command_handlr.assertion(response_json, [])

@allure.story("Scenario: Test Get Products Search With Invalid Keyword")
def test_products_search_without_keyword(session, db_cursor, default_api_login):
    products_search_api = ProductsSearchAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 400"):
        info = products_search_api.products_by_search_without_keyword()
        api_command_handlr.assertion(info.response.status_code, 400)
        api_command_handlr.assertion(info.get_json('errorMsg'), "Search Keyword is required.")


@allure.story("Scenario: Test Get Products Details With Valid id")
def test_products_search_with_valid_product_id(session, db_cursor, default_api_login):
    products_details_api = ProductsDetailsAPI(session)
    api_command_handlr = APICommonHandler()
    database_utils = DatabaseUtil()

    with allure.step("Send products API request and check status = 200"):
        info = products_details_api.products_by_details(201807201824)
        response_json = info.get_json("data")
        api_command_handlr.assertion(info.response.status_code, 200)

    if response_json:
        with allure.step("Verify response is correct by comparing with DB"):
            id = response_json.get("id")
            # 用 id 去撈 product table
            db_product = database_utils.get_products_result_from_db(db_cursor, id)
            db_variants = database_utils.composite_variants(db_cursor, id)
            db_colors = database_utils.composite_color(db_cursor, id)
            db_sizes = database_utils.composite_size(db_cursor, id)
            db_main_image = database_utils.get_products_main_image_from_db(db_cursor, id)
            db_images = database_utils.get_products_images_result_from_db(db_cursor, id)

        with allure.step(
                "Verify response of id, category, title, description, price, texture, wash, place, note, story"):
            api_command_handlr.assertion(response_json.get('id'), db_product.get('id'))
            api_command_handlr.assertion(response_json.get('category'), db_product.get('category'))
            api_command_handlr.assertion(response_json.get('title'), db_product.get('title'))
            api_command_handlr.assertion(response_json.get('description'), db_product.get('description'))
            api_command_handlr.assertion(response_json.get('price'), db_product.get('price'))
            api_command_handlr.assertion(response_json.get('texture'), db_product.get('texture'))
            api_command_handlr.assertion(response_json.get('wash'), db_product.get('wash'))
            api_command_handlr.assertion(response_json.get('place'), db_product.get('place'))
            api_command_handlr.assertion(response_json.get('note'), db_product.get('note'))
            api_command_handlr.assertion(response_json.get('story'), db_product.get('story'))

        with allure.step("Verify response of main_image and images"):
            api_command_handlr.assertion(response_json.get('main_image'), db_main_image)
            api_command_handlr.assertion(response_json.get('images'), db_images)
            #
        with allure.step("Verify response of variants"):
            api_command_handlr.assertion(response_json.get('variants'), db_variants)

        with allure.step("Verify response of colors nad sizes"):
            api_command_handlr.assertion(response_json.get('colors'), db_colors)
            api_command_handlr.assertion(response_json.get('sizes'), db_sizes)

    else:
        api_command_handlr.assertion(response_json, [])


@allure.story("Scenario: Test Get Products Details With Invalid id")
@pytest.mark.parametrize("product_id", ["aaa", -1, 0.026, 111111111111])
def test_products_details_with_invalid_product_id(session, db_cursor, default_api_login, product_id):
    products_details_api = ProductsDetailsAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 400"):
        info = products_details_api.products_by_details(product_id)
        api_command_handlr.assertion(info.response.status_code, 400)
        api_command_handlr.assertion(info.get_json('errorMsg'), "Invalid Product ID")

