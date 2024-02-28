conf = { 
    "color": "blue",
    "size": 15,
    "shlomi": True
}

class Config:
    def __init__(self):
        self._config = conf # set it to conf

    def get_property(self, property_name):
        if property_name not in self._config.keys(): # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]
    

class MongoConfig(Config):
    @property
    def color(self) -> str:
        return self.get_property('color')

    @property
    def size(self) -> int:
        return self.get_property('size')

    @property
    def shlomi(self) -> bool:
        return self.get_property('shlomi')


print(MongoConfig.color)