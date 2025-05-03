## IMPORT LIBRARIES ##
#   Data analysis
import pandas as pd
#  Time series analysis
import macroecon_tools as mt

## GET DATA ##
# Get data from FRED
srcs = {
    "GDPC1": "RGDP",
    "PCEPI": ""
}
data = mt.get_fred(srcs)

# Output
for source in data:
    print(f'{source}:\n{data[source]}')

# print TimeseriesTable
print(f"{data}\n")

# Aggregate to quarterly frequency
data = data.aggregate('QE', method='lastvalue')

# Display data (first 4 rows and last 4 rows)
print(f"{data}\n")

## TRANSFORMATIONS ##
# Real GDP Growth Rate (percent change)
data['logRGDP'] = data['RGDP'].log()
data['growth_rate'] = data['logRGDP'].diff(nlag=4) * 100
print(data['growth_rate'])

# PCE Inflation Rate (percent change)
data['logPCEPI'] = data['PCEPI'].log()
data['inf_rate'] = data['logPCEPI'].diff(nlag=4) * 100

# Display data
pd.options.display.float_format = '{:,.2f}'.format
print(data.df.tail(4))

# Latest Real GDP value
q3_2024_data = data["growth_rate"].loc['2024-09-30']
print(f'2024Q3 real GDP Year over Year Growth Rate: {q3_2024_data:.2f}%\n')

# Plot options
#  Sub sample
date_start = '01-01-1960'
date_end = '12-31-2023'
#  Update variable labels
data['growth_rate'].label = 'Real GDP Year over Year Growth Rate'
data['inf_rate'].label = 'PCE Year over Year Inflation Rate'
# Define variables
x_var = 'growth_rate'
y_var = 'inf_rate'
vars = ['growth_rate', 'inf_rate']
title = 'Real GDP vs PCE Inflation Rate'
# Plot
visualizer = mt.TimeseriesVisualizer(data)
visualizer.subplots('examples/subplots.png', vars, date_start, date_end, is_percent=True)
visualizer.two_vars('examples/two_vars.png', x_var, y_var, title, date_start, date_end, x_is_percent=True, y_is_percent=True)
visualizer.multi_lines('examples/multi_lines.png', vars, title, date_start, date_end, is_percent=True)