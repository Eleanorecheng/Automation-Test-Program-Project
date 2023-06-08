import numpy as np
import pandas as pd


class TestData():
    def read_data(self, sheet_name):
        df = pd.read_excel('../test_data/Stylish_TestCase.xlsx', sheet_name=sheet_name, dtype=str)
        # 處理empty
        df = df.fillna('')
        # 處理 N chars case
        df = df.applymap(lambda x: int(x.replace('chars', '').strip()) * 'B' if 'chars' in x else str(x))
        # 一定要加if不然會把未replace的data轉成int

        checkout_invalid_list = []
        # for row in range(df.shape[0]):
        #     one_row = df.iloc[row, :]
        #     checkout_invalid_list.append(one_row.to_dict())
        # return checkout_invalid_list

        data_dict = df.to_dict('records')
        checkout_invalid_list.append(data_dict)
        return data_dict

    # # 使用 replace 的延伸問題：如果有人名字中真的包含 'chars' 也會被 replace 掉 -> 解法？
    # def replace_term(self, term):
    #     if 'chars' in term:
    #         term = term.replace('chars', "")
    #         result = 'B' * int(term)
    #         return result
