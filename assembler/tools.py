import re


def tobin(value, width):
    if value < 0:
        return bin(value & ((1 << width) - 1))[2:].rjust(width, "1")
    return bin(value)[2:].zfill(width)[-width:]

labelPattern = re.compile("^(?P<label>[a-zA-Z._][a-zA-Z0-9._-]*)$")


def label2immediate(arg, state):
    labelname = labelPattern.match(arg).group('label')
    labelpos = state.labels[labelname]
    diff = labelpos - state.position - 4
    return diff


def immediate2binary(number, size):
    sign = ""
    if number.startswith("-"):
        sign = "-"
        number = number[1:]
    base = 10
    if number.startswith("0b"):
        base = 2
    elif number.startswith("0x"):
        base = 16
    elif number.startswith("0"):
        base = 8
    try:
        result = int(sign + number, base=base)
    except ValueError:
        return False
    if not -2 ** (size - 1) <= result <= 2 ** (size - 1) - 1:
        return False
    return tobin(result, width=size)