from selenium.webdriver.common.by import By
from utils.page_base import PageBase
import logging
logger = logging.getLogger()

class HeaderPage(PageBase):

    cart_icon = (By.XPATH, "//a[@class='header__link']")
    number_of_products_in_cart = (By.XPATH, "//div[@class='header__link-icon-cart-number']")
    cart_header_number = (By.XPATH, "//div[@ class ='cart__header-number']")

    def click_cart_icon(self):
        elem_cart_icon = self.find_element(self.cart_icon, clickable=True, waiting_time=15)
        elem_cart_icon.click()
        self.find_element(self.cart_header_number)
        logger.info(f'Wait until cart-header shows up')

    def check_number_of_products_in_cart(self):
        elem_number_in_cart = self.find_element(self.number_of_products_in_cart)
        logger.info("check_number_of_products_in_cart")
        return elem_number_in_cart.text