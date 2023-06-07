import os

import pytest
from page_objects.checkout_page import CheckoutPage
from page_objects.header_page import HeaderPage
from page_objects.product_page import ProductPage
from test_data.test_data_from_excel import TestData

import allure
import logging
logger = logging.getLogger()

test_data = TestData()
invalid_checkout_data = test_data.read_checkout_with_intalid_value()

@allure.story("Scenario: Checkout with empty cart")
def test_checkout_with_empty_cart(driver):
    header_page = HeaderPage(driver)
    checkout_page = CheckoutPage(driver)
    driver.get(f"{os.getenv('DOMAIN')}/cart.html")

    with allure.step("Click checkout button"):
        assert header_page.check_number_of_products_in_cart() == '0', f"Cart is not empty"
        checkout_page.click_checkout_btn()

    with allure.step("Pop up Alert"):
        get_alert = checkout_page.get_alert_message()
        assert get_alert == "Please Login First", f'Wrong alert message'
        checkout_page.accept_alert()
        assert get_alert == "尚未選購商品", f'Wrong alert message'
        checkout_page.accept_alert()
    with allure.step("Redirect to login page"):
        assert driver.current_url == f"{os.getenv('DOMAIN')}/login.html"
    # 要補 login 狀態跟未 login 狀態

@allure.story("Scenario: Checkout with invalid values (17 Test Cases)")
@pytest.mark.parametrize('invalid_checkout', invalid_checkout_data)
def test_checkout_with_invalid_values(driver, invalid_checkout):
    header_page = HeaderPage(driver)
    checkout_page = CheckoutPage(driver)
    product_page = ProductPage(driver)
    # Login Success
    with allure.step("Add product to shopping Cart"):
        driver.get(f"{os.getenv('DOMAIN')}/product.html?id = 201807201824")
        product_page.select_color()
        product_page.select_size()

        product_page.get_add_to_cart_btn().click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "已加入購物車", f'Wrong alert message'
        product_page.accept_alert()

    with allure.step("Go to shopping Cart"):
        header_page.cart_icon().click()
        driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"


    with allure.step("Input Checkout info"):
        checkout_page.input_fields(invalid_checkout_data['receiver'], invalid_checkout_data['email'], invalid_checkout_data['mobile'], invalid_checkout_data['address'])


