import requests as rq
import json

class Remitano(object):
    """Class handle request to remitano.com api
    """
    host = "https://api.remitano.com"
    
    def __init__(self, api_key=None, api_secret=None, lang='vi', country_code='vn'):
        self.lang = lang
        self.country_code = country_code
        
    def request_public(self, method=None, path=None, payload={}):
        # method:: "POST", "GET"
        
        full_path = self.host + '/api/v1' + path
        headers = {
            'accept': 'application/json',
            'lang': self.lang,
            'country_code': self.country_code
        }
        req = rq.request(method, full_path, headers=headers, data=payload)
        return req.json()
        
    def get_public(self, *args, **kwargs):
        return self.request_public(method="GET", *args, **kwargs)
    
    def post_public(self, *args, **kwargs):
        return self.request_public(method="POST", *args, **kwargs)
        
    def get_ads(self):
        return self.get_public(path='/rates/ads')
    
    def get_exchange(self):
        return self.get_public(path='/rates/exchange')
    
    def offers(self, offer_type=None, country_code='vn', coin=None, coin_currency='eth', offline=False, page=1, per_page=5, username=None):
        """
        :per_page int: Data per request
        :offer_type str: value can be 'buy' or 'sell'
        :country_code str: default is 'vn'
        :coin str: default is 'eth'
        :offline bool: can be False or True
        :page int: number of page
        :coin_currency str: default is eth
        :username str: this is option, can request base on username
        """
        
        if coin is None:
            coin = coin_currency
            
        payload = {
            'offer_type': offer_type,
            'country_code': country_code,
            'coin': coin,
            'offline': offline,
            'page': page,
            'coin_currency': coin_currency,
            'per_page': per_page,
        }

        if username:
            payload['username'] = username
        
        return self.get_public(path='/offers', payload=payload)
    
    def buy_offers(self, *args, **kwargs):
        return self.offers(offer_type='buy', *args, **kwargs)
        
    def sell_offers(self, *args, **kwargs):
        return self.offers(offer_type='sell', *args, **kwargs)
    
    def price_ladders(self, pair=None, payload={}):
        # Not sure about options
        return self.get_public(path='/price_ladders/{pair}'.format(pair=pair), payload=payload)
    
    def best(self, coin_amount=1, coin_currency='eth', country_code="vn", offer_type="buy"):
        payload = {
            'coin_amount': coin_amount,
            'coin_currency': coin_currency,
            'country_code':country_code,
            'offer_type': offer_type,
            'bank_name': 'Vietcombank'
        }

        return self.post_public(path='/offers/best', payload=payload)

    def coin_list_popup_data(self, fiat_currency='VND'):
        payload = {'fiat_currency': fiat_currency}
        return self.get_public(path='/p2p_stats/coin_list_popup_data', payload=payload)
    
    def exchange(self):
        return self.get_public(path='/rates/exchange')
    