import collections

import pytest
import traitlets
from hypothesis import given, settings
from hypothesis import strategies as st

from ipyannotations.controls.togglebuttongroup import (
    ToggleButtonGroup,
    ToggleButtonWithHint,
)

same_elements = lambda x, y: collections.Counter(x) == collections.Counter(y)


@settings(deadline=None)
@given(options=st.lists(st.text(), unique=True))
def test_that_options_are_set(options):

    widget = ToggleButtonGroup(options)
    assert widget.options == options
    assert same_elements(
        [button.description for button in widget.buttons], options
    )
    widget = ToggleButtonGroup([])
    widget.options = options
    assert widget.options == options
    assert same_elements(
        [button.description for button in widget.buttons], options
    )


def test_that_values_are_read_correctly():

    widget = ToggleButtonGroup(["a", "b", "c"])
    assert widget.value == []

    widget.buttons[0].value = True
    assert widget.value == ["a"]

    widget.buttons[1].value = True
    assert same_elements(widget.value, ["a", "b"])


def test_that_toggle_changes_values():

    widget = ToggleButtonGroup(["a", "b", "c"])
    assert widget.value == []

    widget._toggle("a")
    assert widget.value == ["a"]

    widget._toggle("a")
    assert widget.value == []


def test_that_reset_sets_all_values_to_false():

    widget = ToggleButtonGroup(["a", "b", "c"])
    assert widget.value == []

    widget._toggle("a")
    widget._toggle("b")
    assert same_elements(widget.value, ["a", "b"])

    widget._reset()
    assert widget.value == []


def test_that_button_width_is_set_correctly():
    widget = ToggleButtonGroup(["a", "b"])
    assert widget.button_width == "50%"

    widget.button_width = 0.2
    assert widget.button_width == "20%"

    widget.button_width = 200
    assert widget.button_width == "200px"

    widget.button_width = "87%"
    assert widget.button_width == "87%"

    with pytest.raises(traitlets.TraitError):
        widget.button_width = {"test-set", "lol"}


def test_that_enter_exit_for_output_get_called(mocker):
    mock_enter = mocker.patch("ipywidgets.Output.__enter__")
    mock_exit = mocker.patch("ipywidgets.Output.__exit__")

    button = ToggleButtonWithHint("Hi", "50%")

    with button:
        pass

    assert mock_enter.call_count == 1
    assert mock_exit.call_count == 1
