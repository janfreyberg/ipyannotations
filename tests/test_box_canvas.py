from typing import List, Tuple, Union
from hypothesis import given, infer, strategies, assume
from math import isfinite, pi
from unittest.mock import MagicMock, patch
import unittest
import ipycanvas
from ipyannotations.images.canvases import BoundingBoxAnnotationCanvas
from ipyannotations.images.canvases.shapes import BoundingBox
from ipyannotations.images.canvases.utils import dist

from pytest_check import check


@given(data=infer)
def test_reading_and_setting_data(data: List[BoundingBox]):

    canvas = BoundingBoxAnnotationCanvas()

    with patch.object(canvas, "re_draw") as mock_draw:
        canvas.data = [box.data for box in data]
        mock_draw.assert_called()

    assert all(box1 == box2 for box1, box2 in zip(canvas.annotations, data))
    assert canvas.data == [box.data for box in data]


@given(
    click_coords=strategies.coordinates(), drag_coords=strategies.coordinates()
)
def test_click_handling_without_drag(click_coords, drag_coords):

    canvas = BoundingBoxAnnotationCanvas()
    with check:
        assert canvas.annotations == [], "annotations not empyt at init"
        assert (
            canvas._proposed_annotation is None
        ), "proposed annotation not None at init"

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
def test_click_handling_with_drag(click_coords, drag_coords):

    assume(click_coords != drag_coords)

    canvas = BoundingBoxAnnotationCanvas()
    with check:
        assert canvas.annotations == [], "annotations not empyt at init"
        assert (
            canvas._proposed_annotation is None
        ), "proposed annotation not None at init"

    canvas.on_click(*click_coords)

    with check:
        assert canvas.annotations == []
        assert canvas._proposed_annotation is not None
        assert all(
            corner == click_coords
            for corner in canvas._proposed_annotation.corners
        )

    canvas.on_drag(*drag_coords)

    with check:
        assert canvas.annotations == []
        assert canvas._proposed_annotation is not None
        assert click_coords in canvas._proposed_annotation.corners
        assert drag_coords in canvas._proposed_annotation.corners

    canvas.on_release(*drag_coords)

    with check:
        assert canvas.annotations != []
        assert canvas._proposed_annotation is None
        assert click_coords in canvas.annotations[0].corners
        assert drag_coords in canvas.annotations[0].corners


@given(
    click_coords=strategies.coordinates(), drag_coords=strategies.coordinates()
)
def test_undo_creating_new_box(click_coords, drag_coords):

    assume(click_coords != drag_coords)

    canvas = BoundingBoxAnnotationCanvas()

    canvas.on_click(*click_coords)
    canvas.on_drag(*drag_coords)
    canvas.on_release(*drag_coords)

    assert len(canvas.data) == 1
    assert len(canvas._undo_queue) == 1

    canvas._undo_queue.pop()()

    assert len(canvas.data) == 0


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
    canvas.data = [box.data]
    canvas.editing = True

    assume(click_coords != drag_coords)
    assume(
        all(
            dist(click_coords, corner) > canvas.point_size
            for corner in box.corners
        )
    )
    assume(
        all(
            dist(drag_coords, corner) > canvas.point_size
            for corner in box.corners
        )
    )

    # breakpoint()

    canvas.on_click(*click_coords)
    canvas.on_drag(*drag_coords)
    canvas.on_release(*drag_coords)

    unittest.TestCase().assertCountEqual(
        canvas.annotations[0].corners, previous_corners
    )


@given(box=infer, drag_coords=strategies.coordinates())
def test_dragging_corner_in_edit_mode(box: BoundingBox, drag_coords):
    assume(drag_coords not in box.corners)
    previous_corners = box.corners

    click_coords = box.corners[3]

    canvas = BoundingBoxAnnotationCanvas()
    canvas.data = [box.data]
    canvas.editing = True

    canvas.on_click(*click_coords)
    canvas.on_drag(*drag_coords)
    canvas.on_release(*drag_coords)

    assert drag_coords in canvas.annotations[0].corners

    # check undo:
    assert len(canvas._undo_queue) == 1
    canvas._undo_queue.pop()()
    assert drag_coords not in canvas.annotations[0].corners
    unittest.TestCase().assertCountEqual(
        canvas.annotations[0].corners, previous_corners
    )
