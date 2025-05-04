"""
This example demonstrates how to visualize mixed-frequency time series data using the
macroecon_tools library. It fetches quarterly and monthly data from FRED, aggregates
the monthly data to quarterly frequency, and then computes year-over-year growth and
inflation rates. The results are visualized using subplots, two-variable plots, and
multi-line plots.
"""

# ─── DEPENDENCIES ─────────────────────────────────────────────────────────────
import pandas as pd
from pathlib import Path

import macroecon_tools as mt

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────
FRED_SOURCES = {"GDPC1": "RGDP", "PCEPI": "PCEPI"}
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR.mkdir(exist_ok=True)
DATE_START, DATE_END = "1960-01-01", "2023-12-31"
LATEST_DATE = "2024-09-30"

# ─── FETCH & AGGREGATE ─────────────────────────────────────────────────────────
data = mt.get_fred(FRED_SOURCES)

# print each series
for name, series in data.items():
    print(f"{name}:\n{series.to_string()}\n")

# print TimeseriesTable
print(data, "\n")

# quarterly aggregate (last observation)
data = data.aggregate("QE", method="lastvalue")

# show table and snapshot
print(data, "\n")
print("HEAD:\n", data.df.head(4).to_string(), "\n")
print("TAIL:\n", data.df.tail(4).to_string(), "\n")

# ─── TRANSFORMATIONS ────────────────────────────────────────────────────────────
# Real GDP YoY growth (%)
data["growth_rate"] = data["RGDP"].log().diff(4) * 100
data["growth_rate"] = data["growth_rate"].set_label("Real GDP YoY Growth Rate")

# PCE YoY inflation (%)
data["inf_rate"] = data["PCEPI"].log().diff(4) * 100
data["inf_rate"] = data["inf_rate"].set_label("PCE YoY Inflation Rate")

pd.options.display.float_format = "{:,.2f}".format
print(data.df.tail(4).to_string(), "\n")

# latest quarterly growth rate
print(f"{LATEST_DATE} Real GDP YoY Growth Rate: "
      f"{data['growth_rate'].loc[LATEST_DATE]:.2f}%\n")

# ─── PLOTTING ──────────────────────────────────────────────────────────────────
viz = mt.TimeseriesVisualizer(data)

# Plot each series in its own subplot
viz.subplots(
    OUTPUT_DIR / "subplots.png",
    ["growth_rate", "inf_rate"],
    DATE_START,
    DATE_END,
    is_percent=True,
)

# Plot each variables as a different axis
viz.two_vars(
    OUTPUT_DIR / "two_vars.png",
    "growth_rate",
    "inf_rate",
    "Real GDP vs PCE Inflation Rate",
    DATE_START,
    DATE_END,
    x_is_percent=True,
    y_is_percent=True,
)

# Plot multiple series in the same figure
viz.multi_lines(
    OUTPUT_DIR / "multi_lines.png",
    ["growth_rate", "inf_rate"],
    "Real GDP vs PCE Inflation Rate",
    DATE_START,
    DATE_END,
    is_percent=True,
)
