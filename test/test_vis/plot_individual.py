# Test the plot_individual method from the visualizer module

## IMPORT LIBRARIES ##
# Utils
import os, sys
CWD = os.path.dirname(__file__)
#   Data analysis
import pandas as pd
#  Time series analysis
USE_LOCAL_PKG = True
if not USE_LOCAL_PKG:
    from macroecon_tools import TimeseriesTable, Timeseries, get_fred, vis_multi_series
else: # Import local version
    sys.path.append(os.path.join(CWD, '..', '..', 'src', 'macroecon_tools'))
    from timeseries import TimeseriesTable, Timeseries
    from fetch_data import get_fred
    from visualizer import TimeseriesVisualizer

## GET DATA ##
# Get data from FRED
srcs = {
    'GDPC1': 'RGDP',
    'PCEPI': '',
    'UNRATE': '',
    'CPIAUCSL': 'CPI'
}
data: TimeseriesTable = get_fred(srcs, start_date='1940-1-1')
# Visualize
vis = TimeseriesVisualizer(data)
vis.plot_individual(f'{CWD}/individual')