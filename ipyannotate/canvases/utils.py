import io
from typing import Tuple
import ipywidgets as widgets
from ipycanvas import Canvas
from PIL import Image
from palettable.colorbrewer.qualitative import Set2_8


def fit_image(img: widgets.Image, canvas: Canvas) -> Tuple[int, int, int, int]:
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
    # breakpoint()
    x, y = (canvas_width // 2 - width // 2, canvas_height // 2 - height // 2)
    # canvas.draw_image(img, x=x, y=y, width=height, height=width)
    return x, y, width, height


def set_colors():
    while True:
        yield from Set2_8.hex_colors
