import sys
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
from typing import Any, Dict, List, Optional, Tuple

import pyautogui
from pynput import keyboard

from definitions.general import Conditional, Instruction, Command, Stack
from definitions.exceptions import ConditionException, InterpretException, \
    MausMakroException, RetryException
from definitions.enums import Opcode


class Interpreter:

    _call_stack: Stack
    _instructions: List[Instruction]
    _kb_listener: keyboard.Listener
    _label_table: Dict[str, int]
    _program_counter: int

    exit_requested = False
    go_back_on_fail: bool
    is_paused = False
    opts: Dict[str, Any]

    def __init__(self, instructions,
                 label_table: Dict[str, int],
                 opts: Dict[str, Any]):

        self._call_stack = Stack()
        self._instructions = instructions
        self._kb_listener = keyboard.Listener(on_release=self._on_release)
        self._label_table = label_table
        self._program_counter = 0

        self.opts = opts

        # Throw exceptions instead of returning None
        pyautogui.useImageNotFoundException()

        self._kb_listener.start()

    def interpret(self, macro: str):
        self._program_counter = self._label_table[macro]
        retries = 0

        while not self.exit_requested:
            self.prompt_if_paused()
            instr = self._instructions[self._program_counter]

            if instr.opcode == Opcode.END:
                break

            try:
                self._execute_instruction(instr)
                self._program_counter += 1

            except MausMakroException as e:
                if self.exit_requested:
                    break

                print("Command execution failed")
                if self.opts['enable_retry'] \
                   and retries <= self.opts['retry_times']:
                    print("Command retry enabled, retrying command...")
                    self._retry_instruction(instr)

                else:
                    raise e

    def _retry_instruction(self, instr: Instruction):
        retries = 1

        while retries <= self.opts['retry_times']:
            self.prompt_if_paused()
            print(f"Retries: {retries}/{self.opts['retry_times']}")

            try:
                self._execute_instruction(instr)
                return

            except Exception as e:
                print(e)
                retries += 1

        raise RetryException("Maximum retries reached, giving up.")

    def _on_release(self, key):
        try:
            if key.char == 'p':
                print("Pausing execution at the next possible moment...")
                self.is_paused = True

            elif key.char == 'x':
                print("Exiting...")
                self.is_paused = False
                self.exit_requested = True

        except AttributeError:
            # Special key pressed
            pass

    def _execute_instruction(self, instruction: Instruction):
        if isinstance(instruction, Command):
            return self._execute_command(instruction)

        instruction: Conditional
        self._execute_conditional(instruction)

    def _execute_command(self, command: Command) -> Optional[bool]:
        if command.opcode == Opcode.CALL:
            print(f"Call {command.arg}")
            self._call_stack.push(self._program_counter)
            index = self._label_table[command.arg]
            self._program_counter = index

        elif command.opcode == Opcode.CLICK:
            return self._do_click(command.arg)

        elif command.opcode == Opcode.DOUBLE_CLICK:
            return self._do_click(command.arg, is_double=True)

        elif command.opcode == Opcode.EXIT:
            print("Exiting...")
            sys.exit(0)

        elif command.opcode == Opcode.FIND:
            self._find_image(command.arg[0], command.arg[1])

        elif command.opcode == Opcode.JUMP:
            print(f"Jump to {command.arg}")
            index = self._label_table[command.arg]
            self._program_counter = index

        elif command.opcode == Opcode.LABEL:
            return

        elif command.opcode == Opcode.PAUSE:
            self.is_paused = True

        elif command.opcode == Opcode.RETURN:
            if self._call_stack.empty():
                raise InterpretException("Cannot return, no caller!")

            index = self._call_stack.pop()
            self._program_counter = index

        elif command.opcode == Opcode.WAIT:
            print(f"Waiting {command.arg} seconds")
            sleep(command.arg)

        else:
            raise NotImplementedError(f"Instruction {command.opcode} "
                                      "is not implemented!")

    def _execute_conditional(self, cond: Conditional):
        try:
            self._execute_instruction(cond.condition)
            failed = True if cond.negate else False

        except ConditionException:
            failed = False if cond.negate else True

        if cond.else_label and failed:
            new_pc = self._label_table[cond.else_label]

        elif not cond.else_label and failed:
            new_pc = self._label_table[cond.end_label]

        else:
            new_pc = self._program_counter

        self._program_counter = new_pc

    def _do_click(self, args: Tuple[Any, Any], is_double=False):
        clicks = 2 if is_double else 1

        if isinstance(args[0], int):
            print(f"Click at {args[0]},{args[1]}")
            pyautogui.click(x=args[0], y=args[1], clicks=clicks)
            return

        coords = self._find_image(args[0], args[1])
        pyautogui.click(*coords, clicks=clicks)

    @staticmethod
    def _fix_coords(coords: Tuple[int, int]) -> Tuple[int, int]:
        if sys.platform == 'darwin':
            return int(coords[0]/2), int(coords[1]/2)

        return coords

    def _find_image(self, image: str, timeout: int) -> Tuple[int, int]:
        img_path = Path(image)
        grayscale = not self.opts['color_match']
        match_step = self.opts['match_step']

        if not img_path.is_absolute():
            abs_path = Path(self.opts['file']).parent
            img_path = abs_path.joinpath(Path(f'images/{image}'))

        deadline = datetime.now() + timedelta(seconds=timeout)
        print(f"Finding image .. {image}")

        while datetime.now() < deadline:
            try:
                coords = pyautogui.locateCenterOnScreen(str(img_path),
                                                        grayscale=grayscale,
                                                        step=match_step)
                print("Image found")
                return self._fix_coords(coords)

            except pyautogui.ImageNotFoundException:
                # Try again
                pass

            sleep(1)

        raise ConditionException("Image not found within the time limit")

    def prompt_if_paused(self):
        if self.is_paused:
            input("Macro paused. Press ENTER to resume")
            print("Execution will resume in 5 seconds")
            sleep(5)
            self.is_paused = False
