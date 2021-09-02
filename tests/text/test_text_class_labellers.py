from ipyannotations import text
from unittest.mock import MagicMock
from PIL import Image
import numpy as np


def test_submit_with_button(mocker):
    widget = text.ClassLabeller(options=["a", "b"])
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)

    btn = widget.control_elements.buttons["a"].button

    widget.submit(btn)
    submission_function.assert_called_with("a")


def test_submit_with_text_field(mocker):
    widget = text.ClassLabeller(options=["a", "b"])
    submission_function = mocker.MagicMock()
    widget.on_submit(submission_function)

    widget.freetext_widget.value = "test"

    widget.submit(widget.freetext_widget)
    submission_function.assert_called_with("test")


def test_that_displaying_images_doesnt_error():
    widget = text.ClassLabeller()
    widget.display("Hello.")
