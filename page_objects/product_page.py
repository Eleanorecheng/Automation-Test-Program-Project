import random
from selenium.webdriver.common.by import By
from utils.page_base import PageBase
import logging
logger = logging.getLogger()

class ProductPage(PageBase):
    product_title = (By.XPATH, "//div[@class='product__title']")
    product_id = (By.XPATH, "//div[@class='product__id']")
    product_price = (By.XPATH, "//div[@class='product__price']")
    product_color = (By.XPATH, "//div[@class='product__color']")
    product_size = (By.XPATH, "//div[@class='product__size']")
    product_qty_add = (By.XPATH, "//div[@class='product__quantity-add']")
    product_qty_minus = (By.XPATH, "//div[@class='product__quantity-minus']")
    product_qty_value = (By.XPATH, "//div[@class='product__quantity-value']")
    add_to_cart = (By.XPATH, "//button[@class ='product__add-to-cart-button']")
    number_of_products_in_cart = (By.XPATH, "//div[@class='header__link-icon-cart-number']")
    random_product = ""
    product_selected_color = (By.XPATH, "//div[@class='product__color product__color--selected']")

    # 隨機取得首頁中的產品 -> 應該放到其他page
    def select_product_and_enter_product_page(self):
        self.scroll_down()
        elem_random_product = random.choice(self.find_visible_elements(self.product_title))
        self.random_product = elem_random_product.text
        logging.info(f'Selected product: {self.random_product}')

        # self.driver.execute_script("arguments[0].scrollIntoView()", elem_random_product)
        # elem_random_product.click()
        self.driver.execute_script("arguments[0].click()", elem_random_product)
        logger.info("Click product")

        # self.driver.execute_script("arguments[0].click()", elem_random_product)
        self.find_element(self.product_title, clickable=False, waiting_time=15)
        logger.info(f'Select_product_and_enter_product_page')

    # product_page
    def select_color(self):
        elem_selected_color = random.choice(self.find_elements(self.product_color))
        logger.info(f'Selected color: {elem_selected_color.get_attribute("data_id")}')

        elem_selected_color.click()
        logger.info("Click color")

        return elem_selected_color

    def select_size(self):
        elem_selected_size = random.choice(self.find_elements(self.product_size))
        logger.info(f'Selected size: {elem_selected_size.text}')

        elem_selected_size.click()
        logger.info("Click size")
        return elem_selected_size.text

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


    def get_add_to_cart_btn(self):
        logger.info("Method: add_to_cart")
        elem_add_to_cart_btn = self.find_element(self.add_to_cart)
        return elem_add_to_cart_btn

    def check_number_of_products_in_cart(self):
        elem_number_in_cart = self.find_element(self.number_of_products_in_cart)
        logger.info(f'Number in Cart: {elem_number_in_cart.text}')
        return elem_number_in_cart.text

    ## -- 加入購物車前，記錄產品資訊 --
    def get_quantity(self):
        elem_qty_value = self.find_element(self.product_qty_value)
        logger.info(f'Quantity Value: {elem_qty_value.text}')
        return elem_qty_value.text

    def get_title(self):
        elem_title = self.find_element(self.product_title)
        logger.info(f'Title Value: {elem_title.text}')
        return elem_title.text

    def get_id(self):
        elem_id = self.find_element(self.product_id)
        logger.info(f'Id Value: {elem_id.text}')
        return elem_id.text

    def get_price(self):
        elem_price = self.find_element(self.product_price)
        logger.info(f'Price Value: {elem_price.text}')
        return elem_price.text.split('.')[1]

    # 還有 select_color 跟 select_size

    def get_product_color_name_after_mapping(self):
        color_mapping = {
            'FFFFFF': '白色',
            'DDFFBB': '亮綠',
            'CCCCCC': '淺灰',
            'BB7744': '淺棕',
            'DDF0FF': '淺藍',
            '334455': '深藍',
            'FFDDDD': '粉紅'
        }

        product_color = self.select_color().get_attribute("data_id")
        color_code = product_color[-6:]
        color_name = color_mapping.get(color_code)
        return color_name

    def get_product_info(self):
        product_info = {
            'title': self.get_title(),
            'id': self.get_id(),
            'color': self.get_product_color_name_after_mapping(),
            'size': self.select_size(),
            'price': self.get_price()
        }
        return product_info