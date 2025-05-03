# Dependencies
import macroecon_tools as mt

# Test all operators on Timeseries
data = mt.Series([i for i in range(100)])
data.index = mt.date_range('2020-01-01', periods=100)
ts = mt.Timeseries(data, name="dummy data")

# Addition
print(ts)
ts = ts + 1
print(ts)
ts = 1 + ts
print(ts)

# Subtraction
ts = ts - 1
print(ts)
ts = 1 - ts
print(ts)

# Multiplication
ts = ts * 2
print(ts)
ts = 2 * ts
print(ts)

# Division
ts = ts / 2
print(ts)
ts = 2 / ts
print(ts)
