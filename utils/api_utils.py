from datetime import datetime
import logging


class APIBase:
    def __init__(self, session):
        self.response = None
        self.session = session

    def api_request(self, method, url, **kwargs):
        logging.info(f"Request method: {method}")
        logging.info(f"Request url: {self.url}")
        logging.info(f"Request Cookies: {self.session.cookies}")
        logging.info(f"Request headers: {self.session.headers}")
        self.response = self.session.request(method, url, **kwargs)
        logging.info(f"response.json(): {self.response.json()}")

    def get_json(self, title):
        logging.info("get response in json format")
        return self.response.json()[title]
