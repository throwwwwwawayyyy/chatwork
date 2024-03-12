import socket
import threading
import os
import rsa

from components.event_handler import EventHandler
from components.encryption_manager import EncryptionManager
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
    connected: bool
    is_exit_triggered: bool = False
    
    encryptor: EncryptionManager

    def __init__(self, host: str, port: int, event_handler: EventHandler, debug = True) -> None:
        self.host = host
        self.port = port
        
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(CONNECTION_TIMEOUT)

        self.debug = debug
        self.event_handler = event_handler
        self.encryptor = EncryptionManager()

        try:
            self.debug_print(CONNECTING_DEBUG_MSG)
            self.conn.connect((self.host, self.port))
            self.conn.settimeout(None)
            
            self.encryptor.share_keys(self.conn)
            
            self.listen_for_input()
            self.listen_for_exit()
            self.serverInputThread = threading.Thread(target=self.listen_to_messages)
            self.serverInputThread.start()
            
            self.debug_print(CONNECTED_DEBUG_MSG)
            self.connected = True
        except:
            self.debug_print(NOT_CONNECTED_DEBUG_MSG)
            self.connected = False

    def __del__(self):
        self.conn.close()

    def handle_message(self, msg: bytes):
        msg = self.encryptor.decrypt(msg)
        decoded_msg = msg.decode()
        if decoded_msg:
            self.event_handler.trigger_event(SHOW_EVENT_NAME, decoded_msg)
        else:
            self.handle_disconnection()
        
    def handle_disconnection(self):
        self.event_handler.trigger_event(DISCONNECTED_EVENT_NAME)
        
    def handle_exit(self):
        self.is_exit_triggered = True
        self.conn.close()

    def send_message(self, msg: str):
        try:
            data_to_send = msg.encode()
            data_to_send = self.encryptor.encrypt(data_to_send)
            self.conn.send(data_to_send)
        except ConnectionError:
            self.handle_disconnection()

    def listen_to_messages(self):
        while not self.is_exit_triggered:
            try:
                msg: bytes = self.conn.recv(1024)
                self.handle_message(msg)
            except ConnectionError:
                self.handle_disconnection()

    def listen_for_input(self):
        self.event_handler.add_listener(SEND_EVENT_NAME, lambda msg: self.send_message(msg))
        
    def listen_for_exit(self):
        self.event_handler.add_listener(EXIT_EVENT_NAME, lambda: self.handle_exit())

    def debug_print(self, msg: str):
        if self.debug:
            print(msg)