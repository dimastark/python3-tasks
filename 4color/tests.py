"""Unittest for arch of 'Paint the map'"""


import unittest
import geometry as g
import random as rnd
from generator import generate_stripes_graph
from generator import generate_whole_graph, generate_empty_graph
from generator import generate_tree, generate_setted, generate_pie, generate_points


class PointTests(unittest.TestCase):
    """Tests for Point class"""

    def test_comparsion(self):
        """Tests for comparsion"""
        point1 = g.Point(0, 0)
        point2 = g.Point(1, 1)
        point3 = g.Point(0, 0)
        self.assertTrue(point1 < point2)
        self.assertTrue(point1 == point3)

    def test_sub(self):
        """Test subtraction"""
        point1 = g.Point(2, 2)
        point2 = g.Point(1, 1)
        self.assertTrue((point1 - point2) == g.Point(1, 1))

    def test_distance(self):
        """Test distance_to()"""
        point1 = g.Point(0, 0)
        point2 = g.Point(0, 1)
        distance_1 = point1.distance_to(point2)
        distance_2 = point2.distance_to(point1)
        self.assertEqual(distance_1, distance_2)
        self.assertTrue(distance_1 == distance_2 == g.Point.distance(point1, point2))


class TestSector(unittest.TestCase):
    """Test Sector class"""

    def test_special_methods(self):
        """Test special methods: __len__, __eq__"""
        sec = g.Sector(g.Point(1, 1), g.Point(1, 5))
        self.assertEqual(sec.length(), 4)
        self.assertEqual(sec, g.Sector(g.Point(1, 1), g.Point(1, 5)))

    def test_coo_equation(self):
        """Test coo_for_equation()"""
        sec = g.Sector(g.Point(0, 0), g.Point(0, 10))
        coof = sec.coo_for_equation()
        self.assertEqual(coof[0], -10)
        self.assertTrue(coof[1] == coof[2] == 0)

    def test_cointains(self):
        """Testing all methods, that check contains Point in Sector"""
        sec = g.Sector(g.Point(1, 1), g.Point(10, 10))
        self.assertTrue(sec.in_sector(g.Point(5, 5)))
        self.assertTrue(sec.point_is_end(g.Point(1, 1)))
        self.assertTrue(sec.in_with_end(g.Point(1, 1)))
        self.assertFalse(sec.in_sector(g.Point(0, 0)))

    def test_intersect(self):
        """Testing all methods, that check intersection"""
        sec1 = g.Sector(g.Point(0, 0), g.Point(0, 10))
        sec2 = g.Sector(g.Point(0, 0), g.Point(10, 0))
        sec3 = g.Sector(g.Point(-5, 5), g.Point(5, 5))
        self.assertTrue(sec1.is_intersect(sec3))
        self.assertTrue(g.Sector.sec_is_intersect(sec1, sec3))
        self.assertFalse(sec1.is_intersect(sec2))
        self.assertFalse(g.Sector.sec_is_intersect(sec1, sec2))

    def test_match(self):
        """Testing all methods, that check matching"""
        sec1 = g.Sector(g.Point(0, 0), g.Point(0, 10))
        sec2 = g.Sector(g.Point(0, 5), g.Point(0, 15))
        self.assertTrue(sec1.is_match(sec2))
        self.assertTrue(g.Sector.sec_is_match(sec1, sec2))


class TestPainting(unittest.TestCase):
    """Test painting_graph()"""

    def test_without_painting(self):
        """Test func on islands"""
        graph = {'1':[], '2':[], '3':[]}
        ans = g.painting_graph(graph)
        for key in ans:
            self.assertEqual(ans[key], 0)

    def test_cake(self):
        """Test on cake map"""
        graph = {'1':['2', '3', '4'], '2':['1', '3', '4'], '3':['1', '2', '4'], '4':['1', '2', '3']}
        ans = g.painting_graph(graph)
        for key1 in ans:
            for key2 in ans:
                if key1 != key2:
                    self.assertTrue(ans[key1] != ans[key2])

    def test_without_painting_brute(self):
        """Test func on islands"""
        graph = {'1':[], '2':[], '3':[]}
        ans = g.brute_graph(graph)
        for key in ans:
            self.assertEqual(ans[key], 0)

    def test_cake_brute(self):
        """Test on cake map"""
        graph = {'1':['2', '3', '4'], '2':['1', '3', '4'], '3':['1', '2', '4'], '4':['1', '2', '3']}
        ans = g.brute_graph(graph)
        for key1 in ans:
            for key2 in ans:
                if key1 != key2:
                    self.assertTrue(ans[key1] != ans[key2])

    def test_strips(self):
        """Big striped map"""
        count = rnd.randint(10, 1000)
        graph = generate_stripes_graph(count)
        ans = g.painting_graph(graph)
        ans_br = g.brute_graph(graph)
        for i in range(3, count-1):
            self.assertAlmostEqual(ans[str(i)], ans[str(i-2)], delta=2)
            self.assertAlmostEqual(ans[str(i)], ans[str(i+2)], delta=2)
            self.assertAlmostEqual(ans[str(i+2)], ans[str(i-2)], delta=2)
            self.assertEqual(ans_br[str(i)], ans_br[str(i+2)], ans_br[str(i-2)])

    def test_harder(self):
        """Test on Big graph without painting"""
        size = rnd.randint(10, 1000)
        graph = generate_empty_graph(size)
        ans = g.painting_graph(graph)
        ans_br = g.brute_graph(graph)
        set_br = set(list(ans_br.values()))
        set_al = set(list(ans.values()))
        self.assertEqual(1, len(set_br), len(set_al))

    def test_even_harder(self):
        """Test on map, where each country is a neighbor of the previous"""
        def generate_graph():
            """Big graph with many points"""
            graph = {}
            prevs = []
            for i in range(1, count):
                graph[str(i)] = prevs
                prevs.append(str(i))
            return graph
        count = rnd.randint(10, 1000)
        graph = generate_graph()
        ans = g.painting_graph(graph)
        for i in range(1, count-1):
            self.assertNotEqual(ans[str(i)], ans[str(i+1)])

    def test_even_even_harder(self):
        """Test on map, where all countries each other's neighbors"""
        count = rnd.randint(10, 500)
        graph = generate_whole_graph(count)
        ans = g.painting_graph(graph)
        ans_br = g.brute_graph(graph)
        set_br = set(list(ans_br.values()))
        set_al = set(list(ans.values()))
        self.assertEqual(len(list(graph.keys())), len(set_br), len(set_al))


class TestGenerator(unittest.TestCase):
    """Test painting_graph()"""
    def test_tree(self):
        """Test generated tree"""
        tree = generate_tree(5)
        self.assertTrue(34 == len(tree))

    def test_cake(self):
        """Test on cake map"""
        pie = generate_pie(50)
        self.assertTrue(50 < len(pie))

    def test_setted(self):
        """Test func on setted struct"""
        sett = generate_setted(5)
        self.assertTrue(81 == len(sett))

    def test_tree_except(self):
        """Test generated tree"""
        self.assertRaises(ValueError, generate_tree, 10)

    def test_cake_except(self):
        """Test on cake map"""
        self.assertRaises(ValueError, generate_pie, 500)

    def test_setted_except(self):
        """Test func on setted struct"""
        self.assertRaises(ZeroDivisionError, generate_setted, 100)


if __name__ == '__main__':
    unittest.main()
