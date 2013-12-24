from operations import Operation
from operands import Operand2, Opcodes


class SwiOperation(Operation):
    opcodes = {"swi": "1111100"}
    structure = [Opcodes(opcodes), Operand2(25)]

