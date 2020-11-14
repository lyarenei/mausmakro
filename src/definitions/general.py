from typing import Any, List, Optional

from definitions.enums import Opcode


class Executable:

    def execute(self):
        raise NotImplementedError


class Instruction(Executable):

    opcode: Opcode
    arg: Any

    def __init__(self, arg: Any):
        self.arg = arg

    def execute(self):
        raise NotImplementedError


class Conditional(Executable):

    condition: Instruction
    body: List[Instruction]
    else_body: Optional[List[Instruction]] = None

    def execute(self):
        raise NotImplementedError


class Macro:

    name: str
    body: List[Executable]

    def __init__(self, name: str):
        self.name = name
