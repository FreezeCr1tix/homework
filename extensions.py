import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    keys = {
        'DOLLAR': 'USD', 
        'EURO': 'EUR', 
        'RUBLE': 'RUB' 
    }

    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = CurrencyConverter.keys[base.upper()]
        except KeyError:
            raise APIException(f'Value {base} not found.')

        try:
            quote_key = CurrencyConverter.keys[quote.upper()]
        except KeyError:
            raise APIException(f'Value {quote} not found.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Incorrect value amount.')
        r = requests.get(f'https://v6.exchangerate-api.com/apikey/pair/{base_key}/{quote_key}/{amount}')
        resp = json.loads(r.content)
        rate=resp["conversion_rate"]
        result = rate * amount
        return result
