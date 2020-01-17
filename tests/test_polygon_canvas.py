from typing import List, Tuple, Union
from hypothesis import given, infer, strategies, assume
from math import isfinite
from unittest.mock import MagicMock, patch
import ipycanvas
from ipyannotations.images.canvases import PolygonAnnotationCanvas
from ipyannotations.images.canvases.shapes import Polygon, Point


@given(data=infer)
def test_reading_and_setting_data(data: List[Polygon]):

    c = PolygonAnnotationCanvas()

    serialised_data = [polygon.data for polygon in data]

    with patch.object(c, "re_draw") as mock_draw:
        c.data = serialised_data
        mock_draw.assert_called()

    assert all(p1 == p2 for p1, p2 in zip(c.polygons, data))

    print(c.data)
    print("type" in serialised_data)
    assert c.data == serialised_data


@given(point=infer, other_data=infer)
def test_click_handling(point: Point, other_data: List[Polygon]):

    point = point.coordinates
    assume(isfinite(point[0]) and isfinite(point[1]))

    canvas = PolygonAnnotationCanvas()

    assert canvas.current_polygon.points == []

    canvas.on_click(*point)
    assert canvas.current_polygon.points == [
        (round(point[0]), round(point[1]))
    ]


@given(data=infer)
def test_drawing_invokes_canvas_line_to(data: List[Polygon]):

    canvas = PolygonAnnotationCanvas()

    with patch.object(ipycanvas.Canvas, "line_to") as mock_line_to:
        canvas.data = [poly.data for poly in data]

    for polygon in data:
        if len(polygon.points) > 1:
            for point in polygon.points[1:]:
                mock_line_to.assert_any_call(*point)


@given(polygon=infer)
def test_closing_current_polygon(polygon: Polygon):

    canvas = PolygonAnnotationCanvas()
    canvas.current_polygon = polygon

    assume(all((0, 0) < point < canvas.size for point in polygon.points))
    assume(not polygon.closed)
    assume(len(polygon) > 2)

    poly_points = polygon.points.copy()
    poly_start = poly_points[0]

    closing_click = (
        poly_start[0],
        min([canvas.size[1], poly_start[1] + (canvas.point_size - 1)]),
    )

    canvas.on_click(*closing_click)

    print(poly_points)
    print(closing_click)

    assert len(canvas.polygons) == 1
    assert canvas.polygons[0].points[:-1] == poly_points
    # test current polygon is reset
    assert canvas.current_polygon.points == []


@given(polygon=infer, polygons=infer)
def test_editing_mode(polygon: Polygon, polygons: List[Polygon]):

    assume(len(polygon) > 2)

    canvas = PolygonAnnotationCanvas()
    # canvas.polygons = polygons
    canvas.current_polygon = polygon

    pre_move_points = polygon.points.copy()

    canvas.editing = True
    # test that dragging is none by default
    assert canvas.dragging is None

    # clicking on a point sets drag function:
    point_to_drag = polygon.points[0]
    point_target = (50, 50)
    canvas.on_click(*point_to_drag)
    assert canvas.dragging is not None

    # moving mouse moves the point:
    canvas.on_drag(*point_target)
    canvas.on_release(*point_target)

    # test point has moved
    assert canvas.current_polygon.points[0] == (50, 50)
    # test everything else stayed put
    assert canvas.current_polygon.points[1:] == pre_move_points[1:]

    # test release re-set dragging
    assert canvas.dragging is None

    # test undoing moves the point back
    callback = canvas._undo_queue.pop()
    callback()
    assert canvas.current_polygon.points == pre_move_points


@given(polygon=infer)
def test_dragging_without_edit_mode(polygon: Polygon):

    assume(len(polygon) > 4)

    canvas = PolygonAnnotationCanvas()
    canvas.editing = False
    canvas.polygons = [polygon]

    point_to_drag = polygon.points[0]
    point_target = (50, 50)

    canvas.on_click(*point_to_drag)
    canvas.on_drag(*point_target)

    # test point has not moved
    assert canvas.polygons[0].points[0] == point_to_drag


def test_undoing():

    canvas = PolygonAnnotationCanvas()

    coords = [(10, 10), (20, 10), (20, 20), (10, 20)]

    # click a polygon together:
    for coord in coords:
        canvas.on_click(*coord)

    assert canvas.current_polygon.points == coords

    # now undo and check coordinates:
    callback = canvas._undo_queue.pop()
    callback()
    assert canvas.current_polygon.points == coords[:-1]

    # finish the polygon:
    canvas.on_click(*coords[-1])
    canvas.on_click(*coords[0])
    assert len(canvas.polygons) == 1
    callback = canvas._undo_queue.pop()
    callback()
    assert len(canvas.polygons) == 0
    assert canvas.current_polygon.points == coords
