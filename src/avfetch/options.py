import requests
import pandas as pd

class options:
    def __init__(self, av_key: str):
        self.av_key = av_key
        self.floats = ['strike', 'last', 'mark', 'bid', 'ask', 'implied_volatility', 'delta', 'gamma', 'theta', 'vega', 'rho']
        self.ints = ['bid_size', 'ask_size', 'volume', 'open_interest']
        self.strings = ['contractID', 'symbol', 'expiration', 'date', 'type'] 
        pass

    def link(self, date: str, symbol: str, verbose: bool = False) -> pd.DataFrame:
        """
        ______
        Inputs:
            -> date: string (formatted as yyyy-mm-dd)
            -> symbol: string
        _______
        Outputs:
            One link in an option price chain

        """
        url = str(
            "https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&"
            f"symbol={symbol}"
            f"&date={date}"
            f"&apikey={self.av_key}"
        )
        r = requests.get(url).json()
        if verbose:
            print(r)
        data = pd.DataFrame(r['data'])
        data[self.floats] = data[self.floats].apply(pd.to_numeric, errors='coerce').astype(float)
        data[self.strings] = data[self.strings].astype(str)
        data[self.ints] = data[self.ints].apply(pd.to_numeric, errors='coerce').astype("Int64")
        return data

    def from_csv(self, path: str):
        data = pd.read_csv(path)
        data[self.floats] = data[self.floats].apply(pd.to_numeric, errors='coerce').astype(float)
        data[self.strings] = data[self.strings].astype(str)
        data[self.ints] = data[self.ints].apply(pd.to_numeric, errors='coerce').astype("Int64")
        return data
