"""Plotting functions for bibo_21008."""

from __future__ import annotations
from typing import Optional, Sequence, Union
import matplotlib.pyplot as plt

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
