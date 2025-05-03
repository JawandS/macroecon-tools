# Test get_ludvigson function

# get custom classes
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..', '..', 'src', 'macroecon_tools'))
from fetch_data import get_ludvigson
from timeseries import TimeseriesTable

# get data
data = get_ludvigson()
for dataset in data:
    print(f"{dataset}:\n{data[dataset].dropna()}\n")