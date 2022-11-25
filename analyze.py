from __future__ import annotations
import logging
import argparse

from modules.analyser import Analyser


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "-f",
        "--flags",
        default="flags",
        help="Folder containing flags",
    )
    parser.add_argument(
        "-s",
        "--save",
        default="colors.txt",
        help="File to save colors to",
    )
    parser.add_argument(
        "-l",
        "--load",
        action="store_true",
        help="Load colors from file",
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=2,
        help="Number of quantization levels for each channel",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    out_image_path = "out.png"
    out_stats_path = "stats.json"
    out_table_path = "table.md"

    a = Analyser(save_file=args.save, flags_folder=args.flags)

    if a.saveFileExists() and args.load:
        load = True
    else:
        load = False

    if load:
        logging.info("Loading colors from file")
        a.loadColors()
    else:
        logging.info(
            "Loading flags from folder. This may take a while. "
            "Try running with -l to load colors from file "
            "or -v to enable verbose logging"
        )
        a.loadFlags()
        logging.info("Extracting colors from flags")
        a.extractColors()
        logging.info("Saving colors to file")
        a.saveColors()

    logging.info("Quantizing colors")
    a.quantizeColors(levels=args.number)
    logging.info(f"Saving quantized colors to image {out_image_path}")
    a.createOutImage(out_image_path)
    logging.info(f"Saving stats to file {out_stats_path}")
    a.saveStats(out_stats_path)
    logging.info(f"Saving table to file {out_table_path}")
    a.saveTable(out_table_path)
    logging.info("Printing stats to console")
    a.printStats()


if __name__ == "__main__":
    main()
