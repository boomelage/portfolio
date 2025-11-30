import requests
import pandas as pd

class series:
    def __init__(self, av_key: str, frequency: str = 'Daily', outputsize: str = 'compact'):
        self.av_key = av_key
        self.frequency = frequency
        self.outputsize = outputsize
        pass

    def fx(self, from_currency: str, to_currency: str, verbose = False) -> pd.Series:
        """
        fetches a time series for a given forex pair
        
        """
        url = f'https://www.alphavantage.co/query?function=FX_{self.frequency.upper()}&from_symbol={from_currency}&to_symbol={to_currency}&apikey={self.av_key}&outputsize={self.outputsize}'
        r = requests.get(url).json()
        if verbose:
            print(r)
        return pd.Series(pd.DataFrame(r[f'Time Series FX ({self.frequency})'], dtype = float).T['4. close']).rename(str(from_currency+to_currency))
    
    def equity(self, symbol: str, verbose = False) -> pd.Series:
        """
        fetches a time series for a given equity symbol
        
        """
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{self.frequency.upper()}_ADJUSTED&symbol={symbol}&apikey={self.av_key}&outputsize={self.outputsize}'
        r = requests.get(url).json()
        if verbose:
            print(r)
        if self.frequency in ["Weekly", "Monthly"]:
            return pd.Series(pd.DataFrame(r[f'{self.frequency} Adjusted Time Series'], dtype = float).T['5. adjusted close']).rename(symbol)
        elif self.frequency == 'Daily':
            return pd.Series(pd.DataFrame(r[f'Time Series ({self.frequency})'], dtype = float).T['5. adjusted close']).rename(symbol)
        else:
            raise NotImplementedError("Frequency might not exist. Check https://www.alphavantage.co/documentation/")

    def crypto(self, symbol: str, market: str = 'EUR', verbose = False) -> pd.Series:
        """
        fetches a time series for a given cryptocurrency symbol
        
        """
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_{self.frequency.upper()}&symbol={symbol}&market={market}&apikey={self.av_key}'
        r = requests.get(url).json()
        if verbose:
            print(r)
        return pd.Series(pd.DataFrame(r[f'Time Series (Digital Currency {self.frequency})'], dtype = float).T['4. close']).rename(str(symbol+market))