import signal
import sys
from datetime import datetime
from typing import Optional, TextIO

from pynput.mouse import Listener


class Recorder:
    _filename: str
    _listener: Listener
    _output: TextIO
    _start_time: datetime
    _stop_time: datetime

    def __init__(self, filename: str):
        self._filename = filename
        self._listener = Listener(on_click=self._on_click)
        signal.signal(signal.SIGINT, self._signal_handler)

        if self._filename:
            self._output = open(self._filename, 'w')

        else:
            self._output = sys.stdout

        self._write("MACRO macro_name {")

    def record(self):
        with self._listener:
            self._listener.join()

    def _signal_handler(self, sig, frame):
        print('Exiting...')
        self._listener.stop()
        self._write("}")
        self._output.close()

    def _write(self, data: str):
        self._output.write(f"{data}\n")
        self._output.flush()

    def _get_second_delta(self) -> Optional[int]:
        try:
            return int((self._stop_time - self._start_time).total_seconds())
        except (AttributeError, ValueError):
            return None

    def _on_click(self, x, y, button, pressed):
        self._stop_time = datetime.now()
        x = int(x)
        y = int(y)

        if self._get_second_delta() is not None \
                and self._get_second_delta() > 0:
            if self._filename:
                print(f"Wait {self._get_second_delta()} seconds")

            self._write(f"    WAIT {self._get_second_delta()}s")

        if pressed:
            if self._filename:
                print(f"Mouse clicked at ({x}, {y})")

            self._write(f"    CLICK {x},{y}")
            self._start_time = datetime.now()
