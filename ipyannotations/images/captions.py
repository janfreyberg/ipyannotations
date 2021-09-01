from ..generic import FreetextEntry
from .display import image_display_function


class ImageCaption(FreetextEntry):
    def __init__(
        self,
        *args,
        textbox_placeholder=(
            "Please caption this image and press Shift+Enter to submit."
        ),
        num_textbox_rows=5,
        **kwargs,
    ):

        super().__init__(
            *args,
            display_function=image_display_function,
            textbox_placeholder=textbox_placeholder,
            num_textbox_rows=num_textbox_rows,
            **kwargs,
        )
