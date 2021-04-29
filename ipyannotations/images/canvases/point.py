from math import pi
from typing import List

from ipycanvas import hold_canvas
from traitlets import Bool

from .abstract_canvas import AbstractAnnotationCanvas
from .color_utils import hex_to_rgb, rgba_to_html_string
from .image_utils import dist, only_inside_image, trigger_redraw
from .shapes import Point


class PointAnnotationCanvas(AbstractAnnotationCanvas):

    editing = Bool(default_value=False)

    @trigger_redraw
    @only_inside_image
    def on_click(self, x: float, y: float):
        """Handle a click.

        This either adds a point to the canvas, or, if in editing mode, enables
        dragging.

        Parameters
        ----------
        x : float
            The x coordinate, a number relative to the image itself,
            in pixels
        y : float
            The y coordinate, a number relative to the image itself,
            in pixels
        """

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
                        point.move(*old_coordinates)
                        self.re_draw()

                    self._undo_queue.append(undo_move)

                    return

    @trigger_redraw
    @only_inside_image
    def on_drag(self, x: float, y: float):
        """Handle dragging by moving a point.

        Parameters
        ----------
        x : float
            The x coordinate, a number relative to the image itself,
            in pixels
        y : float
            The y coordinate, a number relative to the image itself,
            in pixels
        """

        if self.dragging is None:
            return
        else:
            self.dragging(int(x), int(y))

    @trigger_redraw
    def on_release(self, x: float, y: float):
        """Handle mouse button release by disabling dragging.

        Parameters
        ----------
        x : float
            The x coordinate, a number relative to the image itself,
            in pixels
        y : float
            The y coordinate, a number relative to the image itself,
            in pixels
        """

        self.dragging = None

    @trigger_redraw
    def _undo_new_point(self):
        self.points.pop()

    def re_draw(self):
        """Re-draw the data onto the canvas."""

        with hold_canvas(self):
            canvas = self[1]
            canvas.clear()
            # draw all existing polygons:
            for point in self.points:
                self.draw_point(point)

    def draw_point(self, point: Point):
        """Draw a point.

        Parameters
        ----------
        point : Point
        """

        coordinates = self.image_to_canvas_coordinates(point.coordinates)
        canvas = self[1]
        color = self.colormap.get(point.label, "#000000")
        rgba = hex_to_rgb(color) + (self.opacity,)
        # canvas.stroke_style = rgba_to_html_string(rgba)
        canvas.fill_style = rgba_to_html_string(rgba)
        canvas.stroke_style = rgba_to_html_string((0, 0, 0, 1.0))
        canvas.fill_arc(*coordinates, self.point_size, 0, 2 * pi)
        canvas.stroke_arc(*coordinates, self.point_size, 0, 2 * pi)

    @property
    def data(self):
        """The annotation data, as List[ Dict ].

        The format is a list of dictionaries, with the following key / value
        combinations:

        +------------------+-------------------------+
        |``'type'``        | ``'point'``             |
        +------------------+-------------------------+
        |``'label'``       | ``<class label>``       |
        +------------------+-------------------------+
        |``'coordinates'`` | ``<xy-tuple>``          |
        +------------------+-------------------------+
        """

        return [point.data for point in self.points]

    @data.setter  # type: ignore
    @trigger_redraw
    def data(self, value: List[dict]):
        """Assign annotation data.

        Parameters
        ----------
        value : List[dict]
            The data value, with keys `type`, `label`, and `coordinates`.
        """
        self.points = [
            Point.from_data(point_dict.copy()) for point_dict in value
        ]

    def init_empty_data(self):
        self.points: List[Point] = []
