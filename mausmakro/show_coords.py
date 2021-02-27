import signal
import sys
from typing import TextIO

from pynput.mouse import Listener


class ShowCoords:
    _listener: Listener
    _output: TextIO

    def __init__(self):
        self._listener = Listener(on_click=self._on_click)
        signal.signal(signal.SIGINT, self._signal_handler)
        self._output = sys.stdout

    def start(self):
        with self._listener:
            self._listener.join()

    def _signal_handler(self, sig, frame):
        self._listener.stop()

    def _write(self, data: str):
        self._output.write(f"{data}\n")
        self._output.flush()

    def _on_click(self, x, y, button, pressed):
        x = int(x)
        y = int(y)

        if pressed:
            self._write(f"{x},{y}")
