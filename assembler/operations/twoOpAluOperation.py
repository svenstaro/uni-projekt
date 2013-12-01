from operations import AluOperation
from operands import Register, IgnoreRegister, AluOperand2


class TwoOpAluOperation(AluOperation):
    opcodes = AluOperation.buildAluOpcodes({"not": "01011",
                                            "mov": "00000"})
    argTypes = [Register, IgnoreRegister, AluOperand2]