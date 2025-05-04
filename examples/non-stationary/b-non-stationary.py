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

# ─── HELPERS ───────────────────────────────────────────────────────────────────
def simulate_ar1(rho: float, length: int, seed: int = None) -> pd.Series:
    """
    Simulate an AR(1) process y[t] = rho*y[t-1] + eps[t].
    Returns a pandas Series of length `length` with index 0..length-1.
    """
    rng = np.random.default_rng(seed)
    eps = rng.standard_normal(length)
    y = np.empty(length)
    y[0] = 0.0
    for t in range(1, length):
        y[t] = rho * y[t - 1] + eps[t]
    return pd.Series(y, name=f"AR1(ρ={rho})")


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


# ─── PART 1: STATIONARY VS NON‑STATIONARY AR(1) ─────────────────────────────────
for rho, tag in [(0.8, "stationary"), (1.0, "nonstationary")]:
    sr = simulate_ar1(rho, T, seed=SEED)
    plot_series_and_acf(
        sr,
        filename=f"ar1_{tag}.png",
        title=f"AR(1) Process (ρ={rho}) — {tag.capitalize()}"
    )

# ─── PART 2: FRED RETAIL SALES EXAMPLE ──────────────────────────────────────────
# 1) Fetch series from FRED
data = mt.get_fred({"MRTSSM44000USN": "retail"})

# 2) Visualize raw level
viz = mt.TimeseriesVisualizer(data)
viz.plot_individual(OUTPUT_DIR, ["retail"])

# 3) Compute and plot year‑over‑year growth (in %)
data["retail_growth"] = data["retail"].log().diff(12) * 100
data["retail_growth"].set_label("YoY % Growth: U.S. Retail Sales")
viz.plot_individual(OUTPUT_DIR, ["retail_growth"])

# 4) Plot ACF of growth
plot_series_and_acf(
    data["retail_growth"].dropna(),
    filename="acf_retail_growth.png",
    title="ACF: Retail Sales YoY Growth"
)

# 5) Difference again to induce stationarity and plot
data["retail_diff"] = data["retail_growth"].diff(1)
viz.plot_individual(OUTPUT_DIR, ["retail_diff"])
plot_series_and_acf(
    data["retail_diff"].dropna(),
    filename="acf_retail_diff.png",
    title="ACF: Retail Sales Growth Difference"
)
