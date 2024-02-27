from constants.logic import MessageType
from models.messages import Message, AckMessage, ClientMessage, JoinMessage

class MessageParser:
    @staticmethod
    def parse(msg_to_parse: str) -> tuple[str, bool]:
        parsed_msg: Message

        if msg_to_parse.startswith(str(MessageType.CLIENT.value)):
            parsed_msg = ClientMessage(msg_to_parse)
        elif msg_to_parse.startswith(str(MessageType.ACK.value)):
            parsed_msg = AckMessage(msg_to_parse)
        elif msg_to_parse.startswith(str(MessageType.SERVER.value)):
            parsed_msg = JoinMessage(msg_to_parse)
        else:
            raise Exception("Invalid Message Type")

        return str(parsed_msg), parsed_msg.error