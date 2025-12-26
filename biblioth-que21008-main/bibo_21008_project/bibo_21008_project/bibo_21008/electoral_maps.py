"""Electoral map visualization for Mauritania (TD) election data using Bokeh."""

from __future__ import annotations
from typing import Optional, Sequence
import pandas as pd
import geopandas as gpd

try:
    from bokeh.io import show, output_notebook
    from bokeh.models import (
        GeoJSONDataSource,
        HoverTool,
        LinearColorMapper,
        ColorBar,
        CustomJS,
        Select,
        BasicTicker,
        PrintfTickFormatter,
    )
    from bokeh.layouts import column
    from bokeh.plotting import figure
    from bokeh.palettes import Viridis256
    BOKEH_AVAILABLE = True
except ImportError:
    BOKEH_AVAILABLE = False


def create_td_election_map(
    shapefile_path: str,
    csv_url: str,
    year: int = 2024,
    title_prefix: str = "Résultats électoraux",
    height: int = 600,
    width: int = 800,
    show_plot: bool = True,
    output_type: str = "notebook",
) -> Optional[tuple]:
    """
    Create an interactive Bokeh map visualizing Mauritania election results by region.
    
    Parameters
    ----------
    shapefile_path : str
        Path to the shapefile (e.g., 'mrshape/mrt_admbnda_adm2_ansade_20240327.shp')
    csv_url : str
        URL or path to the election CSV file
    year : int
        Election year to visualize (default: 2024)
    title_prefix : str
        Prefix for the map title (default: 'Résultats électoraux')
    height : int
        Height of the figure in pixels (default: 600)
    width : int
        Width of the figure in pixels (default: 800)
    show_plot : bool
        Whether to display the plot (default: True)
    output_type : str
        Output type: 'notebook' or 'file' (default: 'notebook')
    
    Returns
    -------
    tuple
        (layout, geosource, color_mapper, candidats, merged_gdf)
        The layout containing the interactive map and dropdown selector
    
    Raises
    ------
    ImportError
        If Bokeh or GeoPandas is not installed
    """
    if not BOKEH_AVAILABLE:
        raise ImportError("Bokeh is required for electoral_maps. Install with: pip install bokeh")
    
    try:
        import geopandas as gpd
    except ImportError:
        raise ImportError("GeoPandas is required for electoral_maps. Install with: pip install geopandas")
    
    # Setup output
    if output_type == "notebook":
        output_notebook()
    
    # 1. Load and prepare shapefile
    print("Loading shapefile...")
    gdf = gpd.read_file(shapefile_path).rename(columns={"ADM2_EN": "moughataa"})

    # Convert to Web Mercator for compatibility with tile providers
    try:
        if gdf.crs is None or gdf.crs.to_epsg() != 3857:
            gdf = gdf.to_crs(epsg=3857)
    except Exception:
        # try forcing conversion from EPSG:4326 if available
        try:
            gdf = gdf.to_crs(epsg=3857)
        except Exception:
            pass
    
    # 2. Load election data
    print(f"Loading election data for {year}...")
    df_elections = pd.read_csv(csv_url)
    df_year = df_elections.query(f"year == {year}").copy()
    
    if df_year.empty:
        raise ValueError(f"No election data found for year {year}")
    
    # 3. Pivot data: rows are moughataas, columns are candidates, values are votes
    print("Preparing data pivot...")
    df_pivot = df_year.pivot_table(
        index='moughataa',
        columns='candidate',
        values='nb_votes',
        fill_value=0
    ).reset_index()
    
    # 4. Merge with shapefile
    merged = gdf.merge(df_pivot, on="moughataa", how="left").fillna(0)
    
    # Get candidate names
    candidats = [col for col in df_pivot.columns if col != 'moughataa']
    
    # 5. Prepare columns for display
    merged['votes_display'] = merged[candidats[0]].astype(float)
    merged['current_candidat'] = candidats[0]
    
    # Keep only necessary columns for Bokeh
    cols_to_keep = ['geometry', 'moughataa', 'votes_display', 'current_candidat'] + candidats
    merged = merged[[c for c in cols_to_keep if c in merged.columns]].copy()
    
    # Ensure string columns are properly typed
    for col in merged.columns:
        if col != 'geometry' and not pd.api.types.is_numeric_dtype(merged[col]):
            merged[col] = merged[col].astype(str)
    
    # 6. Create GeoJSON source
    print("Creating Bokeh map...")
    geosource = GeoJSONDataSource(geojson=merged.to_json())
    
    # 7. Setup color mapping
    all_votes = merged[candidats].values.astype(float)
    vote_min = float(all_votes.min())
    vote_max = float(all_votes.max())
    
    color_mapper = LinearColorMapper(
        palette=Viridis256[::-1],
        low=vote_min,
        high=vote_max
    )
    
    color_bar = ColorBar(
        color_mapper=color_mapper,
        ticker=BasicTicker(desired_num_ticks=10),
        formatter=PrintfTickFormatter(format="%d"),
        label_standoff=12,
        location=(0, 0)
    )
    
    # 8. Create figure in Web Mercator projection and add base tiles
    # Compute reasonable x/y ranges from data bounds (with small padding)
    try:
        bounds = merged.total_bounds  # minx, miny, maxx, maxy (in meters)
        minx, miny, maxx, maxy = bounds.tolist()
        pad_x = (maxx - minx) * 0.08 if (maxx - minx) != 0 else 1_000_000
        pad_y = (maxy - miny) * 0.08 if (maxy - miny) != 0 else 800_000
        x_start, x_end = minx - pad_x, maxx + pad_x
        y_start, y_end = miny - pad_y, maxy + pad_y
    except Exception:
        # Fallback ranges roughly suitable for Mauritania
        x_start, x_end = -2000000, -500000
        y_start, y_end = 1600000, 3200000

    p = figure(
        title=f"{title_prefix} : {candidats[0]}",
        height=height,
        width=width,
        x_range=(x_start, x_end),
        y_range=(y_start, y_end),
        x_axis_type="mercator",
        y_axis_type="mercator",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        toolbar_location="above",
    )

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add a tile provider (OpenStreetMap/Carto) for geographic context
    try:
        from bokeh.tile_providers import get_provider, Vendors

        provider = get_provider(Vendors.CARTODBPOSITRON)
        p.add_tile(provider, alpha=0.6)
    except Exception:
        # ignore if tile provider not available
        pass
    
    # 9. Draw patches (regions)
    p.patches(
        'xs', 'ys',
        source=geosource,
        fill_color={'field': 'votes_display', 'transform': color_mapper},
        line_color='black',
        line_width=0.5,
        fill_alpha=0.7,
    )
    
    # 10. Add hover tool
    hover = HoverTool(tooltips=[
        ("Moughataa", "@moughataa"),
        ("Candidat", "@current_candidat"),
        ("Voix", "@votes_display{0,0}")
    ])
    p.add_tools(hover)
    p.add_layout(color_bar, 'right')
    
    # 11. JavaScript callback for candidate selection
    callback = CustomJS(args=dict(source=geosource, p=p), code="""
        var data = source.data;
        var selected = cb_obj.value;
        
        // Update votes_display with selected candidate's votes
        data['votes_display'] = data[selected].slice();
        
        // Update current_candidat for hover
        for (var i = 0; i < data['current_candidat'].length; i++) {
            data['current_candidat'][i] = selected;
        }
        
        // Update title
        p.title.text = "Résultats électoraux : " + selected;
        
        // Notify Bokeh of changes
        source.change.emit();
    """)
    
    # 12. Create dropdown selector
    select = Select(
        title="Choisir un candidat :",
        value=candidats[0],
        options=candidats
    )
    select.js_on_change('value', callback)
    
    # 13. Create layout
    layout = column(select, p)
    
    if show_plot:
        show(layout)
    
    print(f"Map created successfully with {len(candidats)} candidates!")
    return layout, geosource, color_mapper, candidats, merged


