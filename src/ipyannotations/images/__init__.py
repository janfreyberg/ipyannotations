"""Image annotation tools."""
__version__ = "0.1.0"

from .annotator import PolygonAnnotator, PointAnnotator, BoxAnnotator

__all__ = ["PolygonAnnotator", "PointAnnotator", "BoxAnnotator"]
