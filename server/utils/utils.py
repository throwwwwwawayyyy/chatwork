from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.client_manager import ClientManager
    from managers.group_manager import GroupManager


def get_client_by_username(clients: list['ClientManager'], username: str):
    for client in clients:
        if client.username == username:
            return client
        

def get_group_by_name(groups: list['GroupManager'], group_name = str):
    for group in groups:
        if group.name == group_name:
            return group