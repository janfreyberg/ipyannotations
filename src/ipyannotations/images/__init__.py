"""Image annotation tools."""
__version__ = "0.1.0"

from .annotator import BoxAnnotator, PointAnnotator, PolygonAnnotator

__all__ = ["PolygonAnnotator", "PointAnnotator", "BoxAnnotator"]
