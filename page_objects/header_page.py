from selenium.webdriver.common.by import By
from utils.page_base import PageBase
import logging
logger = logging.getLogger()

class HeaderPage(PageBase):

    cart_icon = (By.XPATH, "//div[@class='header__link-icon-cart']")
    number_of_products_in_cart = (By.XPATH, "//div[@class='header__link-icon-cart-number']")

    def cart_icon(self):
        elem_cart = self.find_element(self.cart_icon)
        logger.info("go to cart.html page")
        return elem_cart

    def check_number_of_products_in_cart(self):
        elem_number_in_cart = self.find_element(self.number_of_products_in_cart)
        logger.info("check_number_of_products_in_cart")
        return elem_number_in_cart.text