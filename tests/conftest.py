import functools
import io
import os

import ipywidgets as widgets
import numpy as np
from hypothesis import assume, example, given, infer, settings, strategies
from PIL import Image

from ipyannotations.images.canvases.shapes import BoundingBox, Point, Polygon

settings.register_profile("default_", settings(deadline=None))
settings.load_profile("default_")

coordinates = strategies.tuples(
    strategies.integers(min_value=0, max_value=700),
    strategies.integers(min_value=0, max_value=500),
)

strategies.coordinates = lambda: coordinates


@strategies.composite
def polygons(draw):
    points = strategies.lists(coordinates, min_size=3)
    label = strategies.text()

    return Polygon(draw(points), draw(label))


@strategies.composite
def points(draw):
    label = strategies.text()
    return Point(draw(coordinates), draw(label))


@strategies.composite
def boxes(draw):
    label = strategies.text()
    a = draw(coordinates)
    b = draw(coordinates)
    xyxy = (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))
    return BoundingBox(xyxy, draw(label))


strategies.register_type_strategy(Polygon, polygons())
strategies.register_type_strategy(Point, points())
strategies.register_type_strategy(BoundingBox, boxes())


@strategies.composite
def image_array(draw, image_size=None):
    if image_size is None:
        size = draw(
            strategies.tuples(
                strategies.integers(min_value=40, max_value=1000),
                strategies.integers(min_value=40, max_value=1000),
            )
        )
    else:
        size = image_size
    size = size[::-1]
    ndim = strategies.sampled_from([2, 3])

    if ndim == 3:
        size = size + (3,)

    data = np.random.randint(0, 256, size=size, dtype=np.uint8)
    return data


@strategies.composite
def pil_image(draw, image_size=None):
    return Image.fromarray(draw(image_array(image_size=image_size)))


@strategies.composite
def image_widgets(draw, image_size=None):

    img = draw(pil_image(image_size=image_size))

    buffer = io.BytesIO()
    img.save(buffer, "JPEG")
    widget = widgets.Image(value=buffer.getvalue(), format="jpg")

    return widget


strategies.register_type_strategy(np.ndarray, image_array())
strategies.register_type_strategy(Image.Image, pil_image())
strategies.register_type_strategy(widgets.Image, image_widgets())

strategies.image_widgets = image_widgets
