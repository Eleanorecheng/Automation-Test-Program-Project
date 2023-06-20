import os
from utils.api_utils import APIBase
import logging

class ProductsDetailsAPI(APIBase):
    def products_by_details(self, product_id):
        url_products_details = f'{os.getenv("API_DOMAIN")}/products/details?id={product_id}'
        self.api_request("get", url_products_details)
        logging.info("Send products details request")
        return self
