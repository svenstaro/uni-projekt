from .ignore import Ignore


def Const(value):
    class Const(Ignore):
        @classmethod
        def fromText(cls, arg, state):
            return cls(arg, cls.value)

        @classmethod
        def isValidBinary(cls, arg):
            return arg == cls.value


    return type("Const"+value, (Const,), dict(size=len(value), value=value))
