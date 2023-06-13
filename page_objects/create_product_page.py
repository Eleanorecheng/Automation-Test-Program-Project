import logging

from selenium.webdriver.common.by import By
from test_data.test_data_from_excel import TestData
from utils.page_base import PageBase


class CreateProductPage(PageBase):
    create_product_btn = (By.XPATH, '//button[text()="Create New Product"]')
    category = (By.XPATH, '//select[@name="category"]')
    description = (By.XPATH, '//textarea[@name="description"]')
    main_image = (By.XPATH, '//input[@name="main_image"]')
    submit = (By.XPATH, '//input[@value="Create"]')

    id = (By.XPATH,)
    test_data = TestData()

    def elem_input_field(self, item):
        locator = (By.XPATH, f'//input[@name="{item}"]')
        logging.info("Get input field element")
        return self.find_element(locator)

    # category
    def input_field_dropdown(self, option):
        self.select_item(self.category, option)
        logging.info("Select from drop down")

    def input_field_description(self, content):
        self.input_and_send_key(self.find_element(self.description), content)
        logging.info("Send description field")


    def input_field_general(self, data):
        self.input_field_send_key(title=data['Title'],
                                 price=data['Price'],
                                 texture=data['Texture'],
                                 wash=data['Wash'],
                                 place=data['Place of Product'],
                                 note=data['Note'],
                                 story=data['Story'])
        logging.info("Input field and send key through testing data")


    def input_field_send_key(self, **kwargs):
        for item, content in kwargs.items():
            self.input_and_send_key(self.elem_input_field(item), content)
        logging.info("Input field and send key  with **kwargs")


    def select_product_color(self, color_names):
        if color_names == '全選':
            color_name_list = ['白色', '亮綠', '淺灰', '淺棕', '淺藍', '深藍', '粉紅']
        else:
            color_name_list = color_names.split(',')
            logging.info("Split color names")

        try:
            for color_name in color_name_list:
                color_index = self.produt_color_mapping(color_name.strip())
                color = (By.XPATH, f'//input[@name="color_ids" and @value={color_index}]')
                logging.info("Get color locator")
                self.find_element(color, clickable=True).click()
        except:
            logging.info("No color given")
            return

    def produt_color_mapping(self, color_name):
        color_mapping = ['白色', '亮綠', '淺灰', '淺棕', '淺藍', '深藍', '粉紅']
        try:
            color_id = color_mapping.index(color_name)
            logging.info("Get color mapping index")
            return color_id + 1
        except:
            logging.info("No color index given")
            return

    def select_product_size(self, size_names):
        if size_names == '全選':
            size_name_list = ['S', 'M', 'L', 'XL', 'F']
        else:
            size_name_list = size_names.split(',')
        try:
            for size_name in size_name_list:
                size = (By.XPATH, f'//input[@name="sizes" and @value="{size_name.strip()}"]')
                logging.info("Select product size")
                self.find_element(size, clickable=True).click()
        except:
            logging.info("No size given")
            return


    def upload_main_image(self, image_name):
        try:
            uploader = self.find_element(self.main_image)
            logging.info("Get main image")
            uploader.send_keys(f'{self.test_data.get_data_file_url()}/{image_name}.jpg')
        except:
            logging.info("No main image given")
            return

    def locator_other_image(self, index):
        return (By.XPATH, f'//input[@name="main_image"]//following-sibling::input[@type="file"][{index}]')

    def upload_other_images(self, image_name, index):
        try:
            if image_name != '':
                uploader = self.find_element(self.locator_other_image(index), throw_exception=False)
                uploader.send_keys(f'{self.test_data.get_data_file_url()}/{image_name}.jpg')
        except Exception as e:
            raise e

    def click_create_btn(self):
        self.find_element(self.submit, clickable=True).click()

    def get_product_name_in_products_list(self, product_title):
        locator = (By.XPATH, f'//td[@id="product_title" and text() ="{product_title}"]')
        return self.find_element(locator, throw_exception=False)

    def locator_delete_button(self, product_title):
        return (By.XPATH, f'//td[@id="product_title" and text() ="{product_title}"]//following-sibling::td/button')

    def delete_product(self, product_title):
        try:
            self.find_element(self.locator_delete_button(product_title), clickable=True).click()
        except:
            return None

    def check_product_is_existing_beforehand(self, product_title):
        if self.get_product_name_in_products_list(product_title) != None:
            self.delete_product(product_title)
