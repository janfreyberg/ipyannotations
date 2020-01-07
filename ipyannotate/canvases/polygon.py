from ipycanvas import hold_canvas

from typing import List, Tuple, Optional
from dataclasses import dataclass, field

from math import pi

from .color_utils import hex_to_rgb, rgba_to_html_string
from ._abstract import AbstractAnnotationCanvas


@dataclass
class Polygon:
    points: List[Tuple[int, int]] = field(default_factory=list)
    label: Optional[str] = None
    close_threshold: int = 5

    closed = False

    def append(self, point: Tuple[int, int]):
        # if self.closed:
        #     raise ValueError("Can't append to a closed polygon.")
        # else:
        self.points.append(point)
        if self.is_closed():
            self.points.pop(-1)
            self.closed = True

    @property
    def xy_lists(self):
        if len(self.points) == 0:
            return [], []
        return map(list, zip(*self.points))

    def is_closed(self) -> bool:

        if len(self) < 3:
            return False

        x_start, y_start = self.points[0]
        x_end, y_end = self.points[-1]

        distance = ((x_end - x_start) ** 2 + (y_end - y_start) ** 2) ** 0.5

        return distance < self.close_threshold

    def __len__(self) -> int:
        return len(self.points)

    @property
    def data(self):
        return {"type": "polygon", "label": self.label, "points": self.points}


class PolygonAnnotationCanvas(AbstractAnnotationCanvas):
    def __init__(self, size, classes=None):

        super().__init__(size=size, classes=classes)
        self.polygons: List[Polygon] = []
        self.current_polygon: Polygon = Polygon(label=self.current_class)

    def add_point(self, x: float, y: float):

        if not self.image_extent[0] <= x <= self.image_extent[2]:
            return
        if not self.image_extent[1] <= y <= self.image_extent[3]:
            return

        self.current_polygon.append((int(x), int(y)))

        if self.current_polygon.closed:
            self.polygons.append(self.current_polygon)  # store current poly
            # make new
            self.current_polygon = Polygon(label=self.current_class)
            self._undo_queue.append(self._undo_new_polygon)  # allow undoing
        else:
            self._undo_queue.append(self._undo_new_point)

    def set_class(self, name):
        self.current_polygon.label = name

    def _undo_new_point(self):
        self.current_polygon.points.pop()
        self.re_draw()

    def _undo_new_polygon(self):
        self.current_polygon = self.polygons.pop()
        self.re_draw()

    def re_draw(self):

        with hold_canvas(self):
            self[1].clear()
            # draw all existing polygons:
            for polygon in self.polygons:
                self.draw_polygon(polygon)
            # draw the current polygon:
            self.draw_polygon(self.current_polygon, tentative=True)

    def draw_polygon(self, polygon, tentative=False):

        color = self.colormap.get(polygon.label, "#000000")
        canvas = self[1]
        if len(polygon) == 0:
            return
        rgb = hex_to_rgb(color)
        xs, ys = polygon.xy_lists
        canvas.stroke_style = rgba_to_html_string(rgb + (1.0,))

        if tentative:
            canvas.set_line_dash([10, 5])
            canvas.fill_style = rgba_to_html_string(rgb + (self.opacity,))
        else:
            canvas.set_line_dash([])
            canvas.fill_style = rgba_to_html_string(rgb + (self.opacity,))

        canvas.begin_path()
        current_point = polygon.points[0]
        canvas.move_to(*current_point)
        for next_point in polygon.points[1:]:
            canvas.line_to(*next_point)
            current_point = next_point
        if len(polygon) > 2:
            canvas.close_path()
        canvas.stroke()
        canvas.fill()

        if tentative:
            canvas.fill_style = rgba_to_html_string(rgb + (1.0,))
            canvas.fill_arcs(xs, ys, self.point_size, 0, 2 * pi)
            canvas.fill_style = rgba_to_html_string((255, 180, 180) + (1.0,))
            canvas.stroke_style = rgba_to_html_string((0, 0, 0) + (1.0,))
            canvas.set_line_dash([5, 2])
            canvas.fill_arc(xs[0], ys[0], self.point_size, 0, 2 * pi)
            canvas.stroke_arc(xs[0], ys[0], self.point_size, 0, 2 * pi)

    @property
    def data(self):
        return [polygon.data for polygon in self.polygons]
