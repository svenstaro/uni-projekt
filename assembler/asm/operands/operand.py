from ..structure import Structure


class Operand(Structure):
    start = None

    @classmethod
    def isValidText(cls, arg):
        return arg.startswith(cls.start)
