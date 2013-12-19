from operations import Operation, JumpOperation, TwoOpAluOperation


class PseudoOperation(Operation):
    opcodes = {"ret": JumpOperation.fromText("jmp $15", None).binary,
               "halt": JumpOperation.fromText("jmp #0", None).binary,
               "nop": TwoOpAluOperation.fromText("mov $0, $0", None).binary}
    argTypes = []

