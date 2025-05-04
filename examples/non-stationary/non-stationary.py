"""
This example demonstrates how to visualize a non-stationary time series and its
autocorrelation function (ACF) using the macroecon_tools library.
"""

# ─── DEPENDENCIES ─────────────────────────────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.graphics.tsaplots import plot_acf

import macroecon_tools as mt

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────
T = 501
SEED = 0
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR.mkdir(exist_ok=True)

# ─── HELPER ───────────────────────────────────────────────────────────────────
def plot_series_and_acf(series: pd.Series, filename: str, title: str = None):
    """
    Plot a time series and its ACF below it, save to OUTPUT_DIR/filename.
    """
    fig, (ax_ts, ax_acf) = plt.subplots(2, 1, figsize=(6.5, 5), tight_layout=True)
    
    series.plot(ax=ax_ts, title=title or series.name)
    ax_ts.grid()
    
    plot_acf(series.dropna(), ax=ax_acf, title=f"ACF: {series.name}")
    ax_acf.grid()
    
    fig.savefig(OUTPUT_DIR / filename)
    plt.close(fig)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
# 1) Fetch series from FRED
data = mt.get_fred({"MRTSSM44000USN": "retail"})

# 2) Visualize raw level
viz = mt.TimeseriesVisualizer(data)
data["retail"] = data["retail"].set_label(r"U.S. Retail Sales (MRTSSM44000USN)")
viz.plot_individual(OUTPUT_DIR, ["retail"])

# 3) Compute and plot year‑over‑year growth (in %)
data["retail_growth"] = data["retail"].log().diff(12) * 100
data["retail_growth"] = data["retail_growth"].set_label(r"YoY % Growth: U.S. Retail Sales")
viz.plot_individual(OUTPUT_DIR, ["retail_growth"])

# 4) Plot ACF of growth
plot_series_and_acf(
    data["retail_growth"].dropna(),
    filename="acf_retail_growth.png",
    title="ACF: Retail Sales YoY Growth"
)

# 5) Difference again to induce stationarity and plot
data["retail_diff"] = data["retail_growth"].diff(1)
data["retail_diff"] = data["retail_diff"].set_label(r"1st Difference: U.S. Retail Sales Growth")
viz.plot_individual(OUTPUT_DIR, ["retail_diff"])
plot_series_and_acf(
    data["retail_diff"].dropna(),
    filename="acf_retail_diff.png",
    title="ACF: Retail Sales Growth Difference"
)
