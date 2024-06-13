"""
Unit testing for Dijkstra algorithm.
"""
import unittest
import sys
from pathlib import Path

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.dijkstra import Dijkstra
from data.maps.simple1 import input_matrix

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        # Initialize the Dijkstra with a test graph
        self.test_matrix = input_matrix
        self.dijkstra = Dijkstra(self.test_matrix)

    def test_when_one_shortest_path(self):
        # Test shortest distance with the test graph, only one possible path
        result = self.dijkstra.find_distances((0,1), (10,4))
        self.assertEqual(result["absoluteDistance"], (13.2))
        self.assertEqual(result["shortestPath"], [(0, 1), (1, 1), (2, 1), (3, 2), (3, 3), (3, 4), \
                                                   (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 4)])

    def test_when_multiple_shortest_paths(self):
        # Test shortest distance with the test graph, multiple possible paths
        result = self.dijkstra.find_distances((0,1), (7,13))
        self.assertEqual(result["absoluteDistance"], (17.7))

    def test_no_path_1(self):
        # Test no path with the test graph, start is isolated
        result = self.dijkstra.find_distances((6,3), (11,13))
        self.assertEqual(result, False)

    def test_no_path_2(self):
        # Test no path with the test graph, end is isolated
        result = self.dijkstra.find_distances((0,12), (6,3))
        self.assertEqual(result, False)

    def test_invalid_nodes(self):
        # Test when both nodes are not within the graph
        result = self.dijkstra.find_distances((0,0), (0,8))
        self.assertFalse(result)
        # Test when start node is not within the graph
        result = self.dijkstra.find_distances((11,6), (4,13))
        self.assertFalse(result)
        # Test when end node is not within the graph
        result = self.dijkstra.find_distances((5,8), (10,13))
        self.assertFalse(result)

    def test_reconstruct_path_when_many_solutions(self):
        # Test the path reconstruction function when multiple routes found
        result = self.dijkstra.find_distances((3,2), (3,9))
        came_from = result["cameFrom"]
        test_path = self.dijkstra.reconstruct_path(came_from, (3,9))
        test_path.sort()
        test_path = test_path[0]

        # compares only the "northest route" when multiple different routes found
        expected_path = [(3, 2), (3, 3), (3, 4), (2, 5), (3, 6), (2, 7), (2, 8), (3, 9)]
        self.assertEqual(test_path, expected_path)

    def test_reconstruct_path_when_one_solution(self):
        # Test the path reconstruction function when one route found
        result = self.dijkstra.find_distances((0,1), (0,4))
        came_from = result["cameFrom"]
        test_path = self.dijkstra.reconstruct_path(came_from, (0,4))
        test_path = test_path[0]
        expected_path = [(0, 1), (1, 1), (2, 1), (3, 2), (3, 3), (3, 4), (2, 5), (1, 5), (0, 4)]
        self.assertEqual(test_path, expected_path)

if __name__ == '__main__':
    unittest.main()
