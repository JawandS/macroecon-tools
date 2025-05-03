# Test the subplots method from the subplots module

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
data: TimeseriesTable = get_fred(srcs)
data['RGDP'] = data['RGDP'].set_label('Real GDP')
# Set percent
data['UNRATE'] = data['UNRATE'].set_percent().set_label('Unemployment Rate')
# Visualize
vis = TimeseriesVisualizer(data)
vis.subplots(f'{CWD}/subplots.png', start_date='01-01-1960', end_date='12-31-2023')
vis.subplots(f'{CWD}/subplots2.png', variables=['RGDP'])
