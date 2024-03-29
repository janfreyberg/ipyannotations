"""A widget to use when building a "generic" widget to display data as-is."""

from typing import Any
import IPython.display
import ipywidgets as widgets


def default_display_function(feature):
    """
    A default function that displays the feature and adds some padding.

    Parameters
    ----------
    feature : np.ndarray, pd.Series, pd.DataFrame
        The feature(s) you want to display
    """
    # n_samples = min(n_samples, feature.shape[0])
    IPython.display.display(widgets.Box(layout=widgets.Layout(height="2.5%")))
    IPython.display.display(feature)
    IPython.display.display(widgets.Box(layout=widgets.Layout(height="2.5%")))


class GenericWidgetMixin:
    """
    A mixin class for generic widgets, which handles UI elements and display.
    """

    def __init__(  # noqa: D001
        self,
        display_function=default_display_function,
        allow_freetext=False,
        *args,
        **kwargs
    ):

        super().__init__(*args, **kwargs)
        self.display_widget = widgets.Output(
            layout=widgets.Layout(margin="auto", min_height="50px")
        )
        if allow_freetext:
            self.freetext_widget = widgets.Text(
                value="",
                description="Other:",
                placeholder="Hit enter to submit.",
            )
            self.freetext_widget.on_submit(self.submit)
        else:
            self.freetext_widget = widgets.HBox([])
        self.display_function = display_function

    def display(self, item: Any):
        """Display a data point.

        This function calles the display function provided to the widget,
        and wraps it in a ipywidgets.Output widget to present the display in
        the right location.

        Parameters
        ----------
        item : any
            The data point.
        """
        self.display_widget.clear_output(wait=True)
        with self.display_widget:
            self.display_function(item)
        self.clear()  # type: ignore
