import os
from selenium.webdriver.common.by import By
from utils.page_base import PageBase
from utils.database_utils import DatabaseUtil

class CheckoutPage(PageBase):
    checkout_btn = (By.XPATH, "//div[@class='checkout-button']")
    input_field = (By.XPATH, "(//input[@class='form__field-input'])")

    def click_checkout_btn(self):
        elem_checkout_btn = self.find_element(self.checkout_btn, clickable=True)
        elem_checkout_btn.click()

    def input_fields(self, receiver, email, mobile, address):
        elem_input_field = self.find_elements(self.input_field)
        self.input_and_send_key(elem_input_field[1], receiver)
        self.input_and_send_key(elem_input_field[2], email)
        self.input_and_send_key(elem_input_field[3], mobile)
        self.input_and_send_key(elem_input_field[4], address)




