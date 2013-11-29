#!/usr/bin/env python2.7

import os
import unittest

loader = unittest.TestLoader()
testsuite = loader.discover(os.path.dirname(__file__) + "/../simple32bit")
unittest.TextTestRunner(verbosity=2).run(testsuite)
