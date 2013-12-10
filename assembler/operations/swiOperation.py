from operations import Operation
from operands import Operand2


class SwiOperand2(Operand2):
    size = 25


class SwiOperation(Operation):
    opcodes = {"swi": "1111000"}
    argTypes = [SwiOperand2]

