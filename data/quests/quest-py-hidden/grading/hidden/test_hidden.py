import unittest
from main import secret_value

class TestHidden(unittest.TestCase):
    def test_exact_value(self):
        # Hidden: must be exactly 100
        val = secret_value()
        self.assertEqual(val, 100, "Hidden test failed: Value must be 100")

if __name__ == '__main__':
    unittest.main()