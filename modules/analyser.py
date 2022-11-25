from __future__ import annotations

import glob
import logging

from .color import Color
from .flag import Flag
from .quantizer import Quantizer


class Analyser:
    def __init__(
        self, flags_folder: str = "flags", save_file: str = "colors.txt"
    ) -> Analyser:
        self._flags_folder = flags_folder
        self._save_file = save_file

    def saveFileExists(self) -> bool:
        try:
            logging.debug(f"Checking if {self._save_file} exists")
            with open(self._save_file, "r") as _:
                logging.debug(f"{self._save_file} exists")
                return True
        except FileNotFoundError:
            logging.debug(f"{self._save_file} does not exist")
            return False

    def loadColors(self) -> None:
        self._colors = []
        with open(self._save_file, "r") as f:
            colors = f.read().split(",")
            colors.pop()
            self._colors = [Color.from_hex(color) for color in colors]

        logging.info(f"Loaded {len(self._colors)} colors from {self._save_file}")

    def saveColors(self) -> None:
        logging.debug(f"Saving colors to {self._save_file}")
        with open(self._save_file, "w") as f:
            for color in self._colors:
                f.write(color.hex + ",")
        logging.debug(f"Saved colors to {self._save_file}")

        logging.info(f"Saved {len(self._colors)} colors to {self._save_file}")

    def loadFlags(self) -> None:
        self._flags = []
        for i, path in enumerate(glob.glob(f"{self._flags_folder}/*.png")):
            self._flags.append(Flag(path))
            logging.debug(f"Loaded {path} ({i+1})")

        logging.info(f"Loaded {len(self._flags)} flags")

    def extractColors(self) -> None:
        self._colors = []
        for i, flag in enumerate(self._flags):
            for color in flag.colors:
                self._colors.append(color)
            logging.debug(
                f"Extracted {len(flag.colors)} colors from flag "
                f"{(i)+1}/{len(self._flags)}"
            )
        logging.info(f"Extracted {len(self._colors)} colors")

    def quantizeColors(self, levels: int = 2) -> None:
        self._quantizer = Quantizer(self._colors, levels=levels)
        self._quantizer.quantize()
        logging.debug("Colors quantized")

    def createOutImage(self, path: str, width=1000, height=255) -> None:
        self._quantizer.createOutImage(path=path, width=width, height=height)
        logging.info(f"Created out image at {path}")

    def saveStats(self, path: str) -> None:
        self._quantizer.saveStats(path)
        logging.info(f"Saved stats to {path}")

    def saveTable(self, path: str) -> None:
        self._quantizer.saveTable(path)
        logging.info(f"Saved table to {path}")

    def printStats(self) -> None:
        self._quantizer.printStats()
        logging.info("Printed stats to console")
