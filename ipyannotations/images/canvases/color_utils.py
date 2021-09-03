from typing import Iterator, Tuple

from palettable.colorbrewer.qualitative import Set2_8


def hex_to_rgb(value: str) -> Tuple[int, int, int]:
    """Turn a hex color code to RGB ints.

    Parameters
    ----------
    value : str, the Hex color code

    Returns
    -------
    Tuple[int, int, int], the RGB values
    """
    value = value.lstrip("#")
    lv = len(value) // 3
    rgb: Tuple[int, int, int] = (
        int(value[0:lv], 16),
        int(value[lv : 2 * lv], 16),
        int(value[2 * lv : 3 * lv], 16),
    )
    return rgb


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Turn RGB values into Hex values.

    Parameters
    ----------
    rgb : Tuple[int, int, int]

    Returns
    -------
    str

    Raises
    ------
    ValueError
        If the values are not > 0 && < 255
    """
    if not all(0 <= i <= 255 for i in rgb):
        raise ValueError(
            "RGB integers need to be between 0 and 255 (inclusive)."
        )
    return "#%02x%02x%02x" % rgb


def rgba_to_html_string(rgba: Tuple[int, int, int, float]) -> str:
    """Create an HTML code from an RGBA tuple

    Parameters
    ----------
    rgba : Tuple[int, int, int, float] | Tuple[int, int, int]
        RGB values and an optional alpha value between 0 and 1.

    Returns
    -------
    str

    Raises
    ------
    ValueError
        If the color tuple is not either RGB or RGBA
    """
    if len(rgba) == 4:
        return f"rgba({rgba[0]}, {rgba[1]}, {rgba[2]}, {rgba[3]:.3f})"
    elif len(rgba) == 3:
        return f"rgb({rgba[0]}, {rgba[1]}, {rgba[2]})"
    else:
        raise ValueError("You did not pass a valid color tuple")


def set_colors() -> Iterator[str]:
    """An infinite iterator over the Set2 hex colors.

    Yields
    -------
    str
        A valid hex-string from the Set2 colors. 8 unique colors available.
    """
    while True:
        yield from Set2_8.hex_colors
