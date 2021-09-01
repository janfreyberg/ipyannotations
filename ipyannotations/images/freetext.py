from .. import generic
from .display import image_display_function


class FreetextAnnotator(generic.FreetextAnnotator):
    """A widget for submitting free-text data annotations for images.

    This widget presents a simple text box for data entry, and is designed for
    image captioning, visual descriptions or summarisation.
    """

    def __init__(
        self,
        *args,
        textbox_placeholder: str = (
            "Please caption this image and press Shift+Enter to submit."
        ),
        num_textbox_rows: int = 5,
        **kwargs,
    ):
        """Create a free-text image annotation widget.

        Parameters
        ----------
        textbox_placeholder : str, optional
            The text shown when the textbox is empty, by default:
            "Type the response and press Shift+Enter to submit."
        num_textbox_rows : int
            The height of the text box, in number of rows (of text), default 5.
        """

        super().__init__(
            *args,
            display_function=image_display_function,
            textbox_placeholder=textbox_placeholder,
            num_textbox_rows=num_textbox_rows,
            **kwargs,
        )
