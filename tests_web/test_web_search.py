from collections import Counter
import pytest
from page_objects.search_page import SearchPage
import logging
logger = logging.getLogger()

@pytest.mark.parametrize('test_input', ['洋裝', '', 'Hello'])
def test_search(driver, db_cursor, test_input):
    search_page = SearchPage(driver)
    search_page.input_search_box(test_input)
    search_products_list = search_page.get_search_result_info()

    search_db_list = search_page.get_search_result_from_db(db_cursor, test_input)
    # 用 counter 解決 list 排序不同問題
    compare = Counter(search_products_list) == Counter(search_db_list)
    assert compare == True, f'Search result is not correct'
    logger.info('test_category() INFO message')
