from abc import ABC, abstractmethod

class EmailSender(ABC):
    @abstractmethod
    def send(self) -> None:
        pass