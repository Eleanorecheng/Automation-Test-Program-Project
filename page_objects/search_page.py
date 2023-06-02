from selenium.webdriver.common.by import By
from utils.database_utils import DatabaseUtil
from utils.page_base import PageBase

class SearchPage(PageBase):
    database_util = DatabaseUtil()
    search_box = (By.CSS_SELECTOR,'input[class="header__search-input"]')
    all_products_by_search = (By.XPATH, "//div[contains(@class, 'product__title')]")

    def input_search_box(self, input_value):
        element = self.find_element(self.search_box)
        self.input_and_send_key(element, input_value)

    def scroll_to_load_all_search_result(self):
        current_num = 0
        search_products_list = []
        while True:
            self.scroll_down()
            elem = self.find_element(
                (By.XPATH, f"//div[@class='products' and count(a) > {current_num}]"), throw_exception=False,
                waiting_time=3)
            current_search = self.find_elements(self.all_products_by_search, throw_exception=False)
            if elem is None:
                for search_result in current_search:
                    search_products_list.append(search_result.text)
                return search_products_list
            else:
                current_num = len(current_search)

    # def get_search_result_info(self):
    #     get_current_search_result = self.scroll_to_load_all_search_result()
    #     if get_current_search_result is None:
    #         get_current_search_result = []
    #     search_products_list = []
    #     for search_result in get_current_search_result:
    #         search_products_list.append(search_result.text)
    #     return search_products_list

    def get_search_result_from_db(self, db_cursor, input):
        sql = f"SELECT title from product where title like '%{input}%'"
        return self.database_util.get_db_result(db_cursor, sql)
