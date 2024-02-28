import curses
from constants.colors import CLIColors

def colors_config() -> None:
    curses.start_color()
    curses.init_pair(CLIColors.DEFAULT_COLOR.value, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(CLIColors.INPUT_COLOR.value, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(CLIColors.ADMIN_MESSAGE_COLOR.value, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(CLIColors.SYSTEM_MESSAGE_COLOR.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(CLIColors.YOUR_MESSAGE_COLOR.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(CLIColors.ERROR_COLOR.value, curses.COLOR_RED, curses.COLOR_BLACK)