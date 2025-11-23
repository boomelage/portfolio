import requests
import pandas as pd

def search(av_key: str, keywords: str, verbose: bool = False) -> pd.DataFrame:
	url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={av_key}'
	r = requests.get(url)
	return pd.DataFrame(r.json()['bestMatches'])