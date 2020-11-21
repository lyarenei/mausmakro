from pathlib import Path
from typing import List

from lark import Token, Tree

from definitions.general import Conditional, Executable, Macro
from definitions.instructions import *
from definitions.enums import ArgType, Opcode


class Builder:

    _label_table: List[str]
    _macro_list: List[Macro]

    def __init__(self):
        self._label_table = []
        self._macro_list = []

    @staticmethod
    def parse_token(token: Token) -> Any:
        if token.type == ArgType.NAME or token.type == ArgType.FILE:
            return str(token.value)

        elif token.type == ArgType.COORDS:
            coords = token.value.partition(',')
            return int(coords[0]), int(coords[2])

        elif token.type == ArgType.TIME:
            num = int(''.join(filter(str.isdigit, token.value)))
            if token.value[-1] == 'm':
                num *= 60

            elif token.value[-1] == 'h':
                num *= 3600

            return num

        else:
            raise NotImplementedError(
                f" Parsing for token {token.type} is not implemented!")

    def parse_instruction(self, instruction: Tree) -> Instruction:
        opcode = instruction.data
        arg = tuple(map(self.parse_token, instruction.children))
        arg = arg[0] if len(arg) == 1 else arg

        if opcode == Opcode.CALL:
            assert arg in self._label_table, \
                f"Instruction {opcode} {arg} uses undefined label!"

            return CallInstruction(arg)

        elif opcode == Opcode.CLICK:
            return ClickInstruction(arg)

        elif opcode == Opcode.DOUBLE_CLICK:
            return DoubleClickInstruction(arg)

        elif opcode == Opcode.FIND:
            assert Path(arg[0]).exists(), f"File {arg[0]} does not exist!"
            return FindInstruction(arg)

        elif opcode == Opcode.JUMP:
            return JumpInstruction(arg)

        elif opcode == Opcode.PAUSE:
            return PauseInstruction(arg)

        elif opcode == Opcode.WAIT:
            return WaitInstruction(arg)

        else:
            raise NotImplementedError(
                f"Instruction {instruction} not implemented!")

    def parse_conditional(self, conditional: List[Tree]) -> Conditional:
        instruction = self.parse_instruction(conditional[0])
        cond = Conditional()
        cond.condition = instruction
        cond.body = self.parse_body(conditional[1])

        if len(conditional) > 2:
            cond.else_body = self.parse_body(conditional[2])

        return cond

    def parse_macro(self, tree: Tree) -> Macro:
        assert tree.data == 'macro', \
            f"Invalid tree passed: Expected 'macro' tree, got {tree.data}"

        # noinspection PyTypeChecker
        name = self.parse_token(tree.children[0])

        self._label_table.append(name)
        macro = Macro(name)
        macro.body = self.parse_body(tree.children[1])
        return macro

    def parse_body(self, tree: Tree) -> List[Executable]:
        assert tree.data == 'body', \
            f"Invalid tree passed: Expected 'body' tree, got {tree.data}"

        body: List[Executable] = []
        for child in tree.children:
            if child.data == 'instruction':
                instr = self.parse_instruction(child.children[0])
                body.append(instr)

            elif child.data == 'conditional':
                cond = self.parse_conditional(child.children)
                body.append(cond)

        return body

    def parse_tree(self, tree: Tree) -> List[Macro]:
        assert tree.data == 'start', \
            f"Invalid tree passed: Expected 'start' tree, got {tree.data}"

        for child in tree.children:
            macro = self.parse_macro(child)
            self._macro_list.append(macro)

        return self._macro_list
