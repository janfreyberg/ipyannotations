"""A widget to assign a single class to each data point."""

from typing import Sequence, Union

import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from ..controls.buttongroup import ButtonGroup
from ..controls.dropdownbutton import DropdownButton
from .generic_mixin import GenericWidgetMixin, default_display_function


class ClassLabeller(GenericWidgetMixin, LabellingWidgetMixin, widgets.VBox):
    """
    A classification widget.

    This widget is designed to assign one class (a string label) to each data
    point.
    """

    allow_freetext = traitlets.Bool(True)
    options = traitlets.List(list(), allow_none=True)
    max_buttons = traitlets.Integer(12)
    data: str

    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_freetext: bool = True,
        display_function=default_display_function,
        *args,
        **kwargs,
    ):
        """Create a widget for classification labelling.

        Parameters
        ----------
        options : Sequence[str], optional
            The classes, by default ()
        max_buttons : int, optional
            The number of buttons to allow, before switching to a dropdown
            menu, by default 12
        allow_freetext : bool, optional
            If a text box should be available for new classes, by default True
        display_function : callable, optional
            The function called to display a data point, by
            default default_display_function
        """
        super().__init__(
            allow_freetext=allow_freetext,
            display_function=display_function,
            *args,
            **kwargs,
        )  # type: ignore

        self.sort_button = widgets.Button(
            description="Sort options", icon="sort"
        )
        self.sort_button.on_click(self._sort_options)

        self.options = [str(option) for option in options]
        self._fixed_options = [option for option in self.options]
        self.max_buttons = max_buttons
        self._compose()

    def _sort_options(self, change=None):
        self.options = list(sorted(self.options))

    def submit(  # type: ignore
        self, sender: Union[widgets.Button, widgets.Text]
    ):
        """Trigger the submission functions.

        Parameters
        ----------
        sender : ipywidgets.Button, ipywidgets.Text
            The widget that triggered this.
        """
        if isinstance(sender, widgets.Text) and sender.value:
            value = sender.value
            # check if this is a new option:
            if value not in self.options:
                self.options = self.options + [value]
            sender.value = ""
        else:
            value = sender.description
        self.data = value
        super().submit()

    @traitlets.observe("options", "max_buttons")
    def _compose(self, change=None):

        if len(self.options) <= self.max_buttons:
            self.control_elements = ButtonGroup(self.options)
        else:
            self.control_elements = DropdownButton(self.options)

        self.control_elements.on_click(self.submit)

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
            self.control_elements,
            widgets.HBox(
                [
                    self.freetext_widget,
                    widgets.HBox(
                        [self.sort_button, self.skip_button, self.undo_button]
                    ),
                ],
                layout=widgets.Layout(justify_content="space-between"),
            ),
        ]

    def _handle_keystroke(self, event):
        # the default enter shouldn't apply
        if event.get("key") == "Enter":
            return
        super()._handle_keystroke(event)
        keys = [str(i) for i in range(1, 10)] + ["0"]
        for key, btn in zip(keys, self.control_elements.buttons.values()):
            if event.get("key") == key:
                self.submit(btn)
