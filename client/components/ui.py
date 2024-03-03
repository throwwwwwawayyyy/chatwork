import curses
import os

from components.event_handler import EventHandler
from models.message_parser import MessageTypeParser
from models.ui_message import UIMessage

from utils.input_display import input_prompt, username_prompt, password_prompt
from utils.colors_config import colors_config

from constants.texts import *
from constants.logic import *
from constants.event_names import *
from constants.key_numbers import ENTER_KEY, BACKSPACE_KEY
from constants.colors import CLIColors

class ChatUI:
    event_handler: EventHandler
    msg_parser: MessageTypeParser
    ui_messages: list[UIMessage]
    input_text: str
    input_text_ui: str
    level: int

    username: str
    password: str
    
    disconnected: bool = False

    def __init__(self, event_handler: EventHandler) -> None:
        self.event_handler = event_handler
        self.msg_parser = MessageTypeParser()
        self.ui_messages = []
        self.input_text = ""
        self.input_text_ui = ""
        self.level = USERNAME_LEVEL

        curses.curs_set(0)

        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.refresh()

        colors_config()

        self.messages_win = curses.newwin(curses.LINES - 2, curses.COLS, 0, 0)
        self.input_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)

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

        if len(self.ui_messages) > curses.LINES - 4:
            self.ui_messages.pop(0)

        for i, ui_message in enumerate(self.ui_messages):
            for j, elm in enumerate(ui_message.content):
                color = ui_message.color
                if j > ui_message.content.find(":") and not ui_message.keep_color:
                    color = CLIColors.DEFAULT_COLOR.value

                self.messages_win.addch(i + 1, j + 2, elm, curses.color_pair(color))

        self.messages_win.refresh()

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

        self.ui_messages.append(UIMessage(content=parsed_msg, color=color, keep_color=keep_color))
        self.refresh_window()
        
    def listen_for_disconnection(self):
        self.event_handler.add_listener(DISCONNECTED_EVENT_NAME, lambda: self.handle_disconnection())
        
    def handle_disconnection(self):
        if not self.disconnected:
            self.disconnected = True
            
            content = f"[{SYSTEM_USER}]: {DISCONNECTED_TEXT}"
            color = CLIColors.ERROR_COLOR.value
            keep_color = True
        
            self.ui_messages.append(UIMessage(content=content, color=color, keep_color=keep_color))
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
                    content, color = username_prompt(msg_content)
                    keep_color = True
                elif self.level == PASSWORD_LEVEL:
                    self.password = msg_content
                    content, color = password_prompt(msg_content)
                    keep_color = True
                elif self.level == CHAT_LEVEL:
                    content, color = input_prompt(msg_content)

                prompt = UIMessage(content=content, color=color, keep_color=keep_color)
                self.ui_messages.append(prompt)

    def handle_backspace(self):
        if self.input_text != "":
            self.input_text = self.input_text[:-1]
            self.input_text_ui = self.input_text_ui[:-1]
            
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
            key = self.input_win.getch()
            
            if key:
                if key == ENTER_KEY:
                    self.handle_enter()
                elif key == BACKSPACE_KEY:
                    self.handle_backspace()
                else:
                    self.handle_key(key)