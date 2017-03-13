"""Unittest for arch of lines"""


import unittest
import arch as a
import random as r


class TestsForNeightbor(unittest.TestCase):
    """Testing count_of_neightbor()"""
    def test_first_diag(self):
        """First diag without neightbor"""
        matr = [[0, 1], [1, 1]]
        self.assertEqual(a.count_of_neightbor(matr, (0, 0), 1, 1), 0)

    def test_sec_diag(self):
        """Second diag without neightbor"""
        matr = [[0, 1], [1, 1]]
        self.assertEqual(a.count_of_neightbor(matr, (0, 0), 1, -1), 0)

    def test_horiz(self):
        """Horizontal without neightbor"""
        matr = [[0, 1], [1, 1]]
        self.assertEqual(a.count_of_neightbor(matr, (0, 0), 1, 0), 0)

    def test_verti(self):
        """Vertical without neightbors"""
        matr = [[0, 1], [1, 1]]
        self.assertEqual(a.count_of_neightbor(matr, (0, 0), 0, 1), 0)

    def test_first_diag1(self):
        """First diag of neightbor"""
        matr = [[0, 0], [0, 0]]
        self.assertEqual(a.count_of_neightbor(matr, (0, 0), 1, 1), 1)

    def test_sec_diag1(self):
        """Second diag of neightbor"""
        matr = [[0, 0], [0, 0]]
        self.assertEqual(a.count_of_neightbor(matr, (1, 0), 1, -1), 0)

    def test_horiz1(self):
        """Horizontal of neightbor"""
        matr = [[0, 0], [0, 0]]
        self.assertEqual(a.count_of_neightbor(matr, (0, 0), 1, 0), 1)

    def test_verti1(self):
        """Vertical of neightbor"""
        matr = [[0, 0], [0, 0]]
        self.assertEqual(a.count_of_neightbor(matr, (0, 0), 0, 1), 1)

    def test_stupid(self):
        """Vertical of neightbor"""
        matr = [[0, 0], [0, 0]]
        self.assertEqual(a.count_of_neightbor(matr, (0, 0), 0, 0), 0)

