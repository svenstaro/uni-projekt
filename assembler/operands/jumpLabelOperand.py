from errors import EncodingError
from .labelOperand import LabelOperand
import tools


class JumpLabelOperand(LabelOperand):
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