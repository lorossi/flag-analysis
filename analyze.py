from __future__ import annotations

import glob
import ujson
from PIL import Image, ImageDraw
import logging


from color import Color
from flag import Flag
from quantizer import Quantizer


def get_input_bool(message: str) -> bool:
    while True:
        read = input(message)
        if read == "y":
            return True
        elif read == "n":
            return False
        else:
            print("Invalid input")


def check_file(path: str) -> None:
    try:
        with open(path, "r") as _:
            return True
    except FileNotFoundError:
        return False


def load_colors(path: str = "colors.txt") -> list[Color]:
    with open(path, "r") as f:
        colors = f.read().split(",")
        colors.pop()
        colors = [Color.from_hex(color) for color in colors]

    return colors


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


def save_colors(colors: list[Color], path: str = "colors.txt") -> None:
    with open(path, "w") as f:
        for color in colors:
            f.write(f"{color.hex},")


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


def create_stats(
    palette: list[Color], count: list[int], path: str = "out.json"
) -> None:
    out_data = []
    total = sum(count)

    for i, color in enumerate(palette):
        percentage = round(count[i] / total * 100, 2)
        out_data.append({color.hex: percentage})

    out_data.sort(key=lambda x: list(x.values())[0], reverse=True)

    with open(path, "w") as f:
        ujson.dump(out_data, f, indent=4)


def main():
    file_path = "colors.txt"

    load = False
    if check_file(file_path):
        load = get_input_bool("Load colors from file? (y/n) ")

    if load:
        colors = load_colors(file_path)
        logging.info(f"Loaded {len(colors)} colors")
    else:
        flags = load_flags()
        logging.info(f"Loaded {len(flags)} flags")
        colors = extract_colors(flags)
        logging.info(f"Extracted {len(colors)} colors")
        save_colors(colors, file_path)
        logging.info(f"Saved colors to {file_path}")

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
