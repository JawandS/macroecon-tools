### IMPORT MODULES ###
#   Plotting
import matplotlib.pyplot as plt
#   Scientific computing
import numpy as np
#   Data analysis
import pandas as pd
#   Auto-correlation function
from statsmodels.graphics.tsaplots import plot_acf as acf
#  Time series analysis
USE_LOCAL_PKG = True
if not USE_LOCAL_PKG:
    from macroecon_tools import TimeseriesTable, Timeseries, get_fred, vis_multi_series
else: # Import local version
    import os, sys
    script_dir = os.path.dirname(__file__)
    sys.path.append(os.path.join(script_dir, '..', 'src', 'macroecon_tools'))
    from timeseries import TimeseriesTable, Timeseries
    from fetch_data import get_fred
    from visualizer import vis_multi_subplots, vis_two_vars, vis_multi_lines

### GENERATE STATIONARY DATA ###
# Assign parameters
T = 501
rho = 0.8
# Draw random numbers
rng = np.random.default_rng(seed=0)
eps = rng.standard_normal(T)
# Simulate time series
y = np.zeros(T)
for t in range(1,T):
    y[t] = rho * y[t-1] + eps[t]
# Plot time series
fig, ax = plt.subplots(figsize=(6.5,2.5))
ax.plot(y)
ax.set_title('AR(1)')
ax.grid()
ax.autoscale(tight=True)
# plt.savefig('ar1_stationary.png')
plt.close()
# Plot auto-correlation function
fig, ax = plt.subplots(figsize=(6.5,2.5))
acf(y,ax)
ax.grid()
ax.autoscale(tight=True)
# plt.savefig('acf_ar1_stationary.png')
plt.close()

### NON-STATIONARY DATA ###
# Reassign rho
rho = 1.0
# Simulate time series
y = np.zeros(T)
for t in range(1,T):
    y[t] = rho*y[t-1] + eps[t]
# Plot time series
fig, ax = plt.subplots(figsize=(6.5,2.5))
ax.plot(y)
ax.set_title('AR(1)')
ax.grid()
ax.autoscale(tight=True)
# plt.savefig('ar1_nonstationary.png')
plt.close()
# Plot auto-correlation function
fig, ax = plt.subplots(figsize=(6.5,2.5))
acf(y,ax)
ax.grid()
ax.autoscale(tight=True)
# plt.savefig('acf_ar1_nonstationary.png')
plt.close()

### RETAIL SALES DATA ###
# Get data
data = get_fred(['MRTSSM44000USN'], ['retail'])
print(data['retail'])

# Plot non-stationary data
fig, ax = plt.subplots(figsize=(6.5,2.5))
ax.plot(data['retail'])
ax.set_title('Retail Sales')
ax.yaxis.set_major_formatter('${x:,.0f}M')
ax.grid()
# plt.savefig('retail_nonstationary.png')
plt.close()

# Plot auto-correlation function
fig, ax = plt.subplots(figsize=(6.5,2.5))
acf(data['retail'], ax)
ax.grid()
# plt.savefig('acf_retail_nonstationary.png')
plt.close()

# Retails sales annual growth rate (percent change)
data['retail_growth'] = data['retail'].log().diff(12) * 100

# Plot non-stationary data
fig, ax = plt.subplots(figsize=(6.5, 2.5))
ax.plot(data['retail_growth']) 
ax.set_title('U.S. retail sales year-over-year growth rate')
ax.grid()
ax.autoscale(tight=True)
# plt.savefig('retail_growth_nonstationary.png')
plt.close()

# Plot Autocorrelation Function
fig, ax = plt.subplots(figsize=(6.5,2.5))
acf(data['retail_growth'].dropna(),ax);
ax.grid()
ax.autoscale(tight=True)
# plt.savefig('acf_retail_growth_nonstationary.png')
plt.close()