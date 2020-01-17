from ipycanvas import hold_canvas
from traitlets import Bool, observe

from typing import List

from math import pi

from .utils import dist, trigger_redraw, only_inside_image
from .color_utils import hex_to_rgb, rgba_to_html_string
from ._abstract import AbstractAnnotationCanvas
from .shapes import Polygon


class PolygonAnnotationCanvas(AbstractAnnotationCanvas):

    editing = Bool(default_value=False)

    current_polygon: Polygon
    polygons: List[Polygon]

    @trigger_redraw
    @only_inside_image
    def on_click(self, x: float, y: float):

        if not self.editing:

            x, y = round(x), round(y)
            self.current_polygon.append((x, y))

            if self.current_polygon.closed:
                self.polygons.append(
                    self.current_polygon
                )  # store current poly
                # make new
                self.current_polygon = Polygon(label=self.current_class)
                self._undo_queue.append(
                    self._undo_new_polygon
                )  # allow undoing
            else:
                self._undo_queue.append(self._undo_new_point)

        elif self.editing:
            # see if the x / y is near any points
            for polygon in self.polygons + [self.current_polygon]:
                for index, point in enumerate(polygon.points):
                    if dist(point, (x, y)) < self.point_size:
                        self.dragging = lambda x, y: polygon.move_point(
                            index, (x, y)
                        )

                        def undo_move():
                            polygon.move_point(index, point)
                            self.re_draw()

                        self._undo_queue.append(undo_move)
                        return

    @trigger_redraw
    @only_inside_image
    def on_drag(self, x: float, y: float):

        x, y = int(x), int(y)
        if self.dragging is None:
            return
        else:
            self.dragging(x, y)

    @trigger_redraw
    def on_release(self, x: float, y: float):
        self.dragging = None

    @trigger_redraw
    def set_class(self, name):
        self.current_polygon.label = name

    @trigger_redraw
    def _undo_new_point(self):
        self.current_polygon.points.pop()

    @trigger_redraw
    def _undo_new_polygon(self):
        self.current_polygon = self.polygons.pop(-1)
        self.current_polygon.points.pop(-1)

    @observe("point_size", "editing")
    def re_draw(self, change=None):

        with hold_canvas(self):
            self[1].clear()
            # draw all existing polygons:
            for polygon in self.polygons:
                self.draw_polygon(polygon)
            # draw the current polygon:
            self.draw_polygon(self.current_polygon, tentative=True)

    @observe("point_size")
    def _update_polygon_closing_threshold(self, change):
        self.current_polygon.close_threshold = change.new

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
            canvas.stroke_style = rgba_to_html_string((0, 0, 0) + (1.0,))
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

        # if the polygon isn't closed, draw all points and draw the first
        # point special
        if tentative:
            canvas.fill_style = rgba_to_html_string(rgb + (1.0,))
            canvas.fill_arcs(xs, ys, self.point_size, 0, 2 * pi)
            canvas.fill_style = rgba_to_html_string((255, 180, 180) + (1.0,))
            canvas.stroke_style = rgba_to_html_string((0, 0, 0) + (1.0,))
            canvas.set_line_dash([5, 2])
            canvas.fill_arc(xs[0], ys[0], self.point_size, 0, 2 * pi)
            canvas.stroke_arc(xs[0], ys[0], self.point_size, 0, 2 * pi)

        # if the user is editing, draw all points, always:
        if not tentative and self.editing:
            canvas.fill_style = rgba_to_html_string(rgb + (1.0,))
            canvas.fill_arcs(xs, ys, self.point_size, 0, 2 * pi)

    @property
    def data(self):
        return [polygon.data for polygon in self.polygons]

    @data.setter  # type: ignore
    @trigger_redraw
    def data(self, value: List[dict]):
        self._init_empty_data()
        self.polygons = [
            Polygon.from_data(polygon_dict.copy()) for polygon_dict in value
        ]

    def _init_empty_data(self):
        self.polygons: List[Polygon] = []
        self.current_polygon: Polygon = Polygon(label=self.current_class)
