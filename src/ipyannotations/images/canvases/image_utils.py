import io

from PIL import Image, ImageEnhance
import ipywidgets as widgets


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
