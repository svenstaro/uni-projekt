from .operation import Operation
from .aluOperation import AluOperation
from .twoOpAluOperation import TwoOpAluOperation
from .compareOperation import CompareOperation
from .memOperation import MemOperation
from .labelOperation import LabelOperation
from .jumpOperation import JumpOperation
from .retOperation import RetOperation
from .asciiData import AsciiData


def getOperations(labels):
    operations = [CompareOperation, TwoOpAluOperation, AluOperation, RetOperation, JumpOperation, MemOperation, AsciiData]
    operations = [LabelOperation.create(op, labels) if issubclass(op, LabelOperation) else op for op in operations]
    return operations