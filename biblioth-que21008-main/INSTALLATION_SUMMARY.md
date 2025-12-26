# Installation & Usage Summary

## What Was Added to bibo_21008

### New Module: `electoral_maps.py`

A comprehensive electoral mapping module with improved Bokeh functionality for visualizing Mauritania election data.

**Location:** `bibo_21008_project/bibo_21008_project/bibo_21008/electoral_maps.py`

### Key Functions

1. **`create_td_election_map()`** - Main function for creating interactive election maps
   - Loads shapefile and CSV data automatically
   - Creates interactive dropdown selector for candidates
   - Handles data merging and validation
   - Returns fully configured Bokeh layout

2. **`create_simplified_election_map()`** - For pre-loaded data
   - Works with existing GeoDataFrame and pandas Series
   - Useful for custom data processing

### Updated Files

1. **pyproject.toml** - Added dependencies:
   - `geopandas>=0.12`
   - `bokeh>=3.0`
   - `shapely>=2.0`
   - `pandas>=1.5`

2. **__init__.py** - Exported new functions:
   - `create_td_election_map`
   - `create_simplified_election_map`

3. **GeoPandas.ipynb** - Added example usage cells

## Installation

```bash
# Navigate to project directory
cd bibo_21008_project/bibo_21008_project

# Install in development mode
pip install -e .
```

Or install dependencies individually:
```bash
pip install bokeh geopandas shapely pandas matplotlib
```

## Quick Start

```python
from bibo_21008 import create_td_election_map

# Create interactive map with one function call
layout, geosource, color_mapper, candidats, merged = create_td_election_map(
    shapefile_path="mrshape/mrt_admbnda_adm2_ansade_20240327.shp",
    csv_url="https://raw.githubusercontent.com/binorassocies/rimdata/refs/heads/main/data/results_elections_rim_2019-2024.csv",
    year=2024,
    title_prefix="Résultats électoraux TD 2024",
    height=650,
    width=900
)
```

## Features

✨ **Improvements over original code:**
- ✅ Modular, reusable function
- ✅ Proper error handling
- ✅ Type hints for IDE support
- ✅ Automatic data validation
- ✅ Comprehensive docstrings
- ✅ Works in Jupyter notebooks
- ✅ Interactive candidate dropdown
- ✅ Automatic color mapping
- ✅ Professional tooltip display

## Files Structure

```
bibo_21008_project/
├── bibo_21008/
│   ├── __init__.py           (updated - new exports)
│   ├── electoral_maps.py      (NEW - main module)
│   ├── ELECTORAL_MAPS.md      (NEW - detailed docs)
│   ├── plots.py              (existing)
│   └── styles.py             (existing)
├── pyproject.toml            (updated - new dependencies)
└── README.md
```

## Documentation

See `bibo_21008/ELECTORAL_MAPS.md` for:
- Full API reference
- Usage examples
- Customization options
- Troubleshooting guide
- Data format requirements

## Next Steps

1. Test the new functionality:
   ```bash
   jupyter notebook GeoPandas.ipynb
   ```

2. Review and run the new example cell

3. Integrate into your workflow:
   ```python
   from bibo_21008 import create_td_election_map
   # Use in your notebooks and scripts
   ```

## Support

For issues or questions:
- Check `ELECTORAL_MAPS.md` for documentation
- Review example usage in `GeoPandas.ipynb`
- Check error messages - they provide helpful guidance
