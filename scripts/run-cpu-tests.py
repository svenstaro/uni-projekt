#!/usr/bin/env python2

import unittest

loader = unittest.TestLoader()
testsuite = loader.discover("hardware")
unittest.TextTestRunner(verbosity=2).run(testsuite)
