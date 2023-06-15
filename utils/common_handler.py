import datetime


class APICommonHandler():

    def assert_message(self, expected_result, actual_result):
        return f'Expected Result: {expected_result}, Actual Result: {actual_result} '

    def parse_datetime(self, string_value):
        parsed_datetime = datetime.strptime(string_value[:-5], '%Y-%m-%dT%H:%M:%S')
        return parsed_datetime