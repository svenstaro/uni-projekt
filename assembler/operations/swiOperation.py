from operations import Operation
from operands import Operand2
from operands.immediate import Immediate24


class SwiOperand2(Operand2):
    size = 25
    immType = Immediate24


class SwiOperation(Operation):
    opcodes = {"swi": "1111100"}
    argTypes = [SwiOperand2]

