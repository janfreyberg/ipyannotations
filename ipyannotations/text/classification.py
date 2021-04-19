from typing import Any, Callable, Dict, Optional, Sequence

import IPython.display
import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from ..generic.classification import ClassificationWidget


class ClassLabeller(ClassificationWidget):
    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_other: bool = True,
        hint_function: Optional[Callable] = None,
        hints: Optional[Dict[str, Any]] = None,
        update_hints: bool = True,
        *args,
        **kwargs,
    ):

        super().__init__(
            options=options,
            max_buttons=max_buttons,
            allow_other=allow_other,
            hint_function=hint_function,
            hints=hints,
            update_hints=update_hints,
            *args,
            **kwargs,
        )  # type: ignore
        self.display_function = lambda item: IPython.display.display(
            IPython.display.Markdown(item)
        )


class SentimentLabeller(LabellingWidgetMixin, widgets.VBox):
    data: str = traitlets.Unicode()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def submit(self, sender):
        value = sender.description
        self.data = value
        super().submit()

    def display(self, item):
        with self.display_widget:
            IPython.display.display(IPython.display.Markdown(item))

    def _handle_keystroke(self, event):
        # the default enter shouldn't apply
        if event.get("key") == "Enter":
            return
        super()._handle_keystroke(event)
        for i, btn in enumerate(self.buttons):
            if event.get("key") == f"{i + 1}":
                self.submit(btn)
