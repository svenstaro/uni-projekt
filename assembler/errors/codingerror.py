class CodingError(Exception):
    def __init__(self, val, errString="", inner=None):
        self.val = val
        self.inner = inner
        self.errString = errString

    def __str__(self):
        errstring = "%s:\n%s" % (self.errString, self.val)
        if self.inner is not None:
            errstring += "\n\t" + str(self.inner).replace("\n", "\n\t") 
        return errstring
