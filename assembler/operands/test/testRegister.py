import unittest

from operands import Register
from exceptions.encodingerror import EncodingError


class TestRegister(unittest.TestCase):
    validMappings = {"$0": "0000",
                     "$15": "1111"}

    notEncodable = ["$17", "2", "#4", "$OxF"]

    def testValid(self):
        for (k, v) in TestRegister.validMappings.iteritems():
            self.assertEqual(Register.encode(k), v, "Encoding failed for: %s:" % k)
            self.assertEqual(k, Register.decode(v), "Decoding failed for: %s:" % v)

    def testInvalid(self):
        for k in TestRegister.notEncodable:
            with self.assertRaises(EncodingError):
                Register.encode(k)


if __name__ == '__main__':
    unittest.main()
