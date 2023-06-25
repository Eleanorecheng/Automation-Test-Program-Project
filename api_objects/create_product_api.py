import os

from test_data.test_data_from_excel import TestData
from utils.api_utils import APIBase
import logging


class CreateProductsAPI(APIBase):
    test_data = TestData()

    def arrange_payload(self, test_data):
        product_info = {
            'category': test_data['Category'],
            'title': test_data['Title'],
            'description': test_data['Description'],
            'price': test_data['Price'],
            'texture': test_data['Texture'],
            'wash': test_data['Wash'],
            'place': test_data['Place of Product'],
            'note': test_data['Note'],
            'color_ids': str(test_data['ColorIDs']).split(','),
            'sizes': test_data['Sizes'].split(','),
            'story': test_data['Story'],
            'main_image': test_data['Main Image'],
            'other_images': [test_data['Other Image 1'], test_data['Other Image 2']]
        }

        self.body = product_info
        self.files = []

        if product_info['main_image'] != "":
            main_image = f"{self.test_data.get_data_file_url()}/{product_info['main_image']}.jpg"
            self.files.append(('main_image', open(main_image, 'rb')))

        for image in product_info['other_images']:
            if image != "":
                other_image = f"{self.test_data.get_data_file_url()}/{image}.jpg"
                self.files.append(('other_images', open(other_image, 'rb')))

        return product_info


    def create_product(self, test_data):
        url_create_products = f'{os.getenv("API_Admin_DOMAIN")}/product'
        self.arrange_payload(test_data)
        self.api_request("post", url_create_products, data=self.body, files=self.files)
        logging.info("Send create product request")
        return self
