from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageBase():

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, clickable=False, throw_exception=True):
        try:
            if clickable:
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                )
            else:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(locator)
                )
            return element
        except Exception as e:
            if throw_exception:
                raise e
            print(e)

    def find_elements(self, locator):
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(locator)
        )
        return elements