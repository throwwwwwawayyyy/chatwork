import json

class B:
    @staticmethod
    def test():
        print("test")

b = B()
t = {1: type(b)}
print(json.dumps(t))