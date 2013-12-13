from errors import EncodingError
from .operand2 import Operand2
from .immediate import Immediate24
import tools


class LabelOperand(Operand2):
    size = 25
    immType = Immediate24

    @classmethod
    def isValidText(cls, arg):
        return tools.labelPattern.match(arg) or Operand2.isValidText(arg)

    @classmethod
    def fromText(cls, arg, state):
        try:
            if Operand2.isValidText(arg):
                return super(LabelOperand, cls).fromText(arg, state)
            else:
                imm = "#" + str(tools.label2immediate(arg, state))
                inner = super(LabelOperand, cls).fromText(imm, state)
                return cls(arg, inner.binary, inner)
        except Exception, e:
            raise EncodingError(arg, "is not a valid label", e)