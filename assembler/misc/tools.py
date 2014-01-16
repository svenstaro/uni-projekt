import re
import ast
from ..errors import EncodingError


def tobin(value, width):
    if value < 0:
        msb = "1"
        value += 1 << width
    else:
        msb = "0"
    return bin(value)[2:].rjust(width, msb)[-width:]

labelPattern = re.compile("^(?P<label>[a-zA-Z._][a-zA-Z0-9._-]*)$")


def label2immediate(arg, state):
    try:
        labelname = labelPattern.match(arg).group('label')
    except:
        raise EncodingError(arg, "Not a valid label string")
    try:
        labelpos = state.labels[labelname]
    except:
        raise EncodingError(arg, "Unknown label")
    diff = labelpos - state.position
    return diff


def immediate2binary(number, size):
    try:
        result = ast.literal_eval(number)
    except SyntaxError:
        raise EncodingError(number, "Not a number")
    if not isinstance(result, (int,long)):
        raise EncodingError(number, "Not a number") 
    if result < -2 ** (size - 1):
        raise EncodingError(number, "Number too small")
    if 2 ** (size - 1) - 1 < result:
        raise EncodingError(number, "Number too big")
    return tobin(result, width=size)
