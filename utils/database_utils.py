class DatabaseUtil():

    def get_db_result(self, db_cursor, sql, column):
        result_list = []
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for key, value in enumerate(result):
             result_list.append(f'{value[column]}')  # result_list.append(f'{value["title"]}')
        return result_list