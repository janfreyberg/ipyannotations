from typing import Any, Callable, Dict, Optional, Sequence

from ..generic import ClassificationWidget, MultiClassificationWidget
from .display import image_display_function


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
        self.display_function = image_display_function


class MulticlassLabeller(MultiClassificationWidget):
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
        self.display_function = image_display_function
