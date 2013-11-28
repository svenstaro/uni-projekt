class Structure(object):
    #TODO: Bad name! -- Felix O.
    def __init__(self, arg):
        self.arg = arg

    def encodable(self):
        raise NotImplementedError()

    def encode(self):
        raise NotImplementedError()

    def decodable(self):
        raise NotImplementedError()

    def decode(self):
        raise NotImplementedError()