def create_simplified_election_map(
    gdf: gpd.GeoDataFrame,
    candidate_votes: dict[str, pd.Series],
    title: str = "Election Results",
    height: int = 600,
    width: int = 800,
    show_plot: bool = True,
) -> Optional[tuple]:
    """
    Create a simplified interactive election map from a GeoDataFrame and vote data.
    
    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame with geometry and region names
    candidate_votes : dict
        Dictionary mapping candidate names to vote Series indexed by region
    title : str
        Map title (default: 'Election Results')
    height : int
        Figure height in pixels
    width : int
        Figure width in pixels
    show_plot : bool
        Whether to display the map
    
    Returns
    -------
    tuple
        (layout, geosource, color_mapper, candidats, merged_gdf)
    """
    if not BOKEH_AVAILABLE:
        raise ImportError("Bokeh is required. Install with: pip install bokeh")
    
    # Build dataframe from candidate votes
    votes_df = pd.DataFrame(candidate_votes)
    merged = gdf.merge(votes_df, left_index=True, right_index=True, how='left').fillna(0)
    
    candidats = list(candidate_votes.keys())
    merged['votes_display'] = merged[candidats[0]].astype(float)
    merged['current_candidat'] = candidats[0]
    
    # Prepare for Bokeh
    cols_to_keep = ['geometry', 'votes_display', 'current_candidat'] + candidats
    if 'name' in merged.columns:
        cols_to_keep.insert(1, 'name')
    merged = merged[[c for c in cols_to_keep if c in merged.columns]].copy()
    
    for col in merged.columns:
        if col != 'geometry' and not pd.api.types.is_numeric_dtype(merged[col]):
            merged[col] = merged[col].astype(str)
    
    # Create source
    geosource = GeoJSONDataSource(geojson=merged.to_json())
    
    # Setup colors
    all_votes = merged[candidats].values.astype(float)
    vote_min, vote_max = float(all_votes.min()), float(all_votes.max())
    
    color_mapper = LinearColorMapper(palette=Viridis256[::-1], low=vote_min, high=vote_max)
    color_bar = ColorBar(
        color_mapper=color_mapper,
        ticker=BasicTicker(desired_num_ticks=10),
        formatter=PrintfTickFormatter(format="%d"),
        label_standoff=12,
        location=(0, 0)
    )
    
    # Create figure
    p = figure(
        title=f"{title} : {candidats[0]}",
        height=height,
        width=width,
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    
    p.patches(
        'xs', 'ys',
        source=geosource,
        fill_color={'field': 'votes_display', 'transform': color_mapper},
        line_color='white',
        line_width=0.5,
        fill_alpha=0.9
    )
    
    hover = HoverTool(tooltips=[("Candidat", "@current_candidat"), ("Voix", "@votes_display{0,0}")])
    p.add_tools(hover)
    p.add_layout(color_bar, 'right')
    
    callback = CustomJS(args=dict(source=geosource, p=p), code="""
        var data = source.data;
        var selected = cb_obj.value;
        data['votes_display'] = data[selected].slice();
        for (var i = 0; i < data['current_candidat'].length; i++) {
            data['current_candidat'][i] = selected;
        }
        p.title.text = "Résultats : " + selected;
        source.change.emit();
    """)
    
    select = Select(title="Choisir un candidat :", value=candidats[0], options=candidats)
    select.js_on_change('value', callback)
    
    layout = column(select, p)
    
    if show_plot:
        show(layout)
    
    return layout, geosource, color_mapper, candidats, merged
