from operations import LabelOperation
from operands import LabelOperand


class JumpOperation(LabelOperation):
    def __init__(self, arg, position):
        LabelOperation.__init__(self, arg, position)
        self.argTypes = [LabelOperand.createLabelOperand(self.labels, self.position)]

    opcodes = {"jmp": "1110000",
               "call": "1110001"}

    conditions = {
        # equal or zero
        "eq": "0000",
        "z": "0000",
        "ne": "0001",
        "nz": "0001",
        # lower than
        "lt": "0100",
        "le": "0101",
        # greater than
        "gt": "0110",
        "ge": "0111",
        # overflow
        "o": "1000",
        "no": "1001",
        # carry
        "c": "1010",
        "nc": "1011"}

    for (name, code) in conditions.items():
        opcodes["j" + name] = "110" + code
