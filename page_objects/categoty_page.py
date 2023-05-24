from selenium.webdriver.common.by import By
from page_objects.page_base import PageBase

class CategoryPage(PageBase):
    def select_category(self, category):
        return (By.XPATH,f"//a[text() = '{category}']")
    # 點擊 category menu
    def click_category(self, category):
        category_element = self.find_element(self.select_category(category), clickable=True)
        category_element.click()

    def get_products_by_category(self):
        return (By.XPATH,"//div[contains(@class, 'product__title')]")
    # 取得category中的所有產品
    def get_category_info(self):
        category_products = self.find_elements(self.get_products_by_category())
        category_products_list = []
        for product in category_products:
           category_products_list.append(product.text)
        return category_products_list