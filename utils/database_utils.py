import logging


class DatabaseUtil():

    def get_db_result(self, db_cursor, sql, column):
        result_list = []
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for key, value in enumerate(result):
             result_list.append(f'{value[column]}')  # result_list.append(f'{value["title"]}')
        return result_list

    def get_db_result_no_column(self, db_cursor, sql):
        db_cursor.execute(sql)
        result = db_cursor.fetchone()
        logging.info(f'query result : {result}')
        return result

    def get_user_result_from_db(self, db_cursor, input):
        sql = f"SELECT * from user where email = '{input}'"
        return self.get_db_result_no_column(db_cursor, sql)
