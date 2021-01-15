import unittest

import numpy as np

import vertex_manipulations as vm

X = 0
Y = 1
Z = 2
R = 0
A = 1
E = 2
Q = 3


class MyTestCase(unittest.TestCase):
    def test_arrayXYZtoDAE(self):
        testXYZ = np.array([[2, 2, 2],
                            [3, 0, 4],
                            [3, 0, -4],
                            [-3, -3, -2.5]])
        resultDAE = vm.arrayXYZtoDAE(testXYZ)
        resultDAEdeg = vm.arrayDAEtoDEG(resultDAE)
        print(resultDAE)
        print(resultDAEdeg)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
