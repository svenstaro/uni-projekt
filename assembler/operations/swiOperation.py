from operations import Operation
from operands import Operand2


class SwiOperation(Operation):
    opcodes = {"swi": "1111100"}
    argTypes = [Operand2(25)]

