import pytest
from page_objects.categoty_page import CategoryPage
import logging
logger = logging.getLogger()

# @pytest.mark.parametrize('category', ['女裝', '男裝', '配件'])
@pytest.mark.parametrize("category, expected_products_list", [('女裝',['前開衩扭結洋裝','透肌澎澎防曬襯衫','小扇紋細織上衣','活力花紋長筒牛仔褲','精緻扭結洋裝','透肌澎澎薄紗襯衫','小扇紋質感上衣','經典修身長筒牛仔褲']),
                                                              ('男裝', ['純色輕薄百搭襯衫','時尚輕鬆休閒西裝','經典商務西裝']),
                                                              ('配件',['夏日海灘戶外遮陽帽', '經典牛仔帽', '卡哇伊多功能隨身包','柔軟氣質羊毛圍巾'])])
def test_category(driver, category, expected_products_list):
    category_page = CategoryPage(driver)
    category_page.click_category(category)
    category_products_list = category_page.get_category_info()
    assert category_products_list == expected_products_list
    logger.info('test_category() INFO message')
