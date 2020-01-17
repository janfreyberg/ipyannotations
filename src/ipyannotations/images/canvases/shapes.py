from typing import List, Tuple, Optional, ClassVar
from dataclasses import dataclass, field
from .utils import dist


@dataclass
class Polygon:
    points: List[Tuple[int, int]] = field(default_factory=list)
    label: Optional[str] = None
    close_threshold: ClassVar[int] = 5

    def append(self, point: Tuple[int, int], y: Optional[int] = None):
        if isinstance(point, int) and y is not None:
            point = (point, y)
        # if self.closed:
        #     raise ValueError("Can't append to a closed polygon.")
        # else:
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
        return map(list, zip(*self.points))

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
        point = (round(point[0]), round(point[1]))
        self.points[point_index] = point

    @property
    def data(self):
        return {"type": "polygon", "label": self.label, "points": self.points}

    @classmethod
    def from_data(cls, data: dict):
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
        type_ = data.pop("type")
        if type_ == "point":
            return cls(**data)
