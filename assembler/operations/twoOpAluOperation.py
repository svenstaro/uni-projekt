from .aluOperation import AluOperation
from operands import Register, IgnoreRegister, AluOperand2


class TwoOpAluOperation(AluOperation):
    opcodes = AluOperation.buildAluOpcodes({"not": "1011",
                                            "mov": "0000"})

    argTypes = [Register, IgnoreRegister, AluOperand2]