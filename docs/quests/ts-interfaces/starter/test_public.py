import unittest
from main import solution

class TestPublic(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(solution(), 42)
