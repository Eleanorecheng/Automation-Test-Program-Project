import os

import pytest
from page_objects.header_page import HeaderPage
from page_objects.create_product_page import CreateProductPage
from test_data.test_data_from_excel import TestData

import allure
import logging

logger = logging.getLogger()

test_data = TestData()


@allure.story("Scenario: Create Product Success (3 Test Cases)")
@pytest.mark.parametrize('create_product_success', test_data.read_data('Create Product Success'))
def test_create_product_success(driver, login_in_parallel, create_product_success):
    create_product_page = CreateProductPage(driver)
    driver.get(f"{os.getenv('DOMAIN')}/admin/products.html")

    with allure.step("Fill in Product"):
        driver.get(f"{os.getenv('DOMAIN')}/admin/product_create.html")
        create_product_page.input_field_dropdown(create_product_success['Category'])
        create_product_page.input_field_description(create_product_success['Description'])
        create_product_page.input_field_general(title=create_product_success['Title'],
                                                price=create_product_success['Price'],
                                                texture=create_product_success['Texture'],
                                                wash=create_product_success['Wash'],
                                                place=create_product_success['Place of Product'],
                                                note=create_product_success['Note'],
                                                story=create_product_success['Story'])
        create_product_page.select_product_color(create_product_success['Colors'])
        create_product_page.select_product_size(create_product_success['Sizes'])
        create_product_page.upload_main_image(create_product_success['Main Image'])
        create_product_page.upload_other_images(create_product_success['Other Image 1'], '1')
        create_product_page.upload_other_images(create_product_success['Other Image 2'], '2')

    with allure.step("Create Product"):
        create_product_page.click_create_btn()
        get_alert = create_product_page.get_alert_message()
        assert get_alert == "Create Product Success", f'Wrong alert message'
        create_product_page.accept_alert()

    with allure.step("Go to products list"):
        driver.get(f"{os.getenv('DOMAIN')}/admin/products.html")
        assert create_product_page.get_product_name_in_products_list(create_product_success['Title']) == \
               create_product_success['Title'], f'Product not in the list'

    with allure.step("Delete product"):
        create_product_page.delete_product(create_product_success['Title'])
        get_alert = create_product_page.get_alert_message()
        assert get_alert == "Delete Product Success", f'Wrong alert message'
        create_product_page.accept_alert()


allure.story("Scenario: Create Product with Invalid Value (20 Test Cases)")


@pytest.mark.parametrize('create_product_failed', test_data.read_data('Create Product Failed'))
def test_create_product_failed(driver, login_in_parallel, create_product_failed):
    create_product_page = CreateProductPage(driver)
    driver.get(f"{os.getenv('DOMAIN')}/admin/products.html")

    with allure.step("Fill in Product"):
        driver.get(f"{os.getenv('DOMAIN')}/admin/product_create.html")
        create_product_page.input_field_dropdown(create_product_failed['Category'])
        create_product_page.input_field_description(create_product_failed['Description'])
        create_product_page.input_field_general(title=create_product_failed['Title'],
                                                price=create_product_failed['Price'],
                                                texture=create_product_failed['Texture'],
                                                wash=create_product_failed['Wash'],
                                                place=create_product_failed['Place of Product'],
                                                note=create_product_failed['Note'],
                                                story=create_product_failed['Story'])
        create_product_page.select_product_color(create_product_failed['Colors'])
        create_product_page.select_product_size(create_product_failed['Sizes'])
        create_product_page.upload_main_image(create_product_failed['Main Image'])
        create_product_page.upload_other_images(create_product_failed['Other Image 1'], '1')
        create_product_page.upload_other_images(create_product_failed['Other Image 2'], '2')

    with allure.step("Create Product"):
        create_product_page.click_create_btn()
        get_alert = create_product_page.get_alert_message()
        assert get_alert == create_product_failed['Alert Msg'], f'Wrong alert message'
        create_product_page.accept_alert()


allure.story("Scenario: Create Product without login")


def test_create_product_without_login(driver):
    create_product_page = CreateProductPage(driver)
    driver.get(f"{os.getenv('DOMAIN')}/admin/product_create.html")

    with allure.step("Fill in Product"):
        create_product_page.input_field_dropdown('Men')
        create_product_page.input_field_description('Description')
        create_product_page.input_field_general(title='title',
                                                price='100',
                                                texture='texture',
                                                wash='wash',
                                                place='place of product',
                                                note='note',
                                                story='story')
        create_product_page.select_product_color('亮綠, 淺灰')
        create_product_page.select_product_size('F')
        create_product_page.upload_main_image('sample image')
        create_product_page.upload_other_images('sample image', '1')
        create_product_page.upload_other_images('sample image', '2')
    with allure.step("Create Product"):
        create_product_page.click_create_btn()
        get_alert = create_product_page.get_alert_message()
        assert get_alert == 'Please Login First', f'Wrong alert message'
        create_product_page.accept_alert()
