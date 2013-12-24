from .ignore import Ignore


class OpcodesBaseClass(Ignore):
    @classmethod
    def fromText(cls, arg, state):
        return cls(arg, cls.mapping[arg])

    @classmethod
    def isValidBinary(cls, arg):
        return arg in cls.mapping.values()

    @classmethod
    def fromBinary(cls, arg, state):
        return (key for (key,value) in cls.mapping.items() if value == arg).next()

def Opcodes(mapping):
    return type("Opcodes", (OpcodesBaseClass,), dict(size=len(mapping.values()[0]), mapping=mapping))
