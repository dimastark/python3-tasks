""" Main logic """
from collections import namedtuple, defaultdict
from itertools import combinations


Point = namedtuple('Point', ['x', 'y'])

DIRECTIONS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]


class Life:
    """ Game model """
    def __init__(self, initial_points=None):
        self.cells = defaultdict()
        self.max = Point(x=0, y=0)
        self.min = Point(x=0, y=0)
        self.lives_count = 0

        for coord in initial_points or []:
            self.add(coord)

    def __iter__(self):
        return iter(self.cells)

    def __eq__(self, other):
        return len(set(self.cells) - set(other.cells)) == 0

    def add(self, point):
        """ Add new cell """
        if point.x < self.min.x or point.y < self.min.y:
            self.min = point
        if point.x > self.max.x or point.y > self.max.y:
            self.max = point
        self.cells[point] = (1, 1)
        self.lives_count += 1
        for i, j in DIRECTIONS:
            nxt = Point(x=point.x + i, y=point.y + j)
            if self.cells.get(nxt, (0, 0))[0] != 1:
                self.cells[nxt] = (0, 0)

    def remove(self, x_pos, y_pos):
        """Remove cell from coords"""
        coord = Point(x=x_pos, y=y_pos)
        if self.cells[coord][0] == 1:
            self.lives_count -= 1
        del self.cells[coord]
        self._update()

    def new_generation(self):
        """Generate new generation"""
        for i in self.cells:
            count = self.count_of_livers(i.x, i.y)
            current = self.cells[i][0]
            if count == 3:
                self.cells[i] = (current, 1)
            if 1 >= count or 4 <= count:
                self.cells[i] = (current, 0)
            if count == 2 and current == 1:
                self.cells[i] = (1, 1)
        self._update()

    def _update(self):
        """Update the field"""
        self.lives_count = 0
        todel = []
        toadd = []
        for i in self.cells:
            if self.cells[i][1] == 1:
                toadd.append(i)
            else:
                todel.append(i)
        for item in todel:
            del self.cells[item]
        for item in toadd:
            self.add(item.x, item.y)

    def count_of_livers(self, x_pos, y_pos):
        """Count of live neighbour"""
        count = 0
        for i, j in DIRECTIONS:
            nxt = Point(x=x_pos + i, y=y_pos + j)
            if self.cells.get(nxt, (0, 0))[0] == 1:
                count += 1
        return count

    def get_cell(self, x_pos, y_pos):
        """Getter cells from Life"""
        return self.cells.get(Point(x=x_pos, y=y_pos), (0, 0))

    def is_dad(self, dad):
        """Is 'self' the next generarion of dad?"""
        dad.new_generation()
        return dad == self

    def combinations(self, start, end):
        """Combinations of cells from 'self'"""
        for count in range(start, end):
            for life in combinations(self.cells, count):
                yield life

    def is_eden(self):
        """Is 'self' eden?"""
        mxm = self.max
        mnm = self.min
        size = (abs(mxm.x - mnm.x) - 1, abs(mxm.y - mnm.y) - 1)
        if size[0] <= 6 or size[1] <= 6:
            return False
        for life in self.combinations(self.lives_count, self.lives_count * 4):
            if self.is_dad(Life(life)):
                return False
        return True
