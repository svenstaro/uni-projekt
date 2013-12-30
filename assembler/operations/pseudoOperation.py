from operands import Zero, Register, AluOperand2, Opcodes, Const
from operations import Operation, JumpOperation, AluOperation, AluSOperation
import re


def PseudoOperations():
    class PseudoOperation(Operation):
        underlyingType = None
        pseudo = ""
        real = ""

        @classmethod
        def translate(cls, s, src, dest):
            src = src.replace("$", "\\$")

            srcPattern = "^" + re.sub(r'%(\d)', r'(?P<a\1>.*)', src) + "$"
            destPattern = re.sub(r'%(\d)', r'\\g<a\1>', dest)
            return re.sub(srcPattern, destPattern, s)

        @classmethod
        def fromReal(cls, arg):
            try:
                return cls.translate(arg, cls.pseudo, cls.real)
            except:
                return None


        @classmethod
        def isValidText(cls, arg):
            realarg = cls.fromReal(arg)
            if realarg:
                return cls.underlyingType.isValidText(realarg)
            return False

        @classmethod
        def fromText(cls, line, state):
            realarg = cls.fromReal(line)
            inner = cls.underlyingType.fromText(realarg, state)
            return cls(line, inner.binary, inner)

        @classmethod
        def isValidBinary(cls, arg):
            if not cls.underlyingType.isValidBinary(arg):
                return False
            inner = cls.underlyingType.fromBinary(arg, None)
            text = cls.translate(inner.text, cls.real, cls.pseudo)
            return inner.text != text


        @classmethod
        def fromBinary(cls, arg, state):
            inner = cls.underlyingType.fromBinary(arg, state)
            text = cls.translate(inner.text, cls.real, cls.pseudo)
            return cls(text, inner.binary, inner)


    ops = [("ret", "jmp $15", JumpOperation),

           ("halt", "jmp #-4", JumpOperation),

           ("nop", "add $0, $0, $0", AluOperation),

           ("cmp %0, %1", "subs $0, %0, %1", AluSOperation),
           ("tst %0, %1", "ands $0, %0, %1", AluSOperation),

           ("not %0, %1", "orn %0, $0, %1", AluOperation),
           ("nots %0, %1", "orns %0, $0, %1", AluSOperation),

           ("neg %0, %1", "sub %0, $0, %1", AluOperation),
           ("neg %0, %1", "subs %0, $0, %1", AluSOperation),

           ("mov %0, %1", "add %0, $0, %1", AluOperation),
           ("movs %0, %1", "adds %0, $0, %1", AluSOperation)]

    result = []
    for op in ops:
        pseudo, real, underlyingType = op
        newType = type("PseudoOperation", (PseudoOperation,),
                       dict(pseudo=pseudo, real=real, underlyingType=underlyingType))
        result.append(newType)
    return result
