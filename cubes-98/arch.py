"""This module is architecture for game 'Lines'"""


import random as r


def count_of_neightbor(matr, coord, x_step, y_step):
    """Return the number of identical cells
    on specified direction

    Args:
      matr: matrix of cells
      x, y: coordinates of comparison cell
      x_step, y_step: give direction to comparison
    """
    if x_step == y_step == 0:
        return 0
    length = len(matr)
    factor = 1
    while True:
        if no_inderr(length, coord[1]+y_step*factor, coord[0]+x_step*factor) \
        and matr[coord[1]][coord[0]] == matr[coord[1]+y_step*factor][coord[0]+x_step*factor]:
            factor += 1
        else:
            break
    return factor - 1


def arr_of_neightbor(matrix, coord):
    """Return the number of identical cells
    on all direction

    Args:
      matrix: matrix of cells
      x, y: coordinates of comparison cell
    """
    matr = matrix
    func = count_of_neightbor
    arr = [[func(matr, coord, x_s, y_s) for x_s in (-1, 0, 1)] for y_s in (-1, 0, 1)]
    return arr


def fill(coord, matr, lev):
    """Fill releated with matr[y][x] cells 'lev'

       Args:
         coord: coordinates of cell
         matr: matrix, where need fill
         lev: value for fill
    """
    for y_step in (-1, 0, 1):
        for x_step in (-1, 0, 1):
            if (x_step == 0 or y_step == 0) and x_step != y_step \
            and matr[coord[1]+y_step][coord[0]+x_step] == 0:
                matr[coord[1]+y_step][coord[0]+x_step] = lev


def filled(matr, coord, lev):
    """Make fill() for all cells with 'lev' value

       Args:
         matr: matrix, where need fiil
         coord: coordinates of cell, that shouldn't be fill
         lev: value for fill
    """
    fillen = 0
    if 0 > matr[coord[1]][coord[0]]:
        return False
    for y_pos in range(len(matr)):
        for x_pos in range(len(matr)):
            if matr[y_pos][x_pos] == lev:
                fill((x_pos, y_pos), matr, lev-1)
                fillen += 1
    return fillen > 0


def find(matr, coord, lev):
    """Find cell with 'lev' value in direction

       Args:
         matr: matrix for searching in
         coord: coordinates cell
         lev: value to find
    """
    for y_step in (-1, 0, 1):
        for x_step in (-1, 0, 1):
            if (x_step == 0 or y_step == 0) and x_step != y_step \
            and matr[coord[1]+y_step][coord[0]+x_step] == lev:
                return coord[0]+x_step, coord[1]+y_step
    return None


def find_way(start, end, matr):
    """Return list of steps
    if the object can move
    from (x1, y1) to (x2, y2)
    else return []

    Args:
      matr: matrix of cells
      x1, y1: coordinates of start
      x2, y2: coordinates of end
    """
    end_x, end_y, lev, way = end[0], end[1], -1, [end]
    fill(start, matr, lev)
    found = True
    while found:
        found = filled(matr, end, lev)
        lev -= 1
    lev += 2
    while lev != 0:
        next_s = find(matr, (end_x, end_y), lev)
        if next_s:
            way.append(next_s)
        else:
            return None
        lev += 1
        end_x, end_y = way[-1][0], way[-1][1]
    if abs(end_x-start[0]) != abs(end_y-start[1]):
        if 1 == abs(end_x-start[0]) + abs(end_y-start[1]):
            way.append(start)
            return way
    else:
        return None


def make_border(matrix):
    """Return the original matrix wrapped in units

    Args:
      matr: matrix to wrapped
    """
    height = len(matrix)
    length = len(matrix[0])
    matrix_with_border = list()
    matrix_with_border.append([10 for _ in range(length+2)])
    for j in range(height):
        line = []
        for i in range(length+2):
            if i == 0 or i == length+1:
                line.append(10)
            else:
                line.append(matrix[j][i-1])
        matrix_with_border.append(line)
    matrix_with_border.append([10 for _ in range(length+2)])
    return matrix_with_border


def no_inderr(bord, *values):
    """Return Returns true if all values ​​greater
    or equal than zero and less than the permissible boundaries

    Args:
      bord: limit for the values
      *values: values, that need to check
    """
    for value in values:
        if 0 > value or value >= bord:
            return False
    return True


