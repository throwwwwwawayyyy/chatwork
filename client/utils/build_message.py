from constants.logic import UI_SEP

def build_message(user:str, content:str) -> str:
    return f"[{user}]{UI_SEP} {content}"