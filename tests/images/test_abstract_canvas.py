import pathlib
import tempfile
from typing import Tuple, Union
from unittest.mock import patch

import ipywidgets as widgets
import numpy as np
from hypothesis import assume, given, infer, settings, strategies
from PIL import Image

from ipyannotations.images.canvases._abstract import AbstractAnnotationCanvas
from ipyannotations.images.canvases.image_utils import fit_image

# ImageTypes =


@settings(deadline=None)
@given(img=infer)
def test_that_loading_image_clears_data(
    img: Union[widgets.Image, np.ndarray, Image.Image]
):

    with patch.object(
        AbstractAnnotationCanvas, "init_empty_data"
    ) as mock_init_empty_data:
        canvas = AbstractAnnotationCanvas()
        mock_init_empty_data.reset_mock()
        canvas.load_image(img)

    mock_init_empty_data.assert_called_once()


@settings(deadline=None)
@given(img=infer)
def test_that_loading_image_from_path(img: Image.Image):

    with tempfile.TemporaryDirectory(dir=".") as tmp:
        tmp = pathlib.Path(tmp)
        tmp = tmp / "testfile.jpg"
        img.save(tmp)

        with patch.object(
            AbstractAnnotationCanvas, "init_empty_data"
        ) as mock_init_empty_data:
            canvas = AbstractAnnotationCanvas()
            mock_init_empty_data.reset_mock()
            canvas.load_image(tmp)

    mock_init_empty_data.assert_called_once()


@given(img=infer)
def test_that_fit_image_always_fits_image(img: widgets.Image):

    with patch.object(AbstractAnnotationCanvas, "init_empty_data"):
        canvas = AbstractAnnotationCanvas()

    x0, y0, x1, y1, _, _ = fit_image(img, canvas)

    assert (x1, y1) < canvas.size


@given(
    img=infer, click_x=strategies.floats(0, 1), click_y=strategies.floats(0, 1)
)
def test_that_points_clicked_get_translated_correctly(
    img: widgets.Image, click_x: float, click_y: float
):
    with patch.object(AbstractAnnotationCanvas, "init_empty_data"):
        canvas = AbstractAnnotationCanvas()
        canvas.load_image(img)

    x0, y0, width, height, img_width, img_height = fit_image(img, canvas)
    assume((img_width, img_height) > (20, 20))

    click_x = round(x0 + click_x * width)
    click_y = round(y0 + click_y * height)

    assert (
        (0, 0)
        <= canvas.canvas_to_image_coordinates((click_x, click_y))
        <= (img_width, img_height)
    )

    round_trip_x, round_trip_y = canvas.image_to_canvas_coordinates(
        canvas.canvas_to_image_coordinates((click_x, click_y))
    )
    assert np.isclose(round_trip_x, click_x) and np.isclose(
        round_trip_y, click_y, atol=1
    )

    # assert (0, 0) <= canvas.image_to_canvas_coordinates((0, 0)) <= canvas.size
