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
    cart_item_id = (By.XPATH, "//div[@class='cart__item-id']")
    cart_item_color = (By.XPATH, "//div[@class='cart__item-color']")
    cart_item_size = (By.XPATH, "//div[@class='cart__item-size']")
    cart_item_qty = (By.XPATH, "//select[@class='cart__item-quantity-selector']")
    cart_item_price = (By.XPATH, "//div[@class='cart__item-price-content']")
    cart_item_subtotal = (By.XPATH, "//div[@class='cart__item-subtotal-content']")
    cart_delete_buttons = (By.XPATH, "//div[@class='cart__delete-button']")

    # 點擊購物車icon  -> 應該放到其他page
    def click_cart_icon(self):
        elem_cart_icon = self.find_element(self.cart_icon, clickable=True, waiting_time=15)
        elem_cart_icon.click()
        time.sleep(3)
        self.find_element(self.cart_header_number)
        logger.info(f'Wait until cart-header shows up')

    def get_cart_header_number(self):
        elem_get_cart_number = self.find_element(self.cart_header_number)
        return elem_get_cart_number

    def get_cart_item_name(self):
        elem_cart_item_name = self.find_elements(self.cart_item_name)
        return [item_name.text for item_name in elem_cart_item_name]

    def get_cart_item_id(self):
        elem_cart_item_id = self.find_elements(self.cart_item_id)
        return [item_id.text for item_id in elem_cart_item_id]

    def get_cart_item_color(self):
        elem_cart_item_color = self.find_elements(self.cart_item_color)
        return [item_color.text.split('｜')[1] for item_color in elem_cart_item_color]

    def get_cart_item_size(self):
        elem_cart_item_size = self.find_elements(self.cart_item_size)
        return [item_size.text.split('｜')[1] for item_size in elem_cart_item_size]

    def get_cart_item_price(self):
        elem_cart_item_price = self.find_elements(self.cart_item_price)
        return [item_price.text.split('.')[1] for item_price in elem_cart_item_price]

    def get_cart_item_subtotal(self):
        elem_cart_item_subtotal = self.find_elements(self.cart_item_subtotal)
        return [item_subtotal.text.split('.')[1] for item_subtotal in elem_cart_item_subtotal]

    def delete_random_product(self, random_index):
        locator = (By.XPATH, f'//div[@class="cart__items"]/descendant::div[@class="cart__delete-button"]["{random_index}"]')
        elem_delete_button = self.find_element(locator)
        return elem_delete_button

    def select_qty(self, value):
        select = Select(self.find_element(self.cart_item_qty))
        select.select_by_index(value)
        # return select.first_selected_option().text

    def get_current_quantity(self):
        select = Select(self.find_element(self.cart_item_qty))
        return select.first_selected_option

    def get_shopping_cart_info(self):
        shopping_cart_info = {
            'title': self.get_cart_item_name(),
            'id': self.get_cart_item_id(),
            'color': self.get_cart_item_color(),
            'size': self.get_cart_item_size(),
            'price': self.get_cart_item_price()
        }
        return shopping_cart_info

    def get_all_shopping_cart_info(self):
        all_shoppingcart_info = []
        for i in range(len(self.get_cart_header_number().text)):
            all_shoppingcart_info.append(self.get_shopping_cart_info())
        return all_shoppingcart_info

