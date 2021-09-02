from unittest.mock import MagicMock

from ipyannotations.controls import buttongroup, dropdownbutton
from ipyannotations.generic import classification


def test_submit_with_button(mocker):
    widget = classification.ClassLabeller(options=["a", "b"])
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)

    btn = widget.control_elements.buttons["a"].button

    widget.submit(btn)
    submission_function.assert_called_with("a")


def test_submit_with_text_field(mocker):
    widget = classification.ClassLabeller(options=["a", "b"])
    submission_function = mocker.MagicMock()
    widget.on_submit(submission_function)

    widget.freetext_widget.value = "test"

    widget.submit(widget.freetext_widget)
    submission_function.assert_called_with("test")


def test_changing_options_updates_buttons():
    widget = classification.ClassLabeller(options=["a", "b"])
    assert len(widget.control_elements.buttons.values()) == 2
    widget.options = ["a", "b", "c"]
    assert len(widget.control_elements.buttons.values()) == 3


def test_sorting_options():
    widget = classification.ClassLabeller(options=["b", "a"])
    displayed_opts = [
        btn.description for btn in widget.control_elements.children
    ]
    assert displayed_opts == ["b", "a"]
    widget._sort_options()
    displayed_opts = [
        btn.description for btn in widget.control_elements.children
    ]
    assert displayed_opts == ["a", "b"]


def test_number_keystrokes_trigger_submit(mocker):
    widget = classification.ClassLabeller()
    widget.options = ["a", "b"]
    spy: MagicMock = mocker.MagicMock()
    widget.on_submit(spy)

    test_event = {"key": "1", "type": "keyup"}
    widget._handle_keystroke(test_event)
    spy.assert_called_with("a")
    spy.reset_mock()

    test_event = {"key": "2", "type": "keyup"}
    widget._handle_keystroke(test_event)
    spy.assert_called_with("b")
    spy.reset_mock()

    test_event = {"key": "Enter", "type": "keyup"}
    widget._handle_keystroke(test_event)
    spy.assert_not_called()
    spy.reset_mock()


def test_max_buttons_switches_to_dropdown():
    widget = classification.ClassLabeller(max_buttons=6)
    widget.options = ["a", "b", "c", "d", "e", "f"]
    assert isinstance(widget.control_elements, buttongroup.ButtonGroup)
    widget.options = ["a", "b", "c", "d", "e", "f", "g", "h"]
    assert isinstance(widget.control_elements, dropdownbutton.DropdownButton)
