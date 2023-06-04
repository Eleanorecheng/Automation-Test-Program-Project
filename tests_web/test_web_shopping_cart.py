import os
import pytest
from page_objects.product_page import ProductPage
from page_objects.shopping_cart_page import ShoppingCartPage
import allure
import logging
logger = logging.getLogger()

allure.story("Scenario: Shopping Cart Info Correct")
def test_shopping_cart_info(driver):
    shopping_cart_page = ShoppingCartPage(driver)
    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()

    with allure.step("Select color and size then add to cart"):
        # color_selected = product_page.select_color().get_attribute("data_id")[-6:]
        size_selected = product_page.select_size().text
        get_btn = product_page.get_add_to_cart_btn()
        get_btn.click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "已加入購物車", f'Wrong alert message'
        product_page.accept_alert()

    with allure.step("Click cart icon"):
        shopping_cart_page.click_cart_icon()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"

    with allure.step("Check Cart Info is correct"):
        assert '1' in shopping_cart_page.get_cart_header_number().text, f'Wrong number of product in the cart'
        assert shopping_cart_page.get_cart_item_name() == product_page.random_product, f'Wrong product name in the cart'
        # assert color_selected == shopping_cart_page.get_cart_item_color(), f'Wrong product color in the cart'
        assert size_selected in shopping_cart_page.get_cart_item_size(), f'Wrong product size in the cart'


allure.story("Scenario: Remove product from cart")
def test_shopping_cart_remove_product(driver):
    shopping_cart_page = ShoppingCartPage(driver)
    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()

    with allure.step("Select color and size then add to cart"):
        for i in range(2):
            product_page.select_color()
            product_page.select_size()
            get_btn = product_page.get_add_to_cart_btn()
            get_btn.click()
            get_alert = product_page.get_alert_message()
            assert get_alert == "已加入購物車", f'Wrong alert message'
            product_page.accept_alert()

    with allure.step("Click cart icon and check Cart Info is correct"):
        shopping_cart_page.click_cart_icon()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"
        assert '2' in shopping_cart_page.get_cart_header_number().text, f'Wrong product number in the cart'

    with allure.step("Delete random product"):
        shopping_cart_page.delete_random_product().click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "已刪除商品", f'Wrong alert message'
        product_page.accept_alert()

    with allure.step("Check Cart Info is correct"):
        assert '1' in shopping_cart_page.get_cart_header_number().text, f'Wrong product number in the cart'


allure.story("Scenario: Edit quantity in cart")
def test_shopping_cart_edit_quantity(driver):
    shopping_cart_page = ShoppingCartPage(driver)
    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()

    with allure.step("Select color and size then add to cart"):
        product_page.select_color()
        product_page.select_size()
        get_btn = product_page.get_add_to_cart_btn()
        get_btn.click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "已加入購物車", f'Wrong alert message'
        product_page.accept_alert()

    with allure.step("Click cart icon"):
        shopping_cart_page.click_cart_icon()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"

    with allure.step("Check Cart Info is correct"):
        assert '1' in shopping_cart_page.get_cart_header_number().text, f'Wrong product number in the cart'

    with allure.step("Edit the quantity"):
        shopping_cart_page.select_qty(5)
        get_alert = product_page.get_alert_message()
        assert get_alert == "已修改數量", f'Wrong alert message'
        product_page.accept_alert()
        get_qty = shopping_cart_page.get_current_quantity().text
        assert get_qty == '6', f'Wrong quantity number of the product'
