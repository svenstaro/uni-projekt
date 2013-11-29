from operations import JumpOperation


class RetOperation(JumpOperation):
    opcodes = {"ret": JumpOperation("jmp $15").encode()}
    argTypes = []
