from datetime import datetime


class APIBase:
    def __init__(self, session):
        self.response = None
        self.session = session
    def api_request(self, method, url, **kwargs):
        self.response = self.session.request(method, url, **kwargs)

    def parse_datetime(self, string_value):
        parsed_datetime = datetime.strptime(string_value[:-5], '%Y-%m-%dT%H:%M:%S')
        return parsed_datetime