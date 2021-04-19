"""Widgets to assign multiple classes to data points."""

import time
from typing import List, Sequence

import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from ..controls.togglebuttongroup import ToggleButtonGroup
from .generic_mixin import GenericWidgetMixin, default_display_function


class MultiClassificationWidget(
    GenericWidgetMixin, LabellingWidgetMixin, widgets.VBox
):
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

    allow_freetext = traitlets.Bool(True)
    options = traitlets.List(
        trait=traitlets.Unicode(), default_value=list(), allow_none=True
    )
    max_buttons = traitlets.Integer(12)
    data: List[str] = traitlets.List(
        trait=traitlets.Unicode(), default_value=list()
    )

    def __init__(
        self,
        options: Sequence[str] = (),
        allow_freetext: bool = True,
        display_function=default_display_function,
        *args,
        **kwargs,
    ):
        """
        Create a widget that will render submission options.

        Note that all parameters can also be changed through assignment after
        you create the widget.
        """
        super().__init__(
            allow_freetext=allow_freetext,
            display_function=display_function,
            *args,
            **kwargs,
        )  # type: ignore
        self.options = [str(option) for option in options]
        self.class_selector = ToggleButtonGroup(options=options)
        traitlets.link((self, "data"), (self.class_selector, "value"))
        traitlets.link((self, "options"), (self.class_selector, "options"))
        self._fixed_options = [option for option in self.options]
        self._freetext_timestamp = 0.0

        self.children = [
            self.display_widget,
            self.class_selector,
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
        if event["key"] == "Enter":
            if self._freetext_timestamp > time.time() - 0.1:
                return
        super()._handle_keystroke(event)
        for i, option in zip(range(10), self.class_selector.options):
            if event["key"] == f"{(i + 1) % 10}":
                self.class_selector._toggle(option)

    def freetext_submission(self, sender: widgets.Text):
        if sender is self.freetext_widget and sender.value:
            value = sender.value
            # check if this is a new option:
            if value not in self.options:
                self.options = self.options + [value]

                def _undo_callback():
                    self.options = [
                        opt for opt in self.options if opt != value
                    ]

                self._undo_queue.append(_undo_callback)
            if value not in self.data:
                self.data = self.data + [value]
            sender.value = ""
        self._freetext_timestamp = time.time()

    def undo(self, sender=None):
        if self._undo_queue:
            last_undo_fn = self._undo_queue.pop()
            last_undo_fn()
        for callback in self.undo_fns:
            callback()
