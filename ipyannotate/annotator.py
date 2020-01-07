from typing import List, Callable, Any

import ipywidgets as widgets

from .canvases.polygon import PolygonAnnotationCanvas


class PolygonAnnotator(widgets.VBox):
    # TODO: add buttons and in-sync traitlets to class
    def __init__(self, canvas_size=(500, 500), classes=None):

        self.canvas = PolygonAnnotationCanvas(
            size=canvas_size, classes=classes
        )

        if classes is not None:
            self.class_selector = widgets.Dropdown(
                description="Class:", options=classes
            )
            widgets.link(
                (self.class_selector, "value"), (self.canvas, "current_class")
            )
        else:
            self.class_selector = widgets.Widget()

        self.undo_button = widgets.Button(description="Undo", icon="undo")
        self.undo_button.on_click(self.undo)

        self.submit_button = widgets.Button(
            description="Submit data", icon="tick", button_style="success"
        )
        self.submit_button.on_click(self.submit)

        self.opacity_slider = widgets.FloatSlider(
            value=0.4, min=0, max=1, step=0.025
        )
        widgets.link((self.opacity_slider, "value"), (self.canvas, "opacity"))

        self.edit_button = widgets.ToggleButton(
            description="Adjust", icon="pencil"
        )

        self.control_box = widgets.HBox(
            children=(self.class_selector, self.edit_button, self.undo_button)
        )

        self.submit_callbacks: List[Callable[[Any]]] = []
        self.undo_callbacks: List[Callable[[]]] = []

        super().__init__(
            children=(
                self.canvas,
                self.control_box,
                self.opacity_slider,
                self.submit_button,
            )
        )

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
        return self.canvas.data
