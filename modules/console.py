class Console:
    @staticmethod
    def reset() -> None:
        print("\033[0m", end="")

    @staticmethod
    def rgb(r, g, b):
        print(f"\033[38;2;{r};{g};{b}m", end="")

    @staticmethod
    def bold():
        return print("\033[1m", end="")
