import requests

class options:
    def __init__(self, av_key: str):
        self.av_key = av_key
        pass

    def link(self, date: str, symbol: str, verbose: bool = False):
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
        return r['data']

