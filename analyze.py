from __future__ import annotations

import glob
from PIL import Image, ImageDraw


from color import Color
from flag import Flag
from quantizer import Quantizer


def load_flags(sample_size: int = 10) -> list[Flag]:
    flags = []
    for i, path in enumerate(glob.glob("flags/*.png")):
        flags.append(Flag(path))

        if i > sample_size:
            break

    return flags


def extract_colors(flags: list[Flag]) -> list[Color]:
    colors = []
    for flag in flags:
        for color in flag.colors:
            colors.append(color)

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
        print(f"{color.hex} - {percentage}%")


def main():
    flags = load_flags()
    print(f"Loaded {len(flags)} flags")
    colors = extract_colors(flags)
    print(f"Extracted {len(colors)} colors")
    palette, count = quantize_colors(colors)
    print(f"Quantized {len(palette)} colors")
    create_out_image(palette, count)
    print("Image created")
    create_stats(palette, count)


if __name__ == "__main__":
    main()
