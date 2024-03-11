import curses
import os

from components.event_handler import EventHandler
from models.message_parser import MessageTypeParser
from models.ui_message import UIMessage

from utils.build_message import build_input_message, build_username_message, build_password_message
from utils.colors_config import colors_config

from constants.texts import *
from constants.logic import *
from constants.event_names import *
from constants.key_numbers import *
from constants.colors import CLIColors

class ChatUI:
    event_handler: EventHandler
    msg_parser: MessageTypeParser
    
    ui_messages: list[UIMessage] = []
    
    input_text: str = ""
    input_text_ui: str = ""
    
    level: int = USERNAME_LEVEL
    username: str
    password: str
    
    start_pos: int = 0
    curr_pos: int = 0
    msg_size: int = 0
    
    disconnected: bool = False

    def __init__(self, event_handler: EventHandler) -> None:
        self.event_handler = event_handler
        self.msg_parser = MessageTypeParser()

        curses.curs_set(0)

        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.refresh()

        colors_config()

        self.messages_win = curses.newwin(curses.LINES - 2, curses.COLS, 0, 0)
        self.input_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        
        self.msg_size = curses.LINES - 4

        self.run()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        curses.endwin()

    def refresh_window(self) -> None:
        input_hint: str

        if self.level == PASSWORD_LEVEL:
            input_hint = PASSWORD_HINT_TEXT
        elif self.level == USERNAME_LEVEL:
            input_hint = USERNAME_HINT_TEXT
        elif self.level == WAITING_LEVEL:
            input_hint = WAITING_HINT_TEXT
        else:
            input_hint = INPUT_HINT_TEXT

        curses.resize_term(curses.LINES, curses.COLS)

        self.input_win.clear()
        self.input_win.addstr(0, 0, input_hint + self.input_text_ui, curses.color_pair(CLIColors.INPUT_COLOR.value))
        self.input_win.refresh()

        self.messages_win.clear()
        self.messages_win.border()
        
        s = self.curr_pos

        for i, ui_message in enumerate(self.ui_messages[s:]):
            for j, elm in enumerate(ui_message.content):
                color = ui_message.color
                if j > ui_message.content.find(UI_SEP) and not ui_message.keep_color:
                    color = CLIColors.DEFAULT_COLOR.value
                
                if i < self.msg_size:
                    self.messages_win.addch(i + 1, j + 2, elm, curses.color_pair(color))

        self.messages_win.refresh()
        
    def add_ui_message(self, content:str, color:int, keep_color:bool):
        ui_msg = UIMessage(content=content, color=color, keep_color=keep_color)
        self.ui_messages.append(ui_msg)
        
        if len(self.ui_messages) > self.msg_size:
            self.start_pos += 1
            
        self.curr_pos = self.start_pos

    def listen_for_message(self):
        self.event_handler.add_listener(SHOW_EVENT_NAME, lambda msg: self.handle_msg(msg))

    def handle_msg(self, msg: str):
        parsed_msg, error, color, keep_color = self.msg_parser.parse(msg)

        if not error:
            if self.level < CHAT_LEVEL:
                self.level += 1
        else:
            if self.level == PASSWORD_LEVEL:
                self.level = USERNAME_LEVEL

        self.add_ui_message(parsed_msg, color, keep_color)
        self.refresh_window()
        
    def listen_for_disconnection(self):
        self.event_handler.add_listener(DISCONNECTED_EVENT_NAME, lambda: self.handle_disconnection())
        
    def handle_disconnection(self):
        if not self.disconnected:
            self.disconnected = True
            
            content = f"[{SYSTEM_USER}]{UI_SEP} {DISCONNECTED_TEXT}"
            color = CLIColors.ERROR_COLOR.value
            keep_color = True
        
            self.add_ui_message(content, color, keep_color)
            self.refresh_window()

    def handle_enter(self):
        msg_content: str = self.input_text.strip()
        self.input_text = ""
        self.input_text_ui = ""

        if msg_content == "":
            pass
        elif msg_content == EXIT_MESSAGE:
            os._exit(0)
        else:
            if self.level != WAITING_LEVEL and not self.disconnected:
                self.event_handler.trigger_event(SEND_EVENT_NAME, msg_content)
                content = ""
                color = 0
                keep_color = False

                if self.level == USERNAME_LEVEL:
                    self.username = msg_content
                    self.level += 1
                    content, color = build_username_message(msg_content)
                    keep_color = True
                elif self.level == PASSWORD_LEVEL:
                    self.password = msg_content
                    content, color = build_password_message(msg_content)
                    keep_color = True
                elif self.level == CHAT_LEVEL:
                    content, color = build_input_message(msg_content)

                self.add_ui_message(content, color, keep_color)

    def handle_backspace(self):
        if self.input_text != "":
            self.input_text = self.input_text[:-1]
            self.input_text_ui = self.input_text_ui[:-1]
            
    def handle_up(self):
        self.curr_pos = max(self.curr_pos - 1, 0)
    
    def handle_down(self):
        self.curr_pos = min(self.curr_pos + 1, len(self.ui_messages) - self.msg_size)
            
    def handle_key(self, key: int) -> str:
        self.input_text += chr(key)
        
        if self.level == PASSWORD_LEVEL:
            self.input_text_ui += PASSWORD_DISPLAY_CHARACTER
        else:
            self.input_text_ui += chr(key)

    def run(self) -> None:
        self.listen_for_message()
        self.listen_for_disconnection()

        while True:
            self.refresh_window()
            key = self.stdscr.getch()
            
            if key:
                if key == ENTER_KEY:
                    self.handle_enter()
                elif key == BACKSPACE_KEY:
                    self.handle_backspace()
                elif key == UP_KEY:
                    self.handle_up()
                elif key == DOWN_KEY:
                    self.handle_down()
                else:
                    self.handle_key(key)