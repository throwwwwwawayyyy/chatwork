from constants.logic import PASSWORD_DISPLAY_CHARACTER
from constants.logic import YOUR_USER, SYSTEM_USER
from constants.colors import CLIColors

def password_display(password: str) -> str:
    disp = ""
    for elm in password:
        disp += PASSWORD_DISPLAY_CHARACTER
    
    return disp

def input_prompt(content: str) -> tuple[str, int]:
    prompt = f"[{YOUR_USER}]: {content}"
    color = CLIColors.YOUR_MESSAGE_COLOR.value

    return prompt, color

def username_prompt(content: str) -> tuple[str, int]:
    prompt = f"[{SYSTEM_USER}]: username {content}"
    color = CLIColors.SYSTEM_MESSAGE_COLOR.value

    return prompt, color

def password_prompt(content: str) -> tuple[str, int]:
    prompt = f"[{SYSTEM_USER}]: password {password_display(content)}"
    color = CLIColors.SYSTEM_MESSAGE_COLOR.value

    return prompt, color