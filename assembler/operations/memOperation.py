from labelOperation import LabelOperation
from operands import Register, LabelOperand


class MemOperation(LabelOperation):
    def __init__(self, arg, position):
        LabelOperation.__init__(self, arg, position)
        self.argTypes = [Register, LabelOperand.createLabelOperand(self.labels, self.position)]


    opcodes = {"ld": "101",
               "str": "100"}