import io

from PIL import Image, ImageEnhance
import ipywidgets as widgets


def adjust_contrast(img: widgets.Image, contrast_factor: float):

    pil_image = Image.open(io.BytesIO(img.value))
    pil_image = ImageEnhance.Contrast(pil_image).enhance(contrast_factor)
    buffer = io.BytesIO()
    pil_image.save(buffer, "PNG")
    buffer.seek(0)
    return widgets.Image(value=buffer.read())


def adjust_brightness(img: widgets.Image, brightness_factor: float):

    pil_image = Image.open(io.BytesIO(img.value))
    pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness_factor)
    buffer = io.BytesIO()
    pil_image.save(buffer, "PNG")
    buffer.seek(0)
    return widgets.Image(value=buffer.read())


def adjust(img, contrast_factor: float, brightness_factor: float):

    pil_image = Image.open(io.BytesIO(img.value))
    pil_image = ImageEnhance.Contrast(pil_image).enhance(contrast_factor)
    pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness_factor)
    buffer = io.BytesIO()
    pil_image.save(buffer, "JPEG")
    buffer.seek(0)
    return widgets.Image(value=buffer.read(), format="jpg")
