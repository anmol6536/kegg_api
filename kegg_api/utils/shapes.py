from abc import ABC
from dataclasses import dataclass, field


@dataclass(init=True, repr=True)
class Shape(ABC):
    x: float = field(default=None)  # x coordinate
    y: float = field(default=None)  # y coordinate
    h: float = field(default=None)  # height
    w: float = field(default=None)  # width
    r: float = field(default=None)  # radius
    label: str = field(default=None)

    def __post_init__(self):
        ...


class Rectangle(Shape):
    ...


class Circle(Shape):
    ...


class Line(Shape):
    ...