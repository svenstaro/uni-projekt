def tobin(value, width):
    if value < 0:
        return bin(value & ((1 << width) - 1))[2:].rjust(width, "1")
    return bin(value)[2:].zfill(width)[-width:]
