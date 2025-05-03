# get custom classes
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..', '..', 'src', 'macroecon_tools'))
from fetch_data import get_fred
from timeseries import TimeseriesTable

# get data
data_sources = {
    "GDPC1": "GDP",
    "CPIAUCSL": "CPI"
}
data = get_fred(data_sources)
print(data)

# Get data from FRED
srcs = {
    "GDPC1": "GDP",
    "PCEPI": "CPI"
}
other_data = get_fred(srcs)
# Output
print(other_data)