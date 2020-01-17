from ipyannotations.images.canvases.shapes import Polygon, Point
from hypothesis import given, assume, infer, example, strategies
import numpy as np
import io
from PIL import Image
import ipywidgets as widgets


coordinates = strategies.tuples(
    strategies.integers(min_value=0, max_value=700),
    strategies.integers(min_value=0, max_value=500),
)


@strategies.composite
def polygons(draw):
    points = strategies.lists(coordinates)
    label = strategies.text()

    return Polygon(draw(points), draw(label))


@strategies.composite
def points(draw):
    label = strategies.text()
    return Point(draw(coordinates), draw(label))


@strategies.composite
def image_array(draw):
    size = draw(
        strategies.tuples(
            strategies.integers(min_value=2, max_value=1000),
            strategies.integers(min_value=2, max_value=1000),
        )
    )
    ndim = strategies.one_of(2, 3)

    if ndim == 3:
        size = size + (3,)

    data = np.random.randint(0, 256, size=size, dtype=np.uint8)
    return data


@strategies.composite
def pil_image(draw):
    return Image.fromarray(draw(image_array()))


@strategies.composite
def image_widgets(draw):

    img = draw(pil_image())

    buffer = io.BytesIO()
    img.save(buffer, "JPEG")
    widget = widgets.Image(value=buffer.getvalue(), format="jpg")

    return widget


strategies.register_type_strategy(np.ndarray, image_array())
strategies.register_type_strategy(Image.Image, pil_image())
strategies.register_type_strategy(widgets.Image, image_widgets())
strategies.register_type_strategy(Polygon, polygons())
strategies.register_type_strategy(Point, points())
