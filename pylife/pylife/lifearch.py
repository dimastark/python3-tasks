"""This module is the architechture of Conway's Life"""
from collections import namedtuple, defaultdict
from itertools import combinations as combs
from itertools import product
DSET = set(range(-1, 2))
Coords = namedtuple("Coords", ["x", "y"])


class Life:
    """This module is the architechture of Conway's Life"""
    def __init__(self, iterable=None):
        """Init of the Life class"""
        self.cells = defaultdict()
        self.max = Coords(x=0, y=0)
        self.min = Coords(x=0, y=0)
        self.count_of_live = 0
        if iterable:
            for coord in list(iterable):
                self.add(coord.x, coord.y)

    def __iter__(self):
        """Iter of the Life class"""
        return iter(self.cells)

    def __eq__(self, other):
        """Comparison of Life"""
        return len(set(self.cells) - set(other.cells)) == 0

    def add(self, x_pos, y_pos):
        """Add new cell"""
        coord = Coords(x=x_pos, y=y_pos)
        if x_pos < self.min.x or y_pos < self.min.y:
            self.min = coord
        if x_pos > self.max.x or y_pos > self.max.y:
            self.max = coord
        self.cells[coord] = (1, 1)
        self.count_of_live += 1
        for i, j in product(DSET, DSET):
            if i != 0 or j != 0:
                nxt = Coords(x=x_pos+i, y=y_pos+j)
                if self.cells.get(nxt, (0, 0))[0] != 1:
                    self.cells[nxt] = (0, 0)

    def remove(self, x_pos, y_pos):
        """Remove cell from coords"""
        coord = Coords(x=x_pos, y=y_pos)
        if self.cells[coord][0] == 1:
            self.count_of_live -= 1
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
        self.count_of_live = 0
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
        for i, j in product(DSET, DSET):
            if i != 0 or j != 0:
                nxt = Coords(x=x_pos+i, y=y_pos+j)
                if self.cells.get(nxt, (0, 0))[0] == 1:
                    count += 1
        return count

    def get_cell(self, x_pos, y_pos):
        """Getter cells from Life"""
        return self.cells.get(Coords(x=x_pos, y=y_pos), (0, 0))

    def is_dad(self, dad):
        """Is 'self' the next generarion of dad?"""
        dad.new_generation()
        return dad == self

    def combinations(self, start, end):
        """Combinations of cells from 'self'"""
        for count in range(start, end):
            for life in combs(self.cells, count):
                yield life

    def is_eden(self):
        """Is 'self' eden?"""
        mxm = self.max
        mnm = self.min
        size = (abs(mxm.x - mnm.x) - 1, abs(mxm.y - mnm.y) - 1)
        if size[0] <= 6 or size[1] <= 6:
            return False
        for life in self.combinations(self.count_of_live, self.count_of_live * 4):
            if self.is_dad(Life(life)):
                return False
        return True
