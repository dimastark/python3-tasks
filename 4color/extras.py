"""Extra functions for 4color module"""
from geometry import Point, Sector
import itertools as it


def check_countries(first, second, checker):
    """Check 'first' and 'second' countries by checker()

    Arguments:
        first(list<Sector>) - first country
        second(list<Sector>) - second country
        checker (func) - predicat
    Return (bool)
    """
    return any([checker(i, j) for i, j in it.product(first, second)])


def checks(countries):
    """Multiply check
    *see above*
    """
    checker = Sector.sec_is_intersect
    lst = filter(lambda x: x[0] != x[1], it.product(countries, countries))
    return any(check_countries(i, j, checker) for i, j in lst)


def connect_countries(countries):
    """Connect matching countries

    Arguments:
        countries(list<list<Sector>>) - all countries

    Return graph with connections
    """
    graph = {}
    for i in range(1, len(countries) + 1):
        graph[str(i)] = []
    counter = 1
    for first in countries:
        chooser = 1
        for second in countries:
            if first != second and check_countries(first, second, Sector.sec_is_match):
                graph[str(counter)].append(str(chooser))
                graph[str(chooser)].append(str(counter))
            chooser += 1
        counter += 1
    return graph


def make_country(points):
    """Make country from 'Points' list

    Arguments:
        points(list<Point>) - points to make

    Return country
    """
    country = []
    length = len(points)
    if length > 2:
        for i in range(-1, len(points) - 1):
            start = Point(points[i].x, points[i].y)
            end = Point(points[i + 1].x, points[i + 1].y)
            country.append(Sector(start, end))
        for first in country:
            for second in country:
                if first.is_intersect(second):
                    return None
        return country


def jarvismarch(points):
    """Minimal convex hull"""
    p_ln = len(points)
    rng = list(range(p_ln))
    for i in range(1, p_ln):
        if points[rng[i]].x < points[rng[0]].x:
            rng[i], rng[0] = rng[0], rng[i]
    hull = [rng[0]]
    del rng[0]
    rng.append(hull[0])
    while True:
        right = 0
        for i in range(1, len(rng)):
            if rotate(points[hull[-1]], points[rng[right]], points[rng[i]]) < 0:
                right = i
        if rng[right] == hull[0]:
            break
        else:
            hull.append(rng[right])
            del rng[right]
    return [points[i] for i in hull]


def rotate(p_A, p_B, p_C):
    """Where C relatively AB"""
    first = (p_B.x - p_A.x) * (p_C.y - p_B.y)
    second = (p_B.y - p_A.y) * (p_C.x - p_B.x)
    return first - second
