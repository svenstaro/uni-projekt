from .labelOperand import LabelOperand
from .immediate import Immediate16


class AluOperand2(LabelOperand):
    size = 17
    immType = Immediate16
