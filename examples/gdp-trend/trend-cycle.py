"""
Trend-Cycle Decomposition Example
Using HP and Hamilton filters on quarterly real GDP.
"""

# ─── DEPENDENCIES ──────────────────────────────────────────────────────────────
from pathlib import Path                                   
import macroecon_tools as mt                             

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────
CWD = Path(__file__).resolve().parent                    

# ─── DATA FETCHING & FILTERING ─────────────────────────────────────────────────
data = mt.get_fred({"GDPC1": "RGDP"})               
data["RGDP"] = data["RGDP"].aggregate("QE", method="lastvalue")  

# apply filters
data["hp_cycle"], data["hp_trend"], lam = data["RGDP"].hp_filter()  
print(f"HP Filter λ = {lam:.0f}")                   

data["ham_cycle"], data["ham_trend"], lag, lead = data["RGDP"].hamilton_filter()
print(f"Hamilton filter (lag={lag}, lead={lead})")  

# ─── VISUALIZATION ─────────────────────────────────────────────────────────────
viz = mt.TimeseriesVisualizer(data)

# trends
viz.multi_lines(
    save_path=CWD / "gdp_trends.png",
    variables=["RGDP", "hp_trend", "ham_trend"],
    title="Real GDP Trends (HP vs. Hamilton)"
)

# cycles
viz.multi_lines(
    save_path=CWD / "gdp_cycles.png",
    variables=["hp_cycle", "ham_cycle"],
    title="Real GDP Cyclical Components"
)
