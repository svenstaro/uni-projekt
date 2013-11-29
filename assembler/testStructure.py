from errors import EncodingError, DecodingError


class TestStructure(object):
    def __init__(self):
        self.type = None
        self.validMappings = None
        self.notEncodable = None
        self.notDecodable = None

    def testValid(self):
        for (k, v) in self.validMappings.iteritems():
            self.assertEqual(self.type(k).encode(), v, "Encoding failed for: %s:" % k)
            self.assertEqual(k, self.type(v).decode(), "Decoding failed for: %s:" % v)

    def testNotEncodable(self):
        for k in self.notEncodable:
            with self.assertRaises(EncodingError):
                self.type(k).encode()

    def testNotDecodable(self):
        for k in self.notDecodable:
            with self.assertRaises(DecodingError):
                self.type(k).decode()
