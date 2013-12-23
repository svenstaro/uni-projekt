from .ignore import Ignore


class OpcodesBaseClass(Ignore):
    @classmethod
    def fromText(cls, arg, state):
        return cls(arg, cls.mapping[arg])

    @classmethod
    def isValidBinary(cls, arg):
        return arg in cls.mapping.values()

def Opcodes(mapping):
    return type("Opcodes", (OpcodesBaseClass,), dict(size=len(mapping.values()[0]), mapping=mapping))
