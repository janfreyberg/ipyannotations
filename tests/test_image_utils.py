import numpy as np
import pytest
import io
from PIL import Image
from unittest.mock import patch, MagicMock
import ipywidgets
from ipyannotations.images.canvases.image_utils import load_img, adjust


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
        1.5, abs=1 / 256
    )
