"""Annotate data in jupyter notebooks."""
__version__ = "0.1.1"

from .images import PolygonAnnotator, PointAnnotator, BoxAnnotator

__all__ = ["PolygonAnnotator", "PointAnnotator", "BoxAnnotator"]
