import io
from typing import Tuple
from unittest.mock import MagicMock, patch

import ipywidgets
import ipywidgets as widgets
import numpy as np
import pytest
from hypothesis import assume, given, infer
from PIL import Image
from pytest_mock import MockerFixture

from ipyannotations.images.canvases._abstract import AbstractAnnotationCanvas
from ipyannotations.images.canvases.image_utils import (
    adjust,
    fit_image,
    load_img,
    only_inside_image,
    trigger_redraw,
)


@pytest.fixture
def image_array():
    return np.random.randint(90, 110, (50, 50, 3), dtype=np.uint8)


@pytest.fixture
def pillow_image(image_array):
    return Image.fromarray(image_array)


@pytest.fixture(params=[True, False])
def image_file_path(pillow_image, tmp_path, request):
    path = tmp_path / "img.jpg"
    pillow_image.save(path)
    if request.param:
        return path
    else:
        return str(path)


def test_load_img_fails_with_random_objects():
    class Dummy:
        pass

    with pytest.raises(ValueError):
        load_img(Dummy())


def test_load_img_with_files(image_file_path):

    with patch.object(ipywidgets, "Image") as mockImage:
        load_img(image_file_path)
        mockImage.assert_called_once()
        assert isinstance(mockImage.call_args[1]["value"], bytes)

    with pytest.raises(ValueError):
        load_img("/not/a/real/file")


def test_load_img_from_array(image_array):

    with patch.object(ipywidgets, "Image") as mockImage:
        load_img(image_array)
        mockImage.assert_called_once()
        assert isinstance(mockImage.call_args[1]["value"], bytes)


def test_load_img_directly(pillow_image):

    with patch.object(ipywidgets, "Image") as mockImage:
        load_img(pillow_image)
        mockImage.assert_called_once()
        assert isinstance(mockImage.call_args[1]["value"], bytes)


@patch("requests.get")
def test_load_img_with_url(mock_get: MagicMock):
    test_url = r"http://www.my-test-url.com/hi.jpg"
    mock_get.return_value.configure_mock(content=b"hi")

    with patch.object(ipywidgets, "Image") as mockImage:
        load_img(test_url)
        mockImage.assert_called_with(value=b"hi")


def test_changing_brightness(image_array):

    img_widget = load_img(image_array)
    adjusted_widget = adjust(
        img_widget, contrast_factor=1.0, brightness_factor=1.5
    )
    new_image_array = np.array(
        Image.open(io.BytesIO(initial_bytes=adjusted_widget.value))
    )

    assert (new_image_array / image_array).mean() == pytest.approx(
        1.5, abs=0.01
    )


@given(img=infer)
def test_fit_image_produces_sensible_numbers(img: widgets.Image):
    with patch.object(AbstractAnnotationCanvas, "init_empty_data"):
        canvas = AbstractAnnotationCanvas()
    x0, y0, width, height, img_width, img_height = fit_image(img, canvas)
    assume((img_width, img_height) > (20, 20))
    # test aspect ratio:
    assert np.isclose(width / height, img_width / img_height, rtol=0.05)


def test_only_inside_image(mocker: MockerFixture):

    spy = mocker.MagicMock()

    class TestCanvas:
        image_extent = (100, 100, 200, 200)

        @only_inside_image
        def test_method(self, x, y):
            spy(x, y)

        def canvas_to_image_coordinates(self, xy):
            return xy[0] - 100, xy[1] - 100

    test_canvas = TestCanvas()
    test_canvas.test_method(0, 0)
    spy.assert_not_called()
    test_canvas.test_method(150, 150)
    spy.assert_called_once_with(50, 50)


def test_trigger_redraw(mocker: MockerFixture):
    spy = mocker.MagicMock()

    class TestCanvas:
        image_extent = (100, 100, 200, 200)

        @trigger_redraw
        def test_method(self):
            pass

        def re_draw(self):
            spy()

    test_canvas = TestCanvas()

    test_canvas.test_method()
    spy.assert_called_once()
