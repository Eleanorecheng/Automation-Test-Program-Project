import random
from selenium.webdriver.common.by import By
from utils.page_base import PageBase
import logging
logger = logging.getLogger()

class ProductPage(PageBase):
    all_products_name = (By.XPATH, "//div[contains(@class, 'product__title')]")
    product_name = (By.XPATH, "//div[@class='product__title']")
    product_color = (By.XPATH, "//div[@class='product__color']")
    product_size = (By.XPATH, "//div[@class='product__size']")
    product_qty_add = (By.XPATH, "//div[@class='product__quantity-add']")
    product_qty_minus = (By.XPATH, "//div[@class='product__quantity-minus']")
    product_qty_value = (By.XPATH, "//div[@class='product__quantity-value']")
    add_to_cart = (By.XPATH, "//button[@class ='product__add-to-cart-button']")
    number_of_products_in_cart = (By.XPATH, "//div[@class='header__link-icon-cart-number']")

    def scroll_to_load_all_product_result(self):
        current_num = 0
        all_products_list = []
        while True:
            self.scroll_down()
            elem = self.find_element(
                (By.XPATH, f"//div[@class='products' and count(a) > {current_num}]"), throw_exception=False,
                waiting_time=3)
            current_search = self.find_elements(self.all_products_name, throw_exception=False)
            if elem is None:
                for per_result in current_search:
                    all_products_list.append(per_result.text)
                logger.info("scroll_to_load_all_product_result")
                return all_products_list
            else:
                current_num = len(current_search)


    def select_product_and_enter_product_page(self):
        # 取得所有產品名
        get_all_products_list = self.scroll_to_load_all_product_result()
        # 隨機選擇則產品
        get_selected_product = random.choice(get_all_products_list)
        target = self.driver.find_element(By.XPATH,
                                          f"//div[@class='product__title' and text() = '{get_selected_product}']")
        # 不知為何不能先用scrollIntoView 再 click???
        # self.driver.execute_script("arguments[0].scrollIntoView()", target)
        # target.click()
        self.driver.execute_script("arguments[0].click()", target)
        elem_product_name = self.find_element(self.product_name, clickable=False, waiting_time=15)
        assert elem_product_name.text == get_selected_product
        logger.info("select_product_and_enter_product_page")

    def select_color(self):
        logger.info("Method: select_color")
        get_selected_color = random.choice(self.find_elements(self.product_color))
        get_selected_color.click()
        logger.info("select_color")
        return get_selected_color

    def select_size(self):
        logger.info("Method: select_size")
        get_selected_size = random.choice(self.find_elements(self.product_size))
        get_selected_size.click()
        logger.info("select_size")
        return get_selected_size

    # 驗證 size default 是不會被選到的
    def check_size_default_status(self):
        elem_size = self.find_elements(self.product_size)
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
        logger.info("check_quantity")
        return elem_qty_value.text

    def get_add_to_cart_btn(self):
        logger.info("Method: add_to_cart")
        elem_add_to_cart_btn = self.find_element(self.add_to_cart)
        logger.info("get_add_to_cart_btn")
        return elem_add_to_cart_btn

    def check_number_of_products_in_cart(self):
        elem_number_in_cart = self.find_element(self.number_of_products_in_cart)
        logger.info("check_number_of_products_in_cart")
        return elem_number_in_cart.text
