import requests

class spot:
    def __init__(self, av_key: str):
        self.av_key = av_key
        pass

    def fx(self, from_currency: str, to_currency: str, verbose: bool = False) -> tuple[str, float]:
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&entitlement=delayed&apikey={self.av_key}'
        r = requests.get(url).json()
        if verbose:
            print(r)
        date = str(r['Realtime Currency Exchange Rate']['6. Last Refreshed'])
        rate = float(r['Realtime Currency Exchange Rate']['5. Exchange Rate'])
        return date, rate


    def equity(self, symbol: str, verbose: bool = False) -> tuple[str, float]:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&entitlement=delayed&apikey={self.av_key}'
        r = requests.get(url).json()
        if verbose:
            print(r)
        date = str(r['Global Quote - DATA DELAYED BY 15 MINUTES']['07. latest trading day'])
        price = float(r['Global Quote - DATA DELAYED BY 15 MINUTES']['05. price'])
        return date, price

    