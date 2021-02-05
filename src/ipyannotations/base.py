"""The base class that data labelling widgets should inherit from."""
from typing import Callable, Any
import ipywidgets as widgets


class LabellingWidgetMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skip_fns = []
        self.skip_button = widgets.Button(
            description="Skip", icon="fast-forward"
        )
        self.skip_button.on_click(self.skip)
        self.undo_fns = []
        self.undo_button = widgets.Button(description="Undo", icon="undo")
        self._undo_queue = []
        self.undo_button.on_click(self.undo)

    def on_submit(self, callback: Callable):
        """
        Add a function to call when the user submits a value.

        Parameters
        ----------
        callback : callable
            The function to be called when the widget is submitted.
        """
        if not callable(callback):
            raise ValueError(
                "You need to provide a callable object, but you provided "
                + str(callback)
                + "."
            )
        self.submission_functions.append(callback)

    def submit(self, sender=None):
        """The function that gets called by submitting an option.

        This is called by the button / text field elements and shouldn't be
        called directly.
        """
        # TODO: Implement logic to handle widgets with persistent data state

        # figure out if it's a button or text field
        if isinstance(sender, widgets.Text):
            value = sender.value
        else:
            value = sender.description

        if value is not None and value not in self.options:
            self.options = self.options + [value]

        for callback in self.submission_functions:
            callback(value)

        # self._compose()

    def on_undo(self, callback: Callable):
        """Provide a function that will be called when the user presses "undo".

        Parameters
        ----------
        callback : Callable[[], None]
            The function to be called. Takes no arguments and returns nothing.
        """
        self.undo_fns.append(callback)

    def undo(self, sender=None):
        for callback in self.undo_fns:
            callback()

    def on_skip(self, callback: Callable):
        """Provide a function that will be called when the user presses "Skip".

        Parameters
        ----------
        callback : Callable[[], None]
            The function to be called. Takes no arguments and returns nothing.
        """
        self.skip_fns.append(callback)

    def skip(self, sender=None):
        for callback in self.skip_fns:
            callback()
