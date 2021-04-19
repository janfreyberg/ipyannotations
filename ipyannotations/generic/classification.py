"""A widget to assign a single class to each data point."""

from typing import Sequence

import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin
from ..controls.buttongroup import ButtonGroup
from ..controls.dropdownbutton import DropdownButton
from .generic_mixin import GenericWidgetMixin, default_display_function


class ClassificationWidget(
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

    def submit(self, sender):
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
        for i, btn in enumerate(self.control_elements.buttons.values()):
            if event.get("key") == f"{i + 1}":
                self.submit(btn)
