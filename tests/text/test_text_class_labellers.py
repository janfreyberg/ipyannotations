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


def test_that_multiclass_submits_toggled_buttons(mocker):
    widget = text.MulticlassLabeller(options=["a", "b"])
    widget.class_selector.buttons[0].button.value = True
    assert widget.data == ["a"]
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)
    widget.submit()
    submission_function.assert_called_with(["a"])


def test_that_multiclass_doesnt_error_when_displaying():
    widget = text.MulticlassLabeller(options=["a", "b"])
    widget.display("hello.")


def test_that_sentiment_labeller_doesnt_error():
    widget = text.SentimentLabeller()
    widget.display("hello.")


def test_that_sentiment_labeller_handles_keystrokes(mocker):
    widget = text.SentimentLabeller()
    widget.display("hello.")
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)
    for key, label in zip(
        ["1", "2", "3"], ["negative", "neutral", "positive"]
    ):
        event = {"type": "keyup", "key": key}
        submission_function.reset_mock()
        widget._handle_keystroke(event)
        submission_function.assert_called_once_with(label)
    # normal enter shouldnt trigger submission:
    submission_function.reset_mock()
    widget._handle_keystroke({"type": "keyup", "key": "Enter"})
    submission_function.assert_not_called()
