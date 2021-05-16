import requests


class Crypto:
    def __init__(self):
        self.coin_list = ['ethereum', 'dogecoin', 'bitcoin'],
        self.coin_name = ['eth', 'doge', 'btc']
        self.coin_price = {}
        self.url = 'https://api.nomics.com/v1/currencies/ticker?key=e365ed818393086e839cc4c643f6ad7eeca7a3fc&ids=BTC,ETH,DOGE&interval=1d,30d&convert=KRW&per-page=100&page=1'

    def get_price(self):
        data = requests.get(self.url).json()
        return round(float(data[0].get('price')), 3), round(float(data[1].get('price')), 3), round(float(data[2].get('price')), 3)
