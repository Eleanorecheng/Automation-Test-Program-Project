import os
from utils.api_utils import APIBase
import logging

class LoginAPI(APIBase):
    def login(self, provider, email, password):
        url_login = f'{os.getenv("API_DOMAIN")}/user/login'

        self.payload = {
            "provider": provider,
            "email": email,
            "password": password
        }
        self.api_request("post", url_login, json=self.payload)
        logging.info("Send login request")
        return self