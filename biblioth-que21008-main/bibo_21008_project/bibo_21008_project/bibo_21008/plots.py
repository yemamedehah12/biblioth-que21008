"""Plotting functions for bibo_21008."""

from __future__ import annotations
from typing import Optional, Sequence, Union
import matplotlib.pyplot as plt
from typing import Any

# Optional Bokeh-based map functionality
try:
    from bokeh.io import show
    from bokeh.models import (
        GeoJSONDataSource,
        LinearColorMapper,
        ColorBar,
        HoverTool,
        BasicTicker,
    )
    from bokeh.plotting import figure
    from bokeh.tile_providers import get_provider, Vendors
    from bokeh.palettes import Viridis256
    BOKEH_AVAILABLE = True
except Exception:
    BOKEH_AVAILABLE = False

from .styles import DEFAULT_STYLE, set_bibo_style

Number = Union[int, float]

def _get_color(idx: int) -> str:
    return DEFAULT_STYLE.palette[idx % len(DEFAULT_STYLE.palette)]

def _prep_ax(ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(7.2, 4.2))
    else:
        fig = ax.figure
    return fig, ax

def styled_line(
    x: Sequence[Number],
    y: Sequence[Number],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    marker: Optional[str] = "o",
    color: Optional[str] = None,
    ax=None,
    show: bool = True,
):
    """Styled line plot."""
    set_bibo_style()
    fig, ax = _prep_ax(ax)
    c = color or _get_color(0)
    ax.plot(x, y, marker=marker, color=c)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.margins(x=0.02, y=0.08)
    if show:
        plt.show()
    return fig, ax

def styled_scatter(
    x: Sequence[Number],
    y: Sequence[Number],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    size: Number = 55,
    alpha: float = 0.9,
    color: Optional[str] = None,
    ax=None,
    show: bool = True,
):
    """Styled scatter plot."""
    set_bibo_style()
    fig, ax = _prep_ax(ax)
    c = color or _get_color(1)
    ax.scatter(x, y, s=size, alpha=alpha, color=c, edgecolors="white", linewidths=0.7)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.margins(x=0.02, y=0.08)
    if show:
        plt.show()
    return fig, ax

def styled_bar(
    categories: Sequence[str],
    values: Sequence[Number],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    color: Optional[str] = None,
    rotate_xticks: bool = True,
    ax=None,
    show: bool = True,
):
    """Styled bar chart."""
    set_bibo_style()
    fig, ax = _prep_ax(ax)
    c = color or _get_color(2)
    ax.bar(categories, values, color=c, alpha=0.92)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if rotate_xticks:
        ax.tick_params(axis="x", rotation=20)
    ax.margins(y=0.12)
    if show:
        plt.show()
    return fig, ax

def styled_hist(
    data: Sequence[Number],
    bins: int = 12,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Count",
    color: Optional[str] = None,
    ax=None,
    show: bool = True,
):
    """Styled histogram."""
    set_bibo_style()
    fig, ax = _prep_ax(ax)
    c = color or _get_color(3)
    ax.hist(data, bins=bins, color=c, alpha=0.88, edgecolor="white", linewidth=0.9)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.margins(y=0.08)
    if show:
        plt.show()
    return fig, ax

def styled_box(
    data: Sequence[Sequence[Number]],
    labels: Optional[Sequence[str]] = None,
    title: str = "",
    ylabel: str = "",
    ax=None,
    show: bool = True,
):
    """Styled box plot."""
    set_bibo_style()
    fig, ax = _prep_ax(ax)
    bp = ax.boxplot(data, labels=labels, patch_artist=True, widths=0.55)

    for i, box in enumerate(bp["boxes"]):
        box.set(facecolor=_get_color(i), alpha=0.75, edgecolor="white", linewidth=1.0)
    for whisker in bp["whiskers"]:
        whisker.set(color=(0, 0, 0, 0.55))
    for cap in bp["caps"]:
        cap.set(color=(0, 0, 0, 0.55))
    for median in bp["medians"]:
        median.set(color="black", linewidth=1.5)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.margins(y=0.10)
    if show:
        plt.show()
    return fig, ax


