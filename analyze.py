from __future__ import annotations
import logging


from modules.analyser import Analyser


def get_input_bool(message: str) -> bool:
    while True:
        read = input(message)

        match read.lower():
            case "y":
                return True
            case "n":
                return False
            case _:
                logging.debug(f"Invalid input: {read}")


def main():
    save_file_path = "colors.txt"
    out_image_path = "out.png"
    out_stats_path = "stats.json"
    out_table_path = "table.md"

    a = Analyser(save_file=save_file_path)

    if a.saveFileExists():
        load = get_input_bool("Load colors from file? (Y/N): ")
    else:
        load = False

    if load:
        logging.info("Loading colors from file")
        a.loadColors()
    else:
        logging.info("Loading flags from folder. This may take a while")
        a.loadFlags()
        logging.info("Extracting colors from flags")
        a.extractColors()
        logging.info("Saving colors to file")
        a.saveColors()

    logging.info("Quantizing colors")
    a.quantizeColors()
    logging.info("Saving quantized colors to file")
    a.createOutImage(out_image_path)
    logging.info("Saving stats to file")
    a.saveStats(out_stats_path)
    logging.info("Saving table to file")
    a.saveTable(out_table_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
