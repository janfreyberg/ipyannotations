from copy import copy
from typing import Callable, List, Tuple

import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin


@widgets.register
class TextTaggerCore(widgets.DOMWidget):
    """A text tagging javascript widget."""

    # properties to make sure the right frontend widget is found:
    _view_name = traitlets.Unicode("TextTaggerView").tag(sync=True)
    _model_name = traitlets.Unicode("TextTaggerModel").tag(sync=True)
    _view_module = traitlets.Unicode("ipyannotations").tag(sync=True)
    _model_module = traitlets.Unicode("ipyannotations").tag(sync=True)
    _view_module_version = traitlets.Unicode("^0.1.0").tag(sync=True)
    _model_module_version = traitlets.Unicode("^0.1.0").tag(sync=True)

    text: str = traitlets.Unicode(
        "Lorem ipsum", help="The text to display."
    ).tag(sync=True)
    classes: List[str] = traitlets.List(
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
    """A tagging widget to annotate tokens inside text."""

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
        """A tagging widget to annotate tokens inside text.

        Parameters
        ----------
        classes : list, optional
            The classes of entities to annotate, by default
            ["MISC", "PER", "LOC", "ORG"]
        text : str, optional
            The text to display, by default "Lorem ipsum"
        data : list, optional
            If you have entity annotations for this text already, by default []
        button_width : str, optional
            A valid HTML width string, by default "5em"
        """
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

        self.children = (
            self.text_widget,
            self.class_picker,
            widgets.HBox(
                [self.undo_button, self.skip_button, self.submit_button],
                layout={
                    "align_items": "stretch",
                    "justify_content": "flex-end",
                    "flex_flow": "row wrap",
                },
            ),
            self.event_watcher,
        )

    def display(self, text: str):
        self.text_widget.text = text
        self.text_widget.entity_spans = []

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
        elif len(new_data) == 0:
            self._undo_queue.clear()

    def _handle_keystroke(self, event):
        super()._handle_keystroke(event)
        for i, option in enumerate(self.class_picker.options):
            if event["key"] == f"{(i + 1) % 10}":
                self.class_picker.value = option
            if i == 10:
                break
