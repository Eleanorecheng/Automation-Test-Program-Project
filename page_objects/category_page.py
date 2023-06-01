from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class CategoryPage(PageBase):
    def select_category(self, category):
        return (By.XPATH, f"//a[text() = '{category}']")

    # 點擊 category menu
    def click_category(self, category):
        category_element = self.find_element(self.select_category(category), clickable=True)
        category_element.click()

    # 所有產品路徑
    all_products_by_category = (By.XPATH, "//div[contains(@class, 'product__title')]")

    # 滑到最底達到所有element list
    def scroll_to_load_all_product(self):
        current_num = 0
        while True:
            self.scroll_down()
            elem = self.find_element(
                (By.XPATH, f"//div[@class='products' and count(a) > {current_num}]"), throw_exception=False, waiting_time=3)
            current_products = self.find_elements(self.all_products_by_category)
            if elem is None:
                return current_products
            else:
                current_num = len(current_products)

    # 取得category中的所有產品
    def get_category_info(self):
        get_current_product = self.scroll_to_load_all_product()
        category_products_list = []
        for product in get_current_product:
            category_products_list.append(product.text)
        return category_products_list
