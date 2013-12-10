from operations import AluOperation
from operands import Register, IgnoreRegister, AluOperand2


class TwoOpAluOperation(AluOperation):
    opcodes = AluOperation.buildAluOpcodes({"not": "1011",
                                            "mov": "0000"})
    def __init__(self, arg, position):
        AluOperation.__init__(self, arg, position)
        self.argTypes[1] = IgnoreRegister
