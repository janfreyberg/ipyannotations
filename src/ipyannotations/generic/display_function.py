from typing import Callable, Dict, Union

import IPython.display
import ipywidgets as widgets
from typing_extensions import Literal


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
