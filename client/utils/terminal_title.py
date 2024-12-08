import os

def set_terminal_title(title: str):
    if os.name == "nt":
        os.system(f"title {title}")
    elif os.name == "posix":
        os.system(f"PROMPT_COMMAND='echo -en \"\033]0;{title}\a\"'")

def clear_terminal_title():
    if os.name == "nt":
        os.system(f"title ")
    elif os.name == "posix":
        os.system(f"PROMPT_COMMAND='echo -en \"\033]0; \a\"'")