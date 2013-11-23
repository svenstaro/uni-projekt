import unittest

from operands import Register
from errors import EncodingError, DecodingError


class TestRegister(unittest.TestCase):
    validMappings = {"$0": "0000",
                     "$15": "1111"}

    notEncodable = ["$17", "2", "#4", "$OxF"]

    notDecodable = ["asdf", "12", "00", "11111"]

    def testValid(self):
        for (k, v) in TestRegister.validMappings.iteritems():
            self.assertEqual(Register.encode(k), v, "Encoding failed for: %s:" % k)
            self.assertEqual(k, Register.decode(v), "Decoding failed for: %s:" % v)

    def testNotEncodable(self):
        for k in TestRegister.notEncodable:
            with self.assertRaises(EncodingError):
                Register.encode(k)

    def testNotDecodable(self):
        for k in TestRegister.notDecodable:
            with self.assertRaises(DecodingError):
                Register.decode(k)


if __name__ == '__main__':
    unittest.main()
