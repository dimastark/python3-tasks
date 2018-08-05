"""Generator of graphs"""
#!/usr/bin/env python3
from random import randint
from geometry import Point
from extras import make_country


def generate_tree(height):
    """Return binary tree (planar graph)

    Arguments:
        height (int) - height of three (in range(1, 6))

    Return generated struct
    """
    lay = 50 // height
    ans = []
    fact = 1
    for j in range(height):
        for i in range(0, 50, 50 // fact):
            x_coord = i + 50 // fact
            y_coord = (j + 1) * lay
            top = [Point(i, j * lay), Point(x_coord, j * lay)]
            bot = [Point(x_coord, y_coord), Point(i, y_coord)]
            ans.append(make_country(top + bot))
        fact *= 2
    return ans


def generate_setted(size):
    """Return squares

    Arguments:
        size - size of square (in range(5, 11))

    Return generated set
    """
    ans = []
    div = 50 // size
    rng = list(range(0, 50 - size, 50 // div))
    for i in rng:
        for j in rng:
            top = [Point(i, j), Point(i + size, j)]
            bot = [Point(i + size, j + size), Point(i, j + size)]
            ans.append(make_country(top + bot))
    return ans


def generate_stripes_graph(size):
    """Return graph looks like a stiped thing

    Arguments:
        size (int) - size of graph

    Return generated graph
    """
    graph = {}
    graph['1'] = ['2']
    for i in range(2, size):
        graph[str(i)] = [str(i - 1), str(i + 1)]
    graph[str(size)] = [str(size - 1)]
    return graph


def generate_pie_graph(size):
    """Return graph looks like a pie))0)

    Arguments:
        size (int) - size of graph

    Return generated graph
    """
    graph = generate_stripes_graph(size)
    graph[str(size)].append('1')
    graph['1'].append(str(size))
    return graph


def generate_pie(size):
    """Return triangles looks like a pie))0)

    Arguments:
        size (int) - size (in range(5, 51))

    Return generated triangulations
    """
    piece = size // 4
    ost = size % 4
    rng = list(range(5, 45, 40 // piece))
    rng_ost = list(range(5, 45, 40 // (piece + ost)))
    triangles = []
    center = Point(25, 25)
    top = [Point(0, 0)] + [Point(i, 0) for i in rng]
    left = [Point(0, i) for i in rng] + [Point(0, 50)]
    right = [Point(50, 0)] + [Point(50, i) for i in rng]
    bot = [Point(i, 50) for i in rng_ost] + [Point(50, 50)]
    lst = top + right + bot[::-1] + left[::-1] + [Point(0, 0)]
    for i in range(len(lst) - 1):
        triangles.append(make_country([center] + lst[i:i + 2]))
    return triangles


def generate_empty_graph(size):
    """Return graph without connections

    Arguments:
        size (int) - size of graph

    Return generated graph
    """
    graph = {}
    for i in range(1, size + 1):
        graph[str(i)] = []
    return graph



def generate_points(count):
    """Generate 'count' points"""
    points = []
    while len(points) < count:
        r_x = randint(0, 50)
        r_y = randint(0, 50)
        point = Point(r_x, r_y)
        if point not in points:
            points.append(point)
    return points


def generate_whole_graph(size):
    """Return graph with all connections

    Arguments:
        size (int) - size of graph

    Return generated graph
    """
    graph = {}
    all_points = [str(j) for j in range(1, size + 1)]
    for i in range(1, size + 1):
        graph[str(i)] = list(all_points)
        graph[str(i)].remove(str(i))
    return graph
