from __future__ import annotations

import re
from math import sqrt


class Color:
    def __init__(self, r: int, g: int, b: int) -> Color:
        if any([c < 0 or c > 255 for c in [r, g, b]]):
            raise ValueError("Color values must be between 0 and 255")

        self._r = r
        self._g = g
        self._b = b

        self._toHSV()

    @staticmethod
    def from_hex(hex: str) -> Color:
        if hex[0] == "#":
            hex = hex[1:]
        if len(hex) == 3:
            hex = "".join([c * 2 for c in hex])
        return Color(int(hex[:2], 16), int(hex[2:4], 16), int(hex[4:], 16))

    @staticmethod
    def from_rgb(rgb: str) -> Color:
        groups = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb)
        if groups is None:
            raise ValueError(f"Invalid rgb string: {rgb}")
        return Color(int(groups[1]), int(groups[2]), int(groups[3]))

    def _toHSV(self) -> None:
        r = self._r / 255
        g = self._g / 255
        b = self._b / 255
        c_max = max(r, g, b)
        c_min = min(r, g, b)
        delta = c_max - c_min

        if delta == 0:
            h = 0
        elif c_max == r:
            h = 60 * (((g - b) / delta) % 6)
        elif c_max == g:
            h = 60 * (((b - r) / delta) + 2)
        elif c_max == b:
            h = 60 * (((r - g) / delta) + 4)

        if c_max == 0:
            s = 0
        else:
            s = delta / c_max

        v = c_max

        self._h = int(h)
        self._s = int(s * 100)
        self._v = int(v * 100)

    def dist(self, other: Color) -> int:
        # red mean approximation
        dr = self._r - other.r
        dg = self._g - other.g
        db = self._b - other.b
        r = (self._r + other.r) / 2
        return sqrt(
            (2 + r / 256) * dr * dr + 4 * dg * dg + (2 + (255 - r) / 256) * db * db
        )

    def average(colors: list[Color]) -> Color:
        r = sum([c.r for c in colors]) // len(colors)
        g = sum([c.g for c in colors]) // len(colors)
        b = sum([c.b for c in colors]) // len(colors)
        return Color(r, g, b)

    def copy(self) -> Color:
        return Color(self._r, self._g, self._b)

    def to_dict(self) -> dict[str, int]:
        return {"r": self._r, "g": self._g, "b": self._b}

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def h(self) -> int:
        return self._h

    @property
    def s(self) -> int:
        return self._s

    @property
    def v(self) -> int:
        return self._v

    @property
    def luminance(self) -> int:
        return int(0.299 * self._r + 0.587 * self._g + 0.114 * self._b)

    @property
    def hex(self) -> str:
        return f"#{self._r:02x}{self._g:02x}{self._b:02x}"

    @property
    def rgb(self) -> str:
        return f"rgb({self._r}, {self._g}, {self._b})"

    @property
    def hsv(self) -> str:
        return f"hsv({self._h}, {self._s}%, {self._v}%)"

    def __repr__(self) -> str:
        return self.rgb

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Color) -> bool:
        return self._r == other.r and self._g == other.g and self._b == other.b

    def __hash__(self) -> int:
        return hash((self._r, self._g, self._b))
