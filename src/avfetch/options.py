import requests
import pandas as pd

class options:
    def __init__(self, av_key: str):
        self.av_key = av_key
        self.floats = ['strike', 'last', 'mark', 'bid', 'ask', 'implied_volatility', 'delta', 'gamma', 'theta', 'vega', 'rho']
        self.ints = ['bid_size', 'ask_size', 'volume', 'open_interest']
        self.strings = ['contractID', 'symbol', 'type']
        self.dates = ['expiration', 'date']
        pass

    def cast_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Casts the proper data types and computes additional columns for in the options DataFrame

        Input:
            <- df: Pandas DataFrame

        Output:
            -> Pandas DataFrame

        """
        df[self.floats] = df[self.floats].apply(pd.to_numeric, errors='coerce').astype(float)
        df[self.strings] = df[self.strings].astype(str)
        df[self.ints] = df[self.ints].apply(pd.to_numeric, errors='coerce').astype("int64")
        df[self.dates] = df[self.dates].apply(pd.to_datetime, errors='coerce') 
        df['dtm'] = (df['expiration'] - df['date']).dt.days.astype("int64")
        return df

    def link(self, date: str, symbol: str, verbose: bool = False) -> pd.DataFrame:
        """

        Inputs:
            <- date: string (formatted as yyyy-mm-dd)
            <- symbol: string

        Output:
            -> Pandas DataFrame

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
        return self.cast_format(pd.DataFrame(r['data']))

    def from_csv(self, path: str):
        return self.cast_format(pd.read_csv(path))
