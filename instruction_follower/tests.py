import hrm.levels as levels
import unittest
from os.path import join as _join

def _read(file_name):
    with open(_join('test_programs', file_name), 'r') as f:
        return f.read()

class TestHRM(unittest.TestCase):
    def test_level1(self):
        level = levels.level1(_read('1'))
        self.assertEqual(level([1, 2, 3]), [1, 2, 3])
        self.assertEqual(level([1, 1, 1]), [1, 1, 1])
        self.assertEqual(level([2, 2, 2]), [2, 2, 2])
        self.assertEqual(level([3, 3, 3]), [3, 3, 3])
        self.assertEqual(level([]), [])

    def test_level2(self):
        level = levels.level2(_read('2'))
        self.assertEqual(level([1, 2, 3]), [1, 2, 3])
        self.assertEqual(level([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(level([1]), [1])
        self.assertEqual(level([]), [])

    def test_level3(self):
        level = levels.level3(_read('3'))
        self.assertEqual(level([]), ['B', 'U', 'G'])

    def test_level4(self):
        level = levels.level4(_read('4'))
        self.assertEqual(level([1, 2]), [2, 1])
        self.assertEqual(level(['A', 'B']), ['B', 'A'])
        self.assertEqual(level([]), [])

    def test_level6(self):
        level = levels.level6(_read('6'))
        self.assertEqual(level([1, 2]), [3])
        self.assertEqual(level([1, 2, 3, 4]), [3, 7])
        self.assertEqual(level([3, 7, -5, 15, 15, 15]), [10, 10, 30])
        self.assertEqual(level([]), [])

    def test_level7(self):
        level = levels.level7(_read('7'))
        self.assertEqual(level([0, 0]), [])
        self.assertEqual(level([1, 0, 2, 0]), [1, 2])
        self.assertEqual(level([0, 1, 0, 2]), [1, 2])
        self.assertEqual(level([]), [])

    def test_level8(self):
        level = levels.level8(_read('8'))
        self.assertEqual(level([0, 1]), [0, 3])
        self.assertEqual(level([3, -5]), [9, -15])
        self.assertEqual(level([6, 2]), [18, 6])
        self.assertEqual(level([]), [])

    def test_level9(self):
        level = levels.level9(_read('9'))
        self.assertEqual(level([1, 2]), [])
        self.assertEqual(level([1, 0, 2, 0]), [0, 0])
        self.assertEqual(level([0, 1, 0, -2]), [0, 0])
        self.assertEqual(level([]), [])

    def test_level10(self):
        level = levels.level10(_read('10'))
        self.assertEqual(level([0, 1]), [0, 8])
        self.assertEqual(level([-3, 5]), [-24, 40])
        self.assertEqual(level([6, 2]), [48, 16])
        self.assertEqual(level([]), [])

    def test_level11(self):
        level = levels.level11(_read('11'))
        self.assertEqual(level([1, 2]), [1, -1])
        self.assertEqual(level([1, 0, 2, 0]), [-1, 1, -2, 2])
        self.assertEqual(level([0, 1, 0, -2]), [1, -1, -2, 2])
        self.assertEqual(level([]), [])

    def test_level12(self):
        level = levels.level12(_read('12'))
        self.assertEqual(level([1, 2]), [40, 80])
        self.assertEqual(level([-1, 0, -2, 3]), [-40, 0, -80, 120])
        self.assertEqual(level([]), [])

    def test_level41(self):
        level = levels.level41(_read('41'))
        self.assertEqual(level([97, 21, 69, 0]), [21, 69, 97])
        self.assertEqual(level(['F', 'A', 'L', 'S', 'E', 0]), ['A', 'E', 'F', 'L', 'S'])
        self.assertEqual(level([59, 10, 37, 38, 27, 24, 85, 29, 85, 18, 0]), [10, 18, 24, 27, 29, 37, 38, 59, 85, 85])
        self.assertEqual(level([10, 0]), [10])

if __name__ == '__main__':
    unittest.main()
