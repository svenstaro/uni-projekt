from operations import AluOperation
from operands import Register, IgnoreRegister, AluOperand2


class CompareOperation(AluOperation):
    opcodes = {'cmp': AluOperation.opcodes['subs'],
               'tst': AluOperation.opcodes['ands']}
    argTypes = [IgnoreRegister, Register, AluOperand2]