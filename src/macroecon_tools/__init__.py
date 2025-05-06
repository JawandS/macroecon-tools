r"""
### Overview of Modules:

- **Data Structures**
  - `Timeseries`: extension of `pd.Series` for time series data
  - `TimeseriesTable`: extension of `pd.DataFrame` for time series data

- **Data Retrieval** (with automatic caching)
  - `get_fred()`: fetch data from FRED
  - `get_barnichon()`
  - `get_ludvigson()`

- **`TimeseriesVisualizer`**: plotting options
"""

# Import submodules
from .timeseries import Timeseries, TimeseriesTable
from .fetch_data import get_fred, get_barnichon, get_ludvigson
from .visualizer import TimeseriesVisualizer

# Use pandas to default for missing attributes
import pandas as pd
__all__ = ['Timeseries', 'TimeseriesTable', 'TimeseriesVisualizer', 'get_fred', 'get_barnichon', 'get_ludvigson', 'pd']

def __getattr__(name):
    """
    Default to pandas if attribute not found.
    """
    if hasattr(pd, name):
        return getattr(pd, name)
    raise AttributeError(f"module 'macroecon_tools' has no attribute '{name}'")
