from dataclasses import dataclass, asdict
import json

from users import UserList, User

from constants.logic import SYSTEM_USER, Privileges
from constants.texts import *
from constants.ack_codes import ack_to_text, errored_ack_codes
from constants.colors import CLIColors

from utils.build_message import build_message

class Message:
    type: int
    
    error: bool
    color: int
    keep_color_after_username: bool

    def __init__(self) -> None:
        self.error = False
        self.color = CLIColors.DEFAULT_COLOR.value
        self.keep_color_after_username = False
        
    def deserialize(self, json_msg: dict) -> None:
        self.type = int(json_msg['type'])
        
    def handle(self) -> None:
        pass
    
    def serialize(self):
        result = asdict(self)
        result["type"] = type(self).__name__
        
        return json.dumps(result)

    def __str__(self) -> str:
        return None

@dataclass
class ClientMessage(Message):
    username: str
    content: str

    def __init__(self) -> None:
        super().__init__()
        
    def deserialize(self, json_msg: dict) -> None:
        super().deserialize(json_msg)
        
        self.username = json_msg['username']
        self.content = json_msg['content']
        
    def handle(self) -> None:
        user_list = UserList()
        
        # Check if the user is admin
        if user_list.get_user(self.username).privilege == Privileges.ADMIN.value:
            self.color = CLIColors.ADMIN_MESSAGE_COLOR.value

    def __str__(self) -> str:
        return build_message(self.username, self.content)

@dataclass
class AckMessage(Message):
    code: int

    def __init__(self) -> None:
        super().__init__()

    def deserialize(self, json_msg: dict) -> None:
        super().deserialize(json_msg)
        
        self.code = int(json_msg['code'])

        self.error = (self.code in errored_ack_codes)
        if self.error:
            self.color = CLIColors.ERROR_COLOR.value
            self.keep_color_after_username = True
        else:
            self.color = CLIColors.SYSTEM_MESSAGE_COLOR.value
            self.keep_color_after_username = True

    def __str__(self) -> str:
        return build_message(SYSTEM_USER, ack_to_text[self.code])

@dataclass
class JoinMessage(Message):
    username: str
    privilege: int

    def __init__(self) -> None:
        super().__init__()
        
        self.color = CLIColors.JOIN_LEFT_COLOR.value
        self.keep_color_after_username = True

    def deserialize(self, json_msg: dict) -> None:
        super().deserialize(json_msg)
        
        self.username = json_msg['username']
        self.privilege = int(json_msg['privilege'])

    def handle(self) -> None:
        user_list = UserList()
        
        # Register user to userlist
        user_list.add_user(User(self.username, self.privilege))
    
    def __str__(self) -> str:
        return build_message(SYSTEM_USER, self.username + JOINED_MSG_TEXT)

@dataclass
class InvalidMessage(Message):
    def __init__(self) -> None:
        super().__init__()
        
        self.error = True
        self.color = CLIColors.ERROR_COLOR.value
        self.keep_color_after_username = True
        
    def __str__(self) -> str:
        return build_message(SYSTEM_USER, INVALID_MESSAGE_TEXT)

@dataclass 
class LeaveMessage(Message):
    username: str
    
    def __init__(self) -> None:
        super().__init__()
        
        self.color = CLIColors.JOIN_LEFT_COLOR.value
        self.keep_color_after_username = True
        
    def deserialize(self, json_msg: dict) -> None:
        super().deserialize(json_msg)
        
        self.username = json_msg['username']
        
    def handle(self) -> None:
        user_list = UserList()
        
        # Delete user from userlist
        user_list.del_user(self.username)
        
    def __str__(self) -> str:
        return build_message(SYSTEM_USER, self.username + LEFT_MSG_TEXT)