import datetime


class APICommonHandler():

    def assertion(self, actual_result, expected_result):
        assert actual_result == expected_result, f'Expected Result: {expected_result}, Actual Result: {actual_result} '

    def parse_datetime(self, string_value):
        parsed_datetime = datetime.strptime(string_value[:-5], '%Y-%m-%dT%H:%M:%S')
        return parsed_datetime
