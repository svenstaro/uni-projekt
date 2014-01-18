import re


class Structure(object):
    size = None
    text = None
    binary = None
    inner = None

    def __init__(self, text, binary, inner=None):
        self.text = text
        self.binary = binary
        self.inner = inner

    @classmethod
    def isValidText(cls, arg):
        raise NotImplementedError()

    @classmethod
    def fromText(cls, arg, state):
        raise NotImplementedError()

    @classmethod
    def isValidBinary(cls, arg):
        return re.match("^[01]{%s}$" % cls.size, arg)

    @classmethod
    def fromBinary(cls, arg, state):
        raise NotImplementedError()

    def __str__(self):
        return self.binary
