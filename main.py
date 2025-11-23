import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent / "src"))
import avfetch

av_key = str(Path(__file__).with_name("av_key").read_text().strip())

series = avfetch.series(av_key=av_key,outputsize='full',frequency='Daily')

tickers = [
    "ASML", "NVDA", "INTC", "AMD", "ARM",
    "AMZN", "AAPL", "NET", "MSFT",
    "JPM", "SPY", "GS", "MS", "UBS",
    "LMT", "RTX", "GE", "BA", "GD",

    "BATS.LON", "SHEL.LON",
    
]

df = pd.DataFrame({t: series.equity(t) for t in tickers})

df = df.sort_index(ascending=False).dropna()
print(df)
processed_currencies = []

for c in df.columns:
    data = avfetch.search(av_key,c)
    data.index = data['1. symbol']
    currency = data['8. currency'][c]
    pairname = f'{currency}EUR'
    
    print(f"{c} is denominated in {currency}")
    if currency != "EUR":
        print(f"Converting from {currency} to EUR")
        if currency not in processed_currencies:
            if currency == "GBX":
                currency = "GBP"
                df[c] = df[c]/100
                pairname = f'{currency}EUR'
            df[pairname] = series.fx(from_currency=currency,to_currency="EUR")
            df[f"{c}_EUR"] = df[c].values * df[pairname].values
            processed_currencies.append(currency)
        else:
            df[f"{c}_EUR"] = df[c].values * df[pairname]
    else:
        print(f"Already denominated in euro, adding column '{c}_EUR' for consistency")
        df[f"{c}_EUR"] = df[c]
    print()

df["BTC_EUR"] = series.crypto("BTC")
df["ETH_EUR"] = series.crypto("ETH")

prices = df.sort_index(ascending=False).dropna().filter(like='_EUR')

from pypfopt import expected_returns, EfficientSemivariance

mu = expected_returns.mean_historical_return(prices, frequency=252)
print(mu,'\n')
historical_returns = expected_returns.returns_from_prices(prices)

es = EfficientSemivariance(mu, historical_returns, frequency=252, weight_bounds=(0,0.5))
# asml_idx = prices.columns.get_loc("ASML_EUR")
# es.add_constraint(lambda w, idx=asml_idx: w[idx] >= 0.1)
es.efficient_return(0.075)

# We can use the same helper methods as before
weights = es.clean_weights()
print("Weights:")
for i,j in weights.items():
    print("  ",i,j)
print()
performance = es.portfolio_performance(verbose=True)
