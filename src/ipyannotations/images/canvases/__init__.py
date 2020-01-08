"""
Different types of canvases for annotating images.

All canvases should inherit from _abstract.AbstractAnnotationCanvas.
"""

from .polygon import PolygonAnnotationCanvas

__all__ = ["PolygonAnnotationCanvas"]
