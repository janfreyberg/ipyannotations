from ipycanvas import hold_canvas
from traitlets import Bool

from typing import List, Tuple, Optional
from dataclasses import dataclass

from math import pi

from .utils import dist, trigger_redraw, only_inside_image
from .color_utils import hex_to_rgb, rgba_to_html_string
from ._abstract import AbstractAnnotationCanvas


@dataclass
class Point:
    coordinates: Tuple[int, int]
    label: Optional[str] = None

    def __post_init__(self):
        self.coordinates = tuple(map(round, self.coordinates))

    def move(self, coordinates: Tuple[int, int]):
        self.coordinates = (round(coordinates[0]), round(coordinates[1]))

    @property
    def data(self):
        return {
            "type": "point",
            "label": self.label,
            "coordinates": (self.x, self.y),
        }


class PointAnnotationCanvas(AbstractAnnotationCanvas):

    editing = Bool(default_value=False)

    def __init__(self, size, classes=None):

        super().__init__(size=size, classes=classes)
        self.points: List[Point] = []
        self.dragging = None

    @trigger_redraw
    @only_inside_image
    def on_click(self, x: float, y: float):

        if not self.editing:
            self.points.append(
                Point((round(x), round(y)), label=self.current_class)
            )
            self._undo_queue.append(self._undo_new_point)
        elif self.editing:
            for point in self.points:
                if dist((x, y), point.coordinates) < self.point_size:
                    self.dragging = point.move
                    old_coordinates = point.coordinates

                    def undo_move():
                        point.move(old_coordinates)
                        self.re_draw()

                    self._undo_queue.append(undo_move)

                    return

    @trigger_redraw
    @only_inside_image
    def on_drag(self, x: float, y: float):

        if self.dragging is None:
            return
        else:
            self.dragging((x, y))

    @trigger_redraw
    def on_release(self, x: float, y: float):
        if self.dragging is None:
            return
        self.dragging((x, y))
        self.dragging = None

    @trigger_redraw
    def _undo_new_point(self):
        self.points.pop()

    def re_draw(self):

        with hold_canvas(self):
            canvas = self[1]
            canvas.clear()
            # draw all existing polygons:
            for point in self.points:
                self.draw_point(point)

    def draw_point(self, point):
        canvas = self[1]
        color = self.colormap.get(point.label, "#000000")
        rgba = hex_to_rgb(color) + (self.opacity,)
        # canvas.stroke_style = rgba_to_html_string(rgba)
        canvas.fill_style = rgba_to_html_string(rgba)
        canvas.fill_arc(*point.coordinates, self.point_size, 0, 2 * pi)

    @property
    def data(self):
        return [point.data for point in self.points]