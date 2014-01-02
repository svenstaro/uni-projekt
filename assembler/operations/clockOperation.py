from .operation import Operation
from ..operands import Zero, Opcodes, Register

class ClockOperation(Operation):

    opcodes = {"clk": "1111110"}

    structure = [Opcodes(opcodes), Zero(21), Register]
