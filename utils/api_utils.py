from datetime import datetime
import logging


class APIBase:
    def __init__(self, session):
        self.response = None
        self.session = session

    def api_request(self, method, url, **kwargs):
        self.response = self.session.request(method, url, **kwargs)

    def get_json(self, title):
        logging.info("get response in json format")
        return self.response.json()[title]
