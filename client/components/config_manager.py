import yaml
from typing import Any


class Config:
    def __init__(self, filename: str) -> None:
        with open(f"client/config/{filename}", 'r') as f:
            self._config: dict = yaml.safe_load(f)

    def get_property(self, property_name) -> (Any | None):
        return self._config.get(property_name)


class NetworkConfig(Config):
    def __init__(self) -> None:
        super().__init__("network_config.yml")
    
    @property
    def ip(self) -> str:
        return self.get_property('ip')

    @property
    def port(self) -> int:
        return self.get_property('port')