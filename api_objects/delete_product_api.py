import os
from utils.api_utils import APIBase
import logging

class DeleteProductAPI(APIBase):

    def delete_product(self, product_id):
        url_delete_products = f'{os.getenv("API_Admin_DOMAIN")}/product/{product_id}'
        self.api_request("delete", url_delete_products)
        logging.info("Send delete product request")
        return self