import io
import pathlib
import re
import typing
from dataclasses import dataclass
from functools import singledispatch, wraps
from typing import Any, Callable, Optional, Sequence, Tuple

import ipywidgets as widgets
import numpy as np
from ipycanvas import Canvas
from PIL import Image, ImageEnhance

URL_REGEX = re.compile(
    r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?"
    + r"[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})"
    + r"?(\/.*)?$"
)


@dataclass
class URL:
    value: str

    def __bool__(self):
        return bool(URL_REGEX.match(self.value))


def adjust(
    img: widgets.Image, contrast_factor: float, brightness_factor: float
) -> widgets.Image:
    # turn widgets.Image into Pillow Image
    pil_image = Image.open(io.BytesIO(img.value))
    # apply adjustments
    pil_image = ImageEnhance.Contrast(pil_image).enhance(contrast_factor)
    pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness_factor)
    # turn back into a widget
    buffer = io.BytesIO()
    pil_image.save(buffer, "JPEG")
    buffer.seek(0)
    return widgets.Image(value=buffer.read(), format="jpg")


@singledispatch
def load_img(img: typing.Any):
    """
    Load an image, whether it's from a URL, a file, an array, or an already
    in-memory image.
    """
    raise ValueError(f"Can not load object of type {type(img)} as image.")


@load_img.register(widgets.Image)
def _img_already_widget(img: widgets.Image):
    return img


@load_img.register(bytes)
def _img_already_loaded(img: bytes):
    return widgets.Image(value=img)


@load_img.register(pathlib.Path)
def _load_img_path(img: pathlib.Path):
    """Read image from file"""
    return load_img(img.read_bytes())


@load_img.register(str)
def _load_img_string(img: str):
    """Read image from file or from URL"""
    img_path = pathlib.Path(img)
    if img_path.is_file():
        return load_img(img_path)

    img_url = URL(img)
    if img_url:
        return load_img(img_url)

    raise ValueError(f"{img} is neither an existing path nor a valid URL.")


@load_img.register(URL)
def _load_img_url(img: URL):
    import requests  # noqa: F401

    response = requests.get(img.value)
    response.raise_for_status()
    return load_img(response.content)


@load_img.register(np.ndarray)
def _load_img_ndarray(img: np.ndarray):
    """create image from array"""
    img = Image.fromarray(img.astype(np.uint8))
    return load_img(img)


@load_img.register(Image.Image)
def _load_img_pillow(img: Image.Image):
    """Encode image as bytes"""
    image_io = io.BytesIO()
    img.save(image_io, "JPEG")
    return load_img(image_io.getvalue())


def fit_image(
    img: widgets.Image, canvas: Canvas
) -> Tuple[int, int, int, int, int, int]:
    """Fit an image inside a canvas.

    Parameters
    ----------
    img : widgets.Image
    canvas : Canvas

    Returns
    -------
    Tuple[int, int, int, int, int, int]
        The x and y offset; width and height on the canvas; and original image
        width and height.
    """
    img_width, img_height = Image.open(io.BytesIO(img.value)).size
    canvas_width, canvas_height = canvas.size

    height_ratio, width_ratio = (
        img_height / canvas_height,
        img_width / canvas_width,
    )
    if height_ratio <= 1 and width_ratio <= 1:
        # we can fill and center the whole image
        width, height = img_width, img_height
    elif height_ratio >= width_ratio:
        # height is the limiting factor:
        height = int(img_height / height_ratio)
        width = int(img_width / height_ratio)
    elif height_ratio <= width_ratio:
        # width is the limiting factor:
        height = int(img_height / width_ratio)
        width = int(img_width / width_ratio)
    x, y = (canvas_width // 2 - width // 2, canvas_height // 2 - height // 2)
    return x, y, width, height, img_width, img_height


def dist(q: Sequence[float], p: Sequence[float]) -> float:
    """Euclidian distance between two points.

    Parameters
    ----------
    q : Sequence[float]
        Point q
    p : Sequence[float]
        Point p

    Returns
    -------
    float
        The distance between point q and p.
    """
    return (sum((px - qx) ** 2.0 for px, qx in zip(p, q))) ** 0.5


def trigger_redraw(fn: Callable) -> Callable:
    """Method decorator for functions that need to trigger a re-draw.

    Parameters
    ----------
    fn : Callable
        The function that needs to trigger a re-draw, e.g. because it changes
        the appearance of the canvas.

    Returns
    -------
    Callable
        A wrapped function that, when called, calls the input function and then
        calls the re-draw method on the class.
    """

    @wraps(fn)
    def wrapped_fn(self, *args, **kwargs):
        outp = fn(self, *args, **kwargs)
        self.re_draw()
        return outp

    return wrapped_fn


def only_inside_image(
    fn: Callable[[Any, float, float], Optional[Any]]
) -> Callable:
    """Method decorator for function that needs to only work inside the image.

    The input should be a method that accepts x and y.

    Parameters
    ----------
    fn : Callable
        The method that accepts self, x and y.

    Returns
    -------
    Callable
        A wrapped function that, when called, returns None if x and y are not
        inside the image (indicated by self.image_extent)
    """

    @wraps(fn)
    def wrapped_fn(self, x, y):
        if not self.image_extent[0] <= x <= self.image_extent[2]:
            return
        if not self.image_extent[1] <= y <= self.image_extent[3]:
            return
        x, y = self.canvas_to_image_coordinates((x, y))
        return fn(self, x, y)

    return wrapped_fn
