from typing import List, Callable, Any, Optional

import ipywidgets as widgets

from .canvases._abstract import AbstractAnnotationCanvas
from .canvases.polygon import PolygonAnnotationCanvas
from .canvases.point import PointAnnotationCanvas


class Annotator(widgets.Box):
    def __init__(
        self,
        canvas: AbstractAnnotationCanvas,
        classes: List[str],
        data_postprocessor: Optional[Callable[[List[dict]], Any]] = None,
    ):
        self.canvas = canvas
        self.data_postprocessor = data_postprocessor

        # controls for the data entry:
        data_controls = []
        if classes is not None:
            self.class_selector = widgets.Dropdown(
                description="Class:",
                options=classes,
                layout=widgets.Layout(flex="1 1 auto"),
            )
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
                "width": f"{canvas.size[0]}px",
                "justify_content": "space-between",
            },
        )

        self.submit_callbacks: List[Callable[[Any], None]] = []
        self.undo_callbacks: List[Callable[[], None]] = []
        self.skip_callbacks: List[Callable[[], None]] = []

        super().__init__()
        self.children = (widgets.VBox((self.canvas, self.all_controls)),)

    def on_submit(self, callback: Callable[[Any], None]):
        """Register a callback to handle data when the user clicks "Submit".

        Parameters
        ----------
        callback : Callable[[Any], None]
            A function that takes in data. Usually, this data is a list of
            dictionaries, but you are able to define data post-processors when
            you create an annotator that get called before this callback is
            called. Any return values are ignored.
        """
        self.submit_callbacks.append(callback)

    def submit(self, button):
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

    def undo(self, button):
        if self.canvas._undo_queue:
            undo = self.canvas._undo_queue.pop()
            undo()
        else:
            for callback in self.undo_callbacks:
                callback()

    def on_skip(self, callback: Callable[[], None]):
        """Register a callback to handle when the user clicks "Skip".

        .. note::
            Callbacks are called in order of registration - first registered,
            first called.

        Parameters
        ----------
        callback : Callable[[], None]
            The function to be called when the user clicks "Skip". It should
            take no arguments, and any return values are ignored.
        """
        self.skip_callbacks.append(callback)

    def skip(self, button):
        for callback in self.skip_callbacks:
            callback()

    @property
    def data(self):
        if self.data_postprocessor is not None:
            return self.data_postprocessor(self.canvas.data)
        else:
            return self.canvas.data


class PolygonAnnotator(Annotator):
    def __init__(self, canvas_size=(500, 500), classes=None):

        canvas = PolygonAnnotationCanvas(size=canvas_size, classes=classes)

        super().__init__(canvas, classes)


class PointAnnotator(Annotator):
    def __init__(self, canvas_size=(500, 500), classes=None):

        canvas = PointAnnotationCanvas(size=canvas_size, classes=classes)

        super().__init__(canvas, classes)
