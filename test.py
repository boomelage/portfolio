import sys
from pathlib import Path
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)

sys.path.append(str(Path(__file__).parent / "src"))
import avfetch
av_key = str(Path(__file__).with_name("av_key").read_text().strip())

series = avfetch.series(av_key, outputsize = 'compact')
spot = avfetch.spot(av_key)
intraday = avfetch.intraday(av_key, outputsize = 'compact')
options = avfetch.options(av_key)

spy_link = options.from_csv(str(Path(__file__).parent / "example_data" / "options_data.csv"))

print(spy_link.dtypes)

spy_link = spy_link.sort_values(by=['strike','dtm'],ascending=True)

print(
	spy_link[
		(spy_link['strike'] == 500) & 
		(spy_link['type']=='call')
	]
)

print(intraday.equity("IBM"))