# Test the hamilton method from the timeseries class

## IMPORT LIBRARIES ##
# Utils
import os, sys
CWD = os.path.dirname(__file__)
#   Loading data
import pickle
#  Time series analysis
USE_LOCAL_PKG = True
if not USE_LOCAL_PKG:
    from macroecon_tools import TimeseriesTable, Timeseries, get_fred, vis_multi_series
else: # Import local version
    sys.path.append(os.path.join(CWD, '..', '..', 'src', 'macroecon_tools'))
    from timeseries import Timeseries, TimeseriesTable
    from fetch_data import get_fred
    from visualizer import TimeseriesVisualizer
sys.path.append('/home/js/nonlinear-macro/Python/toolbox')
from data_moments import data_moments

## GET DATA ###
data = get_fred({'GDP': ''})

## TEST ##
data['GDP'] = data['GDP'].aggregate('quarterly', 'mean').log100()
data['GDP-hp-filter'] = data['GDP'].hp_filter()
print(data.tail(20))