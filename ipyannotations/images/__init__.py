"""Image annotation widgets."""

from .annotator import BoxAnnotator, PointAnnotator, PolygonAnnotator
from .captions import ImageCaption
from .classification import ClassLabeller, MulticlassLabeller

__all__ = [
    "PolygonAnnotator",
    "PointAnnotator",
    "BoxAnnotator",
    "ClassLabeller",
    "MulticlassLabeller",
    "ImageCaption",
]
