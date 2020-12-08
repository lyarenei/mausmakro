class MausMakroException(Exception):

    msg: str

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class ConditionException(MausMakroException):
    pass


class ImageException(MausMakroException):
    pass


class InterpretException(MausMakroException):
    pass


class LabelException(MausMakroException):
    pass


class ParserException(MausMakroException):
    pass
