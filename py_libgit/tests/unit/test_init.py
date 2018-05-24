import unittest
from py_libgit.core.init import Init

class TestInit(unittest.TestCase):
    def setUp(self):
        self.init = Init()

    def test_pass(self):

        self.assertEqual(1, 1)
