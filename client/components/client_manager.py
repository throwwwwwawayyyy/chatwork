import socket
import threading
import datetime
import os

from components.event_handler import EventHandler
from constants.event_names import *
from constants.communication import *

class ClientSocketManager:
    host: str
    port: int
    conn: socket.socket
    event_handler: EventHandler
    clientInputThread: threading.Thread
    serverInputThread: threading.Thread
    debug: bool

    def __init__(self, host: str, port: int, event_handler: EventHandler, debug = True) -> None:
        self.host = host
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.debug = debug
        self.event_handler = event_handler

        self.debug_print(CONNECTING_DEBUG_MSG)
        self.debug_print(f"{self.host}, {self.port}")
        self.conn.connect((self.host, self.port))
        self.debug_print(CONNECTED_DEBUG_MSG)

        self.clientInputThread = threading.Thread(target=self.listen_for_input)
        self.serverInputThread = threading.Thread(target=self.listen_to_messages)

        self.clientInputThread.start()
        self.serverInputThread.start()

    def __del__(self):
        self.conn.close()

    def handle_message(self, msg: bytes):
        decoded_msg = msg.decode()
        self.event_handler.trigger_event(SHOW_EVENT_NAME, decoded_msg)

    def send_message(self, msg: str):
        data_to_send = msg.encode()
        self.conn.send(data_to_send)
        #self.debug_log(msg)

    def listen_to_messages(self):
        while(True):
            msg: bytes = self.conn.recv(1024)
            self.handle_message(msg)

    def listen_for_input(self):
        self.event_handler.add_listener(SEND_EVENT_NAME, lambda msg: self.send_message(msg))

    def debug_print(self, msg: str):
        if self.debug:
            print(msg)

    def debug_log(self, msg: str):
        with open(f"{os.getcwd()}/client/debug.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}][{self.host, self.port}][{msg}]\n")
            f.close()