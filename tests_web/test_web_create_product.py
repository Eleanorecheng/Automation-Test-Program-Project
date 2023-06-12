import os
import pytest
from page_objects.create_product_page import CreateProductPage
from test_data.test_data_from_excel import TestData

import allure
import logging

logger = logging.getLogger()

test_data = TestData()


@allure.story("Scenario: Create Product Success (3 Test Cases)")
@pytest.mark.parametrize('create_product_success', test_data.read_data('Create Product Success'))
def test_create_product_success(driver, login_in_parallel, create_product_success, request):
    create_product_page = CreateProductPage(driver)
    driver.get(f"{os.getenv('DOMAIN')}/admin/products.html")
    # create_product_page.check_product_is_existing_beforehand(create_product_success['Title'])

    with allure.step("Go to /product_create.html and create Fill in Product"):
        driver.get(f"{os.getenv('DOMAIN')}/admin/product_create.html")
        create_product_page.input_field_dropdown(create_product_success['Category'])
        create_product_page.input_field_description(create_product_success['Description'])
        # create_product_page.input_field_general(title=create_product_success['Title'],
        #                                         price=create_product_success['Price'],
        #                                         texture=create_product_success['Texture'],
        #                                         wash=create_product_success['Wash'],
        #                                         place=create_product_success['Place of Product'],
        #                                         note=create_product_success['Note'],
        #                                         story=create_product_success['Story'])
        create_product_page.input_field_general(create_product_success)
        create_product_page.select_product_color(create_product_success['Colors'])
        create_product_page.select_product_size(create_product_success['Sizes'])
        create_product_page.upload_main_image(create_product_success['Main Image'])
        create_product_page.upload_other_images(create_product_success['Other Image 1'], '1')
        create_product_page.upload_other_images(create_product_success['Other Image 2'], '2')

    with allure.step("Create Product Success"):
        create_product_page.click_create_btn()
        get_alert = create_product_page.get_alert_message()
        assert get_alert == "Create Product Success", f'Wrong alert message'
        create_product_page.accept_alert()

    with allure.step("Go to products list and check new product shows on the list"):
        driver.get(f"{os.getenv('DOMAIN')}/admin/products.html")
        assert create_product_page.get_product_name_in_products_list(create_product_success['Title']).text == \
               create_product_success['Title'], f'Product not in the list'

    def delete_product_finalizer():
        with allure.step("Delete product and check delete alert"):
            create_product_page.delete_product(create_product_success['Title'])
            get_alert = create_product_page.get_alert_message()
            assert get_alert == "Delete Product Success", f'Wrong alert message'
            create_product_page.accept_alert()
    request.addfinalizer(delete_product_finalizer)


@allure.story("Scenario: Create Product with Invalid Value (20 Test Cases)")
@pytest.mark.parametrize('create_product_failed', test_data.read_data('Create Product Failed'))
def test_create_product_failed(driver, login_in_parallel, create_product_failed, request):
    create_product_page = CreateProductPage(driver)
    driver.get(f"{os.getenv('DOMAIN')}/admin/products.html")
    # create_product_page.check_product_is_existing_beforehand(create_product_failed['Title'])

    with allure.step("Fill in Product"):
        driver.get(f"{os.getenv('DOMAIN')}/admin/product_create.html")
        create_product_page.input_field_dropdown(create_product_failed['Category'])
        create_product_page.input_field_description(create_product_failed['Description'])
        create_product_page.input_field_general(create_product_failed)
        create_product_page.select_product_color(create_product_failed['Colors'])
        create_product_page.select_product_size(create_product_failed['Sizes'])
        create_product_page.upload_main_image(create_product_failed['Main Image'])
        create_product_page.upload_other_images(create_product_failed['Other Image 1'], '1')
        create_product_page.upload_other_images(create_product_failed['Other Image 2'], '2')

    with allure.step("Create Product and check fail alert"):
        create_product_page.click_create_btn()
        get_alert = create_product_page.get_alert_message()
        assert get_alert == create_product_failed['Alert Msg'], f'Wrong alert message'
        create_product_page.accept_alert()

    with allure.step("Go to products list"):
        driver.get(f"{os.getenv('DOMAIN')}/admin/products.html")

    def delete_product_finalizer():
        with allure.step("Delete product and check delete alert"):
            if create_product_page.delete_product(create_product_failed['Title']) != None:
                get_alert = create_product_page.get_alert_message()
                assert get_alert == "Delete Product Success", f'Wrong alert message'
                create_product_page.accept_alert()
    request.addfinalizer(delete_product_finalizer)

@allure.story("Scenario: Create Product without login")
def test_create_product_without_login(driver):
    create_product_page = CreateProductPage(driver)
    driver.get(f"{os.getenv('DOMAIN')}/admin/product_create.html")
    create_product_page.check_product_is_existing_beforehand('Title')

    with allure.step("Fill in Product"):
        create_product_page.input_field_dropdown('Men')
        create_product_page.input_field_description('Description')
        create_product_page.input_field_send_key(title='title', price='100', texture='texture', wash='wash', place='place of product', note='note', story='story')
        create_product_page.select_product_color('亮綠, 淺灰')
        create_product_page.select_product_size('F')
        create_product_page.upload_main_image('sample image')
        create_product_page.upload_other_images('sample image', '1')
        create_product_page.upload_other_images('sample image', '2')

    with allure.step("Create Product and check failed alert"):
        create_product_page.click_create_btn()
        get_alert = create_product_page.get_alert_message()
        assert get_alert == 'Please Login First', f'Wrong alert message'
        create_product_page.accept_alert()
