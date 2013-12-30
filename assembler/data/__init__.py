from .asciiData import AsciiData
from .asciizData import AsciizData
from .binaryData import ByteData, WordData


def getData():
    return [AsciiData, AsciizData, ByteData, WordData]