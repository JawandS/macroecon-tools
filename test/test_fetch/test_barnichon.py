# Test get_barnichon function

# get custom classes
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..', '..', 'src', 'macroecon_tools'))
from fetch_data import get_barnichon
from timeseries import TimeseriesTable

# get data
filepath = os.path.join(script_dir, 'CompositeHWI.csv')
table = TimeseriesTable()
table = get_barnichon(filepath, table, 'V_LF', 'VR')
table = get_barnichon(filepath, table, 'V_hwi', 'hwi')
print(table.df.loc[:'2023-12-01'].dropna())
