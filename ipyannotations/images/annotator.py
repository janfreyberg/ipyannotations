import pathlib
from typing import Any, Callable, List, Optional, Sequence, Type, Union

import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from .canvases.abstract_canvas import AbstractAnnotationCanvas
from .canvases.box import BoundingBoxAnnotationCanvas
from .canvases.point import PointAnnotationCanvas
from .canvases.polygon import PolygonAnnotationCanvas


class Annotator(LabellingWidgetMixin, widgets.VBox):
    """A generic image annotation widget.

    Parameters
    ----------
    canvas : AbstractAnnotationCanvas
        An annotation canvas that implements displaying & annotating
        images.
    options : List[str], optional
        The list of classes you'd like to annotate.
    data_postprocessor : Optional[Callable[[List[dict]], Any]], optional
        A function that transforms the annotation data. By default None.
    """

    options = traitlets.List(
        list(), allow_none=False, help="The possible classes"
    )
    options.__doc__ = """The possible classes"""

    CanvasClass: Type[AbstractAnnotationCanvas]

    def __init__(
        self,
        canvas_size=(700, 500),
        options: Sequence[str] = (),
        data_postprocessor: Optional[Callable[[List[dict]], Any]] = None,
        **kwargs,
    ):
        """Create an annotation widget for images.

        Parameters
        ----------
        canvas_size : tuple, optional, by default (700, 500)
        options : Sequence[str], optional
            The classes to be annotated, by default ()
        data_postprocessor : Optional[Callable[[List[dict]], Any]], optional
            A function to post-process the data, by default None.
        """
        layout = {"width": f"{canvas_size[0]}px"}
        layout.update(kwargs.pop("layout", {}))
        super().__init__(layout=layout)
        self.canvas = self.CanvasClass(canvas_size, classes=options)
        self.data_postprocessor = data_postprocessor

        # controls for the data entry:
        data_controls = []
        self.options = options

        self.class_selector = widgets.Dropdown(
            description="Class:",
            options=options,
            layout=widgets.Layout(flex="1 1 auto"),
        )
        widgets.link((self, "options"), (self.class_selector, "options"))
        widgets.link(
            (self.class_selector, "value"), (self.canvas, "current_class")
        )
        data_controls.append(self.class_selector)

        extra_buttons = []
        button_layout = widgets.Layout(
            # width="auto",
            min_width="80px",
            flex="1 1 auto",
            max_width="120px",
        )

        extra_buttons = [self.undo_button, self.skip_button]
        if hasattr(self.canvas, "editing"):
            self.edit_button = widgets.ToggleButton(
                description="Edit", icon="pencil", layout=button_layout
            )
            widgets.link((self.edit_button, "value"), (self.canvas, "editing"))
            extra_buttons.append(self.edit_button)

        extra_buttons = widgets.HBox(
            extra_buttons,
            layout={
                "align_items": "stretch",
                "justify_content": "flex-end",
                "flex_flow": "row wrap",
            },
        )

        self.data_controls = widgets.VBox(
            children=(
                widgets.HTML("Data input settings"),
                widgets.HBox(
                    (self.class_selector,),
                    layout={
                        "align_items": "stretch",
                        "justify_content": "flex-end",
                    },
                ),
                extra_buttons,
                widgets.HBox(
                    (self.submit_button,),
                    layout={"justify_content": "flex-end"},
                ),
            ),
            layout={"flex": "1 1 auto", "max_width": "600px"},
        )

        # controls for the visualisation of the data:
        viz_controls = []
        if hasattr(self.canvas, "opacity"):
            self.opacity_slider = widgets.FloatSlider(
                description="Opacity", value=0.5, min=0, max=1, step=0.025
            )
            widgets.link(
                (self.opacity_slider, "value"), (self.canvas, "opacity")
            )
            viz_controls.append(self.opacity_slider)
        if hasattr(self.canvas, "point_size"):
            self.point_size_slider = widgets.IntSlider(
                description="Point size", value=5, min=1, max=20, step=1
            )
            widgets.link(
                (self.point_size_slider, "value"), (self.canvas, "point_size")
            )
            viz_controls.append(self.point_size_slider)
        self.brightness_slider = widgets.FloatLogSlider(
            description="Brightness", value=1, min=-1, max=1, step=0.0001
        )
        widgets.link(
            (self.brightness_slider, "value"),
            (self.canvas, "image_brightness"),
        )
        viz_controls.append(self.brightness_slider)
        self.contrast_slider = widgets.FloatLogSlider(
            description="Contrast", value=1, min=-1, max=1, step=0.0001
        )
        widgets.link(
            (self.contrast_slider, "value"), (self.canvas, "image_contrast")
        )
        viz_controls.append(self.contrast_slider)

        self.visualisation_controls = widgets.VBox(
            children=(widgets.HTML("Visualisation settings"), *viz_controls),
            layout={"flex": "1 1 auto"},
        )

        self.all_controls = widgets.HBox(
            children=(self.visualisation_controls, self.data_controls),
            layout={
                "width": f"{self.canvas.size[0]}px",
                "justify_content": "space-between",
            },
        )

        self.submit_callbacks: List[Callable[[Any], None]] = []
        self.undo_callbacks: List[Callable[[], None]] = []
        self.skip_callbacks: List[Callable[[], None]] = []
        self.children = self.children + (
            self.canvas,
            self.all_controls,
            self.canvas.error_output_widget,
        )

    def display(self, image: Union[widgets.Image, pathlib.Path]):
        """Clear the annotations and display an image


        Parameters
        ----------
        image : widgets.Image, pathlib.Path, np.ndarray
            The image, or the path to the image.
        """
        self.canvas.clear()
        self.canvas.load_image(image)

    @property
    def data(self):
        """The annotation data."""
        if self.data_postprocessor is not None:
            return self.data_postprocessor(self.canvas.data)
        else:
            return self.canvas.data

    def undo(self, _: Optional[Any] = None):  # noqa: D001
        if self.canvas._undo_queue:
            undo = self.canvas._undo_queue.pop()
            undo()
        else:
            super().undo()

    def _handle_keystroke(self, event):
        super()._handle_keystroke(event)
        for i, option in enumerate(self.class_selector.options):
            if event["key"] == f"{(i + 1) % 10}":
                self.class_selector.value = option
            if i == 10:
                break


