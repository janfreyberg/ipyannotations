"""A widget to assign free-text captions or descriptions."""

import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from .generic_mixin import GenericWidgetMixin, default_display_function


class FreetextEntry(GenericWidgetMixin, LabellingWidgetMixin, widgets.VBox):
    """
    A flexible data submission widget.

    Submitter allows you to specifiy options, which can be chosen either via
    buttons or a dropdown, and a text field for "other" values.

    Parameters
    ----------
    options : list, tuple, optional
        The data submission options.
    max_buttons : int
        The number buttons you want to display. If len(options) >
        max_buttons, the options will be displayed in a dropdown instead.
    allow_freetext : bool, optional
        Whether the widget should contain a text box for users to type in
        a value not in options.
    hint_function : fun
        A function that will be passed the hint for each label, that displays
        some output that will be displayed under each label and can be
        considered a hint or more in-depth description of a label. During image
        labelling tasks, this might be a function that displays an example
        image.
    hints : dict
        A dictionary with each element of options as a key, and the data that
        gets passed to hint_function as input.
    update_hints : bool
        Whether to update hints as you go through - for options that don't
        have any hints yet.
    """

    data: str = traitlets.Unicode()

    def __init__(
        self,
        display_function=default_display_function,
        textbox_placeholder="Type the response and press Enter to submit.",
        *args,
        **kwargs,
    ):
        """
        Create a widget that will render submission options.

        Note that all parameters can also be changed through assignment after
        you create the widget.
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
