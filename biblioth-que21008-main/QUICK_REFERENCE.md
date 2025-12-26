# bibo_21008 Electoral Maps - Quick Reference

## One-Liner Installation

```bash
pip install -e ./bibo_21008_project/bibo_21008_project
```

## One-Liner Usage

```python
from bibo_21008 import create_td_election_map
layout, _, _, _, _ = create_td_election_map(
    "mrshape/mrt_admbnda_adm2_ansade_20240327.shp",
    "https://raw.githubusercontent.com/binorassocies/rimdata/refs/heads/main/data/results_elections_rim_2019-2024.csv"
)
```

## Full Example

```python
from bibo_21008 import create_td_election_map

# Create map
layout, geosource, color_mapper, candidats, merged_gdf = create_td_election_map(
    shapefile_path="mrshape/mrt_admbnda_adm2_ansade_20240327.shp",
    csv_url="https://raw.githubusercontent.com/binorassocies/rimdata/refs/heads/main/data/results_elections_rim_2019-2024.csv",
    year=2024,
    title_prefix="TD 2024 - Résultats",
    height=650,
    width=900,
    show_plot=True
)

print(f"Map created with candidates: {candidats}")
print(f"Regions in map: {len(merged_gdf)}")
```

## What You Get

| Return Value | Type | Usage |
|---|---|---|
| `layout` | Bokeh layout | The complete interactive map |
| `geosource` | GeoJSONDataSource | GeoJSON data source (for customization) |
| `color_mapper` | LinearColorMapper | Color mapping (for customization) |
| `candidats` | list | List of candidate names |
| `merged_gdf` | GeoDataFrame | Merged spatial data |

## Interactive Features

1. **Dropdown Selector** - Switch between candidates
2. **Hover Tooltips** - See region name, candidate, and vote count
3. **Zoom/Pan** - Explore the map
4. **Reset** - Return to default view

## Customization Examples

### Change Colors
```python
from bokeh.palettes import Plasma256
color_mapper.palette = Plasma256[::-1]
```

### Access the Figure
```python
select_widget, figure = layout.children
figure.title.text = "My Custom Title"
```

### Export Data
```python
# Save the merged geodata
merged_gdf.to_file("output_election_data.shp")

# Save GeoJSON
import json
with open("election_data.geojson", "w") as f:
    json.dump(json.loads(merged_gdf.to_json()), f)
```

## Troubleshooting

| Error | Solution |
|---|---|
| `ImportError: No module named 'bokeh'` | `pip install bokeh` |
| `ImportError: No module named 'geopandas'` | `pip install geopandas shapely` |
| `FileNotFoundError: shapefile not found` | Check shapefile path is correct |
| `ValueError: No election data found for year X` | Check year parameter and CSV content |
| `KeyError: 'moughataa'` | Verify shapefile has `ADM2_EN` column |

## Data Requirements

**Shapefile:**
- Must have `ADM2_EN` column for region names
- Must have valid geometry

**CSV:**
```
year,moughataa,candidate,nb_votes
2024,Nouakchott,Candidate A,1500
```

## Performance Tips

- For first run: ~2-5 seconds to load and process
- Hover updates are instant
- Candidate switching is immediate
- Zoom/pan is smooth

## Advanced: Create Custom Map

```python
from bibo_21008 import create_simplified_election_map
import geopandas as gpd
import pandas as pd

# Load your own data
my_gdf = gpd.read_file("my_regions.shp")
votes = {
    "Candidate A": pd.Series([100, 200], index=[0, 1]),
    "Candidate B": pd.Series([150, 180], index=[0, 1]),
}

layout, _, _, _, _ = create_simplified_election_map(
    gdf=my_gdf,
    candidate_votes=votes,
    title="My Custom Election"
)
```

## Files Modified/Created

✅ Created:
- `bibo_21008/electoral_maps.py` - Main module (200+ lines)
- `bibo_21008/ELECTORAL_MAPS.md` - Full documentation
- `INSTALLATION_SUMMARY.md` - Setup guide
- This quick reference

✅ Updated:
- `pyproject.toml` - Added dependencies
- `__init__.py` - Exported new functions
- `GeoPandas.ipynb` - Added example cells

## Next Steps

1. Install: `pip install -e ./bibo_21008_project/bibo_21008_project`
2. Import: `from bibo_21008 import create_td_election_map`
3. Create: `layout = create_td_election_map(...)`
4. Explore: Use dropdown and hover to interact!

---

**Version:** 1.0.0  
**Library:** bibo_21008  
**Module:** electoral_maps  
**Status:** Ready to use ✓
