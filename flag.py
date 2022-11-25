from __future__ import annotations
from PIL import Image

from color import Color


class Flag:
    def __init__(self, path: str) -> Flag:
        self._openImage(path)
        self._analyzeColors()

    def _openImage(self, path: str) -> None:
        self._image = Image.open(path).convert("RGB")

    def _analyzeColors(self) -> None:
        colors = []
        for x in range(self._image.width):
            for y in range(self._image.height):
                r, g, b = self._image.getpixel((x, y))
                colors.append(Color(r, g, b))

        self._colors = {}
        for c in colors:
            if c not in self._colors:
                self._colors[c] = 1
            else:
                self._colors[c] += 1

    @property
    def colors(self) -> dict[tuple[int, int, int], int]:
        return self._colors
