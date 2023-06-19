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
                          ("accessories", 1), ("women", "")])
def test_products_with_valid_category(session, db_cursor, default_api_login, category, paging):
    products_api = ProductsAPI(session)
    api_command_handlr = APICommonHandler()
    database_utils = DatabaseUtil()

    with allure.step("Send products API request and check status = 200"):
        info = products_api.products_by_category(category, paging)
        response_json = info.get_json("data")
        assert info.response.status_code == 200, api_command_handlr.assert_message(info.response.status_code, 200)
        assert len(response_json) <= 6

    if response_json:
        with allure.step("Verify response is correct by comparing with DB"):
            for response_value in response_json:
                id = response_value.get('id')
                # 用 id 去撈 product table
                db_product = database_utils.get_products_result_from_db(db_cursor, id)
                db_variants = database_utils.composite_variants(db_cursor, id)
                db_colors = database_utils.composite_color(db_cursor, id)
                db_sizes = database_utils.composite_size(db_cursor, id)
                db_main_image = database_utils.get_products_main_image_from_db(db_cursor, id)
                db_images = database_utils.get_products_images_result_from_db(db_cursor, id)

        with allure.step("Verify response of id, category, title, description, price, texture, wash, place, note, story"):
            assert response_value.get('id') == db_product.get('id'), api_command_handlr.assert_message(
                db_product.get('id'), response_value.get('id'))
            assert response_value.get('category') == db_product.get('category'), api_command_handlr.assert_message(
                db_product.get('category'), response_value.get('category'))
            assert response_value.get('title') == db_product.get('title'), api_command_handlr.assert_message(
                db_product.get('title'), response_value.get('title'))
            assert response_value.get('description') == db_product.get(
                'description'), api_command_handlr.assert_message(
                db_product.get('description'), response_value.get('description'))
            assert response_value.get('price') == db_product.get('price'), api_command_handlr.assert_message(
                db_product.get('price'), response_value.get('price'))
            assert response_value.get('texture') == db_product.get('texture'), api_command_handlr.assert_message(
                db_product.get('texture'), response_value.get('texture'))
            assert response_value.get('wash') == db_product.get('wash'), api_command_handlr.assert_message(
                db_product.get('wash'), response_value.get('wash'))
            assert response_value.get('place') == db_product.get('place'), api_command_handlr.assert_message(
                db_product.get('place'), response_value.get('place'))
            assert response_value.get('note') == db_product.get('note'), api_command_handlr.assert_message(
                db_product.get('note'), response_value.get('note'))
            assert response_value.get('story') == db_product.get('story'), api_command_handlr.assert_message(
                db_product.get('story'), response_value.get('story'))

        with allure.step("Verify response of main_image and images"):
            assert response_value.get('main_image') == db_main_image, api_command_handlr.assert_message(
                db_product.get('main_image'), db_main_image)
            assert response_value.get('images') == db_images, api_command_handlr.assert_message(
                db_product.get('images'), db_images)

        with allure.step("Verify response of variants"):
            assert response_value.get('variants') == db_variants, api_command_handlr.assert_message(
                db_product.get('variants'), db_variants)

        with allure.step("Verify response of colors nad sizes"):
            assert response_value.get('colors') == db_colors, api_command_handlr.assert_message(
                db_product.get('colors'), db_colors)
            assert response_value.get('sizes') == db_sizes, api_command_handlr.assert_message(
                db_product.get('sizes'), db_sizes)

    else:
        assert response_json == [], api_command_handlr.assert_message(
                response_json, [])

@allure.story("Scenario: Test Get Products With Invalid Category")
@pytest.mark.parametrize("category, paging", [("cats", 0), ("cats", "")])
def test_products_with_invalid_category(session, db_cursor, default_api_login, category, paging):
    products_api = ProductsAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 400"):
        info = products_api.products_by_category(category, paging)
        assert info.response.status_code == 400, api_command_handlr.assert_message(info.response.status_code, 400)
        assert info.get_json('errorMsg') == "Invalid Category", api_command_handlr.assert_message(info.get_json('errorMsg'), "Invalid Category")

