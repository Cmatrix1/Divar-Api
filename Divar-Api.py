from requests import post, get
from unidecode import unidecode
from time import sleep

YourToken = 'Basic ' ## Enter your token from Cookies below


class Divar:
    def __init__(self, city="tehran", category="real-estate", cnt=10):
        self.city = city
        self.category = category
        self.pro_cnt = cnt
        self.url = "https://api.divar.ir/v8/web-search/3/"
        self.ext_lst = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://divar.ir/',
            'Origin': 'https://divar.ir',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Authorization': YourToken,
            'Connection': 'keep-alive',
        }

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
            if len(self.ext_lst) == self.pro_cnt:
                return False
        return True
    
    def extract_number(self, token):
        response = get(f'https://api.divar.ir/v8/postcontact/web/contact_info/{token}', headers=self.headers).json()
        try:
            return response["widget_list"][0]["data"]["action"]["payload"]["phone_number"]
        except:
            None

    def main(self):
        req = self.__send_request(self.url)
        status = True
        while status:
            status = self.extract_prodcuts(req)
            req = self.__send_request(self.url, req["last_post_date"])
            sleep(2)
        return self.ext_lst

divar = Divar("mashhad", cnt=20)

## For Extract Numbers
for product in divar.main():
    number = divar.extract_number(product["token"])
    print(number)


