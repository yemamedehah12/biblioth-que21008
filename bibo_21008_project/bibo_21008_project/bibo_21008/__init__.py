"""bibo_21008 - personal plotting library."""

from .styles import set_bibo_style
from .plots import (
    styled_line,
    styled_scatter,
    styled_bar,
    styled_hist,
    styled_box,
)

__all__ = [
    "set_bibo_style",
    "styled_line",
    "styled_scatter",
    "styled_bar",
    "styled_hist",
    "styled_box",
]
