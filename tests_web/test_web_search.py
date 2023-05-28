from collections import Counter
import pytest
from page_objects.search_page import SearchPage
import logging
logger = logging.getLogger()

@pytest.mark.parametrize('test_input', ['洋裝', '', 'Hello'])
def test_search(driver, db_cursor, test_input):
    logger.info("Start: test_search")
    search_page = SearchPage(driver)
    logger.info("Input Search Box")
    search_page.input_search_box(test_input)
    logger.info('Get search result')
    search_products_list = search_page.get_search_result_info()
    logger.info('Get search result from DB')

    search_db_list = search_page.get_search_result_from_db(db_cursor, test_input)
    logger.info('Verify search result')
    # 用 counter 解決 list 排序不同問題
    compare = Counter(search_products_list) == Counter(search_db_list)
    assert compare == True, f'Search result is not correct'
    logger.info('test_search finished')
