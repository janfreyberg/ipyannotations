import time
from unittest.mock import MagicMock

from ipyannotations.controls import buttongroup, dropdownbutton
from ipyannotations.generic import classification
from ipyannotations import generic


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
    widget.options = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    spy: MagicMock = mocker.MagicMock()
    widget.on_submit(spy)

    for i, key in enumerate(list(range(1, 10)) + [0]):
        test_event = {"key": str(key), "type": "keyup"}
        widget._handle_keystroke(test_event)
        spy.assert_called_with(widget.options[i])
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


def test_that_multiclass_submits_toggled_buttons(mocker):
    widget = generic.MulticlassLabeller(options=["a", "b"])
    widget.class_selector.buttons[0].button.value = True
    assert widget.data == ["a"]
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)
    widget.submit()
    submission_function.assert_called_with(["a"])
    widget.class_selector.buttons[1].button.value = True
    assert widget.data == ["a", "b"]
    widget.submit()
    submission_function.assert_called_with(["a", "b"])


def test_that_display_resets_toggles(mocker):
    widget = generic.MulticlassLabeller(options=["a", "b"])
    widget.class_selector.buttons[0].button.value = True
    assert widget.data == ["a"]
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)
    widget.submit()
    submission_function.assert_called_with(["a"])

    widget.display("test data")
    assert widget.data == []
    assert not any(
        button.button.value for button in widget.class_selector.buttons
    )


def test_that_keys_toggle_buttons():
    widget = generic.MulticlassLabeller(options=["a", "b"])
    event = {"type": "keyup", "key": "1"}
    widget._handle_keystroke(event)
    assert widget.data == ["a"]
    event = {"type": "keyup", "key": "2"}
    widget._handle_keystroke(event)
    assert widget.data == ["a", "b"]


def test_that_freetext_adds_buttons():
    widget = generic.MulticlassLabeller(options=["a", "b"])
    widget.freetext_widget.value = "c"
    widget.freetext_submission(widget.freetext_widget)
    assert widget.options == ["a", "b", "c"]
    assert len(widget.class_selector.buttons) == 3
    assert widget.data == ["c"]


def test_that_recent_freetext_blocks_submission_on_enter(mocker):
    widget = generic.MulticlassLabeller(options=["a", "b"])
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)
    event = {"type": "keyup", "key": "Enter"}
    widget._freetext_timestamp = time.time()
    widget._handle_keystroke(event)
    submission_function.assert_not_called()
    widget._freetext_timestamp = time.time() - 1.0
    widget._handle_keystroke(event)
    submission_function.assert_called_once_with([])


def test_that_new_buttons_are_removed(mocker):
    widget = generic.MulticlassLabeller(options=["a", "b"])
    widget.freetext_widget.value = "c"
    widget.freetext_submission(widget.freetext_widget)
    undo_function: MagicMock = mocker.MagicMock()
    widget.on_undo(undo_function)
    assert widget.options == ["a", "b", "c"]
    assert len(widget.class_selector.buttons) == 3
    assert widget.data == ["c"]
    assert len(widget._undo_queue) == 1
    widget.undo()
    assert len(widget._undo_queue) == 0
    assert widget.options == ["a", "b"]
    assert len(widget.class_selector.buttons) == 2
    assert widget.data == []
    undo_function.assert_not_called()
    widget.undo()
    assert widget.options == ["a", "b"]
    assert len(widget.class_selector.buttons) == 2
    assert widget.data == []
    undo_function.assert_called_once()
