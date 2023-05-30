from selenium.common import NoSuchElementException # 不能用
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageBase():

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, clickable=False, throw_exception=True, waiting_time=10):
        try:
            if clickable:
                element = WebDriverWait(self.driver, waiting_time).until(
                    EC.element_to_be_clickable(locator)
                )
            else:
                element = WebDriverWait(self.driver, waiting_time).until(
                    EC.presence_of_element_located(locator)
                )
            return element
        except Exception as e:
            if throw_exception:
                raise e
            return None
    def find_elements(self, locator, throw_exception=True):
        try:
            elements = WebDriverWait(self.driver, 3).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            if throw_exception:
                raise e
            return []
    def scroll_down(self):
        return self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

    def input_and_send_key(self, element, input_value):
        element.clear()
        element.send_keys(input_value, Keys.ENTER)

    def get_db_result(self, db_cursor, sql):
        result_list = []
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for key, value in enumerate(result):
            result_list.append(f'{value["title"]}')
        return result_list
