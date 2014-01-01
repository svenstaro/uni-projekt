from assembler.errors import EncodingError, DecodingError
from assembler.misc.state import DecodingState, EncodingState


#noinspection PyUnresolvedReferences
class TestStructure(object):
    def __init__(self):
        self.type = None
        self.validMappings = None
        self.notEncodable = None
        self.notDecodable = None

    def testValid(self):
        for (k, v) in self.validMappings.iteritems():
            self.assertEqual(self.type.fromText(k, EncodingState(0, {})).binary, v, "Encoding failed for: %s:" % k)
            self.assertEqual(k, self.type.fromBinary(v, DecodingState()).text, "Decoding failed for: %s:" % v)

    def testNotEncodable(self):
        for k in self.notEncodable:
            with self.assertRaises(EncodingError):
                self.type.fromText(k, EncodingState(0, {}))

    def testNotDecodable(self):
        for k in self.notDecodable:
            with self.assertRaises(DecodingError):
                self.type.fromBinary(k, DecodingState())
