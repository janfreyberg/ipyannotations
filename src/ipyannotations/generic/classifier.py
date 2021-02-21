"""Input and timing control widgets."""

from typing import Any, Callable, Dict, List, Optional, Sequence

import IPython.display
import ipywidgets as widgets
import traitlets

from ..base import LabellingWidgetMixin

# from .._compatibility import ignore_widget_on_submit_warning
# from .base import SubmissionWidgetMixin
from ..controls.buttongroup import ButtonGroup
from ..controls.dropdownbutton import DropdownButton
from .display_function import default_display_function


class ClassificationWidget(LabellingWidgetMixin, widgets.VBox):
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
    allow_other : bool, optional
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

    allow_other = traitlets.Bool(True)
    options = traitlets.List(list(), allow_none=True)
    max_buttons = traitlets.Integer(12)

    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_other: bool = True,
        display_function=default_display_function,
        hint_function: Optional[Callable] = None,
        hints: Optional[Dict[str, Any]] = None,
        update_hints: bool = True,
        *args,
        **kwargs,
    ):
        """
        Create a widget that will render submission options.

        Note that all parameters can also be changed through assignment after
        you create the widget.
        """
        super().__init__(
            *args,
            **kwargs,
        )
        # self.hint_function = hint_function
        # self.hints = dict() if hints is None else hints
        # if self.hint_function is not None:
        #     for option, feature in self.hints.items():
        #         self.hints[option] = widgets.Output()
        #         with self.hints[option]:
        #             self.hint_function(feature)

        self.sort_button = widgets.Button(
            description="Sort options", icon="sort"
        )
        self.sort_button.on_click(self._sort_options)

        self.display_widget = widgets.Output(
            layout=widgets.Layout(margin="auto")
        )
        if allow_other:
            self.other_widget = widgets.Text(
                value="",
                description="Other:",
                placeholder="Hit enter to submit.",
            )
            self.other_widget.on_submit(self.submit)
        else:
            self.other_widget = widgets.HBox([])
        self.options = [str(option) for option in options]
        self._fixed_options = [option for option in self.options]
        self.max_buttons = max_buttons
        self.allow_other = allow_other
        self.display_function = display_function
        self._compose()

    def add_hint(self, value, hint):
        """Add a hint to the widget.

        Parameters
        ----------
        value : str
            The label for which this hint applies.
        hint : Any
            The data point to use for the hint.
        """
        if (
            self.hint_function is not None
            and self.hints is not None
            and value not in self.hints
        ):
            with self.control_elements.hints[value]:
                self.hint_function(hint)

    def remove_options(self, values):
        """Remove options from the widget.

        Parameters
        ----------
        values : Sequence[str]
            The options to remove.
        """

        self.options = [
            option
            for option in self.options
            if option not in values or option in self._fixed_options
        ]

    def _sort_options(self, change=None):
        self.options = list(sorted(self.options))

    def submit(self, sender):
        if isinstance(sender, widgets.Text):
            value = sender.value
            # check if this is a new option:
            if value not in self.options:
                self.options = self.options + [value]
            sender.value = ""
        else:
            value = sender.description
        self.data = value
        super().submit()

    def display(self, item):
        with self.display_widget:
            IPython.display.clear_output(wait=True)
            self.display_function(item)

    @traitlets.observe("allow_other", "options", "max_buttons")
    def _compose(self, change=None):

        if len(self.options) <= self.max_buttons:
            self.control_elements = ButtonGroup(self.options)
        else:
            self.control_elements = DropdownButton(self.options)

        self.control_elements.on_click(self.submit)

        self.children = [
            self.display_widget,
            self.control_elements,
            widgets.HBox(
                [
                    self.other_widget,
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
