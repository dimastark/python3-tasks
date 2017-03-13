""" Unittest for 'gifparse' """

import os
import unittest
from gifparse import gifparser as g


DIR = os.path.dirname(os.path.abspath(__file__))


class ParserTests(unittest.TestCase):
    """ Test parser on real images """

    def test_comments(self):
        """ Parse comments ext """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/comm.gif'))
        self.assertTrue(len(inf.comments) > 0)

    def test_colors(self):
        """  Parse colors table """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/col.gif'))
        self.assertTrue(len(inf.colors) == 4)

    def test_frames(self):
        """ Parse frames """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/frames.gif'))
        self.assertTrue(len(inf.frames) == 16)

    def test_extensions(self):
        """ Parse extensions """
        inf1 = g.GifInfo(os.path.join(DIR, '..', 'test_files/comm.gif'))
        inf2 = g.GifInfo(os.path.join(DIR, '..', 'test_files/col.gif'))
        inf3 = g.GifInfo(os.path.join(DIR, '..', 'test_files/frames.gif'))
        self.assertEqual(inf1.spec, inf2.spec, inf3.spec)

    def test_header(self):
        """ Parse title """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/col.gif'))
        self.assertTrue(inf.size[0] == inf.size[1])

    def test_2(self):
        """ Test case 2 """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/2.gif'))
        self.assertAlmostEqual(inf.aratio, 1)

    def test_4(self):
        """ Test case 4 """
        with self.assertRaises(ValueError):
            g.GifInfo(os.path.join(DIR, '..', 'test_files/4.gif'))

    def test_5(self):
        """ Test case 5 """
        with self.assertRaises(ValueError):
            g.GifInfo(os.path.join(DIR, '..', 'test_files/5.gif'))

    def test_7(self):
        """ Test case 7 """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/7.gif'))
        self.assertTrue(len(inf.frames) == 7)

    def test_9(self):
        """ Test case 9 """
        with self.assertRaises(ValueError):
            g.GifInfo(os.path.join(DIR, '..', 'test_files/9.gif'))

    def test_13(self):
        """ Test case 13 """
        with self.assertRaises(ValueError):
            g.GifInfo(os.path.join(DIR, '..', 'test_files/13.gif'))

    def test_14(self):
        """ Test case 14 """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/14.gif'))
        self.assertTrue(len(inf.frames) > 100)

    def test_15(self):
        """ Test case 15 """
        with self.assertRaises(ValueError):
            g.GifInfo(os.path.join(DIR, '..', 'test_files/15.gif'))

    def test_16(self):
        """ Test case 16 """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/16.gif'))
        self.assertTrue(inf.frames)

    def test_17(self):
        """ Test case 17 """
        with self.assertRaises(ValueError):
            g.GifInfo(os.path.join(DIR, '..', 'test_files/17.gif'))

    def test_18(self):
        """ Test case 18 """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/18.gif'))
        self.assertAlmostEqual(inf.aratio, 0)

    def test_19(self):
        """ Test case 19 """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/19.gif'))
        self.assertTrue(inf.loops == "Infinity")

    def test_20(self):
        """ Test case 20 """
        inf = g.GifInfo(os.path.join(DIR, '..', 'test_files/20.gif'))
        self.assertTrue(inf.loops == len(inf.frames))


if __name__ == '__main__':
    unittest.main()
