#!/usr/bin/env python

# vim: softtabstop=4:expandtab

import myhdl

alu_ops = {
    "add": "00000",
    "adc": "00001",
    "sub": "00100",
    "sbc": "00101",
    "rsb": "00110",
    "rsc": "00111",

    "mul": "10000",
    "mull":"10001",
    "div": "10010",

    "and": "01000",
    "or" : "01001",
    "xor": "01010",
    "not": "01011",

    "lsl": "01100",
    "asr": "01101",
    "lsr": "01110",
    "rot": "01111"
}

def isRegister(arg):
    return arg.startswith("$")

def regEncode(arg):
    ex = ValueError(arg, "is not a valid register")

    if not arg.startswith("$"):
        raise ex

    try:
        result = int(arg[1:])
    except ValueError:
        raise ex

    if not 0 <= result <= 15:
        raise ex

    return format(result, "04b")

def isImmediate(arg, maxSize=16):
    return arg.startswith("#")

def immEncode(arg, maxSize=16):
    ex = ValueError(arg, "is not a valid %s-bit Immediate"%maxSize)
    if not arg.startswith("#"):
        raise ex
    number = arg[1:]

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
        result = int(sign+number, base=base)
    except ValueError:
        raise ex

    if not -2**(maxSize-1) <= result <= 2**(maxSize-1) -1:
        raise ex

    return myhdl.bin(result,width=maxSize)

def op2Encode(arg):
    try:
        if isRegister(arg):
            return "0" + regEncode(arg) + "0"*12
        if isImmediate(arg):
            return "0" + immEncode(arg)
        raise ValueError(arg, "unknown type")
    except ValueError, e:
        raise ValueError(arg, "is not a valid op2", e)

def buildAluOp(line):
    (command,arguments) = line.split(" ", 1)
    args = [arg.strip() for arg in arguments.split(",")]

    statusflag = "0"
    if command.endswith("s") and alu_ops.has_key(command[:-1]):
        statusflag = "1"
        command = command[:-1]
    if not alu_ops.has_key(command):
        raise ValueError
    return "0" + alu_ops[command] + statusflag + regEncode(args[0]) + regEncode(args[1]) + op2Encode(args[2])
