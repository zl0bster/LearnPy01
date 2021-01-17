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
        testXYZ = np.array([[2., 7., 2.],
                            [-3., 6., 4.],
                            [1., -3., 4.],
                            [-3., -4., 5.],
                            [1.5, 2., -2.5],
                            [-6., 8., -10.],
                            [3., -4., -5.],
                            [-2., -5., -5.],
                            [0, 0, -5.],
                            [3., 0, 0],
                            [0, -3., 0]])
        resultDAE = vm.arrayXYZtoDAE(testXYZ)
        resultXYZ = vm.arrayDAEtoXYZ(resultDAE)
        resultDAEdeg = vm.arrayDAEtoDEG(resultDAE)
        print(resultXYZ)
        print(resultDAEdeg)
        testResult = np.equal(testXYZ, resultXYZ)
        print(testResult)
        self.assertEqual(True, testResult)


if __name__ == '__main__':
    unittest.main()
