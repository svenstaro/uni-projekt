from errors import EncodingError
from operands import Operand2
import re


class LabelOperand(Operand2):
    size = 25
    labelPattern = re.compile("^(?P<label>\.[a-zA-Z0-9_-]+)$")
    labels = None
    position = None

    def encodable(self):
        return self.labelPattern.match(self.arg) or Operand2.encodable(self)

    def encode(self):
        try:
            if Operand2.encodable(self):
                return Operand2.encode(self)

            labelname = self.labelPattern.match(self.arg).group('label')
            labelpos = self.labels[labelname]
            diff  = labelpos - self.position
            self.arg = "#"+str(diff)
            return Operand2.encode(self)
        except Exception, e:
            raise EncodingError(self.arg, "is not a valid label", e)

    @staticmethod
    def createLabelOperand(labels, position):
        class RealLabelOperand(LabelOperand):
            def __init__(self, arg):
                LabelOperand.__init__(self, arg)
                self.labels = labels
                self.position = position
        return RealLabelOperand