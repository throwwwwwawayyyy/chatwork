import json

from constants.logic import *
from constants.colors import CLIColors
from models.message import *
from models.ui_message import UIMessage
from utils.build_message import *

class MessageParser:
    username: str
    password: str
    level: int = USERNAME_LEVEL
    
    def get_username(self) -> str:
        return self.username
    
    def get_level(self) -> int:
        return self.level
    
    def increment_level(self) -> None:
        self.level += 1
        
    def set_level_default(self) -> None:
        self.level = USERNAME_LEVEL
    
    def parse_from_server(self, msg_to_parse: str) -> Message:
        json_msg_obj = json.loads(msg_to_parse)
        msg_obj: Message

        if json_msg_obj['type'] == MessageType.CLIENT.value:
            msg_obj = ClientMessage()     
        elif json_msg_obj['type'] == MessageType.ACK.value:
            msg_obj = AckMessage() 
        elif json_msg_obj['type'] == MessageType.JOIN.value:
            msg_obj = JoinMessage()
        elif json_msg_obj['type'] == MessageType.LEAVE.value:
            msg_obj = LeaveMessage()
        elif json_msg_obj['type'] == MessageType.DISCONNECT.value:
            msg_obj = DisconnectMessage()
        elif json_msg_obj['type'] == MessageType.COMMAND.value:
            msg_obj = CommandMessage()
        elif json_msg_obj['type'] == MessageType.SYSTEM.value:
            msg_obj = SystemMessage()
        else:
            msg_obj = InvalidMessage()
        
        msg_obj.deserialize(json_msg_obj)
        msg_obj.handle()

        return msg_obj
    
    def parse_from_client(self, input_content: str) -> tuple[Message, UIMessage]:
        content = ""
        color = 0
        keep_color_after_username = False
        msg_obj: Message = None

        if self.level == USERNAME_LEVEL:
            self.username = input_content
            self.increment_level()
            header, content, color = build_username_message(input_content)
            keep_color_after_username = True
        elif self.level == PASSWORD_LEVEL:
            self.password = input_content
            header, content, color = build_password_message(input_content)
            keep_color_after_username = True
                    
            msg_obj = AuthMessage(self.username, self.password)
        elif self.level == CHAT_LEVEL:
            if input_content.startswith(COMMAND_PREFIX):  
                cmd_list = input_content.split(" ")
                
                msg_obj = CommandMessage()
                msg_obj.cmd_name = cmd_list[0][COMMAND_PREFIX_INDEX+1:]
                msg_obj.args = cmd_list[1:]
                
                header, content, color = build_command_message(msg_obj.cmd_name, msg_obj.args)
                keep_color_after_username = True
            else:
                header, content, color = build_input_message(input_content)
                    
                msg_obj = ClientMessage()
                msg_obj.username = self.username
                msg_obj.content = input_content
            
        return msg_obj, UIMessage(header, content, color, keep_color_after_username)