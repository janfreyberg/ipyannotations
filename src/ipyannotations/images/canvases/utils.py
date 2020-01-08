import io
from typing import Tuple, Callable, Sequence, Iterator, Optional, Any
import ipywidgets as widgets
from functools import wraps
from ipycanvas import Canvas
from PIL import Image
from palettable.colorbrewer.qualitative import Set2_8


def fit_image(img: widgets.Image, canvas: Canvas) -> Tuple[int, int, int, int]:
    img_width, img_height = Image.open(io.BytesIO(img.value)).size
    canvas_width, canvas_height = canvas.size

    height_ratio, width_ratio = (
        img_height / canvas_height,
        img_width / canvas_width,
    )
    if height_ratio <= 1 and width_ratio <= 1:
        # we can fill and center the whole image
        width, height = img_width, img_height
    elif height_ratio >= width_ratio:
        # height is the limiting factor:
        height = int(img_height / height_ratio)
        width = int(img_width / height_ratio)
    elif height_ratio <= width_ratio:
        # width is the limiting factor:
        height = int(img_height / width_ratio)
        width = int(img_width / width_ratio)
    # breakpoint()
    x, y = (canvas_width // 2 - width // 2, canvas_height // 2 - height // 2)
    # canvas.draw_image(img, x=x, y=y, width=height, height=width)
    return x, y, width, height


def set_colors() -> Iterator[str]:
    """An infinite iterator over the Set2 hex colors.

    Yields
    -------
    str
        A valid hex-string from the Set2 colors. 8 unique colors available.
    """
    while True:
        yield from Set2_8.hex_colors


def dist(q: Sequence[float], p: Sequence[float]) -> float:
    """Euclidian distance between two points.

    Parameters
    ----------
    q : Sequence[float]
        Point q
    p : Sequence[float]
        Point p

    Returns
    -------
    float
        The distance between point q and p.
    """
    return (sum((px - qx) ** 2.0 for px, qx in zip(p, q))) ** 0.5


def trigger_redraw(fn: Callable) -> Callable:
    """Method decorator for functions that need to trigger a re-draw.

    Parameters
    ----------
    fn : Callable
        The function that needs to trigger a re-draw, e.g. because it changes
        the appearance of the canvas.

    Returns
    -------
    Callable
        A wrapped function that, when called, calls the input function and then
        calls the re-draw method on the class.
    """

    @wraps(fn)
    def wrapped_fn(*args, **kwargs):
        outp = fn(*args, **kwargs)
        args[0].re_draw()
        return outp

    return wrapped_fn


def only_inside_image(
    fn: Callable[[Any, float, float], Optional[Any]]
) -> Callable:
    """Method decorator for function that needs to only work inside the image.

    The input should be a method that accepts x and y.

    Parameters
    ----------
    fn : Callable
        The method that accepts self, x and y.

    Returns
    -------
    Callable
        A wrapped function that, when called, returns None if x and y are not
        inside the image (indicated by self.image_extent)
    """

    @wraps(fn)
    def wrapped_fn(self, x, y):
        if not self.image_extent[0] <= x <= self.image_extent[2]:
            return
        if not self.image_extent[1] <= y <= self.image_extent[3]:
            return
        return fn(self, x, y)

    return wrapped_fn
