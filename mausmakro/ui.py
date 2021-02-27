import signal
import sys
from threading import Thread
from typing import Any, Dict, List

from pynput import keyboard
from pynput.keyboard import Key

from mausmakro.interpreter import Interpreter
from mausmakro.lib.observable import MessageType
from mausmakro.lib.observer import Observer
from mausmakro.lib.types import Instruction


class Ui(Observer):
    _kb_listener: keyboard.Listener

    def __init__(self):
        super(Ui, self).__init__()
        self._kb_listener = keyboard.Listener(on_release=self._on_release)
        self._kb_listener.start()

    def update(self, msg_type: MessageType, msg_data: Any):
        if msg_type == MessageType.MESSAGE:
            print(msg_data)

        elif msg_type == MessageType.MAUSMAKRO_EXCEPTION:
            print(f"An error occurred:\n{msg_data}", file=sys.stderr)
            self.stop()

    def start(self,
              macro: str,
              times: int,
              instructions: List[Instruction],
              label_table: Dict[str, int],
              opts: Dict[str, Any]):

        observable = Interpreter(instructions, label_table, opts)
        observable.register(self)
        self.register(observable)
        signal.signal(signal.SIGINT, self.terminate)

        iters = 0
        while iters < times or times == -1:
            try:
                interpret_thread = Thread(target=observable.interpret,
                                          args=[macro])

                interpret_thread.start()
                interpret_thread.join()

            except Exception as e:
                print(
                    f"An error occurred when interpreting the macro:\n{e}",
                    file=sys.stderr
                )
                sys.exit(2)

            iters += 1

    def stop(self):
        self._kb_listener.stop()
        for o in self._observables:
            if isinstance(o, Interpreter):
                o.stop()

    def terminate(self, signum, frame):
        print("Waiting for all running processes to finish execution ..")
        self.stop()
        sys.exit(1)

    def _on_release(self, key):
        for o in self._observables:
            if isinstance(o, Interpreter):
                self.handle_interpreter(o, key)

    @staticmethod
    def handle_interpreter(interpreter: Interpreter, key):
        if key == Key.ctrl:
            interpreter.toggle_execution()
