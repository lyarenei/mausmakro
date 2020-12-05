import random
import string
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from lark import Lark, Token, Tree

from definitions.ebnf import ebnf
from definitions.enums import ArgType, Opcode
from definitions.general import Command, Conditional, Instruction
from definitions.exceptions import ImageException, LabelException, \
    ParserException


class Parser:

    _images_to_check: List[str]
    _labels_to_check: List[str]
    _source_path: str
    _tree: Union[Tree, Tree]

    instructions: List[Instruction]
    label_table: Dict[str, int]

    def __init__(self, file: str):
        self._source_path = file

        lark = Lark(ebnf, parser='lalr')
        with open(file, 'r') as f:
            source = f.read()

        self._images_to_check = []
        self._labels_to_check = []
        self._tree = lark.parse(source)

        self.instructions = []
        self.label_table = {}

    def parse(self) -> Tuple[List[Instruction], Dict[str, int]]:
        self._parse_tree(self._tree)
        self._get_label_mappings()
        return self.instructions, self.label_table

    def perform_checks(self):
        self.check_labels()
        self.check_images()

    def check_labels(self):
        while self._labels_to_check:
            label = self._labels_to_check[0]
            if self._find_label(label):
                self._labels_to_check.remove(label)
            else:
                raise LabelException(f"Label {label} is not defined!")

    def check_images(self):
        abs_path = Path(self._source_path).parent
        for img in self._images_to_check:
            img_path = Path(img)
            if not img_path.is_absolute():
                img_path = abs_path.joinpath(img_path)
                if not img_path.exists():
                    raise ImageException(f"Image {img} not found!")

    def _find_label(self, label: str) -> bool:
        for instr in self.instructions:
            if instr.opcode == Opcode.LABEL:
                instr: Command
                if instr.arg == label:
                    return True

        return False

    def _get_label_mappings(self):
        for i, ins in enumerate(self.instructions):
            if ins.opcode == Opcode.LABEL:
                ins: Command
                self.label_table[ins.arg] = i

    def _parse_tree(self, tree: Tree):
        if tree.data != 'start':
            raise ParserException("Invalid tree passed: "
                                  f"Expected 'start' tree, got '{tree.data}'")

        for child in tree.children:
            self._parse_macro(child)

    def _parse_macro(self, tree: Tree):
        if tree.data != 'macro':
            raise ParserException("Invalid tree passed: "
                                  f"Expected 'macro' tree, got '{tree.data}'")

        # noinspection PyTypeChecker
        name = self.parse_token(tree.children[0])
        self.instructions.append(Command(Opcode.LABEL, name))
        self._parse_body(tree.children[1])
        self.instructions.append(Command(Opcode.END))

    def _parse_body(self, tree: Tree):
        if tree.data != 'body':
            raise ParserException("Invalid tree passed: "
                                  f"Expected 'body' tree, got '{tree.data}'")

        for child in tree.children:
            if child.data == 'instruction':
                cmd = self._parse_command(child.children[0])
                self.instructions.append(cmd)

            else:
                cond = self.parse_conditional(child.children)
                cond.negate = child.data == 'neg_conditional'

    def _parse_command(self, instruction: Tree) -> Command:
        opcode = instruction.data
        arg = tuple(map(self.parse_token, instruction.children))
        arg = arg[0] if len(arg) == 1 else arg

        if opcode == Opcode.CALL:
            self._labels_to_check.append(arg)
            return Command(Opcode.CALL, arg)

        elif opcode == Opcode.CLICK:
            return Command(Opcode.CLICK, arg)

        elif opcode == Opcode.DOUBLE_CLICK:
            return Command(Opcode.DOUBLE_CLICK, arg)

        elif opcode == Opcode.FIND:
            self._images_to_check.append(arg[0])
            return Command(Opcode.FIND, arg)

        elif opcode == Opcode.JUMP:
            self._labels_to_check.append(arg)
            return Command(Opcode.JUMP, arg)

        elif opcode == Opcode.PAUSE:
            return Command(Opcode.PAUSE)

        elif opcode == Opcode.RETURN:
            return Command(Opcode.RETURN)

        elif opcode == Opcode.WAIT:
            return Command(Opcode.WAIT, arg)

        else:
            raise NotImplementedError(f"Instruction {instruction} "
                                      "is not implemented!")

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
            raise NotImplementedError(f" Parsing for token {token.type} "
                                      "is not implemented!")

    def parse_conditional(self, conditional: List[Tree]) -> Conditional:
        cond = Conditional(Opcode.IF)
        cond.condition = self._parse_command(conditional[0])
        cond.end_label = self._generate_label()
        self.instructions.append(cond)

        self._parse_body(conditional[1])

        if len(conditional) > 2:
            self.instructions.append(Command(Opcode.JUMP, cond.end_label))
            cond.else_label = self._generate_label()
            self.instructions.append(Command(Opcode.LABEL, cond.else_label))
            self._parse_body(conditional[2])
        else:
            cond.else_label = None

        self.instructions.append(Command(Opcode.LABEL, cond.end_label))
        return cond

    @staticmethod
    def _generate_label() -> str:
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(8))
