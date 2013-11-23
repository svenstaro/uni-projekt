class Structure(object):
    @staticmethod
    def encodable(line):
        raise NotImplementedError()

    @staticmethod
    def encode(line):
        raise NotImplementedError()

    @staticmethod
    def decodable(arg):
        raise NotImplementedError()

    @staticmethod
    def decode(line):
        raise NotImplementedError()
