import sys

import requests

cache = {}
exchange_codes = []
currency = []


def update_cache(_currency_code, _exchange_code):
    url = f"http://www.floatrates.com/daily/{_currency_code}.json"
    r = requests.get(url)
    data = r.json()
    exchange_codes.append(_exchange_code)
    cache.update({_exchange_code: data[_exchange_code]["rate"]})


def calculate(_currency_code, _exchange_code, _amount_of_money):
    rate = cache[_exchange_code]
    print(f"You received {round(_amount_of_money * rate, 2)} {_exchange_code.upper()}.")


currency_code = input().lower()
if not currency_code:
    sys.exit()

if currency_code != "usd":
    update_cache(currency_code, "usd")
if currency_code != "eur":
    update_cache(currency_code, "eur")


while True:
    exchange_code = input().lower()
    if not exchange_code:
        sys.exit()
    amount_of_money = float(input())
    print("Checking the cache...")

    if exchange_code in exchange_codes:
        print("Oh! It is in the cache!")
        calculate(currency_code, exchange_code, amount_of_money)
    else:
        print("Sorry, but it is not in the cache!")
        update_cache(currency_code, exchange_code)
        calculate(currency_code, exchange_code, amount_of_money)
