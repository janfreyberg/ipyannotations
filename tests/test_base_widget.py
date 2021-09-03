from ipyannotations import base
from unittest.mock import MagicMock
import ipywidgets
import pytest


ENTER_KEYUP = {"type": "keyup", "key": "Enter"}
ENTER_KEYDOWN = {"type": "keydown", "key": "Enter"}
BACKSPACE_KEYDOWN = {"type": "keyup", "key": "Backspace"}


class TestWidget(base.LabellingWidgetMixin, ipywidgets.VBox):
    """
    Widget required as the mixin doesn't work if not also inheriting from VBox.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def test_error_on_passing_non_callable():
    widget = TestWidget()
    with pytest.raises(ValueError):
        widget.on_submit(1)


def test_key_handling(mocker):
    widget = TestWidget()
    submission_function: MagicMock = mocker.MagicMock()
    undo_function: MagicMock = mocker.MagicMock()
    undo_spy: MagicMock = mocker.spy(widget, "undo")
    widget.on_submit(submission_function)
    widget.on_submit(undo_function)
    widget.data = "test data"

    widget._handle_keystroke(ENTER_KEYDOWN)
    submission_function.assert_not_called()

    widget._handle_keystroke(ENTER_KEYUP)
    submission_function.assert_called_with("test data")

    widget._handle_keystroke(BACKSPACE_KEYDOWN)
    undo_spy.assert_called_once()
    undo_function.assert_called_once()
