from math import isfinite, pi
from typing import List, Tuple, Union
from unittest.mock import MagicMock, patch

import ipycanvas
import numpy as np
from hypothesis import assume, given, infer, settings, strategies
from pytest_mock.plugin import MockerFixture

from ipyannotations.images.canvases import PointAnnotationCanvas
from ipyannotations.images.canvases.shapes import Point

IMAGE = np.random.randint(0, 256, size=(500, 700, 3), dtype=np.uint8)
IMAGE_SMALL = np.random.randint(0, 256, size=(400, 600, 3), dtype=np.uint8)


@settings(deadline=None)
@given(data=infer)
def test_reading_and_setting_data(data: List[Point]):

    canvas = PointAnnotationCanvas()
    canvas.load_image(IMAGE)

    with patch.object(canvas, "re_draw") as mock_draw:
        canvas.data = [point.data for point in data]
        mock_draw.assert_called()

    assert all(p1 == p2 for p1, p2 in zip(canvas.points, data))
    assert canvas.data == [point.data for point in data]


@given(point=infer)
def test_click_handling(point: Point):

    point = point.coordinates
    canvas = PointAnnotationCanvas()
    canvas.load_image(IMAGE)
    assert canvas.points == []
    canvas.on_click(*point)
    assert canvas.points[-1].coordinates == (round(point[0]), round(point[1]))


def test_data_is_translated():
    canvas = PointAnnotationCanvas()
    canvas.load_image(IMAGE_SMALL)
    canvas.on_click(0, 100)
    assert canvas.points == []
    canvas.on_click(100, 0)
    assert canvas.points == []
    canvas.on_click(50, 50)
    assert canvas.points[-1].coordinates == (0, 0)


@settings(deadline=None)
@given(data=infer)
def test_drawing_invokes_canvas_line_to(data: List[Point]):

    canvas = PointAnnotationCanvas()
    canvas.load_image(IMAGE)
    with patch.object(ipycanvas.Canvas, "fill_arc") as mock_fill_arc:
        canvas.data = [point.data for point in data]
        pass

    for point in data:
        mock_fill_arc.assert_any_call(
            *point.coordinates, canvas.point_size, 0, 2 * pi
        )


@given(points=infer)
def test_editing_mode(points: List[Point]):
    assume(len(points) > 1)
    canvas = PointAnnotationCanvas()
    canvas.load_image(IMAGE)
    canvas.points = points
    canvas.editing = True

    pre_move_points = [point.data for point in points]

    # test that dragging is none by default
    assert canvas.dragging is None

    # clicking on a point sets drag function:
    point_to_drag = points[0].coordinates
    point_target = (50, 50)
    canvas.on_click(*point_to_drag)
    # check we're in dragging mode:
    assert canvas.dragging is not None

    # moving mouse moves the point:
    canvas.on_drag(*point_target)
    canvas.on_release(*point_target)

    # test point has moved
    assert canvas.points[0].coordinates == (50, 50)
    # test everything else stayed put
    assert canvas.data[1:] == pre_move_points[1:]

    # test release re-set dragging
    assert canvas.dragging is None

    # test undoing moves the point back
    callback = canvas._undo_queue.pop()
    callback()
    assert canvas.data == pre_move_points


@settings(deadline=None)
@given(point=infer)
def test_dragging_without_edit_mode(point: Point):

    canvas = PointAnnotationCanvas()
    canvas.load_image(IMAGE)
    canvas.data = [point.data]

    point_to_drag = point.coordinates
    point_target = (50, 50)

    canvas.on_click(*point_to_drag)
    canvas.on_drag(*point_target)

    # test point has not moved
    assert canvas.data[0] == point.data


@settings(deadline=None)
@given(points=infer)
def test_undo(points: List[Point]):
    assume(len(points) > 1)
    canvas = PointAnnotationCanvas()
    canvas.load_image(IMAGE)
    for point in points:
        canvas.on_click(*point.coordinates)

    assert len(canvas.points) == len(canvas.points)
    assert all(
        p1.coordinates == p2.coordinates
        for p1, p2 in zip(canvas.points, points)
    )

    callback = canvas._undo_queue.pop()
    callback()

    assert len(canvas.points) == (len(points) - 1)
    assert all(
        p1.coordinates == p2.coordinates
        for p1, p2 in zip(canvas.points, points)
    )
