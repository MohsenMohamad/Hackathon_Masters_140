class ANSI:
    RED = "\033[0;31m"
    CYAN = "\u001B[36m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    GREEN_ITALIC = "\033[1;3;32m"
    END = "\033[0m"


def turn_on_colors():
    # set Windows console in virtual terminal
    if __import__("platform").system() == "Windows":
        kernel32 = __import__("ctypes").windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        del kernel32


if __name__ == '__main__':
    print()     # use this to test your color combinations

