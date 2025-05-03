# Replication of
#   Schimitt-Grohe and Uribe, "HETEROGENEOUS DOWNWARD NOMINAL WAGE RIGIDITY:
#       FOUNDATIONS OF A NONLINEAR PHILLIPS CURVE", Figure 2
#
# Copyright (C) 2024  Nathaniel A. Throckmorton, Ph.D.
# Visit https://nathrock.github.io/ for contact information
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#     Add toolblox
import pandas as pd 
import matplotlib.pyplot as plt
import pickle
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../../../toolbox")
from trendline import trendline
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../../src/macroecon_tools")
import __init__ as mt

#    Saving flag
savefig = True
showfig = True
figname = 'figure_SchmittGroheUribe2023_Figure2'

## Load data
f = open(f'{script_dir}/data_test.pkl', 'rb')
dataraw = pickle.load(f)
f.close()


# Sample
date_one = '01-01-1984'
date_two = '01-01-2023'

# Transform data
unemployment_rate = mt.Timeseries(dataraw['tab']['UR'], name='U', source_freq='monthly').aggregate('yearly', 'mean').truncate(date_one, date_two)
wage_inflation = mt.Timeseries(dataraw['tab']['W'], name='W', source_freq='monthly').aggregate('monthly', 'lastvalue').logdiff(12, freq='monthly').aggregate('yearly', 'mean').truncate(date_one, date_two)

## Plot SchmittGroheUribe2023, Figure 2

# Options
fig_opt = {
    'figpos': [1, 1, 6.5, 6],  # Figure width, height (inches)
    'fontsize': 10,  # Font size
    'legadj': 0.03,  # Legend adjustment
    'legstr': ['Data', 'Linear Fit', 'Exp Fit', '2nd-order Poly Fit'],  # Legend strings
    'axispos': [0.08, 0.08, 0.87, 0.85]  # Subplot padding (proportion of outer box)
}

# Figure
subs = [pd.to_datetime('01-Jan-1984'),  pd.to_datetime('31-Dec-2023')]
fig = plt.figure(figsize=(fig_opt['figpos'][2], fig_opt['figpos'][3]))
fig.canvas.manager.set_window_title('SchmittGroheUribe2023, Figure 2')
datatemp = pd.DataFrame({'U': unemployment_rate, 'W': wage_inflation})
data_combined = datatemp[['U', 'W']].dropna()
x = data_combined['U']
y = pd.to_numeric(data_combined['W'])
h = []
h.append(plt.plot(x, y, 'k.', label='Data'))
for t in range(len(y)):
    plt.text(x.iloc[t] + 0.05, y.iloc[t] - 0.01, str(datatemp.index[t].year))
# Linear fit
xhat, yhat, _ = trendline(x, y)
h.append(plt.plot(xhat, yhat, 'k--', label='Linear Fit'))
# Exponential fit
xhat, yhat, _ = trendline(x, y, 'exp')
h.append(plt.plot(xhat, yhat, 'b--', label='Exp Fit'))
# 2nd-order polynomial fit
xhat, yhat, _ = trendline(x, y, 'poly', 2)
h.append(plt.plot(xhat, yhat, 'r--', label='2nd-order Poly Fit'))


# Label and format
plt.xlabel('Unemployment Rate, %')
plt.ylabel('Wage inflation, %/years')
plt.grid(True)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4)

plt.savefig(f'{script_dir}/{figname}.png', dpi=300)
