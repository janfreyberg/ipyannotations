import IPython.display

from ..generic import freetext


class FreeTextEntry(freetext.FreetextEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_function = lambda item: IPython.display.display(
            IPython.display.Markdown(item)
        )
