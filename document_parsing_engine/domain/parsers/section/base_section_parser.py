from abc import ABC, abstractmethod


class BaseSectionParser(ABC):
    @abstractmethod
    def can_parse(self, section) -> bool:
        raise NotImplementedError

    @abstractmethod
    def parse(self, doc: dict, section) -> dict:
        raise NotImplementedError
