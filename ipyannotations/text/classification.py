from typing import Sequence

import IPython.display
import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from ..generic.classification import ClassLabeller
from ..generic.multiclassification import MulticlassLabeller
from ..generic.generic_mixin import GenericWidgetMixin


def _text_display_function(item: str):
    IPython.display.display(IPython.display.Markdown(item))


class ClassLabeller(ClassLabeller):
    """A text classification widget.

    This widget lets you assign a single class to text.
    """

    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_freetext: bool = True,
        *args,
        **kwargs,
    ):
        """Create a widget for classifying text.

        Parameters
        ----------
        options : Sequence[str], optional
            The classes, by default ()
        max_buttons : int, optional
            The number of buttons to allow, before switching to a dropdown
            menu, by default 12
        allow_freetext : bool, optional
            If a text box should be available for new classes, by default True
        """
        super().__init__(
            options=options,
            max_buttons=max_buttons,
            allow_freetext=allow_freetext,
            display_function=_text_display_function,
            *args,
            **kwargs,
        )  # type: ignore


class MulticlassLabeller(MulticlassLabeller):
    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_freetext: bool = True,
        *args,
        **kwargs,
    ):
        """Create a widget for multi-class assignment.

        Parameters
        ----------
        options : Sequence[str], optional
            The options for classes, by default ()
        max_buttons : int, optional
            How many buttons to display before switching to a multi-select
            tool, by default 12
        allow_freetext : bool, optional
            Whether to allow free-text submission in a text box,
            by default True
        """

        super().__init__(
            options=options,
            max_buttons=max_buttons,
            allow_freetext=allow_freetext,
            display_function=_text_display_function,
            *args,
            **kwargs,
        )  # type: ignore


class SentimentLabeller(
    GenericWidgetMixin, LabellingWidgetMixin, widgets.VBox
):
    """A sentiment classification widget.

    This widget presents three label options, for classifying text into
    one of negative, neutral, or positive sentiment.
    """

    data: str = traitlets.Unicode()

    def __init__(self, *args, **kwargs):
        """Create a sentiment classification widget."""
        super().__init__(
            display_function=_text_display_function, *args, **kwargs
        )
        self.buttons = [
            widgets.Button(
                description="negative",
                icon="thumbs-down",
                button_style="danger",
                # layout=button_layout,
            ),
            widgets.Button(
                description="neutral",
                icon="equals",
                # layout=button_layout,
            ),
            widgets.Button(
                description="positive",
                icon="thumbs-up",
                button_style="success",
                # layout=button_layout,
            ),
        ]
        for button in self.buttons:
            button.on_click(self.submit)
        self.display_widget = widgets.Output(
            layout=widgets.Layout(margin="auto")
        )
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
            widgets.HBox(
                [
                    widgets.HBox(),
                    widgets.HBox(self.buttons),
                    widgets.HBox([self.skip_button, self.undo_button]),
                ],
                layout=widgets.Layout(justify_content="space-between"),
            ),
        ]

    def submit(self, sender: widgets.Button):  # type: ignore
        """Submit the label.

        Parameters
        ----------
        sender : widgets.Button
            One of the three interface buttons.
        """
        value = sender.description
        self.data = value
        super().submit()

    def _handle_keystroke(self, event):
        # the default enter shouldn't apply
        if event.get("key") == "Enter":
            return
        super()._handle_keystroke(event)
        for i, btn in enumerate(self.buttons):
            if event.get("key") == f"{i + 1}":
                self.submit(btn)
