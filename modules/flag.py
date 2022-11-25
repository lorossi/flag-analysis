from __future__ import annotations

import logging

from PIL import Image

from .color import Color


class Flag:
    def __init__(self, path: str) -> Flag:
        self._path = path
        self._openImage()
        self._analyzeColors()

    def _openImage(self) -> None:
        logging.debug(f"Opening {self._path}")
        self._image = Image.open(self._path).convert("RGB")
        logging.debug(f"Opened {self._path}")

    def _analyzeColors(self) -> None:
        logging.debug(f"Analysing colors in {self._path}")
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

        logging.debug(
            f"Analysed colors in {self._path}. "
            f"Found {len(self._colors)} unique colors"
        )

    @property
    def colors(self) -> dict[tuple[int, int, int], int]:
        return self._colors
