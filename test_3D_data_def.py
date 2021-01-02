import unittest
import numpy as np

import data_def as d3


class Data3DTestCase(unittest.TestCase):
    POINTXYZ1 = (1.2, -10, 0)
    POINTXYZ2 = (2.5, 1, 0)
    POINTXYZ3 = (2.5, 0, 1.8)
    POINTXYZ4 = [2.5, 0, 1.8]
    POINTS = [POINTXYZ1, POINTXYZ2, POINTXYZ3]
    NPPOINTS = np.asarray(POINTS)

    def test_storage(self):
        a = d3.PointXYZ(*self.POINTXYZ1)
        self.assertEqual(a.get(), self.POINTXYZ1)
        a.set(*self.POINTXYZ2)
        self.assertEqual(a.get(), self.POINTXYZ2)

    def test_point_list(self):
        a = d3.PointXYZ(*self.POINTXYZ1)
        b = d3.PointDAE(*self.POINTXYZ2)
        pl = d3.PointsList(listType="XYZ")
        self.assertEqual(pl.add_point(a), 0)
        with self.assertRaises(TypeError):
            pl.add_point(b)
        self.assertEqual(pl.add_point(self.POINTXYZ2), 1)
        self.assertEqual(pl.add_point(self.POINTXYZ3), 2)
        self.assertEqual(pl.add_point(self.POINTXYZ2), 1)
        self.assertEqual(pl.add_point(self.POINTXYZ4), 2)
        self.assertEqual(pl.add_point(a), 0)
        for i in range(len(pl)):
            self.assertEqual(pl.get_point(i), self.POINTS[i])
        print(pl.np_array())
        print(self.NPPOINTS)
        self.assertEqual(np.array_equal(pl.np_array(), self.NPPOINTS), True)

if __name__ == '__main__':
    unittest.main()
