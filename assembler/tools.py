import re


def tobin(value, width):
    if value < 0:
        return bin(value & ((1 << width) - 1))[2:].rjust(width, "1")
    return bin(value)[2:].zfill(width)[-width:]

labelPattern = re.compile("^(?P<label>[a-zA-Z._-][a-zA-Z0-9._-]*)$")


def label2immediate(arg, state):
    labelname = labelPattern.match(arg).group('label')
    labelpos = state.labels[labelname]
    diff = labelpos - state.position
    return diff
