import sys
from threading import Thread
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
              macro: str,
              times: int,
              instructions: List[Instruction],
              label_table: Dict[str, int],
              opts: Dict[str, Any]):

        observable = Interpreter(instructions, label_table, opts)
        observable.register(self)
        self.register(observable)

        iters = 0
        while iters < times or times == -1:
            try:
                interpret_thread = Thread(target=observable.interpret,
                                          args=[macro])

                interpret_thread.start()
                interpret_thread.join()

            except Exception as e:
                print(f"An error occurred when interpreting the macro:\n{e}")
                sys.exit(2)

            iters += 1

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
