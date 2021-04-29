"""A widget to assign free-text captions or descriptions."""

import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from .generic_mixin import GenericWidgetMixin, default_display_function


class FreetextEntry(GenericWidgetMixin, LabellingWidgetMixin, widgets.VBox):
    """A widget for submitting free-text data annotations.

    This widget presents a simple text box for data entry, and is designed for
    captioning, question answering, and similar tasks.
    """

    data: str = traitlets.Unicode()

    def __init__(
        self,
        display_function=default_display_function,
        textbox_placeholder="Type a response and press Shift+Enter to submit.",
        *args,
        **kwargs,
    ):
        """Create a free-text data annotation widget.

        Parameters
        ----------
        display_function : callable, optional
            The display function called on each data point.
        textbox_placeholder : str, optional
            The text shown when the textbox is empty, by default:
            "Type the response and press Shift+Enter to submit."
        """
        super().__init__(
            display_function=display_function,
            track_keystrokes=True,
            allow_freetext=False,
            *args,
            **kwargs,
        )
        self.freetext_widget = widgets.Textarea(
            placeholder=textbox_placeholder,
            layout={"width": "50%"},
        )
        widgets.link((self, "data"), (self.freetext_widget, "value"))

        self.children = [
            self.display_widget,
            widgets.HBox(
                [
                    self.freetext_widget,
                    widgets.HBox(
                        [
                            self.skip_button,
                            self.undo_button,
                            self.submit_button,
                        ]
                    ),
                ],
                layout=widgets.Layout(justify_content="space-between"),
            ),
            self.event_watcher,
        ]

    def _handle_keystroke(self, event):
        if event["key"] == "Enter" and event["shiftKey"]:
            self.freetext_widget.value = self.freetext_widget.value[:-1]
            super()._handle_keystroke(event)
