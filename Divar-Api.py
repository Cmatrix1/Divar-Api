from requests import post
from unidecode import unidecode
from time import sleep

class Divar:
    def __init__(self, city="tehran", category="clothing", cnt=100):
        self.city = city
        self.category = category
        self.pro_cnt = cnt
        self.url = "https://api.divar.ir/v8/web-search/3/"
        self.ext_lst = []

    def __send_request(self, url, last_post_date=0):
        json = {'json_schema': {'category': {'value': self.category}}, 'last-post-date': last_post_date}
        return post(url+self.category, json=json).json()
    
    def __product_detail(self, product):
        return {
                'token': product['data']['token'],
                'title': product['data']['title'],
                'image': product['data']['image_url'],
                'price': unidecode(product['data']['middle_description_text'][:-6]),
                'description': product['data']['bottom_description_text']}

    def extract_prodcuts(self, content):
        for product in content["web_widgets"]["post_list"]:
            self.ext_lst.append(self.__product_detail(product))
            print(len(self.ext_lst))
            if len(self.ext_lst) == self.pro_cnt:
                return False
        return True

    def main(self):
        req = self.__send_request(self.url)
        status = True
        while status:
            status = self.extract_prodcuts(req)
            req = self.__send_request(self.url, req["last_post_date"])
            sleep(2)
Divar("mashhad", cnt=1000).main()

