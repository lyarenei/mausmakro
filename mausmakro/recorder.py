import signal
import sys
from datetime import datetime
from typing import List, Optional, TextIO

from pynput.mouse import Listener

from mausmakro.lib.enums import Opcode
from mausmakro.lib.types import Command, Instruction


class Recorder:
    _filename: str
    _instructions: List[Instruction]
    _listener: Listener
    _output: TextIO
    _start_time: datetime
    _stop_time: datetime

    def __init__(self, filename: str):
        self._filename = filename
        self._instructions = []
        self._listener = Listener(on_click=self._on_click)
        signal.signal(signal.SIGINT, self._signal_handler)

        if self._filename:
            self._output = open(self._filename, 'w')

        else:
            self._output = sys.stdout

    def record(self):
        print("Recording started. Press Ctrl+C to stop.\n"
              "The macro will be available as soon as the recording stops.")
        with self._listener:
            self._listener.join()

    def print_instructions(self):
        self._write("MACRO macro_name {")

        for i in self._instructions:
            if isinstance(i, Command):
                self.print_command(i)

        self._write("}")

    def print_command(self, cmd: Command):
        data = None
        indent = '    '

        if cmd.opcode == Opcode.CLICK:
            args = map(str, cmd.arg)
            data = f"CLICK {', '.join(args)}"

        elif cmd.opcode == Opcode.WAIT:
            data = f"WAIT {cmd.arg}s"

        self._write(f'{indent}{data}')

    def _signal_handler(self, sig, frame):
        print("\nRecording stopped, here is your macro:\n")
        self._listener.stop()
        self.print_instructions()
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

        if (
                self._get_second_delta() is not None
                and self._get_second_delta() > 0
        ):
            self._write(f"Waited {self._get_second_delta()} seconds")
            cmd = Command(Opcode.WAIT, self._get_second_delta())
            self._instructions.append(cmd)

        if pressed:
            self._write(f"Mouse clicked at ({x}, {y})")
            cmd = Command(Opcode.CLICK, (x, y))
            self._instructions.append(cmd)
            self._start_time = datetime.now()
