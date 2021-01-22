from typing import Any, Dict, List

from pynput import keyboard
from pynput.keyboard import Key

from interpreter import Interpreter
from lib.observable import MessageType
from lib.observer import Observer
from lib.types import Instruction


class Ui(Observer):

    _kb_listener: keyboard.Listener

    def __init__(self):
        super(Ui, self).__init__()
        self._kb_listener = keyboard.Listener(on_release=self._on_release)
        self._kb_listener.start()

    def update(self, msg_type: MessageType, msg_data: Any):
        if msg_type == MessageType.MESSAGE:
            print(msg_data)

    def start(self,
              instructions: List[Instruction],
              label_table: Dict[str, int],
              opts: Dict[str, Any]):
        # TODO create and register observable
        # TODO start interpreting
        pass

    def terminate(self):
        # TODO Stop interpreter, listening for keyboard and exit program
        pass

    def _on_release(self, key):
        for o in self._observables:
            if isinstance(o, Interpreter):
                self.handle_interpreter(o, key)

    @staticmethod
    def handle_interpreter(interpreter: Interpreter, key):
        if key == Key.ctrl:
            interpreter.toggle_execution()
