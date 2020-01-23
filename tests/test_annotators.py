from unittest.mock import patch, MagicMock
from ipyannotations import PolygonAnnotator, PointAnnotator
from ipyannotations.images.annotator import Annotator
from ipyannotations.images.canvases import (
    PolygonAnnotationCanvas,
    PointAnnotationCanvas,
)


def test_creating_widgets():

    annotator = PolygonAnnotator()
    assert isinstance(annotator.canvas, PolygonAnnotationCanvas)

    annotator = PointAnnotator()
    assert isinstance(annotator.canvas, PointAnnotationCanvas)


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
    annotator.on_skip(mock_callback_1)
    annotator.on_skip(mock_callback_2)

    annotator.skip()
    mock_callback_1.assert_called_once()
    mock_callback_2.assert_called_once()


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
