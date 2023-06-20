import os
from utils.api_utils import APIBase
import logging

class ProductsSearchAPI(APIBase):
    def products_by_search(self, keyword, paging):
        if paging != "":
            url_products_search = f'{os.getenv("API_DOMAIN")}/products/search?keyword={keyword}&paging={paging}'
        else:
            url_products_search = f'{os.getenv("API_DOMAIN")}/products/search?keyword={keyword}'

        self.api_request("get", url_products_search)
        logging.info("Send products search request")
        return self

    def products_by_search_without_keyword(self):
        url_products_search = f'{os.getenv("API_DOMAIN")}/products/search?keyword='
        self.api_request("get", url_products_search)
        logging.info("Send products search request")
        return self