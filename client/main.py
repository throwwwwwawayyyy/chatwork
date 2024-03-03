import curses

from components.event_handler import EventHandler
from components.ui import ChatUI
from components.client_manager import ClientSocketManager
from utils.cmd_args_parser import from_args

event_handler = EventHandler()

def init_ui(stdscr):
    chat_ui = ChatUI(event_handler)

def main():
    host_addr, port_num = from_args()

    ClientSocketManager(host_addr, port_num, event_handler, True)
    curses.wrapper(init_ui)

if __name__ == "__main__":
    main()