import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from utils.page_base import PageBase
import logging

logger = logging.getLogger()


class ShoppingCartPage(PageBase):
    cart_icon = (By.XPATH, "//a[@class='header__link']")
    cart_header_number = (By.XPATH, "//div[@ class ='cart__header-number']")
    cart_item_name = (By.XPATH, "//div[@class='cart__item-name']")
    cart_item_color = (By.XPATH, "//div[@class='cart__item-color']")
    cart_item_size = (By.XPATH, "//div[@class='cart__item-size']")
    cart_delete_buttons = (By.XPATH, "//div[@class='cart__delete-button']")
    cart_item_qty = (By.XPATH, "//select[@class='cart__item-quantity-selector']")

    def click_cart_icon(self):
        elem_cart_icon = self.find_element(self.cart_icon, clickable=True, waiting_time=15)
        elem_cart_icon.click()
        self.find_element(self.cart_header_number)
        logger.info(f'Wait until cart-header shows up')

    def get_cart_header_number(self):
        elem_get_cart_number = self.find_element(self.cart_header_number)
        return elem_get_cart_number

    def get_cart_item_name(self):
        elem_cart_item_name = self.find_element(self.cart_item_name)
        return elem_cart_item_name.text

    def get_cart_item_color(self):
        elem_cart_item_color = self.find_element(self.cart_item_color)
        return elem_cart_item_color.text

    def get_cart_item_size(self):
        elem_cart_item_size = self.find_element(self.cart_item_size)
        return elem_cart_item_size.text

    def delete_random_product(self):
        elem_random_delete_button = random.choice(self.find_visible_elements(self.cart_delete_buttons))
        return elem_random_delete_button

    def select_qty(self, value):
        select = Select(self.find_element(self.cart_item_qty))
        select.select_by_index(value)
        # return select.first_selected_option().text

    def get_current_quantity(self):
        select = Select(self.find_element(self.cart_item_qty))
        return select.first_selected_option
