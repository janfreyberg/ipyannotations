import abc
import pathlib
from collections import defaultdict, deque
from typing import Callable, Deque, Optional, Sequence, Tuple, Union

import ipywidgets as widgets
from ipycanvas import MultiCanvas, hold_canvas
from traitlets import Float, Integer, Unicode, observe

from .color_utils import set_colors
from .image_utils import adjust, fit_image, load_img


class AbstractAnnotationCanvas(MultiCanvas):

    current_class = Unicode(allow_none=True)
    opacity = Float(default_value=0.4)
    point_size = Integer(default_value=5, min=1, max=20)

    image_contrast = Float(default_value=1, min=0, max=10)
    image_brightness = Float(default_value=1, min=0, max=10)

    def __init__(  # noqa: D001
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

        self.interaction_canvas.on_mouse_down(self.on_click)
        self.interaction_canvas.on_mouse_move(self.on_drag)
        self.interaction_canvas.on_mouse_up(self.on_release)

        self.current_image: Optional[widgets.Image] = None
        self.dragging: Optional[Callable[[int, int], None]] = None
        self.error_output_widget = widgets.Output()

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

        self.init_empty_data()

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
        self.init_empty_data()

    def clear(self) -> None:
        """Clear the canvas - clear the image and delete any annotations."""
        super().clear()
        self.init_empty_data()

    @observe("current_class")
    def _set_class(self, change):
        self.set_class(change["new"])

    @abc.abstractmethod
    def re_draw(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def on_click(self, x: float, y: float):  # noqa: D001
        pass

    @abc.abstractmethod
    def on_drag(self, x: float, y: float):  # noqa: D001
        pass

    @abc.abstractmethod
    def on_release(self, x: float, y: float):  # noqa: D001
        pass

    @abc.abstractmethod
    def add_point(self, x: float, y: float):  # noqa: D001
        pass

    @abc.abstractmethod
    def set_class(self, class_name: str):  # noqa: D001
        pass

    @abc.abstractmethod
    def init_empty_data(self):
        raise NotImplementedError(
            "This canvas does not implement initialising the data."
        )

    def canvas_to_image_coordinates(
        self, point: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Convert an x, y point from canvas coordinates to image coordinates.

        Parameters
        ----------
        point : Tuple[int, int]
            The point, as integers (or floats, to be rounded) relative to the
            canvas, with 0,0 being the top left, and
            (canvas_width, canvas_height) being the bottom right.

        Returns
        -------
        Tuple[int, int]
            The point relative to the image.
        """
        x, y = point
        adjusted_width = self.image_extent[2] - self.image_extent[0]
        x_adjustment = self.original_width / adjusted_width
        adjusted_height = self.image_extent[3] - self.image_extent[1]
        y_adjustment = self.original_height / adjusted_height
        x = x_adjustment * (x - self.image_extent[0])
        y = y_adjustment * (y - self.image_extent[1])
        x, y = round(x), round(y)
        return x, y

    def image_to_canvas_coordinates(
        self, point: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Convert an x, y point from image coordinates to canvas coordinates.

        Parameters
        ----------
        point : Tuple[int, int]
            The point, as integers (or floats, to be rounded) relative to the
            image, with 0,0 being the top left, and
            (image_width, image_height) being the bottom right.

        Returns
        -------
        Tuple[int, int]
            The point relative to the canvas.
        """
        x, y = point
        adjusted_width = self.image_extent[2] - self.image_extent[0]
        adjusted_height = self.image_extent[3] - self.image_extent[1]
        x = x * adjusted_width / self.original_width + self.image_extent[0]
        y = y * adjusted_height / self.original_height + self.image_extent[1]
        x, y = round(x), round(y)
        return x, y

    # def correct_coordinates(self, point: Tuple[int, int]) -> Tuple[int, int]:
    #     return (
    #         point[0] + self.image_extent[0],
    #         point[1] + self.image_extent[1],
    #     )

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
                x, y, width, height, img_width, img_height = fit_image(
                    image, image_canvas
                )
                image_canvas.draw_image(
                    image, x=x, y=y, width=width, height=height
                )
            self.image_extent = (x, y, x + width, y + height)
            self.original_width = img_width
            self.original_height = img_height

    # def __getattr__(self, name):
    #     if name in ("caching", "width", "height"):
    #         return getattr(self._canvases[0], name)
    #     raise AttributeError(name)
