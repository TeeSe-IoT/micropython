import unittest
# import your modules
import lib.machine
#
class test_case(unittest.TestCase):
    def test_function(self):
        assert lib.machine.Pin(1)
#
if __name__ == '__main__':
    unittest.main()
