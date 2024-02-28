from constants.logic import MessageType, Privileges
from constants.colors import CLIColors
from models.messages import Message, AckMessage, ClientMessage, JoinMessage
from models.users import User, UserList

class MessageParser:
    user_list: UserList

    def __init__(self) -> None:
        self.user_list = UserList()

    def parse(self, msg_to_parse: str) -> tuple[str, bool, int, bool]:
        parsed_msg: Message
        cli_color = CLIColors.DEFAULT_COLOR.value
        keep_color = False

        if msg_to_parse.startswith(str(MessageType.CLIENT.value)):
            parsed_msg = ClientMessage(msg_to_parse)

            if self.user_list.get_user(parsed_msg.username) == Privileges.ADMIN.value:
                cli_color = CLIColors.ADMIN_MESSAGE_COLOR.value
        elif msg_to_parse.startswith(str(MessageType.ACK.value)):
            parsed_msg = AckMessage(msg_to_parse)
            cli_color = CLIColors.SYSTEM_MESSAGE_COLOR.value
            keep_color = True
        elif msg_to_parse.startswith(str(MessageType.SERVER.value)):
            parsed_msg = JoinMessage(msg_to_parse)

            join_user = User(parsed_msg.username, parsed_msg.privilege)
            self.user_list.add_user(join_user)

            cli_color = CLIColors.SYSTEM_MESSAGE_COLOR.value
            keep_color = True
        else:
            raise Exception("Invalid Message Type")
        
        if parsed_msg.error:
            cli_color = CLIColors.ERROR_COLOR.value
            keep_color = True

        return str(parsed_msg), parsed_msg.error, cli_color, keep_color