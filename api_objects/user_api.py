import os

from utils.api_utils import APIBase
from utils.database_utils import DatabaseUtil


class UserAPI(APIBase):
    def login(self, provider, email, password):
        url_login = f'{os.getenv("API_DOMAIN")}/user/login'

        payload = {
            "provider": provider,
            "email": email,
            "password": password
        }
        self.api_request("post", url_login, json=payload)
        return self

    def get_json(self, title):
        return self.response.json()[title]

    def get_user_result_from_db(self, db_cursor, input):
        database_utils = DatabaseUtil()
        sql = f"SELECT * from user where email = '{input}'"
        return database_utils.get_db_result_no_column(db_cursor, sql)

    def assert_message(self, expected_result, actual_result):
        return f'Expected Result: {expected_result}, Actual Result: {actual_result} '

    def logout(self):
        url_logout = f'{os.getenv("API_DOMAIN")}/user/logout'
        self.api_request("post", url_logout)
        return self

    def profile(self):
        url_profile = f'{os.getenv("API_DOMAIN")}/user/profile'
        self.api_request("get", url_profile)
        return self
