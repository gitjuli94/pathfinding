"""
Unit testing for JPS algorithm.
"""
import unittest
import sys
from pathlib import Path
import math

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.JPS import JPS
from data.maps.simple1 import input_matrix

class TestJPS(unittest.TestCase):
    def setUp(self):
        # Initialize the JPS with a test graph
        self.test_matrix = input_matrix
        self.jps = JPS(self.test_matrix)

    def test_shortest_path(self):
        # Test shortest distance with the test graph
        jps = JPS(self.test_matrix)
        result = jps.jps((0,1), (10,4))
        self.assertEqual(result["absoluteDistance"], (13.2))
        self.assertEqual(result["shortestPath"], [(0, 1), (1, 1), (2, 1), (3, 2), (3, 3), (3, 4), \
                                                   (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 4)])

    def test_diagonal_path(self):
        # Test a diagonal path
        test_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        jps = JPS(test_matrix)
        result = jps.jps((0,0), (2,2))
        expected_distance = round(math.sqrt(2) * 2, 1)
        self.assertEqual(result["absoluteDistance"], expected_distance)
        self.assertEqual(result["shortestPath"], [(0, 0), (1, 1), (2, 2)])

    def test_no_path_1(self):
        # Test no path with the test graph, start is isolated
        #jps = JPS(self.test_matrix)
        result = self.jps.jps((6, 3), (11, 13))
        self.assertEqual(result, False)

    def test_no_path_2(self):
        # Test no path with the test graph, end is isolated
        result = self.jps.jps((0,12), (6,3))
        self.assertEqual(result, False)

    def test_invalid_nodes(self):
        # Test when both nodes are not within the graph
        result = self.jps.jps((0,0), (0,8))
        self.assertFalse(result)
        # Test when start node is not within the graph
        result = self.jps.jps((11,6), (4,13))
        self.assertFalse(result)
        # Test when end node is not within the graph
        result = self.jps.jps((5,8), (10,13))
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
