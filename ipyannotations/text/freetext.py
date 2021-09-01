import IPython.display

from .. import generic


class FreetextAnnotator(generic.FreetextAnnotator):
    """A widget for submitting free-text data annotations for text.

    This widget presents a simple text box for data entry, and is designed for
    text summarisation, question answering, or similar.
    """

    def __init__(
        self,
        textbox_placeholder: str = (
            "Please caption this image and press Shift+Enter to submit."
        ),
        num_textbox_rows: int = 5,
        *args,
        **kwargs
    ):
        """Create a free-text text annotation widget.

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
            textbox_placeholder=textbox_placeholder,
            num_textbox_rows=num_textbox_rows,
            display_function=lambda item: IPython.display.display(
                IPython.display.Markdown(item)
            ),
            **kwargs
        )  # type: ignore
