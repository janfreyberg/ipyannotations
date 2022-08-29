"""Widgets to assign multiple classes to data points."""

import time
from typing import Iterable

import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from ..controls.togglebuttongroup import ToggleButtonGroup
from .generic_mixin import GenericWidgetMixin, default_display_function


class MulticlassLabeller(
    GenericWidgetMixin, LabellingWidgetMixin, widgets.VBox
):
    """
    A multi-class data labelling widget.

    Label an arbitrary data point with as many or as few labels as necessary.
    Toggle labels by either clicking on the corresponding button, or by using
    the hotkeys 1-0 (mapped in order in which labels are on screen). Submit
    by either clicking the "Submit" button, or by pressing the Enter key.
    """

    allow_freetext = traitlets.Bool(True)
    options = traitlets.List(
        trait=traitlets.Unicode(), default_value=list(), allow_none=True
    )
    max_buttons = traitlets.Integer(12)
    data = traitlets.List(trait=traitlets.Unicode(), default_value=list())

    def __init__(
        self,
        options: Iterable[str] = (),
        allow_freetext: bool = True,
        display_function=default_display_function,
        *args,
        **kwargs,
    ):
        """
        Create a multi-class labelling widget.

        Parameters
        ----------
        options : list, tuple, optional
            The class label options.
        max_buttons : int
            The number buttons you want to display. If len(options) >
            max_buttons, the options will be displayed in a dropdown instead.
        allow_freetext : bool, optional
            Whether the widget should contain a text box for users to type in
            a value not present in options.
        display_function : callable
            The function called on each datapoint to display it.
        """
        super().__init__(
            allow_freetext=allow_freetext,
            display_function=display_function,
            *args,
            **kwargs,
        )  # type: ignore
        self.options = [str(option) for option in options]
        self.class_selector = ToggleButtonGroup(options=self.options)
        traitlets.link((self, "data"), (self.class_selector, "value"))
        traitlets.link((self, "options"), (self.class_selector, "options"))
        self._fixed_options = [option for option in self.options]
        self._freetext_timestamp = 0.0
        self.freetext_widget.on_submit(self.freetext_submission)

        self.children = [
            widgets.Box(
                (self.display_widget,),
                layout=widgets.Layout(
                    justify_content="center",
                    padding="2.5% 0",
                    display="flex",
                    width="100%",
                ),
            ),
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
        keys = [str(i) for i in range(1, 10)] + ["0"]
        for key, option in zip(keys, self.class_selector.options):
            if event.get("key") == key:
                self.class_selector._toggle(option)

    def freetext_submission(self, sender: widgets.Text):
        """Handle a submission by the free-text widget.

        This is a separate method from `submit`, because it doesn't actually
        submit the data. Instead, it adds the free-text as an option, and
        toggles that option to `True`.

        Parameters
        ----------
        sender : widgets.Text
        """
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

    def undo(self, sender=None):  # noqa: D001
        """Undo the last action.

        This will undo the addition of any free-text, and if none are in the
        queue, functions registered with `on_undo` are called.
        """
        if self._undo_queue:
            last_undo_fn = self._undo_queue.pop()
            last_undo_fn()
        else:
            for callback in self.undo_fns:
                callback()
