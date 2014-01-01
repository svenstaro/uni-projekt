#!/usr/bin/env python2

import unittest, os

loader = unittest.TestLoader()
testsuite = loader.discover(os.path.dirname(__file__) + "/../")
unittest.TextTestRunner(verbosity=2).run(testsuite)
