import unittest
from math import isfinite, pi
from typing import List, Tuple, Union
from unittest.mock import MagicMock, patch

import ipycanvas
import ipywidgets as widgets
import numpy as np
from hypothesis import assume, given, infer, settings, strategies
from pytest_check import check

from ipyannotations.images.canvases import BoundingBoxAnnotationCanvas
from ipyannotations.images.canvases.image_utils import dist
from ipyannotations.images.canvases.shapes import BoundingBox

IMAGE = np.random.randint(0, 256, size=(500, 700, 3), dtype=np.uint8)


@given(data=infer)
def test_reading_and_setting_data(data: List[BoundingBox]):

    canvas = BoundingBoxAnnotationCanvas()

    with patch.object(canvas, "re_draw") as mock_draw:
        canvas.data = [box.data for box in data]
        mock_draw.assert_called()

    assert all(box1 == box2 for box1, box2 in zip(canvas.annotations, data))
    assert canvas.data == [box.data for box in data]


@settings(deadline=None)
@given(click=strategies.coordinates(), drag=strategies.coordinates())
def test_box_creation_workflow(click, drag):
    assume(click != drag)
    canvas = BoundingBoxAnnotationCanvas()
    canvas.load_image(IMAGE)
    assert canvas.annotations == []
    assert canvas._proposed_annotation is None

    canvas.on_click(*click)
    assert canvas.annotations == []
    assert canvas._proposed_annotation.corners == 4 * [click]

    canvas.on_drag(*drag)
    assert canvas.annotations == []
    assert click in canvas._proposed_annotation.corners
    assert drag in canvas._proposed_annotation.corners

    canvas.on_release(*drag)
    print(canvas._proposed_annotation)
    assert canvas._proposed_annotation is None
    assert len(canvas.annotations) == 1
    assert click in canvas.annotations[0].corners
    assert drag in canvas.annotations[0].corners


@given(click_coords=strategies.coordinates())
def test_single_click_handling(click_coords):

    canvas = BoundingBoxAnnotationCanvas()
    canvas.load_image(IMAGE)

    canvas.on_click(*click_coords)
    with check:
        assert canvas.annotations == []
        assert canvas._proposed_annotation is not None
        assert all(
            corner == click_coords
            for corner in canvas._proposed_annotation.corners
        )

    canvas.on_release(*click_coords)
    with check:
        assert canvas.annotations == []
        assert canvas._proposed_annotation is None


@given(
    click_coords=strategies.coordinates(), drag_coords=strategies.coordinates()
)
def test_undo_creating_new_box(click_coords, drag_coords):

    assume(click_coords != drag_coords)
    canvas = BoundingBoxAnnotationCanvas()
    canvas.load_image(IMAGE)
    canvas.on_click(*click_coords)
    canvas.on_drag(*drag_coords)
    canvas.on_release(*drag_coords)

    assert len(canvas.data) == 1
    assert len(canvas._undo_queue) == 1
    assert canvas._proposed_annotation is None
    canvas._undo_queue.pop()()
    assert len(canvas.data) == 0
    assert canvas._proposed_annotation is None


@settings(deadline=None)
@given(
    box=infer,
    click_coords=strategies.coordinates(),
    drag_coords=strategies.coordinates(),
)
def test_dragging_empty_in_edit_mode(
    box: BoundingBox, click_coords, drag_coords
):

    previous_corners = box.corners

    canvas = BoundingBoxAnnotationCanvas()
    canvas.load_image(IMAGE)
    canvas.data = [box.data]
    canvas.editing = True

    assume(click_coords != drag_coords)
    # ensure the clicks are not on the corners:
    assume(
        all(
            dist(drag_coords, corner) > canvas.point_size
            and dist(click_coords, corner) > canvas.point_size
            for corner in box.corners
        )
    )
    canvas.on_click(*click_coords)
    canvas.on_drag(*drag_coords)
    canvas.on_release(*drag_coords)

    assert set(canvas.annotations[0].corners) == set(previous_corners)


@given(box=infer, drag_coords=strategies.coordinates())
def test_dragging_corner_in_edit_mode(box: BoundingBox, drag_coords):
    assume(drag_coords not in box.corners)
    previous_corners = box.corners

    click_coords = box.corners[3]

    canvas = BoundingBoxAnnotationCanvas()
    canvas.load_image(IMAGE)
    canvas.data = [box.data]
    canvas.editing = True

    canvas.on_click(*click_coords)
    canvas.on_drag(*drag_coords)
    canvas.on_release(*drag_coords)

    assert drag_coords in canvas.annotations[0].corners

    assert len(canvas._undo_queue) == 1
    canvas._undo_queue.pop()()
    assert drag_coords not in canvas.annotations[0].corners
    unittest.TestCase().assertCountEqual(
        canvas.annotations[0].corners, previous_corners
    )
