import curses

from components.event_handler import EventHandler
from components.ui import ChatUI
from components.client_manager import ClientSocketManager
from components.config_manager import NetworkConfig

event_handler = EventHandler()

def run_ui(stdscr):
    with ChatUI(stdscr, event_handler) as chat_ui:
        chat_ui.run()

def main():
    network_config = NetworkConfig()

    client = ClientSocketManager(network_config.ip, network_config.port, event_handler, True)
    if client.connected:
        curses.wrapper(run_ui)

if __name__ == "__main__":
    main()