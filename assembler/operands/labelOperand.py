from errors import EncodingError
from operands import Operand2
import re


class LabelOperand(Operand2):
    size = 25
    labelPattern = re.compile("^(?P<label>\.[a-zA-Z0-9_-]+)$")

    def encodable(self):
        return self.labelPattern.match(self.arg) or Operand2.encodable(self)

    def encode(self):
        try:
            if Operand2.encodable(self):
                return Operand2.encode(self)

            labelname = self.labelPattern.match(self.arg).group('label')
            labelpos = self.state.labels[labelname]
            diff = labelpos - self.state.position
            self.arg = "#"+str(diff)
            return Operand2.encode(self)
        except Exception, e:
            raise EncodingError(self.arg, "is not a valid label", e)