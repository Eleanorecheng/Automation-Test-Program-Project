import numpy as np
import pandas as pd


class TestData():
    def read_checkout_with_invalid_value(self):
        df = pd.read_excel('../test_data/Stylish_TestCase.xlsx', sheet_name='Checkout with Invalid Value', dtype=str)
        df = df.fillna('')
        df.applymap(str)

        checkout_invalid_list = []
        for row in range(df.shape[0]):  # 該 datafrane 的總列數
            one_row = df.iloc[row, :]  # 取出第 i 行 row
            checkout_invalid_list.append(one_row.to_dict())

        return checkout_invalid_list

    # 使用 replace 的延伸問題：如果有人名字中真的包含 'chars' 也會被 replace 掉 -> 解法？
    def replace_term(self, term):
        if 'chars' in term:
            term = term.replace('chars', "")
            result = 'B' * int(term)
            return result