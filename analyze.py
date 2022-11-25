from __future__ import annotations

import glob
from PIL import Image, ImageDraw
import logging


from color import Color
from flag import Flag
from quantizer import Quantizer


def load_flags() -> list[Flag]:
    flags = []
    for i, path in enumerate(glob.glob("flags/*.png")):
        flags.append(Flag(path))
        logging.info(f"Loaded {path} ({i+1})")

    return flags


def extract_colors(flags: list[Flag]) -> list[Color]:
    colors = []
    for i, flag in enumerate(flags):
        for color in flag.colors:
            colors.append(color)
        logging.info(
            f"Extracted {len(flag.colors)} colors from flag {(i)+1}/{len(flags)}"
        )

    return colors


def quantize_colors(colors: list[Color], levels=2) -> list[Color]:
    q = Quantizer(colors, levels)
    return q.quantize()


def create_out_image(
    palette: list[Color], count=list[int], width: int = 1000, height: int = 200
) -> None:
    out_image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(out_image)

    scl = sum(count) / width

    x = 0
    for i, color in enumerate(palette):
        w = round(count[i] / scl)
        draw.rectangle((x, 0, x + w, height), fill=color.rgb)
        x += w

    out_image.save("out.png")


def create_stats(palette: list[Color], count: list[int]) -> None:
    total = sum(count)

    for i, color in enumerate(palette):
        percentage = round(count[i] / total * 100, 2)
        logging.info(f"{color.hex} - {percentage}%")


def main():
    flags = load_flags()
    logging.info(f"Loaded {len(flags)} flags")
    colors = extract_colors(flags)
    logging.info(f"Extracted {len(colors)} colors")
    palette, count = quantize_colors(colors)
    logging.info(f"Quantized {len(palette)} colors")
    create_out_image(palette, count)
    logging.info("Image created")
    create_stats(palette, count)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s-%(levelname)s-%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()
