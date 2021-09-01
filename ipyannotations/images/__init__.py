"""Image annotation widgets."""

from .annotator import BoxAnnotator, PointAnnotator, PolygonAnnotator
from .freetext import FreetextAnnotator
from .classification import ClassLabeller, MulticlassLabeller

__all__ = [
    "PolygonAnnotator",
    "PointAnnotator",
    "BoxAnnotator",
    "ClassLabeller",
    "MulticlassLabeller",
    "FreetextAnnotator",
]
