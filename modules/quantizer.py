from __future__ import annotations

import logging
from math import inf

import ujson
from PIL import Image, ImageDraw

from .color import Color
from .console import Console


class Quantizer:
    """This class handles the quantization of colors."""

    def __init__(self, colors: list[Color], levels: int = 2) -> Quantizer:
        """Initialize the quantizer.

        Args:
            colors (list[Color]): list of source colors
            levels (int, optional): number of levels per channel. Defaults to 2.

        Returns:
            Quantizer
        """
        self._colors = [c.copy() for c in colors]
        self._levels = levels
        self._generatePalette()

    def _generatePalette(self) -> None:
        """Generate the palette of colors."""
        self._palette = []
        delta = 255 // (self._levels - 1)

        logging.debug(f"Generating palette with {self._levels} levels per channel")

        for i in range(self._levels):
            for j in range(self._levels):
                for k in range(self._levels):
                    self._palette.append(Color(i * delta, j * delta, k * delta))

        logging.debug(f"Generated palette with {len(self._palette)} colors")

    def _closestColor(self, color: Color) -> Color:
        """Find the closest color in the palette.

        Args:
            color (Color): color to find the closest match for

        Returns:
            Color: closest color in the palette
        """
        min_dist = inf
        closest_color = None

        for palette_color in self._palette:
            dist = color.dist(palette_color)
            if dist < min_dist:
                min_dist = dist
                closest_color = palette_color

        return closest_color

    def quantize(self) -> None:
        """Quantize the colors.

        Returns:
            tuple[list[Color], list[int]]: list of colors and list of counts
        """
        # count the colors
        quantized_colors = {p: 0 for p in self._palette}
        for color in self._colors:
            closest_color = self._closestColor(color)
            quantized_colors[closest_color] += 1

        logging.debug(f"Quantized {len(self._colors)} colors")

        # sort the colors by luminance
        self._colors = []
        # place black and white at the beginning of the list
        self._colors.append(self._palette[0])
        self._colors.append(self._palette[-1])
        for i in range(1, len(self._palette) - 1):
            self._colors.append(self._palette[i])

        # order the count list by the order of the colors list
        self._counts = []
        for color in self._colors:
            self._counts.append(quantized_colors[color])

        total = sum(self._counts)
        logging.debug(f"Quantized colors represent {total} pixels")

        self._createStats()
        self._createTable()

    def _createStats(self):
        self._json_stats = []
        total = sum(self._counts)

        for i, color in enumerate(self._colors):
            self._json_stats.append(
                {
                    "color": color.hex,
                    "frequency": self._counts[i] / total,
                    "count": self._counts[i],
                }
            )

        self._json_stats.sort(key=lambda x: x["frequency"], reverse=True)

        logging.debug(f"Created stats for {len(self._json_stats)} colors")

    def _createTable(self) -> None:
        """Create a table of the quantized colors.

        Returns:
            str: table of quantized colors
        """
        self._table = "|color|frequency|count|\n"
        self._table += "|:---:|:---:|:---:|\n"

        for stat in self._json_stats:
            self._table += f"|{stat['color']}|{stat['frequency']}|{stat['count']}|\n"

        logging.debug(f"Created table for {len(self._json_stats)} colors")

    def createOutImage(self, path="out.png", width=1000, height=200) -> None:
        out_image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(out_image)
        scl = sum(self._counts) / width

        x = 0
        for i, color in enumerate(self._colors):
            w = round(self._counts[i] / scl)
            draw.rectangle((x, 0, x + w, height), fill=color.rgb)
            x += w

        out_image.save(path)

        logging.debug(f"Created output image {path}")

    def saveStats(self, path="stats.json") -> None:
        with open(path, "w") as f:
            ujson.dump(self._json_stats, f, indent=4)

        logging.debug(f"Saved stats to {path}")

    def saveTable(self, path="table.md") -> None:
        with open(path, "w") as f:
            f.write(self._table)

        logging.debug(f"Saved table to {path}")

    def printStats(self) -> None:
        for stat in self._json_stats:
            color = Color.from_hex(stat["color"])
            percent = round(stat["frequency"] * 100, 2)
            Console.rgb(*color)
            print(f"{color.hex} - {percent:04}%")

        Console.reset()