class GameBoard:
    """Class that describes the game board"""

    def __init__(self, rang, combo, colors_count):
        """Initialize a game board

           Args:
             rang: size of field
             combo: size of combo lines
             colors_count: count of colors
        """
        self.rang = rang
        self._prepare_board(rang)
        self._colors_count = colors_count
        self.adds = []
        self.add_circles(rang)
        self.stand_circles()
        self._score = 0
        self._combo = combo

    def _prepare_board(self, rang):
        """Prepare field (rang*rang) for game

           Args:
             rang: size of field
        """
        self._field = [[0 for _ in range(rang)] for _ in range(rang)]

    def __str__(self):
        """Returns a string representation of the field"""
        line = str()
        for i in range(self.rang):
            for j in range(self.rang):
                line += str(self._field[i][j])
            line += '\n'
        return line

    def add_circles(self, count):
        """Add 'count' or less new objects on buffer
           for stand_circles()

           Args:
             count: count of circles

           Note: non greater than rang*rang
        """
        field = str(self)
        empty = field.count('0')
        if count <= empty:
            added = count
        else:
            added = empty
        for _ in range(added):
            rand_x = r.randrange(0, self.rang)
            rand_y = r.randrange(0, self.rang)
            if self._field[rand_y][rand_x] == 0:
                self.adds.append((rand_x, rand_y, r.randrange(1, self._colors_count+1)))
            else:
                self.add_circles(1)

    def stand_circles(self):
        """Add new objects on the field from buffer"""
        while len(self.adds) != 0:
            next_inf = self.adds.pop()
            if self._field[next_inf[1]][next_inf[0]] == 0:
                self._field[next_inf[1]][next_inf[0]] = next_inf[2]
            else:
                while True:
                    x_r = r.randrange(0, self.rang)
                    y_r = r.randrange(0, self.rang)
                    if self._field[y_r][x_r] == 0:
                        self._field[y_r][x_r] = next_inf[2]
                        break

    def get_value(self, x_pos, y_pos):
        """Getter for get value in coordinates (x,y) from field

           Args:
             x_pos, y_pos: coordinates in field
        """
        if no_inderr(self.rang, x_pos, y_pos):
            return self._field[y_pos][x_pos]
        else:
            raise IndexError("Out of field")

    def get_score(self):
        """Getter for get scores value"""
        return self._score

    def make_move(self, start, end):
        """Makes a move (move object from (x1,y1) to (x2,y2)), if possible"""
        if no_inderr(self.rang, start[0], start[1]) and no_inderr(self.rang, end[0], end[1]):
            matr = make_border(self._field)
            if self._field[start[1]][start[0]] != 0 and self._field[end[1]][end[0]] == 0:
                way = find_way((start[0]+1, start[1]+1), (end[0]+1, end[1]+1), matr)
                if way:
                    self._field[end[1]][end[0]] = self._field[start[1]][start[0]]
                    self._field[start[1]][start[0]] = 0
                    self.stand_circles()
                    self._remove_matches(end)
                    self.add_circles(self.rang//3)
                return way

    def _remove_direct(self, sides, coord, x_st, y_st):
        """Find and destroy lines with 'combo' elements directly"""
        if sides[1-y_st][1-x_st] + sides[1+y_st][1+x_st] + 1 >= self._combo:
            self._score += 25 * (sides[1-y_st][1-x_st] + sides[1+y_st][1+x_st])
            for i in range(1, sides[1-y_st][1-x_st] + 1):
                self._field[coord[1]-y_st*i][coord[0]-x_st*i] = 0
            for i in range(1, sides[1+y_st][1+x_st] + 1):
                self._field[coord[1]+y_st*i][coord[0]+x_st*i] = 0
            self._field[coord[1]][coord[0]] = 0

    def _remove_matches(self, coord):
        """Find and destroy lines with 'combo' elements"""
        sides = arr_of_neightbor(self._field, coord)
        self._remove_direct(sides, coord, -1, 0)
        self._remove_direct(sides, coord, 0, -1)
        self._remove_direct(sides, coord, -1, -1)
        self._remove_direct(sides, coord, -1, 1)
