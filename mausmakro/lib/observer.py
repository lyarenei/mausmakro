from __future__ import annotations

from typing import Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from lib.observable import Observable, MessageType


class Observer:
    _observables: List[Observable]

    def __init__(self):
        self._observables = []

    def register(self, observable: Observable):
        self._observables.append(observable)

    def unregister(self, observable: Observable):
        self._observables.remove(observable)

    def update(self, msg_type: MessageType, msg_data: Any):
        raise NotImplementedError
