
from requests import cookies, post, get
from unidecode import unidecode
from time import sleep

class Divar:
    def __init__(self, headers: dict = None, cookies: dict = None):
        self.url = "https://api.divar.ir/v8/web-search/3/"
        self.headers = headers or {}
        self.cookies = cookies or {}

    def send_request(self, 
                     category: str = "light", 
                     last_post_date: int = 0, 
                     min_price: int = 0,
                     query: str = ""):
        json = {
            "json_schema": {
                "category": {
                    "value": category
                },
                "cities": [
                    "3"
                ],
                "price": {
                    "min": min_price
                },
                "query": query
            },
            "last-post-date": last_post_date,
            "page": 1
        }
        return post(self.url+category, json=json).json()

    def get_product_detail(self, product_data):
        return {
            'token': product_data['token'],
            'title': product_data['title'],
            'image': product_data['image_url'],
            'price': unidecode(product_data['middle_description_text'][:-6]),
            'description': product_data['bottom_description_text']
            }

    def get_prodcuts(self, 
                     category: str = "ROOT", 
                     last_post_date: int = 0, 
                     min_price: int = 0,
                     query: str = ""):
        
        response = self.send_request(category, last_post_date, min_price, query)
        for product in response["web_widgets"].get("post_list", []):
            yield self.get_product_detail(product["data"])

    def get_all_products(self, 
                     category: str = "ROOT", 
                     last_post_date: int = 0, 
                     min_price: int = 0,
                     query: str = ""):
        
        response = self.send_request(category, last_post_date, min_price, query)
        while last_post_date != None:
            for product in response["web_widgets"].get("post_list", []):
                yield self.get_product_detail(product["data"])

            last_post_date = response["last_post_date"]
            response = self.send_request(category, last_post_date, min_price, query)

    def get_number(self, post_token):
        response = get(
            f'https://api.divar.ir/v8/postcontact/web/contact_info/{post_token}', headers=self.headers).json()
        try:
            return response["widget_list"][0]["data"]["action"]["payload"]["phone_number"]
        except KeyError:
            return None


