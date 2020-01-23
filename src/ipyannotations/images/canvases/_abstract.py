from ipycanvas import MultiCanvas, hold_canvas
import ipywidgets as widgets
from typing import Tuple, Optional, Sequence, Deque, Callable, Union
from collections import deque, defaultdict
import abc
from traitlets import Unicode, Float, Integer, observe
import pathlib

from .utils import set_colors, fit_image
from .image_utils import adjust, load_img


class AbstractAnnotationCanvas(MultiCanvas):

    current_class = Unicode(allow_none=True)
    opacity = Float(default_value=0.4)
    point_size = Integer(default_value=5, min=1, max=20)

    image_contrast = Float(default_value=1, min=0, max=10)
    image_brightness = Float(default_value=1, min=0, max=10)

    def __init__(
        self,
        size: Tuple[int, int] = (700, 500),
        classes: Optional[Sequence[str]] = None,
        **kwargs
    ):
        super().__init__(n_canvases=3, size=size, **kwargs)
        self._undo_queue: Deque[Callable] = deque([])
        self.image_extent = (0, 0, *size)

        self.image_canvas = self[0]
        self.annotation_canvas = self[1]
        self.interaction_canvas = self[2]

        self.interaction_canvas.on_mouse_down(self.on_click)
        self.interaction_canvas.on_mouse_move(self.on_drag)
        self.interaction_canvas.on_mouse_up(self.on_release)

        self.current_image: Optional[widgets.Image] = None
        self.dragging: Optional[Callable[[int, int], None]] = None

        # register re_draw as handler for obacity changes
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

    def load_image(self, image: Union[widgets.Image, str, pathlib.Path]):
        """Display an image on the annotation canvas.

        Parameters
        ----------
        image : Union[widgets.Image, str, pathlib.Path]
            The image, or the path to the image.
        """
        image = load_img(image)
        self.current_image = image
        self._display_image()
        self._init_empty_data()

    @observe("current_class")
    def _set_class(self, change):
        self.set_class(change["new"])

    @abc.abstractmethod
    def re_draw(self, *args, **kwargs):
        pass

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

    @observe("image_contrast", "image_brightness")
    def _display_image(self, *change):
        if self.current_image is not None:
            if self.image_brightness != 1 or self.image_contrast != 1:
                image = adjust(
                    self.current_image,
                    contrast_factor=self.image_contrast,
                    brightness_factor=self.image_brightness,
                )
            else:
                image = self.current_image

            image_canvas = self[0]
            with hold_canvas(image_canvas):
                x, y, width, height = fit_image(image, image_canvas)
                image_canvas.draw_image(
                    image, x=x, y=y, width=width, height=height
                )
                self.image_extent = (x, y, x + width, y + height)
