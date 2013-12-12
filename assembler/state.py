

class State(object):
    pass


class EncodingState(State):
    def __init__(self, labels, position):
        self.labels = labels
        self.position = position


class DecodingState(State):
    pass
