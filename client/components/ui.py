import curses
import os

from components.event_handler import EventHandler
from models.message_parser import MessageParser
from models.prompts import Prompt

from utils.input_display import input_prompt, username_prompt, password_prompt
from utils.colors_config import colors_config

from constants.texts import PASSWORD_HINT_TEXT, USERNAME_HINT_TEXT, WAITING_HINT_TEXT, INPUT_HINT_TEXT
from constants.logic import *
from constants.event_names import SHOW_EVENT_NAME, SEND_EVENT_NAME
from constants.key_numbers import ENTER_KEY, BACKSPACE_KEY
from constants.colors import CLIColors

class ChatUI:
    event_handler: EventHandler
    msg_parser: MessageParser
    prompts: list[Prompt]
    input_text: str
    level: int

    username: str
    password: str

    def __init__(self, event_handler: EventHandler) -> None:
        self.event_handler = event_handler
        self.msg_parser = MessageParser()
        self.prompts = []
        self.input_text = ""
        self.level = USERNAME_LEVEL

        curses.curs_set(0)

        self.stdscr = curses.initscr()
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
        self.input_win.addstr(0, 0, input_hint + self.input_text, curses.color_pair(CLIColors.INPUT_COLOR.value))
        self.input_win.refresh()

        self.messages_win.clear()
        self.messages_win.border()

        if len(self.prompts) > curses.LINES - 4:
            self.prompts.pop(0)

        for i, prompt in enumerate(self.prompts):
            for j, elm in enumerate(prompt.content):
                color = prompt.color
                if j > prompt.content.index(":") and not prompt.keep_color:
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

        self.prompts.append(Prompt(content=parsed_msg, color=color, keep_color=keep_color))
        self.refresh_window()

    def handle_enter(self):
        msg_content: str = self.input_text
        self.input_text = ""

        if msg_content == EXIT_MESSAGE:
            os._exit(0)
        else:
            if self.level != WAITING_LEVEL:
                self.event_handler.trigger_event(SEND_EVENT_NAME, msg_content)
                p_content = ""
                p_color = 0
                p_keep_color = False

                if self.level == USERNAME_LEVEL:
                    self.username = msg_content
                    self.level += 1
                    p_content, p_color = username_prompt(msg_content)
                    p_keep_color = True
                elif self.level == PASSWORD_LEVEL:
                    self.password = msg_content
                    p_content, p_color = password_prompt(msg_content)
                    p_keep_color = True
                elif self.level == CHAT_LEVEL:
                    p_content, p_color = input_prompt(msg_content)

                prompt = Prompt(content=p_content, color=p_color, keep_color=p_keep_color)
                self.prompts.append(prompt)

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