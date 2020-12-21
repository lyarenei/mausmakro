from enum import Enum


class EqualEnum(Enum):

    def __eq__(self, other):
        return str(self) == str(other) \
               or str(self.value).lower() == str(other).lower()


class Opcode(EqualEnum):

    CALL = 'call'
    CLICK = 'click'
    DOUBLE_CLICK = 'double_click'
    END = 'end'
    EXIT = 'exit'
    FIND = 'find'
    GOTO = 'goto'
    IF = 'if'
    JUMP = 'jump'
    LABEL = 'label'
    PAUSE = 'pause'
    PCLICK = 'pclick'
    PFIND = 'pfind'
    RETURN = 'return'
    WAIT = 'wait'


class ArgType(EqualEnum):
    NAME = 'name'
    FILE = 'file'
    COORDS = 'coords'
    TIME = 'time'
