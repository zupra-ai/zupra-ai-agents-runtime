from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def remove(self, entity):
        pass

    @abstractmethod
    def find_all(self):
        pass