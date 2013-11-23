# vim: softtabstop=4:expandtab


class Operand(object):
    @staticmethod
    def isA(arg):
        raise NotImplementedError()

    @staticmethod
    def encode(arg):
        raise NotImplementedError()

    @staticmethod
    def decode(arg):
        raise NotImplementedError()
