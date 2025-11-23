import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent / "src"))
import avfetch

av_key = str(Path(__file__).with_name("av_key").read_text().strip())


series = avfetch.series(av_key)

spot = avfetch.spot(av_key)

intraday = avfetch.intraday(av_key)

print(intraday.equity("NET"))