def bokeh_td_election_map(
    gdf,
    value_col: str,
    name_col: Optional[str] = None,
    tile: str = "CARTODBPOSITRON",
    palette: Any = None,
    width: int = 800,
    height: int = 700,
    zoom: int = 6,
    show_plot: bool = True,
):
    """Create an interactive choropleth map for Chad (ISO 'TD') election results using Bokeh.

    Parameters
    - gdf: GeoDataFrame containing geometries and a column with election values.
    - value_col: Column name with numeric values to color by.
    - name_col: Optional column name for hover labels (defaults to index).
    - tile: Tile provider name from `bokeh.tile_providers.Vendors`.
    - palette: Color palette (list-like) or one of Bokeh palettes.
    - width, height: plot size in pixels.
    - zoom: initial zoom level (used to set scale around centroid).
    - show_plot: whether to call `bokeh.show` before returning the figure.

    Returns the Bokeh `figure` instance.
    """
    if not BOKEH_AVAILABLE:
        raise RuntimeError("Bokeh is not available in the environment. Install `bokeh` to use this function.")

    # Resolve default palette at runtime to avoid evaluating bokeh palettes
    if palette is None:
        try:
            # import locally to avoid module-level dependency during import time
            from bokeh.palettes import Viridis256 as _Viridis256

            palette = _Viridis256
        except Exception:
            # fallback to a simple gray palette
            palette = ["#d9d9d9"]

    import geopandas as gpd
    # Ensure GeoDataFrame
    if not hasattr(gdf, "geometry"):
        raise TypeError("gdf must be a GeoDataFrame with a 'geometry' column")

    # Work in WebMercator for tile compatibility
    gdf = gdf.copy()
    if gdf.crs is None or gdf.crs.to_epsg() != 3857:
        try:
            gdf = gdf.to_crs(epsg=3857)
        except Exception:
            # if original crs is geographic, try converting from EPSG:4326
            gdf = gdf.to_crs(epsg=3857)

    # Prepare GeoJSON source
    geo_source = GeoJSONDataSource(geojson=gdf.to_json())

    # Compute color mapper range
    vals = gdf[value_col].dropna()
    if vals.size == 0:
        low, high = 0, 1
    else:
        low, high = float(vals.min()), float(vals.max())
        if low == high:
            low = 0

    color_mapper = LinearColorMapper(palette=palette, low=low, high=high)

    # Create figure with mercator axes
    p = figure(
        x_axis_type="mercator",
        y_axis_type="mercator",
        width=width,
        height=height,
        tools="pan,wheel_zoom,reset,save",
        active_scroll="wheel_zoom",
    )

    # Add tile provider
    try:
        provider = get_provider(getattr(Vendors, tile))
    except Exception:
        provider = get_provider(Vendors.CARTODBPOSITRON)
    p.add_tile(provider)

    # Draw the patches
    p.patches(
        "xs",
        "ys",
        source=geo_source,
        fill_color={"field": value_col, "transform": color_mapper},
        line_color="gray",
        line_width=0.4,
        fill_alpha=0.9,
    )

    # Hover tool: try to display provided name column or index
    if name_col and name_col in gdf.columns:
        hover_name = f"@{name_col}"
    else:
        # create a display name property from index
        gdf = gdf.reset_index().rename(columns={"index": "_idx_for_hover"})
        geo_source = GeoJSONDataSource(geojson=gdf.to_json())
        hover_name = "@_idx_for_hover"
        # rebind patches with new source
        p.renderers = []
        p.add_tile(provider)
        p.patches(
            "xs",
            "ys",
            source=geo_source,
            fill_color={"field": value_col, "transform": color_mapper},
            line_color="gray",
            line_width=0.4,
            fill_alpha=0.9,
        )

    hover = HoverTool(tooltips=[("name", hover_name), (value_col, f"@{value_col}")])
    p.add_tools(hover)

    # Color bar
    color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(), label_standoff=8, width=12, location=(0, 0))
    p.add_layout(color_bar, "right")

    # Auto-center on data
    try:
        bounds = gdf.total_bounds  # (minx, miny, maxx, maxy)
        cx = (bounds[0] + bounds[2]) / 2.0
        cy = (bounds[1] + bounds[3]) / 2.0
        p.x_range.start = cx - 1_000_000 / (2 ** (zoom - 1))
        p.x_range.end = cx + 1_000_000 / (2 ** (zoom - 1))
        p.y_range.start = cy - 800_000 / (2 ** (zoom - 1))
        p.y_range.end = cy + 800_000 / (2 ** (zoom - 1))
    except Exception:
        pass

    if show_plot:
        show(p)

    return p
