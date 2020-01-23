from typing import Tuple


def hex_to_rgb(value: str) -> Tuple[int, int, int]:
    value = value.lstrip("#")
    lv = len(value) // 3
    rgb: Tuple[int, int, int] = (
        int(value[0:lv], 16),
        int(value[lv : 2 * lv], 16),
        int(value[2 * lv : 3 * lv], 16),
    )
    return rgb


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    if not all(0 <= i <= 255 for i in rgb):
        raise ValueError(
            "RGB integers need to be between 0 and 255 (inclusive)."
        )
    return "#%02x%02x%02x" % rgb


def rgba_to_html_string(rgba: Tuple[int, int, int, float]) -> str:
    if len(rgba) == 4:
        return f"rgba({rgba[0]}, {rgba[1]}, {rgba[2]}, {rgba[3]:.3f})"
    elif len(rgba) == 3:
        return f"rgb({rgba[0]}, {rgba[1]}, {rgba[2]})"
    else:
        raise ValueError("You did not pass a valid color tuple")
