from enum import Enum, auto
from typing import Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from lib.observer import Observer


class MessageType(Enum):
    MESSAGE = auto()


class Observable:

    _observers: List[Observer]

    def __init__(self):
        self._observers = []

    def register(self, observer: Observer):
        self._observers.append(observer)

    def unregister(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, msg_type: MessageType, msg_data: Any):
        for observer in self._observers:
            observer.update(msg_type, msg_data)
