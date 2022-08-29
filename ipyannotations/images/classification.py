from typing import Sequence
from functools import partial

from .. import generic
from .display import image_display_function


class ClassLabeller(generic.ClassLabeller):
    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_freetext: bool = True,
        image_size=(500, 500),
        # hint_function: Optional[Callable] = None,
        # hints: Optional[Dict[str, Any]] = None,
        # update_hints: bool = True,
        *args,
        **kwargs,
    ):
        """Create a widget for class label assignment.

        Parameters
        ----------
        options : Sequence[str], optional
            The classes to be assigned, by default ()
        max_buttons : int, optional
            The maximum numbers of buttons to display before switching
            to a dropdown menu, by default 12
        allow_freetext : bool, optional
            Whether a free-text entry box should be displayed,
            by default True
        image_size : tuple(int, int)
            The image size to be displayed, in pixels.
        """

        super().__init__(
            options=options,
            max_buttons=max_buttons,
            allow_freetext=allow_freetext,
            display_function=partial(
                image_display_function, fit_into=image_size
            ),
            *args,
            **kwargs,
        )  # type: ignore


class MulticlassLabeller(generic.MulticlassLabeller):
    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_freetext: bool = True,
        image_size=(500, 500),
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
        image_size : tuple(int, int)
            The image size to be displayed, in pixels.
        """

        super().__init__(
            options=options,
            max_buttons=max_buttons,
            allow_freetext=allow_freetext,
            display_function=partial(
                image_display_function, fit_into=image_size
            ),
            *args,
            **kwargs,
        )  # type: ignore
