import os
import random

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
        product_page.select_color()
        product_page.select_size()
        product_info = product_page.get_product_info()
        product_page.get_add_to_cart_btn().click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "已加入購物車", f'Wrong alert message'
        product_page.accept_alert()

    with allure.step("Click cart icon"):
        shopping_cart_page.click_cart_icon()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"

    with allure.step("Check Cart Info is correct"):
        shopping_cart_info = shopping_cart_page.get_shopping_cart_info()
        assert product_info == shopping_cart_info, f'Product_info: {product_info} does nt match shopping_cart_info: {shopping_cart_info}'

allure.story("Scenario: Remove product from cart")
@pytest.mark.parametrize('num', [2])
def test_shopping_cart_remove_product(driver, num):
    shopping_cart_page = ShoppingCartPage(driver)
    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()
    products_info = []

    with allure.step("Select color and size then add to cart"):
        for i in range(num):
            product_page.select_color()
            product_page.select_size()

            products_info.append(product_page.get_product_info())

            get_btn = product_page.get_add_to_cart_btn()
            get_btn.click()
            get_alert = product_page.get_alert_message()
            assert get_alert == "已加入購物車", f'Wrong alert message'
            product_page.accept_alert()

    with allure.step("Click cart icon and store shopping_cart_info_before_delete"):
        shopping_cart_page.click_cart_icon()
        assert driver.current_url == f"{os.getenv('DOMAIN')}/cart.html"
        shopping_cart_info_before_delete = shopping_cart_page.get_all_shopping_cart_info()

    with allure.step("Delete random product"):
        random_index = random.randint(1, num)
        shopping_cart_page.delete_random_product(random_index).click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "已刪除商品", f'Wrong alert message'
        product_page.accept_alert()

    with allure.step("Remove deleted product from products_info and cart_info"):
        products_info.remove(products_info[random_index-1])
        print ("bbbb", shopping_cart_info_before_delete)

        shopping_cart_info_after_delete = shopping_cart_info_before_delete.remove(shopping_cart_info_before_delete[random_index-1])
        print ("ccc", shopping_cart_info_after_delete)

    with allure.step("Check Cart Info is correct by comparing shopping_cart_info_before_delete and shopping_cart_info_after_delete"):
        assert shopping_cart_info_after_delete != shopping_cart_info_before_delete

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
