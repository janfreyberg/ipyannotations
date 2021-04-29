from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Tuple

from .image_utils import dist


@dataclass
class Polygon:
    points: List[Tuple[int, int]] = field(default_factory=list)
    label: Optional[str] = None
    close_threshold: ClassVar[int] = 5

    def append(self, point: Tuple[int, int]):
        """Add a point to the polygon.

        Parameters
        ----------
        point : Tuple[int, int]
            The (x, y) coordinates of the point.
        """
        point = (round(point[0]), round(point[1]))
        self.points.append(point)
        if self._is_closed():
            # ensure last point is identical to first:
            self.points.pop(-1)
            self.points.append(self.points[0])

    @property
    def xy_lists(self):
        if len(self.points) == 0:
            return [], []
        return list(map(list, zip(*self.points)))

    @property
    def xs(self):
        return [point[0] for point in self.points]

    @property
    def ys(self):
        return [point[1] for point in self.points]

    @property
    def closed(self) -> bool:
        return len(self.points) > 2 and self.points[0] == self.points[-1]

    def _is_closed(self) -> bool:

        if len(self) < 3:
            return False

        return dist(self.points[0], self.points[-1]) < self.close_threshold

    def __len__(self) -> int:
        return len(self.points)

    def move_point(self, point_index: int, point: Tuple[int, int]):
        """Move a point in the polygon.

        Parameters
        ----------
        point_index : int
            The index of the point.
        point : Tuple[int, int]
            The new coordinates.
        """
        point = (round(point[0]), round(point[1]))
        self.points[point_index] = point

    @property
    def data(self):
        return {"type": "polygon", "label": self.label, "points": self.points}

    @classmethod
    def from_data(cls, data: dict):
        """Create a polygon from a dictionary.

        Parameters
        ----------
        data : dict
            The data should have the keys: 'type', 'label', 'coordinates'. The
            value for the 'type' key needs to be 'polygon'.
        """
        type_ = data.pop("type")
        if type_ == "polygon":
            return cls(**data)


@dataclass
class Point:
    coordinates: Tuple[int, int]
    label: str = ""

    def __post_init__(self):
        self.coordinates = tuple(map(round, self.coordinates))

    def move(self, x: int, y: int):
        """Move a point to new coordinates.

        Parameters
        ----------
        x : int
        y : int
        """
        self.coordinates = (round(x), round(y))

    @property
    def data(self) -> dict:
        return {
            "type": "point",
            "label": self.label,
            "coordinates": self.coordinates,
        }

    @classmethod
    def from_data(cls, data: dict):
        """Create a point from a dictionary.

        Parameters
        ----------
        data : dict
            The data should have the keys: 'type', 'label', 'coordinates'. The
            value for the 'type' key needs to be 'point'.
        """
        type_ = data.pop("type")
        if type_ == "point":
            return cls(**data)


@dataclass
class BoundingBox:
    xyxy: Tuple[int, int, int, int]
    label: str = ""

    def __post_init__(self):
        self.xyxy = tuple(map(round, self.xyxy))

    def move_corner(self, idx: int, new_x: int, new_y: int):
        """Move a corner of the bounding

        Parameters
        ----------
        idx : int
            The corner to be moved, starting with 0 in the top left
            corner, going counter-clockwise.
        new_x : int
        new_y : int
        """
        x_idx, y_idx = [(0, 1), (0, 3), (2, 3), (2, 1)][idx]
        new_xy = list(self.xyxy)
        new_xy[x_idx] = round(new_x)
        new_xy[y_idx] = round(new_y)
        self.xyxy = tuple(new_xy)  # type: ignore

    @property
    def corners(self) -> List[Tuple[int, int]]:
        x0, y0, x1, y1 = self.xyxy
        return [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]

    @property
    def data(self) -> dict:
        x0, y0, x1, y1 = self.xyxy
        return {
            "type": "box",
            "label": self.label,
            "xyxy": (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)),
        }

    @classmethod
    def from_data(cls, data: dict):
        """Create a box from a dictionary.

        Parameters
        ----------
        data : dict
            The data should have the keys: 'type', 'label', 'coordinates'. The
            value for the 'type' key needs to be 'box'.
        """
        type_ = data.pop("type")
        if type_ == "box":
            return cls(**data)
        else:
            raise ValueError(
                "The key 'type' in the data you supplied is not 'box'"
            )
