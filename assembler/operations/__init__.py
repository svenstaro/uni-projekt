from .operation import Operation
from .aluOperation import AluOperation, AluSOperation
from .clockOperation import ClockOperation
from .memOperation import MemOperation
from .jumpOperation import JumpOperation
from .pseudoOperation import PseudoOperations
from .swiOperation import SwiOperation
from .stackOperation import PushOperation, PopOperation


def getOperations():
    return PseudoOperations() + [AluOperation, AluSOperation, ClockOperation, JumpOperation, MemOperation, SwiOperation, PushOperation, PopOperation]
