class CodingError(Exception):
    def __init__(self, val, errString="", inner=None):
        self.val = val
        self.inner = inner
        self.errString = errString
        Exception.__init__(self, str(self))

    def __str__(self):
        errstring = self.__class__.__name__ +  ": %s %s" % (self.val, self.errString)
        if self.inner is not None:
            errstring += "(was: %s)" % str(self.inner)
        return errstring
