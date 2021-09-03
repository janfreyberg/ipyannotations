from ipyannotations import images
from unittest.mock import MagicMock
from PIL import Image
import numpy as np


def test_submit_with_button(mocker):
    widget = images.ClassLabeller(options=["a", "b"])
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)

    btn = widget.control_elements.buttons["a"].button

    widget.submit(btn)
    submission_function.assert_called_with("a")


def test_submit_with_text_field(mocker):
    widget = images.ClassLabeller(options=["a", "b"])
    submission_function = mocker.MagicMock()
    widget.on_submit(submission_function)

    widget.freetext_widget.value = "test"

    widget.submit(widget.freetext_widget)
    submission_function.assert_called_with("test")


def test_that_displaying_images_doesnt_error():
    widget = images.ClassLabeller()
    widget.display(Image.new("RGB", size=(50, 50), color=(0, 0, 0)))
    widget.display(np.zeros((50, 50)))


def test_that_multiclass_submits_toggled_buttons(mocker):
    widget = images.MulticlassLabeller(options=["a", "b"])
    widget.class_selector.buttons[0].button.value = True
    assert widget.data == ["a"]
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)
    widget.submit()
    submission_function.assert_called_with(["a"])


def test_that_multiclass_doesnt_error_when_displaying(mocker):
    widget = images.MulticlassLabeller(options=["a", "b"])
    widget.display(Image.new("RGB", size=(50, 50), color=(0, 0, 0)))
    widget.display(np.zeros((50, 50)))
