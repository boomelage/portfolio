import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent / "src"))
import avfetch
av_key = str(Path(__file__).with_name("av_key").read_text().strip())

series = avfetch.series(av_key, outputsize = 'compact')
spot = avfetch.spot(av_key)
intraday = avfetch.intraday(av_key, outputsize = 'compact')
options = avfetch.options(av_key)

spy_link = pd.DataFrame(options.link('2025-11-26','SPY'))
help(spy_link.to_csv)
spy_link.to_csv('options_data.csv',index=False)

print(spy_link)