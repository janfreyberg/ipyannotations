import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from .._frontend import module_name, module_version


@widgets.register
class TextTaggerCore(widgets.DOMWidget):
    """A text tagging javascript widget."""

    # properties to make sure the right frontend widget is found:
    _view_name = traitlets.Unicode("TextTaggerView").tag(sync=True)
    _model_name = traitlets.Unicode("TextTaggerModel").tag(sync=True)
    _model_module = traitlets.Unicode(module_name).tag(sync=True)
    _model_module_version = traitlets.Unicode(module_version).tag(sync=True)
    _view_module = traitlets.Unicode(module_name).tag(sync=True)
    _view_module_version = traitlets.Unicode(module_version).tag(sync=True)

    text = traitlets.Unicode("Lorem ipsum", help="The text to display.").tag(
        sync=True
    )
    classes = traitlets.List(
        trait=traitlets.Unicode(), default_value=["MISC", "PER", "LOC", "ORG"]
    ).tag(sync=True)
    selected_class = traitlets.Unicode().tag(sync=True)
    snap_to_word_boundary = traitlets.Bool().tag(sync=True)
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
        snap_to_word_boundary=True,
        **kwargs,
    ):
        """Create a text tagging "core" widget.

        This is a front-end widget that displays its 'text' attribute. When a
        sub-string is highlighted, it will snap to the word boundaries, and
        mark it as a span of type `widget.selected_class`. All spans that are
        highlighted are available under `widget.entity_spans`, which is also
        assignable.

        Select the type of entity to tag by clicking its corresponding button,
        or by using the hotkeys 1-0. Hotkeys are mapped to entities in the
        order in which they appear on screen.

        Parameters
        ----------
        text : str, optional
            The text to display in the frontend, by default "Lorem ipsum"
        classes : list, optional
            The possible classes to assign to a span, by default
            ["MISC", "PER", "LOC", "ORG"].
        entity_spans : list, optional
            The currently highlighted spans, by default []
        snap_to_word_boundary : bool
            Whether to always snap to the word boundary, even when a
            word is only partially selected.
        """
        super().__init__(
            text=text,
            classes=classes,
            entity_spans=entity_spans,
            snap_to_word_boundary=snap_to_word_boundary,
            **kwargs,
        )
        if not self.selected_class:
            self.selected_class = self.classes[0]


class TextTagger(LabellingWidgetMixin, widgets.VBox):
    """A tagging widget to annotate tokens inside text."""

    data = traitlets.List(
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
        snap_to_word_boundary=True,
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
        snap_to_word_boundary : bool
            Whether or not the widget should expand selections to the word
            boundaries. For most languages, this should be left True, but some
            languages are based off single characters (e.g. traditional
            mandarin).
        """
        super().__init__()
        self.text_widget = TextTaggerCore(
            text=text,
            classes=classes,
            entity_spans=data,
            snap_to_word_boundary=snap_to_word_boundary,
        )
        self.class_selector = widgets.ToggleButtons(
            options=classes,
            description="Class to tag:",
            style=widgets.ToggleButtonsStyle(button_width=button_width),
        )
        widgets.link(
            (self.class_selector, "value"),
            (self.text_widget, "selected_class"),
        )
        widgets.link((self, "data"), (self.text_widget, "entity_spans"))
        self.children = (self.text_widget, self.class_selector)

        self.children = (
            self.text_widget,
            self.class_selector,
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
        self.__undo_in_process = False

    def display(self, text: str):
        """Display text to be tagged.

        Parameters
        ----------
        text : str
        """
        self.text_widget.text = text
        self.clear()
        self._undo_queue.clear()

    @traitlets.observe("data")
    def _append_undo_fn(self, proposal: dict):
        if self.__undo_in_process:
            return
        old_data = proposal["old"]

        def _undo_data_change():
            self.__undo_in_process = True
            self.data = old_data
            self.__undo_in_process = False

        self._undo_queue.append(_undo_data_change)

    def _handle_keystroke(self, event):
        super()._handle_keystroke(event)
        keys = [str(i) for i in range(1, 10)] + ["0"]
        for key, option in zip(keys, self.class_selector.options):
            if event.get("key") == key:
                self.class_selector.value = option
