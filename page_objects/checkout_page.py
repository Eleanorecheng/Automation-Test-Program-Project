from selenium.webdriver.common.by import By
from utils.page_base import PageBase


class CheckoutPage(PageBase):
    checkout_btn = (By.XPATH, "//button[@class='checkout-button']")
    input_field_receiver = (By.XPATH, '//div[text()="收件人姓名"]/following-sibling::input')
    input_field_email = (By.XPATH, '//div[text()="Email"]/following-sibling::input')
    input_field_mobile = (By.XPATH, '//div[text()="手機"]/following-sibling::input')
    input_field_address = (By.XPATH, '//div[text()="地址"]/following-sibling::input')
    form_title = (By.XPATH, "//div[@class='form__title']")
    # input_field_iframe = (By.XPATH, f'//input[@id={id}]')

    input_field_card_number = (By.XPATH, '//input[@id="cc-number"]')
    input_field_exp_date = (By.XPATH, '//input[@id="cc-exp"]')
    input_field_security_code = (By.XPATH, '//input[@id="cc-ccv"]')

    thankyou_msg = (By.XPATH, '//div[@class="thankyou__title"]')

    def click_checkout_btn(self):
        elem_checkout_btn = self.find_element(self.checkout_btn, clickable=True)
        elem_checkout_btn.click()

    def input_fields(self, receiver, email, mobile, address, deliver_time):
        self.input_and_send_key(self.find_element(self.input_field_receiver), receiver)
        self.input_and_send_key(self.find_element(self.input_field_email), email)
        self.input_and_send_key(self.find_element(self.input_field_mobile), mobile)
        self.input_and_send_key(self.find_element(self.input_field_address), address)
        if self.transform_deliver_time(deliver_time) != '':
            self.get_deliver_time(self.transform_deliver_time(deliver_time)).click()

    def show_form_title(self):
        self.find_element(self.form_title)

    def get_deliver_time(self, deliver_time):
        # return self.find_element((By.XPATH, f"//label[text() ={deliver_time}]/input"))
        return self.find_element((By.XPATH, f'//label[text()="{deliver_time}"]'), throw_exception=False)

    def transform_deliver_time(self, data_deliver_time):
        if data_deliver_time == 'Morning':
            return '08:00-12:00'
        elif data_deliver_time == 'Afternoon':
            return '14:00-18:00'
        elif data_deliver_time == 'Anytime':
            return '不指定'
        else:
            return ''

    def get_iframe(self, id):
        return (By.XPATH, f'//div[@id="{id}"]/child::iframe')

    def get_iframe_input(self, id):
        return (By.XPATH, f'//div[@id="{id}"]/child::iframe/input')

    def iframe_input_fields_card_number(self, id, card_number):
        self.switch_iframe(self.get_iframe(id))
        elem_card_number = self.find_element(self.input_field_card_number)
        self.input_and_send_key(elem_card_number, card_number)
        self.switch_default_content()

    def iframe_input_fields_exp_date(self, id, exp_date):
        self.switch_iframe(self.get_iframe(id))
        elem_exp_date = self.find_element(self.input_field_exp_date)
        self.input_and_send_key(elem_exp_date, exp_date)
        self.switch_default_content()

    def iframe_input_fields_security_code(self, id, security_code):
        self.switch_iframe(self.get_iframe(id))
        elem_security_code = self.find_element(self.input_field_security_code)
        self.input_and_send_key(elem_security_code, security_code)
        self.switch_default_content()

    def check_thank_you_title(self):
        self.find_element(self.thankyou_msg)
        self.find_element(self.form_title)

    def get_order_info_element(self, info_item):
        # return self.find_element((By.XPATH, f"//label[text() ={deliver_time}]/input"))
        return self.find_element(
            (By.XPATH, f'//div[text()="{info_item}"]/following-sibling::div[@class="form__field-value"]')).text

    def get_order_info(self):
        order_info_list = {
            'receiver': self.get_order_info_element('收件人: '),
            'email': self.get_order_info_element('Email: '),
            'mobile': self.get_order_info_element('手機: '),
            'address': self.get_order_info_element('地址: '),
            'deliver time': self.get_order_info_element('配送時間: ')
        }
        return order_info_list
