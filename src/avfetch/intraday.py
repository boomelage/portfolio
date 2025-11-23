import requests
import pandas as pd

class intraday:
    def __init__(self, av_key: str, interval: str = "5min", outputsize: str = "compact"):
        self.interval = interval
        self.av_key = av_key
        self.outputsize = outputsize
        pass

    def equity(self, symbol: str, verbose: bool = False) -> pd.Series:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY" \
              f"&symbol={symbol}&interval={self.interval}&entitlement=delayed&" \
              f"outputsize={self.outputsize}&apikey={self.av_key}"
        r = requests.get(url).json()
        if verbose:
            print(r)
        return pd.DataFrame(r['Time Series (5min)'], dtype = float).T['4. close'].rename(symbol)
