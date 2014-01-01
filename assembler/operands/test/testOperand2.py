# TODO
import unittest

from assembler.misc.testStructure import TestStructure
from assembler.operands import Operand2


class TestOperand2(TestStructure, unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        self.type = Operand2 # Register
        self.validMappings = {} # {"$0": "0000", "$15": "1111"}
        self.notEncodable = [] #["$17", "2", "#4", "$OxF"]
        self.notDecodable = [] #["asdf", "12", "00", "11111"]


if __name__ == '__main__':
    unittest.main()
