from ipyannotations.images.canvases.shapes import Polygon, Point, BoundingBox

from hypothesis import given, assume, infer, example, strategies


TEST_POLYGON_POINTS_OPEN = [(0, 0), (0, 50), (50, 50), (50, 0)]
TEST_POLYGON_POINTS_CLOSED = [(0, 0), (0, 50), (50, 50), (50, 0), (0, 0)]


# ----------------
# Polygons


@given(poly=infer)
def test_polygon_round_trips(poly: Polygon):
    assert poly == Polygon.from_data(poly.data)


@given(poly=infer)
def test_polygon_length(poly: Polygon):
    assert len(poly) == len(poly.points)


@given(poly=infer)
def test_polygon_closed_property(poly: Polygon):

    # polygon has to have more points than to be closed
    assume(len(poly.points) > 2)

    assert poly.closed == (poly.points[0] == poly.points[-1])

    # manually close it & test it worked
    poly.append(poly.points[0])
    assert poly.closed


@given(poly=infer)
def test_moving_individual_points(poly: Polygon):

    assume(len(poly.points) > 3)

    poly.move_point(0, (25, 25))

    assert poly.points[0] == (25, 25)


@given(poly=infer)
def test_that_adding_point_close_by_closes(poly: Polygon):

    assume(len(poly.points) > 3)

    start_point = poly.points[0]
    max_dist = poly.close_threshold
    approximate_nearby = (start_point[0] + max_dist // 2, start_point[1])

    poly.append(approximate_nearby)

    assert poly.closed


@given(poly=infer)
def test_that_polygon_doesnt_close_if_only_two_points(poly: Polygon):

    assume(len(poly.points) == 1)

    start_point = poly.points[0]
    max_dist = poly.close_threshold
    approximate_nearby = (start_point[0] + max_dist // 2, start_point[1])

    poly.append(approximate_nearby)

    assert not poly.closed


@given(poly=infer)
@example(poly=Polygon())
def test_getting_xy_lists_works(poly: Polygon):

    xlist, ylist = poly.xy_lists

    assert all(x == xy[0] for x, xy in zip(xlist, poly.points))
    assert all(y == xy[1] for y, xy in zip(ylist, poly.points))


# -------------------------
# Points


@given(p=infer)
def test_point_round_trips(p: Point):
    assert p == Point.from_data(p.data)


@given(p=infer, q=infer)
def test_point_move(p: Point, q: Point):
    #  test moving point from A to B
    p.move(*q.coordinates)
    assert p.coordinates == q.coordinates


# -------------------------
# Boxes


@given(p=infer)
def test_box_round_trips(p: BoundingBox):
    assert p == BoundingBox.from_data(p.data)


@given(p=infer, q=infer, idx=strategies.integers(min_value=0, max_value=3))
def test_box_corner_move(p: BoundingBox, q: Point, idx):
    #  test moving point from A to B
    p.move_corner(idx, *q.coordinates)

    x0, y0, x1, y1 = p.data["xyxy"]

    assert x0 <= x1
    assert y0 <= y1
    assert q.coordinates[0] in (x0, x1)
    assert q.coordinates[1] in (y0, y1)


@given(p=infer)
def test_box_corner_property(p: BoundingBox):

    corners = p.corners

    assert corners[0] <= corners[1]
    assert corners[0] <= corners[2]
    assert corners[0] <= corners[3]
