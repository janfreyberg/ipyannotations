from math import pi
from typing import List, Optional

import ipywidgets as widgets
from ipycanvas import hold_canvas
from traitlets import Bool, observe

from .abstract_canvas import AbstractAnnotationCanvas
from .color_utils import hex_to_rgb, rgba_to_html_string
from .image_utils import dist, only_inside_image, trigger_redraw
from .shapes import BoundingBox


class BoundingBoxAnnotationCanvas(AbstractAnnotationCanvas):

    editing = Bool(default_value=False)
    annotations: List[BoundingBox]
    _proposed_annotation: Optional[BoundingBox] = None

    debug_output = widgets.Output()

    @observe("point_size", "editing")
    def re_draw(self, _=None):  # noqa: D001

        with hold_canvas(self):
            self.annotation_canvas.clear()
            # draw all existing polygons:
            for annotation in self.annotations:
                self.draw_box(annotation)
            # draw the current box:
            if self._proposed_annotation is not None:
                self.draw_box(self._proposed_annotation, proposed=True)

    def draw_box(self, box: BoundingBox, proposed: bool = False):
        """Draw a box onto the canvas.

        Parameters
        ----------
        box : BoundingBox
            The box to draw.
        proposed : bool, optional
            Whether this box is a proposal, by default False
        """

        color = self.colormap.get(box.label, "#000000")
        canvas = self[1]
        rgb = hex_to_rgb(color)

        canvas.line_width = 3
        canvas.stroke_style = rgba_to_html_string(rgb + (1.0,))
        canvas.set_line_dash([10, 5] if proposed else [])
        canvas.fill_style = rgba_to_html_string(rgb + (self.opacity,))
        corners = [
            self.image_to_canvas_coordinates(corner) for corner in box.corners
        ]
        canvas.begin_path()
        canvas.move_to(*corners[0])
        for corner in corners[1:]:
            canvas.line_to(*corner)
        canvas.close_path()
        canvas.stroke()

        x0, y0, x1, y1 = box.xyxy
        x0, y0 = self.image_to_canvas_coordinates((x0, y0))
        x1, y1 = self.image_to_canvas_coordinates((x1, y1))
        if self.editing:
            canvas.fill_style = rgba_to_html_string(rgb + (1.0,))
            canvas.fill_arcs(
                [x0, x0, x1, x1], [y0, y1, y0, y1], self.point_size, 0, 2 * pi
            )

    @trigger_redraw
    @only_inside_image
    def on_click(self, x: float, y: float):
        """Handle a click.

        This function either starts a new proposed box and sets the
        dragging functionality, or in editing mode sets dragging one of
        the corners.

        Parameters
        ----------
        x : float
            The x coordinate, relative to the image.
        y : float
            The y coordinate, relative to the image.
        """

        if not self.editing:
            x, y = int(x), int(y)
            self._proposed_annotation = BoundingBox(
                (x, y, x, y), label=self.current_class
            )

            def drag_func(x, y):
                if self._proposed_annotation is not None:
                    self._proposed_annotation.move_corner(2, x, y)

            self.dragging = drag_func

        elif self.editing:
            # see if the x / y is near any points
            for box in self.annotations:
                for index, point in enumerate(box.corners):
                    if dist(point, (x, y)) < self.point_size:
                        self.dragging = lambda x, y: box.move_corner(
                            index, x, y
                        )

                        def undo_move():
                            box.move_corner(index, *point)
                            self.re_draw()

                        self._undo_queue.append(undo_move)
                        return

    @trigger_redraw
    @only_inside_image
    def on_drag(self, x: float, y: float):
        """Handle a dragging action.

        Parameters
        ----------
        x : float
            The new x coordinate, relative to the image.
        y : float
            The new y coordinate, relative to the image.
        """

        if self.dragging is None:
            return
        else:
            self.dragging(int(x), int(y))

    @trigger_redraw
    def on_release(self, x: float, y: float):
        """Handle a mouse release.

        This function will re-set the dragging handler, and append a new
        box to the annotation data if required.

        Parameters
        ----------
        x : float
        y : float
        """

        self.dragging = None
        if self._proposed_annotation is not None:
            x0, y0, x1, y1 = self._proposed_annotation.xyxy

            if not (x0 == x1 and y0 == y1):
                self.annotations.append(self._proposed_annotation)
                self._undo_queue.append(self._undo_new_box)

            self._proposed_annotation = None

    @trigger_redraw
    def _undo_new_box(self):
        self.annotations.pop()

    def init_empty_data(self):
        self.annotations: List[BoundingBox] = []
        self._undo_queue.clear()

    @property
    def data(self):
        """
        The annotation data, as List[ Dict ].

        The format is a list of dictionaries, with the following key / value
        combinations:

        +------------------+-------------------------------+
        |``'type'``        | ``'box'``                     |
        +------------------+-------------------------------+
        |``'label'``       | ``<class label>``             |
        +------------------+-------------------------------+
        |``'xyxy'``        | ``<tuple of x0, y0, x1, y1>`` |
        +------------------+-------------------------------+
        """

        return [annotation.data for annotation in self.annotations]

    @data.setter  # type: ignore
    @trigger_redraw
    def data(self, value: List[dict]):
        """Set the annotation data on this canvas.

        Parameters
        ----------
        value : List[dict]
            List of dictionaries, with keys `type`, `label`, and `xyxy`.
        """
        self.init_empty_data()
        self.annotations = [
            BoundingBox.from_data(annotation.copy()) for annotation in value
        ]
