# Electoral Maps Module for bibo_21008

## Overview

The `electoral_maps` module provides enhanced Bokeh-based interactive visualization for election data, with a focus on Mauritania (TD) electoral results.

## Features

✨ **Key Features:**
- Interactive candidate selection via dropdown selector
- Automatic color mapping based on vote counts
- Hover tooltips showing region and vote details
- Support for custom titles, dimensions, and styling
- Proper error handling for missing data
- Type hints for IDE autocompletion
- Works seamlessly in Jupyter notebooks

## Installation

```bash
# Install the library with all dependencies
pip install -e ./bibo_21008_project/bibo_21008_project

# Or install dependencies separately
pip install bokeh geopandas shapely pandas matplotlib
```

## API Reference

### `create_td_election_map()`

Create an interactive election map for Mauritania with automatic data loading and processing.

**Parameters:**
- `shapefile_path` (str): Path to the shapefile (e.g., `'mrshape/mrt_admbnda_adm2_ansade_20240327.shp'`)
- `csv_url` (str): URL or path to the election CSV file
- `year` (int): Election year to visualize (default: 2024)
- `title_prefix` (str): Prefix for the map title (default: 'Résultats électoraux')
- `height` (int): Figure height in pixels (default: 600)
- `width` (int): Figure width in pixels (default: 800)
- `show_plot` (bool): Whether to display the plot (default: True)
- `output_type` (str): Output type - 'notebook' or 'file' (default: 'notebook')

**Returns:**
Tuple of `(layout, geosource, color_mapper, candidats, merged_gdf)`

**Example:**

```python
from bibo_21008 import create_td_election_map

layout, geosource, color_mapper, candidats, merged = create_td_election_map(
    shapefile_path="mrshape/mrt_admbnda_adm2_ansade_20240327.shp",
    csv_url="https://raw.githubusercontent.com/binorassocies/rimdata/refs/heads/main/data/results_elections_rim_2019-2024.csv",
    year=2024,
    title_prefix="Résultats électoraux TD 2024",
    height=650,
    width=900
)
```

### `create_simplified_election_map()`

Create an election map from pre-loaded GeoDataFrame and vote data.

**Parameters:**
- `gdf` (GeoDataFrame): GeoDataFrame with geometry and region names
- `candidate_votes` (dict): Dictionary mapping candidate names to vote Series
- `title` (str): Map title (default: 'Election Results')
- `height` (int): Figure height in pixels
- `width` (int): Figure width in pixels
- `show_plot` (bool): Whether to display the map

**Example:**

```python
from bibo_21008 import create_simplified_election_map
import geopandas as gpd
import pandas as pd

# Load your data
gdf = gpd.read_file("path/to/shapefile.shp")
candidate_votes = {
    "Candidate A": pd.Series([100, 200, 150], index=gdf.index),
    "Candidate B": pd.Series([150, 180, 200], index=gdf.index),
}

layout, geosource, color_mapper, candidats, merged = create_simplified_election_map(
    gdf=gdf,
    candidate_votes=candidate_votes,
    title="My Election Results"
)
```

## Interactive Features

### Candidate Selection

The map includes a dropdown selector (Select widget) that allows you to:
- Change the displayed candidate
- Automatically update the color mapping
- Update hover tooltips with new candidate data
- See the title update to reflect the selected candidate

### Hover Information

Hover over any region to see:
- **Moughataa**: Name of the region
- **Candidat**: Name of the selected candidate
- **Voix**: Number of votes received

## Data Format Requirements

### Shapefile

Required columns:
- `ADM2_EN`: Name of the administrative region (Moughataa)
- `geometry`: Geographic geometry data

### CSV Data

Required columns:
- `year`: Election year
- `moughataa`: Region name (must match shapefile names)
- `candidate`: Candidate name
- `nb_votes`: Number of votes

Example CSV structure:
```
year,moughataa,candidate,nb_votes
2024,Nouakchott,Candidate A,1500
2024,Nouakchott,Candidate B,1200
2024,Akjoujt,Candidate A,800
...
```

## Customization

### Color Palettes

The module uses `Viridis256` palette by default, but you can modify the returned `color_mapper`:

```python
from bokeh.palettes import Plasma256, Cividis256

layout, geosource, color_mapper, candidats, merged = create_td_election_map(...)

# Modify color mapper palette
color_mapper.palette = Plasma256[::-1]
```

### Title and Styling

Customize the figure after creation:

```python
# Access the figure from the layout
from bokeh.layouts import column
select, p = layout.children

p.title.text = "Custom Title"
p.title.text_font_size = "16pt"
```

## Troubleshooting

### "Bokeh is required"
```bash
pip install bokeh
```

### "GeoPandas is required"
```bash
pip install geopandas shapely
```

### Data not matching
- Ensure moughataa names in CSV exactly match those in the shapefile
- Use `.upper()` or `.strip()` to normalize names if needed
- Check for accent differences (é vs e)

### Missing regions appear gray
This is expected behavior - regions with no data for a candidate will appear in light gray.

## Examples

See the main notebook for complete working examples:
- [GeoPandas.ipynb](../GeoPandas.ipynb) - Full tutorial with multiple visualization approaches

## Integration with bibo_21008

The electoral_maps module integrates with the bibo_21008 library ecosystem:

```python
from bibo_21008 import (
    set_bibo_style,
    create_td_election_map,
    styled_bar,  # Other bibo_21008 functions
)

# Apply consistent styling
set_bibo_style()

# Create election map
layout, ... = create_td_election_map(...)
```

## Performance Notes

- Large shapefiles (>100MB) may take time to load
- GeoJSON conversion is automatic but can be memory-intensive for complex geometries
- Hover tooltips update in real-time as you change candidates

## License

Part of the bibo_21008 personal library project.
