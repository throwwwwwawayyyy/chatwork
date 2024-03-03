import socket
import threading
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
        self.conn.settimeout(CONNECTION_TIMEOUT)

        self.debug = debug
        self.event_handler = event_handler

        try:
            self.debug_print(CONNECTING_DEBUG_MSG)
            self.conn.connect((self.host, self.port))
        except:
            self.debug_print(NOT_CONNECTED_MSG)
            os._exit(-1)
        finally:
            self.conn.settimeout(None)
            
            self.listen_for_input()

            self.serverInputThread = threading.Thread(target=self.listen_to_messages)
            self.serverInputThread.start()

    def __del__(self):
        self.conn.close()

    def handle_message(self, msg: bytes):
        decoded_msg = msg.decode()
        if decoded_msg:
            self.event_handler.trigger_event(SHOW_EVENT_NAME, decoded_msg)
        else:
            self.handle_disconnection()
        
    def handle_disconnection(self):
        self.event_handler.trigger_event(DISCONNECTED_EVENT_NAME)

    def send_message(self, msg: str):
        try:
            data_to_send = msg.encode()
            self.conn.send(data_to_send)
        except ConnectionError:
            self.handle_disconnection()

    def listen_to_messages(self):
        while(True):
            try:
                msg: bytes = self.conn.recv(1024)
                self.handle_message(msg)
            except ConnectionError:
                self.handle_disconnection()

    def listen_for_input(self):
        self.event_handler.add_listener(SEND_EVENT_NAME, lambda msg: self.send_message(msg))

    def debug_print(self, msg: str):
        if self.debug:
            print(msg)