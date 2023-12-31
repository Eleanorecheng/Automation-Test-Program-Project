import logging
from selenium.webdriver import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageBase():

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, clickable=False, throw_exception=True, waiting_time=10):
        logging.info(f"Locator: {locator}") # checkout case flaky issue
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
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            if throw_exception:
                raise e
            return []

    def scroll_down(self):
        return self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

    def find_visible_elements(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(locator))
            return element
        except Exception as e:
            raise e

    def input_and_send_key(self, element, input_value):
        element.clear()
        element.send_keys(input_value, Keys.ENTER)

    def get_alert_message(self):
        # create alert object
        alert = WebDriverWait(self.driver, 15).until(EC.alert_is_present())
        # get alert text
        return alert.text

    def accept_alert(self):
        # create alert object
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert.accept()

    def switch_iframe(self, locator):
        self.driver.switch_to.frame(self.find_element(locator, True))

    def switch_default_content(self):
        self.driver.switch_to.default_content()

    # select item from select list
    def select_item(self, locator, option):
        select = Select(self.find_element(locator))
        select.select_by_visible_text(option)

    # get selected item's text
    def get_selected_item_value(self, locator):
        select = Select(self.find_element(locator))
        return select.first_selected_option.text