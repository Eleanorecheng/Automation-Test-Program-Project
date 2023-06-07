import numpy as np
import pandas as pd


class TestData():
    def read_checkout_with_intalid_value(self):
        df_checkout_invalid = pd.read_excel('../test_data/Stylish_TestCase.xlsx', sheet_name='Checkout with Invalid Value')
        checkout_invalid_list = []

        for row in range(df_checkout_invalid.shape[0]):  # 該 datafrane 的總列數
            one_row = df_checkout_invalid.iloc[row, :]  # 取出第 i 行 row
            checkout_invalid_list.append({
                'receiver': self.replace_term(one_row['Receiver']),
                'email': self.replace_term(one_row['Email']),
                'mobile': one_row['Mobile'],
                'address': self.replace_term(one_row['Address']),
                'deliver Time': one_row['Deliver Time'],
                'credit card no': one_row['Credit Card No'],
                'expiry date': one_row['Expiry Date'],
                'security code': one_row['Security Code']
            })
        return checkout_invalid_list

# 使用 replace 的延伸問題：如果有人名字中真的包含 'chars' 也會被 replace 掉 -> 解法？
    def replace_term(self, term):
        if term is not np.nan and "chars" in term:
            times = int(str(term).replace('chars', ''))
            result = 'B' * times
            return result


