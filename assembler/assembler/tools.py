import re
import ast


def tobin(value, width):
    if value < 0:
        msb = "1"
        value += 1 << width
    return bin(value)[2:].rjust(width, "1")[-width:]

labelPattern = re.compile("^(?P<label>[a-zA-Z._][a-zA-Z0-9._-]*)$")


def label2immediate(arg, state):
    labelname = labelPattern.match(arg).group('label')
    labelpos = state.labels[labelname]
    diff = labelpos - state.position
    return diff


def immediate2binary(number, size):
    try:
        result = ast.literal_eval(number)
    except SyntaxError:
        return False
    if not -2 ** (size - 1) <= result <= 2 ** (size - 1) - 1:
        return False
    return tobin(result, width=size)
