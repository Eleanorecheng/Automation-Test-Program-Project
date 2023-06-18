import os
from utils.api_utils import APIBase
import logging

class ProductsAPI(APIBase):
    def products_by_category(self, category, paging):
        if paging != "":
            url_products = f'{os.getenv("API_DOMAIN")}/products/{category}?paging={paging}'
        else:
            url_products = f'{os.getenv("API_DOMAIN")}/products/{category}'

        self.api_request("get", url_products)
        logging.info("Send products request")
        return self

    def products_by_category_no_category(self, paging):
        url_products = f'{os.getenv("API_DOMAIN")}/products/?paging={paging}'

        self.api_request("get", url_products)
        logging.info("Send products request")
        return self