import os
from selenium.webdriver.common.by import By
from utils.page_base import PageBase
from utils.database_utils import DatabaseUtil


class LoginPage(PageBase):
    database_util = DatabaseUtil()
    email_field = (By.XPATH, "//input[@id='email']")
    password_field = (By.XPATH, "//input[@id='pw']")
    login_btn = (By.XPATH, "//button[@class='login100-form-btn']")
    logout_btn = (By.XPATH, "//*[@class='profile__content']/button")

    def input_email_and_password_to_login(self, email, password):
        elem_email = self.find_element(self.email_field)
        self.input_and_send_key(elem_email, email)
        elem_password = self.find_element(self.password_field)
        self.input_and_send_key(elem_password, password)
        elem_login_btn = self.find_element(self.login_btn, clickable=True)
        elem_login_btn.click()

    def get_local_storage(self, key):
        jwt_token = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", "jwtToken")
        return jwt_token

    def set_local_storage(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def click_logout_btn(self):
        elem_logout_btn = self.find_element(self.logout_btn, clickable=True)
        elem_logout_btn.click()

    def get_access_token_from_db(self, db_cursor):
        sql = f"SELECT access_token from user where email = '{os.getenv('EMAIL')}'"
        # 預期只會拿回一筆 access_token, 而 get_db_result 是回傳一個 list, 因此取第一筆
        return self.database_util.get_db_result(db_cursor, sql, "access_token")[0]