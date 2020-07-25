import abc
import pathlib
from collections import deque, defaultdict
from typing import Tuple, Optional, Sequence, Deque, Callable, Union

import ipywidgets as widgets
from PIL import ImageOps, Image
from ipycanvas import MultiCanvas, hold_canvas
from traitlets import Unicode, Float, Integer, observe

from .image_utils import (
    adjust,
    load_img,
    fit_image,
    pil_to_widget,
    widget_to_pil,
)
from .utils import set_colors


class AbstractAnnotationCanvas(MultiCanvas):
    current_class = Unicode(allow_none=True)
    opacity = Float(default_value=0.4)
    point_size = Integer(default_value=5, min=1, max=20)

    image_contrast = Float(default_value=1, min=0, max=10)
    image_brightness = Float(default_value=1, min=0, max=10)

    zoom_scale = Float(default_value=1, min=1)
    zoomed_image_x = Float(default_value=0, min=0, max=1)
    zoomed_image_y = Float(default_value=0, min=0, max=1)

    def __init__(
        self,
        size: Tuple[int, int] = (700, 500),
        classes: Optional[Sequence[str]] = None,
        **kwargs
    ):
        super().__init__(n_canvases=3, width=size[0], height=size[1], **kwargs)
        self._undo_queue: Deque[Callable] = deque([])
        self.image_extent = (0, 0, *size)

        self.image_canvas = self[0]
        self.annotation_canvas = self[1]
        self.interaction_canvas = self[2]

        self.interaction_canvas.on_mouse_down(self._on_click)
        self.interaction_canvas.on_mouse_move(self._on_drag)
        self.interaction_canvas.on_mouse_up(self._on_release)

        self.current_image = Image.new(mode="RGB", size=size, color="grey")
        self.dragging: Optional[Callable[[int, int], None]] = None

        #  Caches for the image at given zoom scale,
        #  and zoomed image crop that fits within the canvas
        self.zoom_scale = 1
        self.zoomed_image: Optional[Image.Image] = None
        self.image_crop: Optional[Image.Image] = None

        # register re_draw as handler for opacity changes
        # note this is done here rather than as a decorator as re_draw is
        # an abstract method for now.
        self.observe(
            lambda *x: self.re_draw(),
            names=["opacity", "editing", "point_size", "nothing"],
        )

        if classes is not None:
            self.colormap = {
                cls_: col for cls_, col in zip(classes, set_colors())
            }
        else:
            self.colormap = defaultdict(lambda: "#000000")

        self._init_empty_data()
        self._update_zoom()

    def load_image(self, image: Union[widgets.Image, str, pathlib.Path]):
        """Display an image on the annotation canvas.

        Parameters
        ----------
        image : Union[widgets.Image, str, pathlib.Path]
            The image, or the path to the image.
        """
        # let's keep the image as Image.Image type
        image = widget_to_pil(load_img(image))
        # fit image to canvas size
        image, (x, y, width, height) = fit_image(image, self.size)
        self.image_extent = (x, y, x + width, y + height)
        self.current_image = image
        self._update_zoom()
        self._init_empty_data()

    @observe("current_class")
    def _set_class(self, change):
        self.set_class(change["new"])

    @abc.abstractmethod
    def re_draw(self, *args, **kwargs):
        pass

    def _on_click(self, x: float, y: float):
        self.on_click(*self.map_canvas_coords_to_image(x, y))

    def _on_drag(self, x: float, y: float):
        self.on_drag(*self.map_canvas_coords_to_image(x, y))

    def _on_release(self, x: float, y: float):
        self.on_release(*self.map_canvas_coords_to_image(x, y))

    @abc.abstractmethod
    def on_click(self, x: float, y: float):
        pass

    @abc.abstractmethod
    def on_drag(self, x: float, y: float):
        pass

    @abc.abstractmethod
    def on_release(self, x: float, y: float):
        pass

    @abc.abstractmethod
    def add_point(self, x: float, y: float):
        pass

    @abc.abstractmethod
    def set_class(self, class_name: str):
        pass

    @abc.abstractmethod
    def _init_empty_data(self):
        raise NotImplementedError(
            "This canvas does not implement initialising the data."
        )

    @observe("zoom_scale")
    def _update_zoom(self, *change):
        """
        Update the cached zoomed image.
        This operation is time consuming and should be computed
        as little as possible.
        """
        self.zoomed_image = ImageOps.scale(self.current_image, self.zoom_scale)
        self._update_crop()

    @observe("zoomed_image_x", "zoomed_image_y")
    def _update_crop(self, *change):
        """
        Update the cached zoomed image.
        This operation is time consuming and should be computed
        as little as possible.
        """
        minx = self.zoomed_image_x * self.zoomed_image.width
        maxx = self.zoomed_image_x * self.zoomed_image.width + self.width
        miny = self.zoomed_image_y * self.zoomed_image.height
        maxy = self.zoomed_image_y * self.zoomed_image.height + self.height
        self.image_crop = self.zoomed_image.crop(box=(minx, miny, maxx, maxy))
        self._display_image()
        self.re_draw()

    @observe("image_contrast", "image_brightness")
    def _display_image(self, *change):
        image = self.image_crop
        if self.image_brightness != 1 or self.image_contrast != 1:
            image = adjust(
                image,
                contrast_factor=self.image_contrast,
                brightness_factor=self.image_brightness,
            )

        with hold_canvas(self.image_canvas):
            self.image_canvas.draw_image(pil_to_widget(image))
            self.image_canvas.stroke_rect(0, 0, self.width, self.height)

    def map_canvas_coords_to_image(self, x, y):
        """
        Convert Mouse (x, y) coordinates to (x', y')
        the coordinates within the current_image
        """
        x = int(
            (x + self.zoomed_image_x * self.zoomed_image.width)
            / self.zoom_scale
        )
        y = int(
            (y + self.zoomed_image_y * self.zoomed_image.height)
            / self.zoom_scale
        )
        return x, y

    def map_image_coords_to_canvas(self, x, y):
        x = (
            int(x * self.zoom_scale)
            - self.zoomed_image_x * self.zoomed_image.width
        )
        y = (
            int(y * self.zoom_scale)
            - self.zoomed_image_y * self.zoomed_image.height
        )
        return x, y
