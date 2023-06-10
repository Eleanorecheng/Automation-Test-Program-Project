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


@allure.story("Scenario: Checkout with empty cart")
def test_checkout_with_empty_cart(driver, login_in_parallel):
    header_page = HeaderPage(driver)
    checkout_page = CheckoutPage(driver)
    driver.get(f"{os.getenv('DOMAIN')}/cart.html")

    with allure.step("Click checkout button"):
        assert header_page.check_number_of_products_in_cart() == '0', f"Cart is not empty"
        checkout_page.click_checkout_btn()

    with allure.step("Pop up Alert"):
        # get_alert = checkout_page.get_alert_message()
        # assert get_alert == "Please Login First", f'Wrong alert message'
        # checkout_page.accept_alert()
        get_alert = checkout_page.get_alert_message()
        assert get_alert == "尚未選購商品", f'Wrong alert message'
        checkout_page.accept_alert()
    with allure.step("Redirect to cart page"):
        assert driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"
    # 要補 login 狀態跟未 login 狀態


@allure.story("Scenario: Checkout with invalid values (17 Test Cases)")
@pytest.mark.parametrize('invalid_checkout_data', test_data.read_data('Checkout with Invalid Value'))
def test_checkout_with_invalid_values(driver, invalid_checkout_data, login_in_parallel):
    header_page = HeaderPage(driver)
    checkout_page = CheckoutPage(driver)
    product_page = ProductPage(driver)

    with allure.step("Add product to shopping Cart"):
        driver.get(f"{os.getenv('DOMAIN')}/product.html?id=201807201824")
        product_page.select_color()
        product_page.select_size()
        product_page.get_add_to_cart_btn().click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "已加入購物車", f'Wrong alert message'
        product_page.accept_alert()

    with allure.step("Go to shopping Cart"):
        header_page.click_cart_icon()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"

    with allure.step("Input Checkout info"):
        checkout_page.input_fields(invalid_checkout_data['Receiver'], invalid_checkout_data['Email'],
                                   invalid_checkout_data['Mobile'], invalid_checkout_data['Address'],
                                   invalid_checkout_data['Deliver Time'])

    with allure.step("Input Payment info"):
        checkout_page.iframe_input_fields_card_number("card-number", invalid_checkout_data['Credit Card No'])
        checkout_page.iframe_input_fields_exp_date("card-expiration-date", invalid_checkout_data['Expiry Date'])
        checkout_page.iframe_input_fields_security_code("card-ccv", invalid_checkout_data['Security Code'])

    with allure.step("Click checkout button"):
        checkout_page.click_checkout_btn()

    with allure.step("Check error message"):
        get_alert = product_page.get_alert_message()
        assert get_alert == invalid_checkout_data['Alert Msg'], f'Wrong alert message: {get_alert}'
        product_page.accept_alert()

@pytest.mark.parametrize('valid_checkout_data', test_data.read_data('Checkout with Valid Value'))
def test_checkout_with_valid_values(driver, valid_checkout_data, login_in_parallel):
    header_page = HeaderPage(driver)
    checkout_page = CheckoutPage(driver)
    product_page = ProductPage(driver)

    with allure.step("Add product to shopping Cart"):
        driver.get(f"{os.getenv('DOMAIN')}/product.html?id=201807201824")
        product_page.select_color()
        product_page.select_size()
        product_page.get_add_to_cart_btn().click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "已加入購物車", f'Wrong alert message'
        product_page.accept_alert()

    with allure.step("Go to shopping Cart"):
        header_page.click_cart_icon()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"

    with allure.step("Input Checkout info"):
        checkout_page.input_fields(valid_checkout_data['Receiver'], valid_checkout_data['Email'],
                                   valid_checkout_data['Mobile'], valid_checkout_data['Address'],
                                   valid_checkout_data['Deliver Time'])

    with allure.step("Input Payment info"):
        checkout_page.iframe_input_fields_card_number("card-number", valid_checkout_data['Credit Card No'])
        checkout_page.iframe_input_fields_exp_date("card-expiration-date", valid_checkout_data['Expiry Date'])
        checkout_page.iframe_input_fields_security_code("card-ccv", valid_checkout_data['Security Code'])

    with allure.step("Click checkout button"):
        checkout_page.click_checkout_btn()

    with allure.step("Check error message"):
        get_alert = checkout_page.get_alert_message()
        assert get_alert == '付款成功', f'Wrong alert message: {get_alert}'
        checkout_page.accept_alert()

    with allure.step("Check Thank You page"):
        assert f"{os.getenv('DOMAIN')}/thankyou.html" in driver.current_url
        checkout_page.check_thank_you_title()
        order_info_list = checkout_page.get_order_info()
        assert order_info_list["receiver"] == valid_checkout_data['Receiver'], f'Wrong Receiver Info: {order_info_list["receiver"]}'
        assert order_info_list["email"] == valid_checkout_data['Email'], f'Wrong Receiver Info: {order_info_list["email"]}'
        assert order_info_list["mobile"] == valid_checkout_data['Mobile'], f'Wrong Receiver Info: {order_info_list["mobile"]}'
        assert order_info_list["address"] == valid_checkout_data['Address'], f'Wrong Receiver Info: {order_info_list["address"]}'
        # assert order_info_list['deliver time'] == valid_checkout_data['Deliver Time'], f'Wrong Receiver Info: {order_info_list["deliver time"]}'
