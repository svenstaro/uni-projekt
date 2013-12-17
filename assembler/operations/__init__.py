from .operation import Operation
from .aluOperation import AluOperation
from .twoOpAluOperation import TwoOpAluOperation
from .compareOperation import CompareOperation
from .memOperation import MemOperation
from .jumpOperation import JumpOperation
from .pseudoOperation import PseudoOperation
from .swiOperation import SwiOperation


def getOperations():
    return [CompareOperation, TwoOpAluOperation, AluOperation, PseudoOperation, JumpOperation, MemOperation,
                  SwiOperation]