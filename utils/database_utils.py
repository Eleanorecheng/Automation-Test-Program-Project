import logging
import os


class DatabaseUtil():

    def get_db_result(self, db_cursor, sql, column):
        result_list = []
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for key, value in enumerate(result):
            result_list.append(f'{value[column]}')  # result_list.append(f'{value["title"]}')
        return result_list

    def get_db_result_fetchone(self, db_cursor, sql):
        db_cursor.execute(sql)
        result = db_cursor.fetchone()
        logging.info(f'query result : {result}')
        return result

    def get_db_result_fetchall(self, db_cursor, sql):
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        logging.info(f'query result : {result}')
        return result

    # /login
    def get_user_result_from_db(self, db_cursor, input):
        sql = f"SELECT id, provider, email, name, picture, access_token, access_expired, login_at from user where email = '{input}'"
        return self.get_db_result_fetchone(db_cursor, sql)

    # /products -> id 去拿 product table 資訊
    # def get_products_count_from_db_by_page(self, db_cursor, category, paging):
    #     sql_count = f"SELECT id FROM product WHERE category = '{category}' LIMIT {(paging+1)*6} UNION ALL SELECT FOUND_ROWS()"
    #     return self.get_db_result_fetchone(db_cursor, sql_count)[0]

    def get_products_result_from_db(self, db_cursor, id):
        sql = f"SELECT id, category, title, description, price, texture, wash, place, note, story \
            FROM product WHERE id = {id}"
        return self.get_db_result_fetchone(db_cursor, sql)

    def get_products_main_image_from_db(self, db_cursor, id):
        sql = f"SELECT main_image FROM product WHERE id = {id}"
        main_image_filename = self.get_db_result_fetchone(db_cursor, sql)['main_image']
        main_image = f"{os.environ.get('DOMAIN')}/assets/{id}/{main_image_filename}"
        return main_image

    def get_products_variants_result_from_db(self, db_cursor, product_id):
        sql = f"SELECT variant.product_id, color.code, variant.size, variant.stock \
        FROM variant INNER JOIN product on product.id = variant.product_id \
        INNER JOIN color on color.id = variant.color_id \
        WHERE variant.product_id = {product_id}"
        return self.get_db_result_fetchall(db_cursor, sql)

    def composite_variants(self, db_cursor, product_id):
        variants = []
        for value in enumerate(self.get_products_variants_result_from_db(db_cursor, product_id)):
            variant = {
                'color_code': f"{value[1]['code']}",
                'size': f"{value[1]['size']}",
                'stock': value[1]['stock']
            }
            variants.append(variant)
        return variants


    def get_products_color_result_from_db(self, db_cursor, product_id):
        sql = f"SELECT DISTINCT color.code, color.name \
        FROM variant INNER JOIN product on product.id = variant.product_id \
        INNER JOIN color on color.id = variant.color_id WHERE variant.product_id = {product_id}"
        return self.get_db_result_fetchall(db_cursor, sql)

    def composite_color(self, db_cursor, product_id):
        colors = []
        for value in enumerate(self.get_products_color_result_from_db(db_cursor, product_id)):
            color = {
                'code': value[1]['code'],
                'name': value[1]['name']
            }
            colors.append(color)
        return colors

    def get_products_size_result_from_db(self, db_cursor, product_id):
        sql = f"Select distinct size from variant WHERE product_id = {product_id}"
        return self.get_db_result_fetchall(db_cursor, sql)

    def composite_size(self, db_cursor, product_id):
       db_data = self.get_products_size_result_from_db(db_cursor, product_id)
       sizes = [size['size'] for size in db_data]
       return sizes

    def get_products_images_result_from_db(self, db_cursor, product_id):
        sql = f"SELECT image FROM product_images WHERE product_id ={product_id}"
        images = [f"{os.environ.get('DOMAIN')}/assets/{product_id}/{filename['image']}" for filename in self.get_db_result_fetchall(db_cursor, sql)]
        return images



    # /products search -> id 去拿 product table 資訊
    def get_products_search_result_from_db(self, db_cursor, keyword):
        sql = f"SELECT id, title FROM product where title like '%{keyword}%'"
        return self.get_db_result_fetchone(db_cursor, sql)