"""The architechture for 'Painting the map'"""
class Point:
    """Class geometry point"""

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def __str__(self):
        return str(self.x) + " " + str(self.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __gt__(self, other):
        return other < self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return self.x + self.y * 19

    def distance_to(self, other):
        """Distance from self to other"""
        first = abs(self.x - other.x)
        second = abs(self.y - other.y)
        return (first * first + second * second)**0.5

    def nearest(self, points):
        """Find nearest point for 'self' in 'points'"""
        min_p = points[0]
        min_d = self.distance_to(min_p)
        for i in points:
            if self.distance_to(i) < min_d:
                min_d = self.distance_to(i)
                min_p = i
        return min_p

    @staticmethod
    def distance(first, second):
        """Distance from first to second"""
        return first.distance_to(second)


class Sector:
    """Class of geometry sector"""
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return "<" + str(self.start) + ", " + str(self.end) + ">"
    def __eq__(self, other):
        return (self.start == other.start and self.end == other.end) or \
               (self.end == other.start and self.start == other.end)

    def length(self):
        """Len of vector"""
        vector = self.start - self.end
        return (vector.x * vector.x + vector.y * vector.y)**0.5

    def coo_for_equation(self):
        """Cooficients for equation"""
        coo_a = self.start.y - self.end.y
        coo_b = self.end.x - self.start.x
        coo_c = self.start.x * self.end.y - self.end.x * self.start.y
        return coo_a, coo_b, coo_c

    def in_sector(self, point):
        """Is 'point' in 'self'?"""
        in_rect = self.start.x < point.x < self.end.x or self.start.y < point.y < self.end.y
        coo_a, coo_b, coo_c = self.coo_for_equation()
        return in_rect and 0 == coo_a * point.x + coo_b * point.y + coo_c

    def point_is_end(self, point):
        """Is point is end for self?"""
        return self.end == point or self.start == point

    def is_intersect(self, other):
        """Is intersect self other?"""
        other_start = other.start
        other_end = other.end
        part1 = (self.end.x - self.start.x) * (other_end.y - other_start.y)
        part2 = (self.end.y - self.start.y) * (other_end.x - other_start.x)
        lenght = part1 - part2
        part1 = (self.start.y - other_start.y) * (other_end.x - other_start.x)
        part2 = (self.start.x - other_start.x) * (other_end.y - other_start.y)
        width = part1 - part2
        part1 = (self.start.y - other_start.y) * (self.end.x - self.start.x)
        part2 = (self.start.x - other_start.x) * (self.end.y - self.start.y)
        height = part1 - part2
        if lenght == 0:
            return False
        norm_first = width / lenght
        norm_second = height / lenght
        return 0 < norm_first < 1 and 0 < norm_second < 1

    def in_with_end(self, point):
        """Is point in self (with ends include)?"""
        return self.point_is_end(point) or self.in_sector(point)

    def is_match(self, other):
        """Check matching self and other"""
        return (self.in_sector(other.start)  and other.in_sector(self.start)) \
        or (self.in_sector(other.end) and other.in_sector(self.start)) \
        or (self.in_sector(other.start) and other.in_sector(self.end)) \
        or (self.in_sector(other.end) and other.in_sector(self.end)) \
        or (self.in_with_end(other.end) and self.in_with_end(other.start)) \
        or (other.in_with_end(self.end) and other.in_with_end(self.start)) \

    def points(self):
        """Return start and end of Sector"""
        copy_start = Point(self.start.x, self.start.y)
        copy_end = Point(self.end.x, self.end.y)
        return [copy_start, copy_end]

    def point_upper(self, point):
        """Is point upper?"""
        d_a, d_b, d_c = self.coo_for_equation()
        return d_a * point.x + d_b * point.y + d_c >= 0


    @staticmethod
    def sec_is_match(first, second):
        """Check first and second for matching"""
        rev = Sector(second.end, second.start)
        return first.is_match(second) or first.is_match(rev)

    @staticmethod
    def sec_is_intersect(first, second):
        """Check first and second for intersecting"""
        return first.is_intersect(second)


def painting_graph(graph):
    """Painting the graph"""
    result = {}
    colors = [0]

    def count_border():
        """Sort edges of graph"""
        counts_of_inc = {}
        for key in graph:
            counts_of_inc[key] = len(graph[key])
        tuples = sorted(counts_of_inc.items(), key=lambda t: t[::-1], reverse=True)
        return tuples

    def colorize():
        """Colorize the graph"""

        def remove_color():
            """Remove color from stack"""
            for color in colors:
                if color not in colors_stack:
                    return color
            color = colors[-1] + 1
            colors.append(color)
            return color

        for key in sort:
            colors_stack = []
            for key2 in graph[key[0]]:
                if key2 in result:
                    colors_stack.append(result[key2])
            ej_color = remove_color()
            result[key[0]] = ej_color
        return result

    sort = count_border()
    return colorize()

def brute_graph(graph):
    """Painting the graph with bruteforce"""
    colors = {}
    def correct(num):
        """Check"""
        for country in graph[str(num)]:
            if colors.get(str(country), -1) == colors[str(num)]:
                return False
        return True

    def brute_colorize():
        """Bruteforce"""
        num = 1
        while num <= len(graph):
            for i in range(0, len(graph)+1):
                colors[str(num)] = i
                if correct(num):
                    num += 1
                    break
        return colors

    return brute_colorize()
