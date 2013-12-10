from operations import AluOperation
from operands import Register, IgnoreRegister, AluOperand2


class CompareOperation(AluOperation):
    opcodes = {'cmp': AluOperation.opcodes['subs'],
               'tst': AluOperation.opcodes['ands']}

    def __init__(self, arg, position):
        AluOperation.__init__(self, arg, position)
        self.argTypes[0] = IgnoreRegister