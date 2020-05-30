import pathlib
import tempfile
from typing import Union
from unittest.mock import patch

import ipywidgets as widgets
import numpy as np
from PIL import Image
from hypothesis import given, infer
from ipyannotations.images.canvases._abstract import AbstractAnnotationCanvas

from src.ipyannotations.images.canvases.image_utils import fit_image


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

