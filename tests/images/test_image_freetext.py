from unittest.mock import MagicMock
from PIL import Image
import numpy as np
import ipywidgets as widgets

from ipyannotations.images import freetext


def traverse_children(widget: widgets.Box):
    yield widget
    for child_widget in widget.children:
        if isinstance(child_widget, widgets.Box):
            yield from traverse_children(child_widget)
        else:
            yield child_widget


def test_freetext_submission_text():
    widget = freetext.FreetextAnnotator()
    widget.freetext_widget.value = "Test text."
    assert widget.data == "Test text."
    # check this is in the DOM
    assert widget.freetext_widget in list(traverse_children(widget))


def test_shift_enter_submits():
    widget = freetext.FreetextAnnotator()
    widget.freetext_widget.value = "Test text. "
    spy = MagicMock()
    widget.on_submit(spy)

    test_event = {"type": "keyup", "key": "Enter", "shiftKey": True}
    widget._handle_keystroke(test_event)

    spy.assert_called_once_with("Test text.")


def test_that_displaying_images_doesnt_error():
    widget = freetext.FreetextAnnotator()
    widget.display(Image.new("RGB", size=(50, 50), color=(0, 0, 0)))
    widget.display(np.zeros((50, 50)))
