from ..generic import FreetextEntry
from .display import image_display_function


class ImageCaption(FreetextEntry):
    def __init__(self, *args, **kwargs):

        super().__init__(
            display_function=image_display_function, *args, **kwargs
        )
