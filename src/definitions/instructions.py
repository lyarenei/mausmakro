import sys
from datetime import datetime, timedelta
from time import sleep
from typing import Any, Optional, Tuple

import pyautogui

from definitions.enums import Opcode
from definitions.general import Instruction


class CallInstruction(Instruction):

    opcode = Opcode.CALL

    def __init__(self, arg: str):
        super().__init__(arg)

    def execute(self):
        print(f"Call {self.arg}")


class ClickInstruction(Instruction):

    opcode = Opcode.CLICK
    clicks = 1
    image: Optional[str] = None
    timeout: Optional[int] = None

    def __init__(self, arg: Tuple[Any, int]):
        super().__init__(arg)

        # Click on image instead of coords
        if isinstance(arg[0], str):
            pyautogui.useImageNotFoundException()
            self.image = arg[0]
            self.timeout = arg[1]

    @staticmethod
    def _fix_coords(coords: Tuple[int, int]) -> Tuple[int, int]:
        if sys.platform == 'darwin':
            return int(coords[0]/2), int(coords[1]/2)

        return coords

    def execute(self):
        if self.image:
            deadline = datetime.now() + timedelta(seconds=self.timeout)
            print(f"Finding image .. {self.image}")
            while datetime.now() < deadline:
                try:
                    coords = pyautogui.locateCenterOnScreen(self.image,
                                                            grayscale=True,
                                                            step=2)
                    coords = self._fix_coords(coords)
                    pyautogui.click(*coords, clicks=self.clicks)
                    print("Image found")
                    return True
                except pyautogui.ImageNotFoundException:
                    pass

                sleep(0.5)

            print("Image not found within the time limit")
            raise pyautogui.ImageNotFoundException

        else:
            print(f"Click at {self.arg[0]},{self.arg[1]}")
            pyautogui.click(x=self.arg[0], y=self.arg[1], clicks=self.clicks)


class DoubleClickInstruction(ClickInstruction):

    opcode = Opcode.DOUBLE_CLICK
    clicks = 2

    def __init__(self, arg: Tuple[Any, int]):
        super().__init__(arg)


class FindInstruction(Instruction):

    opcode = Opcode.FIND
    timeout: int

    def __init__(self, arg: Tuple[str, int]):
        super().__init__(arg)
        pyautogui.useImageNotFoundException()

        self.arg = arg[0]
        self.timeout = arg[1]

    def execute(self):
        deadline = datetime.now() + timedelta(seconds=self.timeout)
        print(f"Finding image .. {self.arg}")
        while datetime.now() < deadline:
            try:
                pyautogui.locateOnScreen(self.arg,
                                         grayscale=True,
                                         step=2)
                print("Image found")
                return
            except pyautogui.ImageNotFoundException:
                pass

            sleep(0.5)

        print("Image not found within the time limit")
        raise pyautogui.ImageNotFoundException


class JumpInstruction(Instruction):

    opcode = Opcode.JUMP

    def __init__(self, arg: str):
        super().__init__(arg)

    def execute(self):
        print(f"Jump {self.arg}")


class WaitInstruction(Instruction):

    opcode = Opcode.WAIT

    def __init__(self, arg: int):
        super().__init__(arg)

    def execute(self):
        print(f"Waiting {self.arg} seconds")
        sleep(self.arg)
