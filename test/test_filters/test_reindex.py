# test how pandas handles reindexing

# imports
import pandas as pd

# Generate dummy data
og_data = pd.Series([i for i in range(10)], index=pd.date_range('2000-01-01', periods=10, freq='QS'))
print(og_data)

# Reindex quarter end
qe_data = og_data.resample('QE').last()
print(qe_data)

# Reindex to daily
# daily_data = og_data.resample('D')
# print(daily_data)
