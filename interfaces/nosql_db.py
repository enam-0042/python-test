from abc import ABC, abstractmethod
from typing import Any

class NoSQLDatabase(ABC):
    @abstractmethod
    def connect(self):
        raise NotImplementedError("Implement the connect method")

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError("implement the disconnect method")

    @abstractmethod
    def set(self, key: Any, value: Any, exp=604800):
        raise NotImplementedError("Implement the add method here")

    @abstractmethod
    def get(self, key: Any):
        raise NotImplementedError("add the get method")
