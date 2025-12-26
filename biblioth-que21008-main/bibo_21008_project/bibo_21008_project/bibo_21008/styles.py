"""Style utilities for bibo_21008."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import matplotlib as mpl

@dataclass(frozen=True)
class BiboStyle:
    font_family: str = "DejaVu Sans"
    font_size: int = 11
    title_size: int = 14
    label_size: int = 11
    line_width: float = 2.2
    grid_alpha: float = 0.25
    spine_alpha: float = 0.35
    tick_alpha: float = 0.8
    palette: tuple[str, ...] = (
        "#2E86AB",  # blue
        "#F18F01",  # orange
        "#C73E1D",  # red
        "#6A4C93",  # purple
        "#2A9D8F",  # green
        "#264653",  # dark
    )

DEFAULT_STYLE = BiboStyle()

def set_bibo_style(style: Optional[BiboStyle] = None) -> None:
    """Apply the bibo_21008 Matplotlib style globally."""
    s = style or DEFAULT_STYLE
    mpl.rcParams.update({
        "font.family": s.font_family,
        "font.size": s.font_size,
        "axes.titlesize": s.title_size,
        "axes.labelsize": s.label_size,
        "axes.titleweight": "bold",
        "axes.grid": True,
        "grid.alpha": s.grid_alpha,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": (0, 0, 0, s.spine_alpha),
        "xtick.color": (0, 0, 0, s.tick_alpha),
        "ytick.color": (0, 0, 0, s.tick_alpha),
        "lines.linewidth": s.line_width,
        "figure.dpi": 110,
        "savefig.dpi": 160,
    })
