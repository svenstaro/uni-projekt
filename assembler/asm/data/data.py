from ..structure import Structure


class Data(Structure):
    start = None
    size = None

    @classmethod
    def isValidText(cls, arg):
        return arg.startswith(cls.start)

    @classmethod
    def getBinarysize(cls, arg):
        return cls.size
