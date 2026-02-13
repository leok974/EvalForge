import unittest
from main import secret_value

class TestPublic(unittest.TestCase):
    def test_positive(self):
        # Public: just needs to be positive
        val = secret_value()
        self.assertGreater(val, 0)

if __name__ == '__main__':
    unittest.main()