import pytest
from page_objects.product_page import ProductPage
import allure
import logging

logger = logging.getLogger()

@allure.story("Scenario: Color Selection")
def test_product_select_color(driver):
    logger.info("Start: test_product_select_color")

    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()

    with allure.step("Select color and verify highlightning"):
        color_selected = product_page.select_color()
        assert 'product__color product__color--selected' == color_selected.get_attribute(
            'class'), f'selected color is not highlighted'

    logger.info("Finish: test_product_select_color")


@allure.story("Scenario: Size Selection")
def test_product_select_size(driver):
    logger.info("Start: test_product_select_size")

    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()

    with allure.step("Select size and verify highlightning"):
        size_selected = product_page.select_size()
        assert 'product__size product__size--selected' == size_selected.get_attribute(
            'class'), f'selected size is not highlighted'

    logger.info("Finish: test_product_select_size")


@allure.story("Scenario: Quantity Editor Disabled")
def test_quantity_disabled(driver):
    logger.info("Start: test_quantity_disabled")

    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()
    product_page.check_size_default_status()

    with allure.step("Increase quantity by clicking 1 time"):
        product_page.increase_quantity(1)
        assert product_page.check_quantity() == '1', f'quantity is added when add_btn is disabled'
    with allure.step("Decrease quantity by clicking 1 time"):
        product_page.decrease_quantity(1)
        assert product_page.check_quantity() == '1', f'quantity is minused when add_btn is disabled'

    logger.info("Finish: test_quantity_disabled")


@allure.story("Scenario: Quantity Editor - Increase Quantity")
def test_increase_quantity(driver):
    logger.info("Start: test_increase_quantity")

    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()
    product_page.select_size()

    with allure.step("Increase quantity by clicking 8 time"):
        product_page.increase_quantity(8)
        assert product_page.check_quantity() == '9', f'quantity is {product_page.check_quantity()}'
    with allure.step("Increase quantity by clicking 2 time"):
        product_page.increase_quantity(2)
        assert product_page.check_quantity() == '9', f'quantity is {product_page.check_quantity()}'

    logger.info("Finish: test_increase_quantity")


@allure.story("Scenario: Quantity Editor - Decrease Quantity")
def test_decrease_quantity(driver):
    logger.info("Start: test_decrease_quantity")

    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()
    product_page.select_size()

    with allure.step("Increase quantity by clicking 8 time"):
        product_page.increase_quantity(8)
        assert product_page.check_quantity() == '9', f'quantity is {product_page.check_quantity()}'
    with allure.step("Decrease quantity by clicking 8 time"):
        product_page.decrease_quantity(8)
        assert product_page.check_quantity() == '1', f'quantity is {product_page.check_quantity()}'

    logger.info("Finish: test_decrease_quantity")


@allure.story("Scenario: Add To Cart - Success")
@pytest.mark.parametrize('add_to_cart_time', [1, 5])
def test_add_to_cart(driver, add_to_cart_time):
    logger.info("Start: test_add_to_cart")
    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()
    product_page.select_size()

    with allure.step("Check 'Add to cart' wording"):
        get_btn = product_page.get_add_to_cart_btn()
        assert get_btn.text == "加入購物車", f'Wrong info on add_to_cart_btn'

    with allure.step("Click button: Add to cart"):
        for i in range(add_to_cart_time):
            get_btn.click()
            get_alert = product_page.get_alert_message()
            assert get_alert == "已加入購物車", f'Wrong alert message'
            product_page.accept_alert()
    with allure.step("Check product number in cart"):
        get_cart_number = product_page.check_number_of_products_in_cart()
        assert str(add_to_cart_time) == get_cart_number, f'Wrong number in cart'

    logger.info("Finish: test_add_to_cart")


@allure.story("Scenario: Add To Cart - Failure")
def test_cannot_add_to_cart(driver):
    logger.info("Start: test_cannot_add_to_cart")

    product_page = ProductPage(driver)
    product_page.select_product_and_enter_product_page()
    product_page.check_size_default_status()
    with allure.step("Check 'Add to cart' wording"):
        get_btn = product_page.get_add_to_cart_btn()
        assert get_btn.text == "請選擇尺寸", f'Wrong info on add_to_cart_btn'

    with allure.step("Click button: Add to cart"):
        get_btn.click()
        get_alert = product_page.get_alert_message()
        assert get_alert == "請選擇尺寸", f'Wrong alert message'
        product_page.accept_alert()

    logger.info("Finish: test_cannot_add_to_cart")
