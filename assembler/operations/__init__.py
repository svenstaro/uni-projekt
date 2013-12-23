from .operation import Operation
from .aluOperation import AluOperation
from .memOperation import MemOperation
from .jumpOperation import JumpOperation
from .pseudoOperation import PseudoOperations
from .swiOperation import SwiOperation
from. stackOperation import StackOperation


def getOperations():
    return PseudoOperations() + [AluOperation, JumpOperation, MemOperation, SwiOperation, StackOperation]
