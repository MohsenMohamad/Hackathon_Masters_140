# Bonus 1 Impl
class ANSI:
    RED = "\033[0;31m"
    CYAN = "\u001B[36m"
    YELLOW = "\u001b[33m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    GREEN_ITALIC = "\033[1;3;32m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    LIGHT_PURPLE = "\033[1;35m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


def turn_on_colors():
    # set Windows console in virtual terminal so we can see all colors
    if __import__("platform").system() == "Windows":
        kernel32 = __import__("ctypes").windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        del kernel32


def get_cyan():  # For the server access problem
    return ANSI.CYAN


def get_end():   # For the server access problem
    return ANSI.END


def get_red():   # For the client access problem
    return ANSI.RED


def get_yellow():   # For the client access problem
    return ANSI.YELLOW
