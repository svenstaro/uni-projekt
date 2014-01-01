from .operation import Operation
from .aluOperation import AluOperation, AluSOperation
from .memOperation import MemOperation
from .jumpOperation import JumpOperation
from .pseudoOperation import PseudoOperations
from .swiOperation import SwiOperation
from .stackOperation import PushOperation, PopOperation


def getOperations():
    return PseudoOperations() + [AluOperation, AluSOperation, JumpOperation, MemOperation, SwiOperation, PushOperation, PopOperation]
