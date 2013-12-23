from operands import Zero, Register, AluOperand2
from operations import Operation, JumpOperation, AluOperation


def PseudoOperations():
    class PseudoOperation(Operation):
        pass

    ops = [("ret",  JumpOperation.fromText("jmp $15", None).binary, []),

           ("halt", JumpOperation.fromText("jmp #0", None).binary, []),

           ("nop", AluOperation.fromText("add $0, $0, $0", None).binary, []),

           ("cmp", AluOperation.opcodes['subs'], [Zero(4), Register, AluOperand2]),
           ("tst", AluOperation.opcodes['ands'], [Zero(4), Register, AluOperand2]),

           ("not", AluOperation.opcodes['orn'], [Register, Zero(4), AluOperand2]),
           ("nots", AluOperation.opcodes['orns'], [Register, Zero(4), AluOperand2]),

           ("neg", AluOperation.opcodes['sub'], [Register, Zero(4), AluOperand2]),
           ("negs", AluOperation.opcodes['subs'], [Register, Zero(4), AluOperand2]),

           ("mov", AluOperation.opcodes['add'], [Register, Zero(4), AluOperand2]),
           ("movs", AluOperation.opcodes['adds'], [Register, Zero(4), AluOperand2])]

    result = []
    for op in ops:
        name, opcode, argTypes = op
        newType = type(name.capitalize() + "PseudoOperation", (PseudoOperation,),
                       dict(opcodes={name: opcode}, argTypes=argTypes))
        result.append(newType)
    return result
