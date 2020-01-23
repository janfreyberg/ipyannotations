"""
Different types of canvases for annotating images.

All canvases should inherit from _abstract.AbstractAnnotationCanvas.
"""

from .polygon import PolygonAnnotationCanvas
from .point import PointAnnotationCanvas
from .box import BoundingBoxAnnotationCanvas

__all__ = [
    "PolygonAnnotationCanvas",
    "PointAnnotationCanvas",
    "BoundingBoxAnnotationCanvas",
]