@allure.story("Scenario: Test Get Products With Invalid Paging")
@pytest.mark.parametrize("category, paging", [("women", -1), ("men", "aaaaaaaaa")])
def test_products_with_invalid_paging(session, db_cursor, default_api_login, category, paging):
    products_api = ProductsAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 400"):
        info = products_api.products_by_category(category, paging)
        assert info.response.status_code == 400, api_command_handlr.assert_message(info.response.status_code, 400)
        assert info.get_json('errorMsg') == "Invalid Paging format", api_command_handlr.assert_message(
            info.get_json('errorMsg'), "Invalid Paging format")

@allure.story("Scenario: Test Get Products Search With Valid Keyword")
@pytest.mark.parametrize("keyword, paging", [("洋裝", 0),  ("襯衫", 1), ("二手衣", 0)])
def test_products_search_with_valid_keyword(session, db_cursor, default_api_login, keyword, paging):
    products_search_api = ProductsSearchAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 200"):
        info = products_search_api.products_by_search(keyword, paging)
        response_json = info.get_json("data")
        database_utils = DatabaseUtil()

        assert info.response.status_code == 200, api_command_handlr.assert_message(info.response.status_code, 200)
        assert len(response_json) <= 6


    if response_json:
        with allure.step("Verify response is correct by comparing with DB"):
            for response_value in response_json:
                id = response_value.get('id')
                # 用 id 去撈 product table
                db_product = database_utils.get_products_result_from_db(db_cursor, id)
                db_variants = database_utils.composite_variants(db_cursor, id)
                db_colors = database_utils.composite_color(db_cursor, id)
                db_sizes = database_utils.composite_size(db_cursor, id)
                db_main_image = database_utils.get_products_main_image_from_db(db_cursor, id)
                db_images = database_utils.get_products_images_result_from_db(db_cursor, id)

        with allure.step("Verify response of id, category, title, description, price, texture, wash, place, note, story"):
            assert response_value.get('id') == db_product.get('id'), api_command_handlr.assert_message(
                db_product.get('id'), response_value.get('id'))
            assert response_value.get('category') == db_product.get('category'), api_command_handlr.assert_message(
                db_product.get('category'), response_value.get('category'))
            assert response_value.get('title') == db_product.get('title'), api_command_handlr.assert_message(
                db_product.get('title'), response_value.get('title'))
            assert response_value.get('description') == db_product.get(
                'description'), api_command_handlr.assert_message(
                db_product.get('description'), response_value.get('description'))
            assert response_value.get('price') == db_product.get('price'), api_command_handlr.assert_message(
                db_product.get('price'), response_value.get('price'))
            assert response_value.get('texture') == db_product.get('texture'), api_command_handlr.assert_message(
                db_product.get('texture'), response_value.get('texture'))
            assert response_value.get('wash') == db_product.get('wash'), api_command_handlr.assert_message(
                db_product.get('wash'), response_value.get('wash'))
            assert response_value.get('place') == db_product.get('place'), api_command_handlr.assert_message(
                db_product.get('place'), response_value.get('place'))
            assert response_value.get('note') == db_product.get('note'), api_command_handlr.assert_message(
                db_product.get('note'), response_value.get('note'))
            assert response_value.get('story') == db_product.get('story'), api_command_handlr.assert_message(
                db_product.get('story'), response_value.get('story'))

        with allure.step("Verify response of main_image and images"):
            assert response_value.get('main_image') == db_main_image, api_command_handlr.assert_message(
                db_product.get('main_image'), db_main_image)
            assert response_value.get('images') == db_images, api_command_handlr.assert_message(
                db_product.get('images'), db_images)

        with allure.step("Verify response of variants"):
            assert response_value.get('variants') == db_variants, api_command_handlr.assert_message(
                db_product.get('variants'), db_variants)

        with allure.step("Verify response of colors nad sizes"):
            assert response_value.get('colors') == db_colors, api_command_handlr.assert_message(
                db_product.get('colors'), db_colors)
            assert response_value.get('sizes') == db_sizes, api_command_handlr.assert_message(
                db_product.get('sizes'), db_sizes)

    else:
        assert response_json == [], api_command_handlr.assert_message(
            response_json, [])

