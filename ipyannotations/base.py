"""The base class that data labelling widgets should inherit from."""
from typing import Callable, List, Optional, Any

import ipyevents
import ipywidgets as widgets

CallbackList = List[Callable]


class LabellingWidgetMixin:
    def __init__(self, *args, track_keystrokes=True, **kwargs):  # noqa: D001
        super().__init__(*args, **kwargs)
        button_layout = widgets.Layout(
            # width="auto",
            min_width="80px",
            flex="1 1 auto",
            max_width="120px",
        )
        self.skip_button = widgets.Button(
            description="Skip",
            icon="fast-forward",
            layout=button_layout,
        )
        self.skip_fns: CallbackList = []
        self.skip_button.on_click(self.skip)

        self.undo_button = widgets.Button(
            description="Undo",
            icon="undo",
            layout=button_layout,
        )
        self.undo_fns: CallbackList = []
        self._undo_queue: CallbackList = []
        self.undo_button.on_click(self.undo)

        self.submit_button = widgets.Button(
            description="Submit",
            icon="check",
            button_style="success",
            layout=button_layout,
        )
        self.submission_functions = []
        self.submit_button.on_click(self.submit)

        self.event_watcher = ipyevents.Event(
            source=self,
            watched_events=["keyup"] if track_keystrokes else [],
            prevent_default_actions=True,
        )
        self.event_watcher.on_dom_event(self._handle_keystroke)
        self.children = self.children + (self.event_watcher,)

    def on_submit(self, callback: Callable):
        """
        Add a function to call when the user submits a value.

        Parameters
        ----------
        callback : Callable[[Any], None]
            The function to be called when the widget is submitted.
        """
        if not callable(callback):
            raise ValueError(
                "You need to provide a callable object, but you provided "
                + str(callback)
                + "."
            )
        self.submission_functions.append(callback)

    def submit(self, sender: Any = None):
        """The function that gets called by submitting an option.

        This is called by the button / text field elements and shouldn't be
        called directly.

        Parameters
        ----------
        sender : Optional
            The "sender" that invoked this callback. This is ignored.
        """
        if hasattr(self, "data"):
            value = self.data
        else:
            raise NotImplementedError(
                "Submission for this widget doesn't seem to be implemented."
            )

        for callback in self.submission_functions:
            callback(value)

    def on_undo(self, callback: Callable):
        """Provide a function that will be called when the user presses "undo".

        Parameters
        ----------
        callback : Callable[[], None]
            The function to be called. Takes no arguments and returns nothing.
        """
        self.undo_fns.append(callback)

    def undo(self, sender=None):
        """
        Undo (i.e. call the functions in the undo queue.)

        Parameters
        ----------
        sender : Optional
            The "sender" that invoked this callback. This is ignored.
        """
        if self._undo_queue:
            last_undo_fn = self._undo_queue.pop()
            last_undo_fn()
        else:
            for callback in self.undo_fns:
                callback()

    def skip(self, sender: Optional[widgets.Button] = None):
        """
        Skip a data point.

        Parameters
        ----------
        sender : Optional
            The "sender" that invoked this callback. This is ignored.
        """
        for callback in self.submission_functions:
            callback(None)

    def clear(self):
        """Clear this widget's data."""
        if "data" in self.class_traits():
            self.data = self.class_traits()["data"].default()

    def _handle_keystroke(self, event):
        if event["type"] != "keyup":
            return
        if event["key"] == "Enter":
            self.submit()
        elif event["key"] == "Backspace":
            self.undo()
