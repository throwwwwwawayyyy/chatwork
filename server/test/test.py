class Config:
    def __init__(self, filename):
        self._config = conf

    def get_property(self, property_name):
        return self._config.get(property_name)
    

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