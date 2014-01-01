import unittest


from assembler.misc.testStructure import TestStructure
from assembler.operands import Register

class TestRegister(unittest.TestCase, TestStructure):
    def setUp(self):
        self.type = Register
        self.validMappings = {"$0": "0000", "$15": "1111"}
        self.notEncodable = ["$17", "2", "#4", "$OxF"]
        self.notDecodable = ["asdf", "12", "00", "11111"]

if __name__ == '__main__':
    unittest.main()
