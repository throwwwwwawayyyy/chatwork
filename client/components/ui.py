import curses
import os

from components.event_handler import EventHandler
from utils.message_parser import MessageParser

from constants.texts import PASSWORD_HINT_TEXT, USERNAME_HINT_TEXT, WAITING_HINT_TEXT, INPUT_HINT_TEXT
from constants.logic import *
from constants.event_names import SHOW_EVENT_NAME, SEND_EVENT_NAME
from constants.key_numbers import ENTER_KEY, BACKSPACE_KEY

class ChatUI:
    event_handler: EventHandler
    messages: list
    input_text: str
    level: int

    username: str
    password: str

    def __init__(self, event_handler: EventHandler) -> None:
        self.event_handler = event_handler
        self.messages = []
        self.input_text = ""
        self.level = USERNAME_LEVEL

        curses.curs_set(0)

        self.stdscr = curses.initscr()
        self.stdscr.clear()
        self.stdscr.refresh()

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
        self.input_win.addstr(0, 0, input_hint + self.input_text)
        self.input_win.refresh()

        self.messages_win.clear()
        self.messages_win.border()

        for i, message in enumerate(self.messages):
            try:
                self.messages_win.addstr(i + 1, 1, message)
            except curses.error:
                self.messages.pop(0)
                self.refresh_window()
                return

        self.messages_win.refresh()

    def listen_for_message(self):
        self.event_handler.add_listener(SHOW_EVENT_NAME, lambda msg: self.handle_msg(msg))

    def handle_msg(self, msg: str):
        parsed_msg, error = MessageParser.parse(msg)

        if not error:
            if self.level < CHAT_LEVEL:
                self.level += 1

        self.messages.append(parsed_msg)
        self.refresh_window()

    def handle_enter(self):
        msg_content: str = self.input_text
        self.input_text = ""

        if msg_content == EXIT_MESSAGE:
            os._exit(0)
        else:
            if self.level == USERNAME_LEVEL:
                self.username = msg_content
                self.level += 1
            elif self.level == PASSWORD_LEVEL:
                self.password = msg_content

            if self.level != WAITING_LEVEL:
                self.event_handler.trigger_event(SEND_EVENT_NAME, msg_content)

                if self.level == CHAT_LEVEL:
                    self.messages.append(f"[{YOUR_USER}]: {msg_content}")

    def handle_backspace(self):
        if self.input_text != "":
            self.input_text = self.input_text[:-1]

    def run(self) -> None:
        self.listen_for_message()

        while True:
            self.refresh_window()
            key = self.input_win.getch()

            if key == ENTER_KEY:
                self.handle_enter()
            elif key == BACKSPACE_KEY:
                self.handle_backspace()
            else:
                self.input_text += chr(key)