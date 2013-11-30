from operations import Operation, JumpOperation


class RetOperation(Operation):
    opcodes = {"ret": JumpOperation("jmp $15", -1).encode()}
    argTypes = []
