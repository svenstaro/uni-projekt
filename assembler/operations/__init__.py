from .operation import Operation
from .aluOperation import AluOperation, AluSOperation
from .clockOperation import ClockOperation
from .memOperation import MemOperation
from .jumpOperation import JumpOperation
from .pseudoOperation import PseudoOperations
from .stackOperation import PushOperation, PopOperation
from .hwiOperation import LedOperation, ButOperation
from .rs232Operation import Rs232rx, Rs232tx


def getOperations():
    return PseudoOperations() + \
           [AluOperation, AluSOperation, ClockOperation, JumpOperation,
            MemOperation, PushOperation, PopOperation,
            LedOperation, ButOperation, Rs232rx, Rs232tx]
