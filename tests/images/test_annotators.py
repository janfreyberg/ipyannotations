from typing import Union
from unittest.mock import MagicMock, patch
import ipywidgets as widgets
import numpy as np
from PIL import Image
from ipyannotations.images import (
    PointAnnotator,
    PolygonAnnotator,
    BoxAnnotator,
)
from ipyannotations.images.canvases import shapes
from ipyannotations.images.annotator import Annotator
from ipyannotations.images.canvases import (
    PointAnnotationCanvas,
    PolygonAnnotationCanvas,
    BoundingBoxAnnotationCanvas,
)
from ipyannotations.images.canvases.abstract_canvas import (
    AbstractAnnotationCanvas,
)
from hypothesis import assume, given, infer, settings, strategies


class TestCanvas(AbstractAnnotationCanvas):
    """Test canvas to test the abstract canvas."""

    def init_empty_data(self):
        self.data = []


class TestAnnotator(Annotator):
    """Test Annotator to test the base implementation."""

    CanvasClass = TestCanvas


@settings(deadline=None)
@given(img=infer)
def test_annotator_load_image(
    img: Union[widgets.Image, np.ndarray, Image.Image]
):
    with patch.object(
        AbstractAnnotationCanvas, "load_image", autospec=True
    ) as patch_load_image, patch.object(
        AbstractAnnotationCanvas, "clear", autospec=True
    ) as patch_clear:
        annotator = TestAnnotator()
        annotator.display(img)
        patch_load_image.assert_called_once()
        patch_clear.assert_called_once()


def test_handling_keystrokes(mocker):
    widget = TestAnnotator(options=["a", "b"])
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)
    # test enter:
    widget.canvas.data = [{"test_data": "hello"}]
    widget._handle_keystroke({"type": "keyup", "key": "Enter"})
    submission_function.assert_called_once_with([{"test_data": "hello"}])
    # test the class selection:
    # (self.class_selector, "value"), (self.canvas, "current_class")
    assert widget.canvas.current_class == "a"
    widget._handle_keystroke({"type": "keyup", "key": "2"})
    assert widget.canvas.current_class == "b"
    widget._handle_keystroke({"type": "keyup", "key": "1"})
    assert widget.canvas.current_class == "a"


def test_data_post_processing(mocker):
    widget = TestAnnotator(
        options=["a", "b"], data_postprocessor=lambda data: data + ["extra"]
    )
    submission_function: MagicMock = mocker.MagicMock()
    widget.on_submit(submission_function)
    # test enter:
    widget.canvas.data = [{"test_data": "hello"}]
    assert widget.data == [{"test_data": "hello"}, "extra"]
    widget.submit()
    submission_function.assert_called_once_with(
        [{"test_data": "hello"}, "extra"]
    )


@given(polygon=infer, point=infer, box=infer, img=infer)
def test_creating_widgets_setting_and_reading_data(
    polygon: shapes.Polygon,
    point: shapes.Point,
    box: shapes.BoundingBox,
    img: widgets.Image,
):
    """Smoke test for initialisation."""
    annotator = PolygonAnnotator()
    annotator.display(img)
    assert isinstance(annotator.canvas, PolygonAnnotationCanvas)
    annotator.data = [polygon.data]
    assert annotator.canvas.data == [polygon.data] == annotator.data
    annotator = PointAnnotator()
    annotator.display(img)
    assert isinstance(annotator.canvas, PointAnnotationCanvas)
    annotator.data = [point.data]
    assert annotator.canvas.data == [point.data] == annotator.data
    annotator = BoxAnnotator()
    annotator.display(img)
    assert isinstance(annotator.canvas, BoundingBoxAnnotationCanvas)
    annotator.data = [box.data]
    assert annotator.canvas.data == [box.data] == annotator.data


def test_undo():

    mock_queue_callback = MagicMock()
    mock_base_callback = MagicMock()
    annotator = PolygonAnnotator()
    annotator.on_undo(mock_base_callback)

    annotator.undo()
    mock_base_callback.assert_called_once()
    mock_base_callback.reset_mock()

    annotator.canvas._undo_queue.append(mock_queue_callback)
    annotator.undo()
    mock_queue_callback.assert_called_once()
    mock_base_callback.assert_not_called()
    annotator.undo()
    mock_base_callback.assert_called_once()


def test_skip():
    mock_callback_1 = MagicMock()
    mock_callback_2 = MagicMock()
    annotator = PolygonAnnotator()
    annotator.on_submit(mock_callback_1)
    annotator.on_submit(mock_callback_2)

    annotator.skip()
    mock_callback_1.assert_called_once_with(None)
    mock_callback_2.assert_called_once_with(None)


def test_submit():
    mock_callback_1 = MagicMock()
    mock_callback_2 = MagicMock()
    # mock_data = MagicMock()
    annotator = PolygonAnnotator()
    annotator.on_submit(mock_callback_1)
    annotator.on_submit(mock_callback_2)

    with patch.object(PolygonAnnotator, "data") as mock_data:
        annotator.submit()
        mock_callback_1.assert_called_once_with(mock_data)
        mock_callback_2.assert_called_once_with(mock_data)
