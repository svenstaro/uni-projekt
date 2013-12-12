from .operation import Operation
from .aluOperation import AluOperation
from .twoOpAluOperation import TwoOpAluOperation
from .compareOperation import CompareOperation
from .memOperation import MemOperation
from .jumpOperation import JumpOperation
from .retOperation import RetOperation
from .swiOperation import SwiOperation
from .asciiData import AsciiData


def getOperations():
    return [CompareOperation, TwoOpAluOperation, AluOperation, RetOperation, JumpOperation, MemOperation,
                  SwiOperation, AsciiData]