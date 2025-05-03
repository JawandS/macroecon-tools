import pickle 
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../../src/macroecon_tools")
import timeseries as mt
import tools

# Load data (pickle)
data_raw_in = os.path.join(script_dir, 'data_raw.test')
f = open(data_raw_in, 'rb')
dataraw = pickle.load(f)["tab"]
f.close()

# print(dataraw['GDP'].dropna())
# exit()

## Transform data
# Sample
D1 = '01-Jan-1989'
D2 = '31-Dec-2019'
# Quarterly GDP
GDP = mt.Timeseries(dataraw['GDP'].dropna(), name='GDP', source_freq='quarterly')
GDP_q = GDP.aggregate('quarterly', 'lastvalue')
# print(GDP_q)
# print(pd.DataFrame({
    # 'GDP': GDP_q
# }))
# print(mt.TimeseriesTable({
    # 'GDP': GDP_q
# }))
# exit()
# data 
data = mt.TimeseriesTable({
    # Quarterly GDP growth rate
    "GDP-logdiff": GDP_q.logdiff(1).truncate(D1, D2),
    # Quarterly cyclical GDP
    "GDP-hfilter": GDP_q.log100().hamilton_filter(D1, D2, lag_len=4, lead_len=8),
})

print('Summary Statistics')
vars = ['GDP-logdiff', 'GDP-hfilter']
# Select stats
moms = ['mean', 'SD', 'Skew', 'Kurt']
# Calculate statistics and display
tools.data_moments(data, vars, moms)

# Plot data
# Figure width, height (inches)
fig_opt = {
    'figpos': [1, 1, 6.5, 4],
    'fontsize': 10,
    # Subplot padding (proportion of axis box)
    'pad': {
        'topmarg': 0.03,
        'leftmarg': 0.08,
        'vspace': 0.05,
        'hspace': 0.08,
        'rightmarg': 0.02,
        'botmarg': 0.09
    }
}

# Plot
vars = data.columns()
nvars = len(vars)
fig, axes = plt.subplots(nvars, 1, figsize=(10, 8))
fig.subplots_adjust(
    top=1-fig_opt['pad']['topmarg'],
    bottom=fig_opt['pad']['botmarg'],
    left=fig_opt['pad']['leftmarg'],
    right=1-fig_opt['pad']['rightmarg'],
    hspace=fig_opt['pad']['hspace'],
    wspace=fig_opt['pad']['vspace']
)
ylims = []
recessions = [(datetime(1980, 1, 1), datetime(1991, 7, 1)), (datetime(1990, 7, 1), datetime(1991, 3, 1)), (datetime(2001, 3, 1), datetime(2001, 11, 1)), (datetime(2007, 12, 1), datetime(2009, 6, 1)), (datetime(2020, 2, 1), datetime(2020, 4, 1))]
data_index = data.index()
for ivar in range(nvars):
    plt.subplot(nvars, 1, ivar + 1)
    ax = axes[ivar]
    ax.plot(data_index, data[vars[ivar]])
    ax.set_ylabel(vars[ivar])
    ax.grid(True)
    
    if ivar == nvars - 1:
        ax.set_xlabel('Quarters')
    
    ylims.append(ax.get_ylim())
    axes[ivar].set_ylim(ylims[ivar])
    # shade the recession periods if within time period
    for i in range(len(recessions)):
        if recessions[i][0] >= data_index[0] and recessions[i][1] <= data_index[-1]:
            plt.axvspan(recessions[i][0], recessions[i][1], color='gray', alpha=0.5)

# save figure
# plt.savefig('data_class_test.png')
# show figure
plt.show()
# close figure
plt.close()