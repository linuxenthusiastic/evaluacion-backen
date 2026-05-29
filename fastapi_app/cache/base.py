from abc import ABC, abstractmethod


class BaseCache(ABC):

    @abstractmethod
    def get(self, key: str):
        ...

    @abstractmethod
    def set(self, key: str, value, ttl: int):
        ...

    @abstractmethod
    def delete_pattern(self, pattern: str):
        ...