class PolygonAnnotator(Annotator):
    """An annotator for drawing polygons on an image.

    To draw a polygon, click anywhere you'd like to start. Continue to click
    along the edge of the polygon until arrive back where you started. To
    finish, simply click the first point (highlighted in red). It may be
    helpful to increase the point size if you're struggling (using the slider).

    You can change the class of a polygon using the dropdown menu while the
    polygon is still "open", or unfinished. If you make a mistake, use the Undo
    button until the point that's wrong has disappeared.

    You can move, but not add / subtract polygon points, by clicking the "Edit"
    button. Simply drag a point you want to adjust. Again, if you have
    difficulty aiming at the points, you can increase the point size.

    You can increase or decrease the contrast and brightness  of the image
    using the sliders to make it easier to annotate. Sometimes you need to see
    what's behind already-created annotations, and for this purpose you can
    make them more see-through using the "Opacity" slider.

    Parameters
    ----------
    canvas_size : (int, int), optional
        Size of the annotation canvas in pixels.
    classes : List[str], optional
        The list of classes you want to create annotations for, by default
        None.
    """

    CanvasClass = PolygonAnnotationCanvas

    @property
    def data(self):
        """
        The annotation data, as List[ Dict ].

        The format is a list of dictionaries, with the following key / value
        combinations:

        +------------------+-------------------------+
        |``'type'``        | ``'polygon'``           |
        +------------------+-------------------------+
        |``'label'``       | ``<class label>``       |
        +------------------+-------------------------+
        |``'points'``      | ``<list of xy-tuples>`` |
        +------------------+-------------------------+
        """
        return super().data

    @data.setter
    def data(self, value):  # noqa: D001
        self.canvas.data = value


class PointAnnotator(Annotator):
    """An annotator for drawing points on an image.

    To add a point, select the class using the dropdown menu, and click
    anywhere on the image. You can undo adding points, and you can adjust the
    point's position using the "Edit" button. To make this easier, you may
    want to adjust the point size using the appropriate slider.

    You can increase or decrease the contrast and brightness  of the image
    using the sliders to make it easier to annotate. Sometimes you need to see
    what's behind already-created annotations, and for this purpose you can
    make them more see-through using the "Opacity" slider.

    Parameters
    ----------
    canvas_size : (int, int), optional
        Size of the annotation canvas in pixels.
    classes : List[str], optional
        The list of classes you want to create annotations for, by default
        None.
    """

    CanvasClass = PointAnnotationCanvas

    @property
    def data(self):
        """
        The annotation data, as List[ Dict ].

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
        return super().data

    @data.setter
    def data(self, value):  # noqa: D001
        self.canvas.data = value


class BoxAnnotator(Annotator):
    """An annotator for drawing boxes on an image.

    To add a box, simply click on one of the corners, and drag the mouse to
    the corner opposite. The box will grow as you drag your mouse. To adjust
    the box after, you can click the "Edit" button and drag any of the corners
    to where you want them.

    You can increase or decrease the contrast and brightness  of the image
    using the sliders to make it easier to annotate. Sometimes you need to see
    what's behind already-created annotations, and for this purpose you can
    make them more see-through using the "Opacity" slider.

    Parameters
    ----------
    canvas_size : (int, int), optional
        Size of the annotation canvas in pixels.
    classes : List[str], optional
        The list of classes you want to create annotations for, by default
        None.
    """

    CanvasClass = BoundingBoxAnnotationCanvas

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
        return super().data

    @data.setter
    def data(self, value):  # noqa: D001
        self.canvas.data = value
