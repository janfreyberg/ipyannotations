import pathlib
from typing import Union

import numpy as np
from PIL import Image
from ipycanvas import MultiCanvas
from ipywidgets import widgets
from traitlets import Float, observe


class ZoomCanvas(MultiCanvas):
    """Canvas which contains a square that follows the mouse cursor on click"""

    # the position of the zoomed rectangle is given
    # as a ratio of the width or height of the canvas
    rect_height = Float(default_value=1, min=0, max=1)
    rect_width = Float(default_value=1, min=0, max=1)
    x = Float(default_value=0, min=0, max=1)
    y = Float(default_value=0, min=0, max=1)

    def __init__(self, width: int = 100, height: int = 100):
        super().__init__(n_canvases=2, width=width, height=height)
        self.image_ratio = 1
        self.enable = False
        self.draw_contour()
        self[1].on_mouse_move(self.move_rect)
        self[1].on_mouse_down(self.enable_move)
        self[1].on_mouse_up(self.disable_move)

    def draw_contour(self):
        self[0].stroke_rect(0, 0, self.width, self.height)

    def draw_current_rectangle(self):
        self[1].stroke_rect(
            self.x * self.width,
            self.y * self.height,
            self.rect_width * self.width,
            self.rect_height * self.height,
        )

    def load_image(self, image: Union[str, pathlib.Path, Image.Image]):
        if not isinstance(image, Image.Image):
            image = Image.open(image)
        img_width, img_height = image.size
        self.image_ratio = img_height / img_width
        # modify the canvas shape dynamically
        self.height = self.width * self.image_ratio
        resized_image = image.resize(size=(self.width, self.height))
        self[0].put_image_data(np.asarray(resized_image))
        self.rect_width = 1
        self.rect_height = 1
        self.draw_contour()
        self.draw_current_rectangle()

    def enable_move(self, *args):
        self.enable = True

    def disable_move(self, *args):
        self.enable = False

    def clear_current_rect(self):
        self[1].clear()

    @observe("rect_width", "rect_height")
    def update_rect_size(self, *change):
        self.clear_current_rect()
        self.move_rect(self.x, self.y, refresh=True)

    def move_rect(self, x, y, refresh=False):
        if self.enable or refresh:
            # the cursor (x, y) is at the center of the rectangle
            # but the rectangle is drawn from the top left corner
            x = round(x / self.width - self.rect_width / 2, 5)
            y = round(y / self.height - self.rect_height / 2, 5)
            with self.hold_trait_notifications():
                self.x = max(0, min(1 - self.rect_width, x))
                self.y = max(0, min(1 - self.rect_height, y))
            self.clear_current_rect()
            self.draw_current_rectangle()


class ZoomController(widgets.VBox):
    """
    Widget with buttons to zoom in and out of the image.
    """

    zoom_scale = Float(default_value=1, min=1)

    def __init__(self, width: int = 200, height: int = 200):
        self.canvas = ZoomCanvas(width=width, height=height)
        self.text = widgets.Text(layout={"width": "60px"})

        layout = {"width": "30px"}
        self.zoom_plus_btn = widgets.Button(description="+", layout=layout)
        self.zoom_minus_btn = widgets.Button(description="-", layout=layout)
        self.zoom_plus_btn.on_click(self.zoom_plus)
        self.zoom_minus_btn.on_click(self.zoom_minus)
        zoom_controls = widgets.HBox(
            [self.zoom_plus_btn, self.zoom_minus_btn, self.text]
        )

        super().__init__()
        self.children = [zoom_controls, self.canvas]
        self.layout.margin = '0px 0px 0px 20px'
        self.layout.align_items = 'center'
        self.update_zoom()

    @observe("zoom_scale")
    def update_zoom(self, *change):
        with self.canvas.hold_trait_notifications():
            self.canvas.rect_width = 1 / self.zoom_scale
            self.canvas.rect_height = 1 / self.zoom_scale

        self.text.value = f"{self.zoom_scale * 100:.0f}%"

    def load_image(self, image: Union[str, pathlib.Path, Image.Image]):
        self.canvas.load_image(image)

    def zoom_plus(self, *args, **kwargs):
        self.zoom_scale += 0.1

    def zoom_minus(self, *args, **kwargs):
        self.zoom_scale = max(1, self.zoom_scale - 0.1)
