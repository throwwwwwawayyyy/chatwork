import curses

from components.event_handler import EventHandler
from components.ui import ChatUI
from components.client_manager import ClientSocketManager
from utils.cmd_args_parser import from_args

event_handler = EventHandler()

def run_ui(stdscr):
    with ChatUI(stdscr, event_handler) as chat_ui:
        chat_ui.run()

def main():
    host_addr, port_num = from_args()

    client = ClientSocketManager(host_addr, port_num, event_handler, True)
    if client.connected:
        curses.wrapper(run_ui)

if __name__ == "__main__":
    main()