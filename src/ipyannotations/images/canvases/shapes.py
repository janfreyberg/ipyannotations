from typing import List, Tuple, Optional, ClassVar, Any, Dict
from dataclasses import dataclass, field
from .utils import dist


@dataclass
class Polygon:
    points: List[Tuple[int, int]] = field(default_factory=list)
    label: Optional[str] = None
    close_threshold: ClassVar[int] = 5
    extra_info: Dict[str, Any] = field(default_factory=dict)

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
        info = {"type": "polygon", "label": self.label, "points": self.points}
        info.update(self.extra_info)
        return info

    @classmethod
    def from_data(cls, data: dict):
        type_ = data.pop("type")

        if type_ != "polygon":
            raise ValueError(
                "Polygon data needs to contain the key-value pair "
                "'type': 'polygon'."
            )

        native_args, extra_args = {}, {}
        for name, val in data.items():
            if name in cls.__annotations__:
                native_args[name] = val
            else:
                extra_args[name] = val

        native_args["extra_info"] = extra_args
        return cls(**native_args)


@dataclass
class Point:
    coordinates: Tuple[int, int]
    label: str = ""
    extra_info: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.coordinates = tuple(map(round, self.coordinates))

    def move(self, x: int, y: int):
        self.coordinates = (round(x), round(y))

    @property
    def data(self) -> dict:
        info = {
            "type": "point",
            "label": self.label,
            "coordinates": self.coordinates,
        }
        info.update(self.extra_info)
        return info

    @classmethod
    def from_data(cls, data: dict):
        type_ = data.pop("type")
        if type_ != "point":
            raise ValueError(
                "Point data needs to contain the key-value pair "
                "'type': 'point'."
            )

        native_args, extra_args = {}, {}
        for name, val in data.items():
            if name in cls.__annotations__:
                native_args[name] = val
            else:
                extra_args[name] = val

        native_args["extra_info"] = extra_args
        return cls(**native_args)


@dataclass
class BoundingBox:
    xyxy: Tuple[int, int, int, int]
    label: str = ""

    def __post_init__(self):
        self.xyxy = tuple(map(round, self.xyxy))

    def move_corner(self, idx, new_x: int, new_y: int):
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
        info = {
            "type": "box",
            "label": self.label,
            "xyxy": (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)),
        }
        info.update(self.extra_info)
        return info

    @classmethod
    def from_data(cls, data: dict):
        type_ = data.pop("type")
        if type_ != "point":
            raise ValueError(
                "Box data needs to contain the key-value pair "
                "'type': 'box'."
            )

        native_args, extra_args = {}, {}
        for name, val in data.items():
            if name in cls.__annotations__:
                native_args[name] = val
            else:
                extra_args[name] = val

        native_args["extra_info"] = extra_args
        return cls(**native_args)
