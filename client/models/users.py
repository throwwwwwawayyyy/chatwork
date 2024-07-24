class User:
    name: str
    privilege: int

    def __init__(self, name: str, privilige: int) -> None:
        self.name = name
        self.privilege = privilige

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return (self.name == other.name and self.privilege == other.privilege)
        return False
    
    def __ne__(self, other: object) -> bool:
        if isinstance(other, User):
            return (self.name != other.name or self.privilege != other.privilege)
        return True
    
class Singleton(object):
    _instances = None
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instances, class_):
            class_._instances = object.__new__(class_, *args, **kwargs)
        return class_._instances

class UserList(Singleton):
    user_list: list[User] = []

    def add_user(self, user: User) -> None:
        for _user in self.user_list:
            if user == _user:
                return

        self.user_list.append(user)

    def get_user(self, name: str) -> User:
        for _user in self.user_list:
            if _user.name == name:
                return _user
            
        return None
    
    def del_user(self, name: str) -> None:
        for _user in self.user_list:
            if _user.name == name:
                self.user_list.remove(_user)
                break