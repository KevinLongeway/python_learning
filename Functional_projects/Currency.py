import requests

API_KEY = "fca_live_bCzqBjrovaSPaG4vRgE4cq1hC3NZAoU9mRZRUqqM"
BASE_URL = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}"

CURRENCIES = ["USD", "EUR", "GBP", "JPY",
              "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"]


def convert_currency(base):
    currencies = ",".join(CURRENCIES)
    url = f'{BASE_URL}&base_currency={base}&currencies={currencies}'
    try:
        response = requests.get(url)
        data = response.json()
        return data["data"]
    except:
        print("Invalid Currency")
        return None


while True:
    base = input("Enter base currency (q for quit): ").upper()

    if base == 'Q':
        exit()

    data = convert_currency(base)
    if not data:
        continue

    del data[base]
    for ticker, value in data.items():
        print(f'{ticker}: {value}')
