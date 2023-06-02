import random
from selenium.webdriver.common.by import By
from utils.page_base import PageBase
import logging

logger = logging.getLogger()


class ProductPage(PageBase):
    product_name = (By.XPATH, "//div[@class='product__title']")
    product_color = (By.XPATH, "//div[@class='product__color']")
    product_size = (By.XPATH, "//div[@class='product__size']")
    product_qty_add = (By.XPATH, "//div[@class='product__quantity-add']")
    product_qty_minus = (By.XPATH, "//div[@class='product__quantity-minus']")
    product_qty_value = (By.XPATH, "//div[@class='product__quantity-value']")
    add_to_cart = (By.XPATH, "//button[@class ='product__add-to-cart-button']")
    number_of_products_in_cart = (By.XPATH, "//div[@class='header__link-icon-cart-number']")

    # 隨機取得畫面中的產品
    def select_product_and_enter_product_page(self):
        self.scroll_down()
        elem_random_product = random.choice(self.find_visible_elements(self.product_name))
        logging.info(f'Selected product: {elem_random_product.text}')

        self.driver.execute_script("arguments[0].scrollIntoView()", elem_random_product)
        elem_random_product.click()
        logger.info("Click product")

        # self.driver.execute_script("arguments[0].click()", elem_random_product)
        self.find_element(self.product_name, clickable=False, waiting_time=15)
        logger.info(f'Select_product_and_enter_product_page')

    def select_color(self):
        elem_selected_color = random.choice(self.find_elements(self.product_color))
        logger.info(f'Selected color: {elem_selected_color.text}')

        elem_selected_color.click()
        logger.info("Click color")

        return elem_selected_color

    def select_size(self):
        elem_selected_size = random.choice(self.find_elements(self.product_size))
        logger.info(f'Selected size: {elem_selected_size.text}')

        elem_selected_size.click()
        logger.info("Click size")
        return elem_selected_size

    # 驗證 size default 是不會被選到的
    def check_size_default_status(self):
        for element in self.find_elements(self.product_size):
            assert 'product__size product__size--selected' != element.get_attribute('class'), f'size is selected !!'
        logger.info("check_size_default_status")

    def increase_quantity(self, click_time):
        logger.info("Method: increase_quantity")
        elem_add_qty = self.find_element(self.product_qty_add, clickable=True)
        for i in range(click_time):
            elem_add_qty.click()
        logger.info("increase_quantity")

    def decrease_quantity(self, click_time):
        logger.info("Method: decrease_quantity")
        elem_minus_qty = self.find_element(self.product_qty_minus, clickable=True)
        for i in range(click_time):
            elem_minus_qty.click()
        logger.info("decrease_quantity")

    def check_quantity(self):
        logger.info("Method: check_quantity")
        elem_qty_value = self.find_element(self.product_qty_value)
        logger.info(f'Quantity Value: {elem_qty_value.text}')
        return elem_qty_value.text

    def get_add_to_cart_btn(self):
        logger.info("Method: add_to_cart")
        elem_add_to_cart_btn = self.find_element(self.add_to_cart)
        return elem_add_to_cart_btn

    def check_number_of_products_in_cart(self):
        elem_number_in_cart = self.find_element(self.number_of_products_in_cart)
        logger.info(f'Number in Cart: {elem_number_in_cart.text}')
        return elem_number_in_cart.text
