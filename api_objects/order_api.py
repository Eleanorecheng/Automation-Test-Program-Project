import json
import os
import urllib

from utils.api_utils import APIBase
import logging
from test_data.test_data_from_excel import TestData

test_data = TestData()

read_payload = test_data.read_data('API Checkout with Invalid Value')


class OrderAPI(APIBase):

    def get_prime(self):
        url_getPrime = "https://js.tappaysdk.com/tpdirect/sandbox/getprime"
        headers = {
            "x-api-key": f'{os.getenv("X_API_KEY")}',
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            'jsonString':
                {
                    "cardnumber": "4242424242424242",
                    "cardduedate": "202404",
                    "cardccv": "424",
                    "appid": 12348,
                    "appkey": f'{os.getenv("X_API_KEY")}',
                    "appname": "54.201.140.239",
                    "url": f'{os.getenv("DOMAIN")}',
                    "port": "",
                    "protocol": "http:",
                    "fraudid": ""
                }
        }
        encoded_data = urllib.parse.urlencode(data)
        self.api_request("post", url_getPrime, headers=headers, data=encoded_data)
        logging.info("Send get prime request")
        return self.get_json("card")["prime"]

    def order(self, test_data):
        if test_data["Prime"] == 'empty':
            prime = ""
        elif test_data["Prime"] == 'invalid':
            prime = test_data["Prime"]
        else:
            prime = self.get_prime()

        url_order = f'{os.getenv("API_DOMAIN")}/order'
        self.payload = {
            "prime": f'{prime}',
            "order": {
                "shipping": test_data["Shipping"],
                "payment": test_data["Payment"],
                "subtotal": test_data["Subtotal"],
                "freight": test_data["Freight"],
                "total": test_data["Total"],
                "recipient": {
                    "name": test_data["Receiver"],
                    "phone": test_data["Mobile"],
                    "email": test_data["Email"],
                    "address": test_data["Address"],
                    "time": test_data["Deliver Time"]
                },
                "list": [
                    {
                        "color": eval(test_data['Color']),
                        "id": test_data["Id"],
                        "image": test_data["Image"],
                        "name": test_data["Name"],
                        "price": test_data["Price"],
                        "qty": test_data["Qty"],
                        "size": test_data["Size"]
                    }
                ]
            }
        }
        # int(0) can parsr empty string
        print("payload", self.payload)
        self.api_request("post", url_order, json=self.payload)
        logging.info("Send order request")
        return self

    def get_order_info(self, order_id):
        url_get_order = f'{os.getenv("API_DOMAIN")}/order/{order_id}'
        self.api_request("get", url_get_order)
        return self
