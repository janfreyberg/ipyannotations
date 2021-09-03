import re

from hypothesis import given, strategies
import pytest

from ipyannotations.images.canvases.color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    rgba_to_html_string,
)

HEX_REGEX = re.compile(r"^(#)([0-9A-Fa-f]{8}|[0-9A-Fa-f]{6})$")
HTML_RGB_REGEX = re.compile(r"^(r)(g)(b)\(([0-9]{1,3}\,\ ){2}([0-9]{1,3})\)")
HTML_RGBA_REGEX = re.compile(
    r"^(r)(g)(b)(a)\(([0-9]{1,3}\,\ ){2}([0-9]{1,3})"
    + r"\, ([0-1]\.)([0-9]){1,10}\)$"
)

rgb_colors = strategies.tuples(
    strategies.integers(0, 255),
    strategies.integers(0, 255),
    strategies.integers(0, 255),
)

rgba_colors = strategies.tuples(
    strategies.integers(0, 255),
    strategies.integers(0, 255),
    strategies.integers(0, 255),
    strategies.floats(0, 1.0),
)


@given(rgb_colors)
def test_rgb_to_hex_and_back(color):
    hex_col = rgb_to_hex(color)
    assert HEX_REGEX.match(hex_col)
    assert hex_to_rgb(hex_col) == color


def test_rgb_to_hex_failure():
    color = (277, 128, 0)
    with pytest.raises(ValueError):
        hex_col = rgb_to_hex(color)


@given(rgb_colors)
def test_rgb_to_html(color):
    rgb_string = rgba_to_html_string(color)
    assert HTML_RGB_REGEX.match(rgb_string)
    for i in color:
        assert str(i) in rgb_string


@given(rgba_colors)
def test_rgba_to_html(color):
    rgb_string = rgba_to_html_string(color)
    assert HTML_RGBA_REGEX.match(rgb_string)
    for i in color:
        assert str(i) in rgb_string or str(round(i, 3)) in rgb_string
