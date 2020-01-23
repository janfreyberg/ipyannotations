import io
import typing
import pathlib
from functools import singledispatch
from dataclasses import dataclass
import re
from PIL import Image, ImageEnhance
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
