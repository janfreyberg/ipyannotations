from typing import Callable, List, Tuple
from copy import copy
import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin


@widgets.register
class TextTaggerCore(widgets.DOMWidget):
    """An example widget."""

    # properties to make sure the right frontend widget is found:
    _view_name = traitlets.Unicode("TextTaggerView").tag(sync=True)
    _model_name = traitlets.Unicode("TextTaggerModel").tag(sync=True)
    _view_module = traitlets.Unicode("ipyannotations").tag(sync=True)
    _model_module = traitlets.Unicode("ipyannotations").tag(sync=True)
    _view_module_version = traitlets.Unicode("^0.1.0").tag(sync=True)
    _model_module_version = traitlets.Unicode("^0.1.0").tag(sync=True)

    text = traitlets.Unicode("Lorem ipsum", help="The text to display.").tag(
        sync=True
    )
    classes = traitlets.List(
        trait=traitlets.Unicode, default_value=["MISC", "PER", "LOC", "ORG"]
    ).tag(sync=True)
    selected_class = traitlets.Unicode().tag(sync=True)
    entity_spans = traitlets.List(
        trait=traitlets.Tuple(
            traitlets.Int(), traitlets.Int(), traitlets.Unicode()
        )
    ).tag(sync=True)
    palette = traitlets.List(
        trait=traitlets.Unicode(),
        default_value=[
            "#8dd3c7",
            "#ffffb3",
            "#bebada",
            "#fb8072",
            "#80b1d3",
            "#fdb462",
            "#b3de69",
            "#fccde5",
            "#d9d9d9",
            "#bc80bd",
            "#ccebc5",
            "#ffed6f",
        ],
    ).tag(sync=True)

    def __init__(
        self,
        text="Lorem ipsum",
        classes=["MISC", "PER", "LOC", "ORG"],
        entity_spans=[],
        **kwargs,
    ):
        super().__init__(
            text=text, classes=classes, entity_spans=entity_spans, **kwargs
        )
        if not self.selected_class:
            self.selected_class = self.classes[0]


class TextTagger(LabellingWidgetMixin, widgets.VBox):
    """A tagging widget."""

    data: List[Tuple[int, int, str]] = traitlets.List(
        trait=traitlets.Tuple(
            traitlets.Int(), traitlets.Int(), traitlets.Unicode()
        )
    )

    def __init__(
        self,
        classes=["MISC", "PER", "LOC", "ORG"],
        text="Lorem ipsum",
        data=[],
        button_width="5em",
    ):
        super().__init__()
        self.text_widget = TextTaggerCore(
            text=text, classes=classes, entity_spans=data
        )
        self.class_picker = widgets.ToggleButtons(
            options=classes,
            description="Class to tag:",
            style=widgets.ToggleButtonsStyle(button_width=button_width),
        )
        widgets.link(
            (self.class_picker, "value"), (self.text_widget, "selected_class")
        )
        widgets.link((self, "data"), (self.text_widget, "entity_spans"))
        self.children = (self.text_widget, self.class_picker)

        self._undo_queue = []

        self.children = (
            self.text_widget,
            self.class_picker,
            widgets.HBox(
                [self.undo_button, self.skip_button],
                layout={
                    "align_items": "stretch",
                    "justify_content": "flex-end",
                    "flex_flow": "row wrap",
                },
            ),
        )

    def undo(self, *_):
        if self._undo_queue:
            last_undo_fn = self._undo_queue.pop()
            last_undo_fn()
        else:
            super().undo()

    @traitlets.observe("data")
    def _append_undo_fn(self, proposal: dict):
        old_data = proposal["old"]
        new_data = proposal["new"]
        diff = set(new_data) - set(old_data)
        if len(diff) == 1:
            latest_added_point = next(iter(diff))

            def _undo_adding_point():
                data = self.data.copy()
                data.remove(latest_added_point)
                self.data = data

            self._undo_queue.append(_undo_adding_point)
