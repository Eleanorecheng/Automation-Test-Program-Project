
# 可以合在一起
class DatabaseUtil():

    def get_db_result(self, db_cursor, sql):
        result_list = []
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for key, value in enumerate(result):
            result_list.append(f'{value["title"]}')
        return result_list

    def get_search_result_from_db(self, db_cursor, input):
        sql = f"SELECT title from product where title like '%{input}%'"
        return self.get_db_result(db_cursor, sql)