import re

class Structure(object):
    size = None

    #TODO: Bad name! -- Felix O.
    def __init__(self, arg):
        self.arg = arg

    def encodable(self):
        raise NotImplementedError()

    def encode(self):
        raise NotImplementedError()

    def decodable(self):
        return re.match("^[01]{%s}$" % self.size, self.arg)

    def decode(self):
        raise NotImplementedError()
