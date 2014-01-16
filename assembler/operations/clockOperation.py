from .operation import Operation
from ..operands import Zero, Opcodes, Register


class ClockOperation(Operation):

    opcodes = {"clk": "111101"}

    structure = [Opcodes(opcodes), Zero(22), Register]
