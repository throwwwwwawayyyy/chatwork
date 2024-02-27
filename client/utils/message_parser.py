from constants.logic import MessageType
from models.messages import Message, AckMessage, ClientMessage, JoinMessage

class MessageParser:
    @staticmethod
    def parse(msg_to_parse: str) -> tuple[str, bool]:
        parsed_msg: Message
    
        if msg_to_parse.startswith(MessageType.CLIENT):
            parsed_msg = ClientMessage(msg_to_parse)
        elif msg_to_parse.startswith(MessageType.ACK):
            parsed_msg = AckMessage(msg_to_parse)
        elif msg_to_parse.startswith(MessageType.SERVER):
            parsed_msg = JoinMessage(msg_to_parse)
        else:
            raise "Invalid Message Type"

        return str(parsed_msg), parsed_msg.error