class TestForObstacles(unittest.TestCase):
    """Testing find_way()"""
    def test_no_obst(self):
        """Easy way"""
        matr1 = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
        self.assertTrue(a.find_way((1, 1), (4, 4), a.make_border(matr1)))

    def test_hard_labirinth(self):
        """Hard way"""
        matr2 = [[0, 0, 1, 0, 0],
                 [1, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 1, 1, 0, 0],
                 [0, 0, 0, 0, 0]]
        self.assertTrue(a.find_way((1, 1), (1, 4), a.make_border(matr2)))

    def test_obstacles(self):
        """No way"""
        matr3 = [[0, 0, 1, 0],
                 [0, 0, 1, 0],
                 [1, 1, 1, 0],
                 [0, 0, 0, 0]]
        self.assertFalse(a.find_way((0, 0), (3, 3), a.make_border(matr3)))

    def test_lazytest(self):
        """No moving"""
        matr1 = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
        self.assertFalse(a.find_way((0, 0), (0, 0), a.make_border(matr1)))

    def test_obst(self):
        """Diagonally move"""
        matr1 = [[0, 1, 0, 0],
                 [1, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
        self.assertFalse(a.find_way((1, 1), (4, 4), a.make_border(matr1)))


class TestForBorder(unittest.TestCase):
    """Test make_border()"""
    def test_correct_work(self):
        """Simple test of correct work"""
        matr = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        test_matr = a.make_border(matr)
        self.assertTrue(test_matr[0][0] != 0)
        self.assertTrue(test_matr[-1][-1] != 0)
        self.assertTrue(test_matr[-1][0] != 0)
        self.assertTrue(test_matr[0][-1] != 0)

    def test_not_square(self):
        """Test on rectangle"""
        matr = [[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]
        test_matr = a.make_border(matr)
        self.assertTrue(test_matr[0][0] != 0)
        self.assertTrue(test_matr[-1][-1] != 0)
        self.assertTrue(test_matr[-1][0] != 0)
        self.assertTrue(test_matr[0][-1] != 0)


class TestForIndErr(unittest.TestCase):
    """Testing no_inderr()"""
    def test_with_ind_err(self):
        """Index Error in sequence"""
        self.assertFalse(a.no_inderr(2, 3, 4))

    def test_without_ind_err(self):
        """No Index Error in sequence"""
        self.assertTrue(a.no_inderr(2, 1))

    def test_zero_equal(self):
        """Equal zero"""
        self.assertTrue(a.no_inderr(2, 0))


class TestForStr(unittest.TestCase):
    """Test str(GameBoard)"""
    def test_correct_work(self):
        """Simple test of correct work"""
        game_board = a.GameBoard(8, 2, 2)
        str_field = str(game_board)
        leng = len(str_field)
        self.assertTrue(str_field[r.randint(0, leng-1)])

    def test_full_field(self):
        """Testing on full field"""
        game_board = a.GameBoard(8, 2, 2)
        game_board.add_circles(64)
        game_board.stand_circles()
        str_field = str(game_board)
        self.assertTrue(str_field.count("0") == 0)


class TestForAdd(unittest.TestCase):
    """Test add_circles() and add_circles()"""
    def test_zero_circles(self):
        """Zero circles added on board"""
        game_board = a.GameBoard(8, 2, 3)
        start_count = str(game_board).count('0')
        game_board.add_circles(0)
        game_board.stand_circles()
        self.assertTrue(start_count == str(game_board).count('0'))

    def test_minus_circles(self):
        """Minus circles added on board"""
        game_board = a.GameBoard(8, 2, 3)
        start_count = str(game_board).count('0')
        game_board.add_circles(-1)
        game_board.stand_circles()
        self.assertTrue(start_count == str(game_board).count('0'))

    def test_many_circles(self):
        """Many circles added on board"""
        game_board = a.GameBoard(8, 2, 3)
        game_board.add_circles(66)
        game_board.stand_circles()
        self.assertTrue(0 == str(game_board).count('0'))


class TestForRemove(unittest.TestCase):
    """Test fill()"""
    def test_fill(self):
        """Regular test"""
        matr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        a.fill((1, 1), matr, -1)
        self.assertTrue(-1 == matr[0][1] == matr[1][0] == matr[2][1] == matr[1][2])

    def test_corner(self):
        """Corner test"""
        matr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        a.fill((0, 0), matr, -1)
        self.assertTrue(-1 == matr[1][0] == matr[0][1])

    def test_without_fill(self):
        """Without filling test"""
        matr = [[0, -2, 0], [-2, 0, -2], [0, -2, 0]]
        a.fill((1, 1), matr, -1)
        self.assertFalse(-1 == matr[0][1] == matr[1][0] == matr[2][1] == matr[1][2])


class TestForFilled(unittest.TestCase):
    """Test filled()"""
    def test_filled(self):
        """Regular test"""
        matr = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
        a.filled(matr, (0, 0), -1)
        self.assertTrue(-1 == matr[1][1])

    def test_without_filled(self):
        """Without 'filled' test"""
        matr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        a.filled(matr, (1, 1), -1)
        self.assertFalse(-1 == matr[0][1] == matr[1][0] == matr[2][1] == matr[1][2])


class TestForFind(unittest.TestCase):
    """Test find()"""
    def test_find(self):
        """Regular test"""
        matr = [[0, -1, 0], [0, 0, 0], [0, 0, 0]]
        tup = a.find(matr, (1, 1), -1)
        self.assertTrue(tup == (1, 0))

    def test_exception(self):
        """Exception test"""
        matr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertRaises(a.find(matr, (0, 0), -1))

    def test_not_find(self):
        """Not find test"""
        matr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        tup = a.find(matr, (1, 1), -1)
        self.assertFalse(tup)


class TestGameBoard(unittest.TestCase):
    """Test GameBoard class"""
    def test_correct_get(self):
        """Test getter of value"""
        board = a.GameBoard(8, 2, 3)
        self.assertTrue(board.get_value(5, 5) == 0 or board.get_value(5, 5))
        with self.assertRaises(IndexError):
            board.get_value(9, 9)

    def test_correct_score(self):
        """Test getter of score"""
        board = a.GameBoard(8, 2, 3)
        self.assertEqual(board.get_score(), 0)

    def test_correct_move(self):
        """Test move"""
        board = a.GameBoard(3, 2, 3)
        board._field = [[0, 1, 0], [1, 1, 1], [0, 0, 0]]
        self.assertTrue(board.make_move((1, 0), (2, 0)))
        self.assertFalse(board.make_move((1, 0), (2, 2)))

if __name__ == '__main__':
    unittest.main()
