from constants.logic import PASSWORD_DISPLAY_CHARACTER
from constants.logic import YOUR_USER, SYSTEM_USER, UI_SEP
from constants.logic import Privileges
from constants.texts import USERNAME_MSG_TEXT, PASSWORD_MSG_TEXT
from constants.colors import CLIColors

def build_message(user:str, content:str, privilege:int = 0) -> tuple[str,str]:
    priv_sign = ""
    if privilege == Privileges.MOD.value:
        priv_sign = " $"
    elif privilege == Privileges.ADMIN.value:
        priv_sign = " #"
    elif privilege == Privileges.ROOT.value:
        priv_sign = " @"
    
    return f"[{user}{priv_sign}]{UI_SEP}", content

def password_display(password: str) -> str:
    disp = ""
    for elm in password:
        disp += PASSWORD_DISPLAY_CHARACTER
    
    return disp

def build_input_message(content: str, privilege:int = 0) -> tuple[str, str, int]:
    header, msg = build_message(YOUR_USER, content, privilege)
    color = CLIColors.YOUR_MESSAGE_COLOR.value

    return header, msg, color

def build_username_message(content: str) -> tuple[str, str, int]:
    header, msg = build_message(SYSTEM_USER, USERNAME_MSG_TEXT + content)
    color = CLIColors.SYSTEM_MESSAGE_COLOR.value

    return header, msg, color

def build_password_message(content: str) -> tuple[str, str, int]:
    header, msg = build_message(SYSTEM_USER, PASSWORD_MSG_TEXT + password_display(content))
    color = CLIColors.SYSTEM_MESSAGE_COLOR.value

    return header, msg, color

def build_command_message(cmd_name: str, args: list[str]) -> tuple[str, str, int]:
    header, msg = build_message(YOUR_USER, f"Activated '{cmd_name}' with args={args}")
    color = CLIColors.YOUR_MESSAGE_COLOR.value
    
    return header, msg, color