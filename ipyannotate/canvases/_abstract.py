from ipycanvas import MultiCanvas
import ipywidgets as widgets
from typing import Tuple, Optional, Sequence
from collections import deque, defaultdict
import abc
from traitlets import Unicode, observe

from .utils import set_colors, fit_image


class AbstractAnnotationCanvas(MultiCanvas):

    current_class = Unicode()

    def __init__(
        self, size: Tuple[int, int], classes: Optional[Sequence[str]] = None
    ):
        super().__init__(n_canvases=3, size=size)
        self.point_size = 5
        self._undo_queue = deque([])
        self.image_extent = (0, 0, *size)

        self.image_canvas = self[0]
        self.annotation_canvas = self[1]
        self.interaction_canvas = self[2]

        self.interaction_canvas.on_mouse_down(self._on_click)

        if classes is not None:
            self.colormap = {
                cls_: col for cls_, col in zip(classes, set_colors())
            }
        else:
            self.colormap = defaultdict(lambda: "#000000")

    def load_image(self, image: widgets.Image):
        image_canvas = self[0]
        x, y, width, height = fit_image(image, image_canvas)
        image_canvas.draw_image(image, x=x, y=y, width=width, height=height)
        self.image_extent = (x, y, x + width, y + height)

    @observe("current_class")
    def _set_class(self, change):
        self.set_class(change["new"])
        self.re_draw()

    @abc.abstractmethod
    def re_draw(self):
        pass

    def _on_click(self, x: float, y: float):
        self.add_point(x, y)
        self.re_draw()

    @abc.abstractmethod
    def add_point(self, x: float, y: float):
        pass

    @abc.abstractmethod
    def set_class(self, class_name: str):
        pass
