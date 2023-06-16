import logging
import os
from utils.api_utils import APIBase
from utils.database_utils import DatabaseUtil


class ProfileAPI(APIBase):
    def profile(self):
        url_profile = f'{os.getenv("API_DOMAIN")}/user/profile'
        self.api_request("get", url_profile)
        logging.info("Send profile request")
        return self
