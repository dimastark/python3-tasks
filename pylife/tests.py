"""Unittest for arch of lines"""

import copy
import unittest

from pylife import lifearch as a


class TestsForGeneration(unittest.TestCase):
    """Testing new_genetation()"""
    def test_alive(self):
        """Test alive"""
        board = a.Life()
        board.add(1, 0)
        board.add(0, 0)
        board.add(1, 1)
        board.new_generation()
        self.assertEqual(board.get_cell(0, 1), (1, 1))

    def test_dead(self):
        """Test dead"""
        board = a.Life()
        board.add(0, 0)
        board.add(1, 1)
        board.new_generation()
        self.assertEqual(board.get_cell(0, 0)[0], 0)

    def test_living(self):
        """Test living"""
        board = a.Life()
        board.add(1, 0)
        board.add(0, 0)
        board.add(1, 1)
        board.new_generation()
        self.assertEqual(board.get_cell(1, 0)[0], 1)

    def test_negative(self):
        """Test living"""
        board = a.Life()
        board.add(-100, -100)
        self.assertEqual(board.get_cell(-100, -100)[0], 1)

    def test_titan(self):
        """Test living"""
        board = a.Life()
        board.add(0, 0)
        board.add(0, 1)
        board.add(1, 0)
        board.add(1, 1)
        start = copy.copy(board)
        board.new_generation()
        self.assertEqual(board, start)


class TestLivers(unittest.TestCase):
    """Test count_of_livers()"""
    def test_four(self):
        """Four livers"""
        board = a.Life()
        board.add(0, 1)
        board.add(1, 0)
        board.add(1, 2)
        board.add(2, 1)
        self.assertEqual(board.count_of_livers(1, 1), 4)

    def test_zero(self):
        """Zero livers"""
        board = a.Life()
        self.assertEqual(board.count_of_livers(1, 1), 0)


class TestForIter(unittest.TestCase):
    """Test __iter__"""
    def test_iterable(self):
        """Test iter of Life"""
        board = a.Life()
        self.assertTrue(iter(board))

    def test_list(self):
        """Test list"""
        board = a.Life()
        board.cells = [[(0, 0), (0, 0)], [(0, 0), (0, 0)]]
        for line in board.cells:
            for cell in line:
                self.assertEqual((0, 0), cell)


class TestForGetter(unittest.TestCase):
    """Test __iter__"""
    def test_exist(self):
        """Test iter of Life"""
        board = a.Life()
        board.add(0, 0)
        self.assertEqual(board.get_cell(0, 0), (1, 1))

    def test_not_exist(self):
        """Test list"""
        board = a.Life()
        self.assertEqual(board.get_cell(0, 0), (0, 0))


if __name__ == '__main__':
    unittest.main()