@allure.story("Scenario: Test Get Products Search With Invalid Keyword")
def test_products_search_without_keyword(session, db_cursor, default_api_login):
    products_search_api = ProductsSearchAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 400"):
        info = products_search_api.products_by_search_without_keyword()
        assert info.response.status_code == 400, api_command_handlr.assert_message(info.response.status_code, 400)
        assert info.get_json('errorMsg') == "Search Keyword is required.", api_command_handlr.assert_message(info.get_json('errorMsg'), "Search Keyword is required.")

@allure.story("Scenario: Test Get Products Details With Valid id")
def test_products_search_with_valid_product_id(session, db_cursor, default_api_login):
    products_details_api = ProductsDetailsAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 200"):
        info = products_details_api.products_by_details(201807201824)
        response_json = info.get_json("data")
        database_utils = DatabaseUtil()

        assert info.response.status_code == 200, api_command_handlr.assert_message(info.response.status_code, 200)
        # assert len(response_json) <= 6 # assert len(response_json) <= 6 # 不能用 len，因為這邊是"data": {} 而非 "data": [{}]

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

        with allure.step("Verify response of id, category, title, description, price, texture, wash, place, note, story"):
            assert response_json.get('id') == db_product.get('id'), api_command_handlr.assert_message(
                db_product.get('id'), response_json.get('id'))
            assert response_json.get('category') == db_product.get('category'), api_command_handlr.assert_message(
                db_product.get('category'), response_json.get('category'))
            assert response_json.get('title') == db_product.get('title'), api_command_handlr.assert_message(
                db_product.get('title'), response_json.get('title'))
            assert response_json.get('description') == db_product.get(
                'description'), api_command_handlr.assert_message(
                db_product.get('description'), response_json.get('description'))
            assert response_json.get('price') == db_product.get('price'), api_command_handlr.assert_message(
                db_product.get('price'), response_json.get('price'))
            assert response_json.get('texture') == db_product.get('texture'), api_command_handlr.assert_message(
                db_product.get('texture'), response_json.get('texture'))
            assert response_json.get('wash') == db_product.get('wash'), api_command_handlr.assert_message(
                db_product.get('wash'), response_json.get('wash'))
            assert response_json.get('place') == db_product.get('place'), api_command_handlr.assert_message(
                db_product.get('place'), response_json.get('place'))
            assert response_json.get('note') == db_product.get('note'), api_command_handlr.assert_message(
                db_product.get('note'), response_json.get('note'))
            assert response_json.get('story') == db_product.get('story'), api_command_handlr.assert_message(
                db_product.get('story'), response_json.get('story'))

        with allure.step("Verify response of main_image and images"):
            assert response_json.get('main_image') == db_main_image, api_command_handlr.assert_message(
                db_product.get('main_image'), db_main_image)
            assert response_json.get('images') == db_images, api_command_handlr.assert_message(
                db_product.get('images'), db_images)

        with allure.step("Verify response of variants"):
            assert response_json.get('variants') == db_variants, api_command_handlr.assert_message(
                db_product.get('variants'), db_variants)

        with allure.step("Verify response of colors nad sizes"):
            assert response_json.get('colors') == db_colors, api_command_handlr.assert_message(
                db_product.get('colors'), db_colors)
            assert response_json.get('sizes') == db_sizes, api_command_handlr.assert_message(
                db_product.get('sizes'), db_sizes)

    else:
        assert response_json == [], api_command_handlr.assert_message(
            response_json, [])

@allure.story("Scenario: Test Get Products Details With Invalid id")
@pytest.mark.parametrize("product_id", ["aaa", -1, 0.026, 111111111111])
def test_products_details_with_invalid_product_id(session, db_cursor, default_api_login, product_id):
    products_details_api = ProductsDetailsAPI(session)
    api_command_handlr = APICommonHandler()

    with allure.step("Send products API request and check status = 400"):
        info = products_details_api.products_by_details(product_id)
        assert info.response.status_code == 400, api_command_handlr.assert_message(info.response.status_code, 400)
        assert info.get_json('errorMsg') == "Invalid Product ID", api_command_handlr.assert_message(info.get_json('errorMsg'), "Invalid Product ID")
