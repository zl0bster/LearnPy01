import unittest
import numpy as np

import data_def as d3


class MyTestCase(unittest.TestCase):
    def test_edges_list(self):
        edgeList = [(i, i + 1) for i in range(8)]
        halfList = edgeList[::-1]
        fullList = edgeList[:]
        for val in halfList:
            arg = (val[1], val[0])
            fullList.append(arg)
        el = d3.EdgeList()
        print(edgeList, '\n', fullList)
        for edge in fullList:
            el.add_edge(v1=edge[0], v2=edge[1])
        print('+ ' * 10)
        for edge in el:
            print(edge)
        uniqueList = el.get_unique()
        print(uniqueList)
        print(uniqueList == edgeList)
        self.assertEqual(uniqueList, edgeList)


if __name__ == '__main__':
    unittest.main()
