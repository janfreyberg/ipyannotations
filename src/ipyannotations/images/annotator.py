import pathlib
from typing import List, Callable, Any, Optional, Union, Type, Sequence
import traitlets
import ipywidgets as widgets

from .canvases._abstract import AbstractAnnotationCanvas
from .canvases.polygon import PolygonAnnotationCanvas
from .canvases.point import PointAnnotationCanvas
from .canvases.box import BoundingBoxAnnotationCanvas


class Annotator(widgets.VBox):
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
        # **kwargs,
    ):
        """Create an annotation widget for images."""
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

        self.undo_button = widgets.Button(
            description="Undo", icon="undo", layout=button_layout
        )
        self.undo_button.on_click(self.undo)
        extra_buttons.append(self.undo_button)

        self.skip_button = widgets.Button(
            description="Skip", icon="fast-forward", layout=button_layout
        )
        self.skip_button.on_click(self.skip)
        extra_buttons.append(self.skip_button)

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

        self.submit_button = widgets.Button(
            description="Submit data",
            icon="tick",
            button_style="success",
            layout=button_layout,
        )
        self.submit_button.on_click(self.submit)

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
                description="Opacity", value=1, min=0, max=1, step=0.025
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

        super().__init__()
        self.children = [self.canvas, self.all_controls]

    def display(self, image: Union[widgets.Image, pathlib.Path]):
        """Clear the annotations and display an image


        Parameters
        ----------
        image : widgets.Image, pathlib.Path, np.ndarray
            The image, or the path to the image.
        """
        self.canvas.clear()
        self.canvas.load_image(image)

    def on_submit(self, callback: Callable[[Any], None]):
        """Register a callback to handle data when the user clicks "Submit".

        .. note::
            Callbacks are called in order of registration - first registered,
            first called.

        Parameters
        ----------
        callback : Callable[[Any], None]
            A function that takes in data. Usually, this data is a list of
            dictionaries, but you are able to define data post-processors when
            you create an annotator that get called before this callback is
            called. Any return values are ignored.
        """
        self.submit_callbacks.append(callback)

    def submit(self, button: Optional[Any] = None):
        """Trigger the "Submit" callbacks.

        This function is called when users click "Submit".

        Parameters
        ----------
        button : optional
            Ignored argument. Supplied when invoked due to a button click.
        """
        for callback in self.submit_callbacks:
            callback(self.data)

    def on_undo(self, callback: Callable[[], None]):
        """Register a callback to handle when the user clicks "Undo".

        Note that any callback registered here is only called when the canvas
        is empty - while there are annotations on the canvas, "Undo" actually
        undoes the annotations, until the canvas is empty.

        Parameters
        ----------
        callback : Callable[[], None]
            A function to be called when users press "Undo". This should be
            a function that takes in no arguments; any return values are
            ignored.
        """
        self.undo_callbacks.append(callback)

    def undo(self, button: Optional[Any] = None):
        """Trigger the "Undo" callbacks.

        This function is called when users click "Undo".

        Parameters
        ----------
        button : optional
            Ignored argument. Supplied when invoked due to a button click.
        """
        if self.canvas._undo_queue:
            undo = self.canvas._undo_queue.pop()
            undo()
        else:
            for callback in self.undo_callbacks:
                callback()

    def on_skip(self, callback: Callable[[], None]):
        """Register a callback to handle when the user clicks "Skip".

        Parameters
        ----------
        callback : Callable[[], None]
            The function to be called when the user clicks "Skip". It should
            take no arguments, and any return values are ignored.
        """
        self.skip_callbacks.append(callback)

    def skip(self, button: Optional[Any] = None):
        """Trigger the "Skip" callbacks.

        This function is called when users click "Skip".

        Parameters
        ----------
        button : optional
            Ignored argument. Supplied when invoked due to a button click.
        """
        for callback in self.skip_callbacks:
            callback()

    @property
    def data(self):
        """The annotation data."""
        if self.data_postprocessor is not None:
            return self.data_postprocessor(self.canvas.data)
        else:
            return self.canvas.data


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
    def data(self, value):
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
    def data(self, value):
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
    def data(self, value):
        self.canvas.data = value
