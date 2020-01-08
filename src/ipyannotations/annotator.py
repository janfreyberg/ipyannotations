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
            description="Brightness", value=1, min=-1, max=1, step=0.01
        )
        widgets.link(
            (self.brightness_slider, "value"),
            (self.canvas, "image_brightness"),
        )
        viz_controls.append(self.brightness_slider)
        self.contrast_slider = widgets.FloatLogSlider(
            description="Contrast", value=1, min=-1, max=1, step=0.01
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

        super().__init__()
        self.children = (widgets.VBox((self.canvas, self.all_controls)),)

    def on_submit(self, callback):
        self.submit_callbacks.append(callback)

    def submit(self, button):
        for callback in self.submit_callbacks:
            callback(self.canvas.data)

    def on_undo(self, callback):
        self.undo_callbacks.append(callback)

    def undo(self, button):
        if self.canvas._undo_queue:
            undo = self.canvas._undo_queue.pop()
            undo()
        else:
            for callback in self.undo_callbacks:
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
