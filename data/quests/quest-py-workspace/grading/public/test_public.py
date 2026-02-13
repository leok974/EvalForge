import unittest
from helper import calculate

class TestWorkspace(unittest.TestCase):
    def test_calculate_returns_42(self):
        self.assertEqual(calculate(), 42)

if __name__ == '__main__':
    unittest.main()