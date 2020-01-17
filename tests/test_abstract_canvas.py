import ipywidgets as widgets
import tempfile
import pathlib
from unittest.mock import patch
from hypothesis import given, assume, infer
from typing import Union

import numpy as np
from PIL import Image

from ipyannotations.images.canvases._abstract import AbstractAnnotationCanvas
from ipyannotations.images.canvases.utils import fit_image

# ImageTypes =


@given(img=infer)
def test_that_loading_image_clears_data(
    img: Union[widgets.Image, np.ndarray, Image.Image]
):

    with patch.object(
        AbstractAnnotationCanvas, "_init_empty_data"
    ) as mock_init_empty_data:
        canvas = AbstractAnnotationCanvas()
        mock_init_empty_data.reset_mock()
        canvas.load_image(img)

    mock_init_empty_data.assert_called_once()


@given(img=infer)
def test_that_loading_image_from_path(img: Image.Image):

    with tempfile.TemporaryDirectory(dir=".") as tmp:
        tmp = pathlib.Path(tmp)
        tmp = tmp / "testfile.jpg"
        img.save(tmp)

        with patch.object(
            AbstractAnnotationCanvas, "_init_empty_data"
        ) as mock_init_empty_data:
            canvas = AbstractAnnotationCanvas()
            mock_init_empty_data.reset_mock()
            canvas.load_image(tmp)

    mock_init_empty_data.assert_called_once()


@given(img=infer)
def test_that_fit_image_always_fits_image(img: widgets.Image):

    with patch.object(AbstractAnnotationCanvas, "_init_empty_data"):
        canvas = AbstractAnnotationCanvas()

    x0, y0, x1, y1 = fit_image(img, canvas)

    assert (x1, y1) < canvas.size
