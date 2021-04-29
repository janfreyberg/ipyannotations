"""
Different types of canvases for annotating images.

All canvases should inherit from abstract_canvas.AbstractAnnotationCanvas.
"""

from .box import BoundingBoxAnnotationCanvas
from .point import PointAnnotationCanvas
from .polygon import PolygonAnnotationCanvas

__all__ = [
    "PolygonAnnotationCanvas",
    "PointAnnotationCanvas",
    "BoundingBoxAnnotationCanvas",
]
