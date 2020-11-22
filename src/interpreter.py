from typing import List

from lark import Tree

from builder import Builder
from definitions.general import Conditional, Executable, Instruction, Macro
from definitions.enums import Opcode


class Interpreter:

    _macro_list: List[Macro]
    _instruction_list: List[Executable]

    def __init__(self, ast: Tree):
        self._macro_list = Builder().parse_tree(ast)
        self._instruction_list = []

    def _get_macro(self, name: str):
        for m in self._macro_list:
            if m.name == name:
                return m

        raise ValueError(f"Macro {name} is not defined!")

    def _do_interpret(self):
        while self._instruction_list:
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

        else:
            instr.execute()

    def _do_conditional(self, cond: Conditional):
        try:
            cond.condition.execute()
            body = cond.body.copy()
        except Exception:
            if cond.else_body:
                body = cond.else_body.copy()
            else:
                return

        body.extend(self._instruction_list)
        self._instruction_list = body

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
