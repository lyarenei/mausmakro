import random
import string
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from lark import Lark, Token, Tree

from lib.ebnf import ebnf
from lib.enums import ArgType, Opcode
from lib.types import Command, Conditional, Instruction
from lib.exceptions import ImageException, LabelException, \
    ParserException


class Parser:

    _images_to_check: List[str]
    _labels_to_check: List[str]
    _source_path: str
    _tree: Union[Tree, Tree]

    instructions: List[Instruction]
    label_table: Dict[str, int]
    macro_defined = False

    def __init__(self, path: str, source: str):

        self._images_to_check = []
        self._labels_to_check = []
        self._source_path = path

        lark = Lark(ebnf, parser='lalr')
        self._tree = lark.parse(source)

        self.instructions = []
        self.label_table = {}

    def parse(self) -> Tuple[List[Instruction], Dict[str, int]]:
        self._parse_tree(self._tree)
        self._get_label_mappings()
        return self.instructions, self.label_table

    def perform_checks(self):
        if not self.macro_defined:
            raise ParserException("At least one macro must be defined!")

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
        for img in self._images_to_check:
            img_path = Path(img)
            if not img_path.is_absolute():
                abs_path = Path(self._source_path).parent
                img_path = abs_path.joinpath(Path(f'images/{img}'))

            if not img_path.exists():
                raise ImageException(f"Image {img} not found! "
                                     "Please make sure to put the images "
                                     "inside implicit 'images' directory "
                                     "at the specified macro file "
                                     "location if not using absolute "
                                     "paths for the images.")

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
                                  f"Expected 'start', got '{tree.data}'")

        for child in tree.children:
            self._parse_macro(child)

    def _parse_macro(self, tree: Tree):
        if tree.data != 'macro' and tree.data != 'procedure':
            raise ParserException("Invalid tree passed: "
                                  "Expected 'macro' or 'procedure', "
                                  f"got '{tree.data}'")

        # noinspection PyTypeChecker
        name = self.parse_token(tree.children[0])
        self._add_label(name)
        self.instructions.append(Command(Opcode.LABEL, name))
        self._parse_body(tree.children[1])

        if tree.data == 'macro':
            self.macro_defined = True
            self.instructions.append(Command(Opcode.END))
            return

        self.instructions.append(Command(Opcode.RETURN))

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

        elif opcode == Opcode.CLICK \
                or opcode == Opcode.PCLICK:
            if isinstance(arg[0], str):
                self._images_to_check.append(arg[0])
                return Command(Opcode(opcode), arg)

            return Command(Opcode.CLICK, arg)

        elif opcode == Opcode.DOUBLE_CLICK:
            if isinstance(arg[0], str):
                self._images_to_check.append(arg[0])

            return Command(Opcode.DOUBLE_CLICK, arg)

        elif opcode == Opcode.FIND \
                or opcode == Opcode.PFIND:
            self._images_to_check.append(arg[0])
            return Command(Opcode(opcode), arg)

        elif opcode == Opcode.JUMP:
            self._labels_to_check.append(arg)
            return Command(Opcode.JUMP, arg)

        elif opcode == Opcode.LABEL:
            self._add_label(arg)
            return Command(Opcode.LABEL, arg)

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

    def _add_label(self, label: str):
        if label in self._labels_to_check:
            raise LabelException(f"Label {label} has been already defined!")

        self._labels_to_check.append(label)
