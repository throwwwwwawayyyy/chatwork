import curses

from components.event_handler import EventHandler

from models.message import *
from models.ui_message import UIMessage

from utils.message_parser import MessageParser
from utils.build_message import build_input_message, build_username_message, build_password_message
from utils.colors_config import colors_config
from utils.terminal_title import set_terminal_title, clear_terminal_title
from utils.string_utils import handle_display_string, pad_header

from constants.texts import *
from constants.logic import *
from constants.event_names import *
from constants.key_numbers import *
from constants.colors import CLIColors

class ChatUI:
    event_handler: EventHandler
    parser: MessageParser
    
    ui_messages: list[UIMessage] = []
    
    input_text: str = ""
    input_text_ui: str = ""
    
    changed_title: bool = False
    
    start_pos: int = 0
    curr_pos: int = 0
    msg_size: int = 0
    
    disconnected: bool = False
    is_exit_triggered: bool = False

    def __init__(self, stdscr, event_handler: EventHandler) -> None:
        self.stdscr = stdscr
        self.event_handler = event_handler
        self.parser = MessageParser()
        
    def __enter__(self):
        curses.curs_set(0)

        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.refresh()

        colors_config()
        set_terminal_title(WELCOME_APP_TITLE)

        self.messages_win = curses.newwin(curses.LINES - 2, curses.COLS, 0, 0)
        self.input_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        
        self.msg_size = curses.LINES - 4
        
        return self
        
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        curses.endwin()
        self.event_handler.trigger_event(EXIT_EVENT_NAME)

    def refresh_window(self) -> None:
        input_hint: str

        if self.parser.get_level() == PASSWORD_LEVEL:
            input_hint = PASSWORD_HINT_TEXT
        elif self.parser.get_level() == USERNAME_LEVEL:
            input_hint = USERNAME_HINT_TEXT
        elif self.parser.get_level() == WAITING_LEVEL:
            input_hint = WAITING_HINT_TEXT
        else:
            input_hint = INPUT_HINT_TEXT
            
            if not self.changed_title:
                set_terminal_title(f"{HOME_APP_TITLE} - {self.parser.get_username()}")
                self.changed_title = True

        curses.resize_term(curses.LINES, curses.COLS)
        
        input_bar_text = handle_display_string(self.input_text_ui)

        self.input_win.clear()
        for i, chr in enumerate(input_hint + input_bar_text):
            if i < curses.COLS - 1:
                self.input_win.addch(0, i, chr, curses.color_pair(CLIColors.INPUT_COLOR.value))
        self.input_win.refresh()

        self.messages_win.clear()
        self.messages_win.border()
        
        s = self.curr_pos

        current_header = ""
        for i, ui_message in enumerate(self.ui_messages[s:]):
            header = ""
            if ui_message.header != current_header:
                current_header = ui_message.header
                header = ui_message.header
            else:
                header = pad_header(ui_message.header)
            
            display_content = header + " " + handle_display_string(ui_message.content)
            for j, elm in enumerate(display_content):
                color = ui_message.color
                if j > ui_message.content.find(UI_SEP) and not ui_message.keep_color_after_username:
                    color = CLIColors.DEFAULT_COLOR.value
                
                if i < self.msg_size and i < curses.COLS - 1:
                    self.messages_win.addch(i + 1, j + 2, elm, curses.color_pair(color))

        self.messages_win.refresh()
        
    def add_ui_message(self, ui_msg: UIMessage):
        self.ui_messages.append(ui_msg)
        
        if len(self.ui_messages) > self.msg_size:
            self.start_pos += 1
            
        self.curr_pos = self.start_pos

    def listen_for_message(self):
        self.event_handler.add_listener(SHOW_EVENT_NAME, lambda msg: self.handle_msg(msg))

    def handle_msg(self, msg_to_parse: str):
        msg_obj = self.parser.parse_from_server(msg_to_parse)

        if not msg_obj.error:
            if self.parser.get_level() < CHAT_LEVEL:
                self.parser.increment_level()
        else:
            if self.parser.get_level() == PASSWORD_LEVEL:
                self.parser.set_level_default()

        for line in msg_obj.display_list():
            self.add_ui_message(UIMessage(line[0], line[1], msg_obj.color, msg_obj.keep_color_after_username))
        self.refresh_window()
        
    def listen_for_disconnection(self):
        self.event_handler.add_listener(DISCONNECTED_EVENT_NAME, lambda: self.handle_disconnection())
        
    def handle_disconnection(self):
        self.disconnected = True

    def handle_enter(self):
        msg_content: str = self.input_text.strip()
        self.input_text = ""
        self.input_text_ui = ""

        if msg_content == "":
            pass
        elif msg_content == EXIT_MESSAGE:
            self.is_exit_triggered = True
        elif self.parser.get_level() != WAITING_LEVEL and not self.disconnected:
                msg_obj, ui_msg_obj = self.parser.parse_from_client(msg_content)

                if msg_obj is not None:
                    msg_obj.handle()
                    self.event_handler.trigger_event(SEND_EVENT_NAME, msg_obj.serialize())
                    
                self.add_ui_message(ui_msg_obj)

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
        
        if self.parser.get_level() == PASSWORD_LEVEL:
            self.input_text_ui += PASSWORD_DISPLAY_CHARACTER
        else:
            self.input_text_ui += chr(key)

    def run(self) -> None:
        self.listen_for_message()
        self.listen_for_disconnection()

        while not self.is_exit_triggered:
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
                    
        clear_terminal_title()