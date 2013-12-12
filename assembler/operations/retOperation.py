from operations import Operation, JumpOperation


class RetOperation(Operation):
    opcodes = {"ret": JumpOperation("jmp $15", None).encode()}
    argTypes = []

