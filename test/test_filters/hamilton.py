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

## REFERENCE ##
# with open(f'{CWD}/data_guide.pkl', 'rb') as f:
#     data = pickle.load(f)
# #   Select variables
# vars = ['GDP', 'GDPDef', 'STIR', 'UR', 'CBSpread']
#   Select statistics
moms = ['mean', 'SD', 'Skew', 'Kurt']
# data_moments(data["hamilton"], vars, moms)
# print()
''' data_test.py
            GDP GDP-logdiff GDP-hfilter
mean  12507.290       4.522      -0.000
SD     4700.273       2.511       2.624
Skew      0.217      -1.482      -1.200
Kurt     -1.111       5.274       1.869
'''

''' timeseries.py
            GDP GDP-logdiff GDP-hfilter
mean  12507.290       4.492      -0.000
SD     4700.273       2.499       2.624
Skew      0.217      -1.506      -1.200
Kurt     -1.111       5.391       1.869
'''

## TEST ##
# Get data
# srcs = {
#     'GDP': '',
#     'GDPDEF': 'GDPDef',
#     'DTB3': 'STIR',
#     'UNRATE': 'UR',
#     'BAA10Y': 'CBSpread'
# }
srcs = {
    'GDP': ''
}
data = get_fred(srcs, force_fetch=True)
# Aggregate
data = data.aggregate('QS-OCT', method='lastvalue')
# Get logdiff
date_one = '01-01-1989' # '01-Jan-1989'
data['GDP-logdiff'] = data['GDP'].truncate(date_one, '31-Dec-2019').logdiff(1)
print(data['GDP-logdiff'])
# Apply hamilton filter
data['GDP-hfilter'] = data['GDP'].log100().hamilton_filter('01-Jan-1989', '31-Dec-2019')
# Truncate GDP
data['GDP'] = data['GDP'].truncate('01-Jan-1989', '31-Dec-2019')
# Display
print(data.data_moments(moments=moms))
print(data['GDP-hfilter'])