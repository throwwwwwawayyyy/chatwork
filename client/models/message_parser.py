from constants.logic import MessageType, Privileges
from constants.colors import CLIColors
from models.message import *
from models.users import User, UserList

class MessageTypeParser:
    user_list: UserList

    def __init__(self) -> None:
        self.user_list = UserList()

    def parse(self, msg_to_parse: str) -> tuple[str, bool, int, bool]:
        parsed_msg: Message

        if msg_to_parse.startswith(str(MessageType.CLIENT.value)):
            parsed_msg = ClientMessage(msg_to_parse)

            # Get user credentials
            if self.user_list.get_user(parsed_msg.username) == Privileges.ADMIN.value:
                parsed_msg.color = CLIColors.ADMIN_MESSAGE_COLOR.value
        elif msg_to_parse.startswith(str(MessageType.ACK.value)):
            parsed_msg = AckMessage(msg_to_parse)
        elif msg_to_parse.startswith(str(MessageType.JOIN.value)):
            parsed_msg = JoinMessage(msg_to_parse)
            
            # Register user to userlist
            self.user_list.add_user(User(parsed_msg.username, parsed_msg.privilege))
        else:
            parsed_msg = InvalidMessage(msg_to_parse)

        return str(parsed_msg), parsed_msg.error, parsed_msg.color, parsed_msg.keep_color