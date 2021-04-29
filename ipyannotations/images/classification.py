from typing import Sequence

from ..generic import ClassificationWidget, MultiClassificationWidget
from .display import image_display_function


class ClassLabeller(ClassificationWidget):
    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_freetext: bool = True,
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
        # hint_function : Optional[Callable], optional
        #     A function that displays, by default None
        # hints : Optional[Dict[str, Any]], optional
        #     [description], by default None
        # update_hints : bool, optional
        #     [description], by default True
        """

        super().__init__(
            options=options,
            max_buttons=max_buttons,
            allow_freetext=allow_freetext,
            # hint_function=hint_function,
            # hints=hints,
            # update_hints=update_hints,
            *args,
            **kwargs,
        )  # type: ignore
        self.display_function = image_display_function


class MulticlassLabeller(MultiClassificationWidget):
    def __init__(
        self,
        options: Sequence[str] = (),
        max_buttons: int = 12,
        allow_freetext: bool = True,
        # hint_function: Optional[Callable] = None,
        # hints: Optional[Dict[str, Any]] = None,
        # update_hints: bool = True,
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
        # hint_function : Optional[Callable], optional
        #     [description], by default None
        # hints : Optional[Dict[str, Any]], optional
        #     [description], by default None
        # update_hints : bool, optional
        #     [description], by default True
        """

        super().__init__(
            options=options,
            max_buttons=max_buttons,
            allow_freetext=allow_freetext,
            # hint_function=hint_function,
            # hints=hints,
            # update_hints=update_hints,
            *args,
            **kwargs,
        )  # type: ignore
        self.display_function = image_display_function
