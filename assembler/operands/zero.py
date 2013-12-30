from .ignore import Ignore


def Zero(size):
    class Zero(Ignore):
        @classmethod
        def fromText(cls, arg, state):
            return cls(arg, "0"*cls.size)

        @classmethod
        def isValidBinary(cls, arg):
            return arg == "0"*cls.size

    return type("Zero"+str(size), (Zero,), dict(size=size))