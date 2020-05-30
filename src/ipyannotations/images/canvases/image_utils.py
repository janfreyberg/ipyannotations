import io
import pathlib
from functools import singledispatch
from dataclasses import dataclass
import re
from typing import Tuple, Any

from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import ipywidgets as widgets


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


def pil_to_widget(image: Image.Image) -> widgets.Image:
    buffer = io.BytesIO()
    image.save(buffer, "JPEG")
    buffer.seek(0)
    return widgets.Image(value=buffer.read(), format="jpg")


def widget_to_pil(image: widgets.Image):
    return Image.open(io.BytesIO(image.value))


def fit_image(
        img: Image.Image, size
) -> Tuple[Image.Image, Tuple[int, int, int, int]]:
    img_width, img_height = img.size
    desired_width, desired_height = size

    ratio = max(img_width / desired_width, img_height / desired_height)
    img = ImageOps.scale(img, ratio)

    width, height = img.size
    x, y = ((desired_width - width) // 2, (desired_height - height) // 2)

    border = (x, y, desired_width - x - width, desired_height - y - height)
    img = ImageOps.expand(img, border=border)

    return img, (x, y, width, height)


def adjust(
    img: Image.Image, contrast_factor: float, brightness_factor: float
) -> Image.Image:
    img = ImageEnhance.Contrast(img).enhance(contrast_factor)
    img = ImageEnhance.Brightness(img).enhance(brightness_factor)
    return img


@singledispatch
def load_img(img: Any):
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
