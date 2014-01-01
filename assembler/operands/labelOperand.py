from ..misc import tools
from ..errors import EncodingError
from .operand2 import Operand2


class LabelOperand(Operand2(25)):

    @classmethod
    def isValidText(cls, arg):
        return tools.labelPattern.match(arg) or super(LabelOperand, cls).isValidText(arg)

    @classmethod
    def fromText(cls, arg, state):
        try:
            if super(LabelOperand, cls).isValidText(arg):
                return super(LabelOperand, cls).fromText(arg, state)
            else:
                imm = "#" + str(tools.label2immediate(arg, state) - 4)
                inner = super(LabelOperand, cls).fromText(imm, state)
                return cls(arg, inner.binary, inner)
        except Exception, e:
            raise EncodingError(arg, "is not a valid label", e)
