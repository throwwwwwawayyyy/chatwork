import json

from constants.logic import MessageType
from models.message import *

class MessageTypeParser:
    @staticmethod
    def parse(msg_to_parse: str) -> Message:
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
        else:
            msg_obj = InvalidMessage()
        
        msg_obj.deserialize(json_msg_obj)
        msg_obj.handle()

        return msg_obj