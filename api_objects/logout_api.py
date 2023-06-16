import logging
import os
from utils.api_utils import APIBase
from utils.database_utils import DatabaseUtil


class LogoutAPI(APIBase):
    def logout(self):
        url_logout = f'{os.getenv("API_DOMAIN")}/user/logout'
        self.api_request("post", url_logout)
        logging.info("Send logout request")

        return self
