import sys
from typing import List
import signal
from time import sleep

from lark import Tree

from builder import Builder
from definitions.general import Conditional, Executable, Instruction, Macro
from definitions.enums import Opcode


class Interpreter:

    _macro_list: List[Macro]
    _instruction_list: List[Executable]
    is_paused: bool

    def __init__(self, ast: Tree):
        self._macro_list = Builder().parse_tree(ast)
        self._instruction_list = []
        self.is_paused = False
        signal.signal(signal.SIGINT, self._sigint_handler)

    def _get_macro(self, name: str):
        for m in self._macro_list:
            if m.name == name:
                return m

        raise ValueError(f"Macro {name} is not defined!")

    def _do_interpret(self):
        while self._instruction_list:
            if self.is_paused:
                print("Macro paused.")
                input("Press ENTER to continue "
                      "or send INT signal again to exit.\n")
                print("Execution will resume in 5 seconds")
                self.is_paused = False
                sleep(5)

            ins = self._instruction_list.pop(0)
            if isinstance(ins, Instruction):
                self._do_instruction(ins)

            elif isinstance(ins, Conditional):
                self._do_conditional(ins)

    def _do_instruction(self, instr: Instruction):
        if instr.opcode == Opcode.CALL:
            macro = self._get_macro(instr.arg)
            body = macro.body.copy()
            body.extend(self._instruction_list)
            self._instruction_list = body

        elif instr.opcode == Opcode.JUMP:
            macro = self._get_macro(instr.arg)
            self._instruction_list.clear()
            self._instruction_list = macro.body.copy()

        elif instr.opcode == Opcode.PAUSE:
            self.is_paused = True

        else:
            instr.execute()

    def _do_conditional(self, cond: Conditional):
        try:
            cond.condition.execute()
            failed = False
        except Exception:
            failed = True

        main_branch = cond.body.copy()
        else_branch = cond.else_body.copy() if cond.else_body else None

        if failed:
            new_instr_list = main_branch if cond.negate else else_branch
        else:
            new_instr_list = else_branch if cond.negate else main_branch

        if new_instr_list:
            new_instr_list.extend(self._instruction_list)
            self._instruction_list = new_instr_list

    def interpret(self, macro_name: str, repeats: int = -1):
        macro = self._get_macro(macro_name)
        loops = 0
        while True:
            if repeats >= 0:
                print(f"Iteration: {loops}")
                loops += 1
                if loops > repeats:
                    break
            self._instruction_list = macro.body.copy()
            self._do_interpret()

    def _sigint_handler(self, sig, frame):
        if self.is_paused:
            print("Macro is already paused, exiting...")
            sys.exit(0)

        self.is_paused = True
