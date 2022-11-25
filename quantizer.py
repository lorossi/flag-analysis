from __future__ import annotations
from math import inf
from color import Color


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
        self._levels = levels - 1
        self._generatePalette()

    def _generatePalette(self) -> None:
        """Generate the palette of colors."""
        self._palette = []
        delta = 255 // self._levels

        for i in range(self._levels + 1):
            for j in range(self._levels + 1):
                for k in range(self._levels + 1):
                    self._palette.append(Color(i * delta, j * delta, k * delta))

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

    def quantize(self) -> tuple[list[Color], list[int]]:
        """Quantize the colors.

        Returns:
            tuple[list[Color], list[int]]: list of colors and list of counts
        """
        # count the colors
        quantized_colors = {p: 0 for p in self._palette}
        for color in self._colors:
            closest_color = self._closestColor(color)
            quantized_colors[closest_color] += 1

        # sort the colors by luminance
        colors = []
        # place black and white at the beginning of the list
        colors.append(self._palette[0])
        colors.append(self._palette[-1])
        for i in range(1, len(self._palette) - 1):
            colors.append(self._palette[i])

        # order the count list by the order of the colors list
        counts = []
        for color in colors:
            counts.append(quantized_colors[color])

        return colors, counts
