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
from data.maps.paris import input_matrix as paris
from data.maps.newyork import input_matrix as newyork

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        pass

    def test_shortest_path_simple_map(self):
        matrix = [
                [0,0,0],
                [1,1,0],
                [0,1,0]
                ]
        dijkstra = Dijkstra(matrix)
        result = dijkstra.find_distances((0,0), (2,2))
        self.assertEqual(result["absoluteDistance"], (4))
        self.assertEqual(result["shortestPath"], [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)])


    def test_shortest_path_complex_map_paris(self):
        # Test scenario from moving AI: Paris_0_256.map	256	256	29	9	253	253	388.61731567
        # route direction: upper left corner -> bottom right corner
        start, end = (9,29), (253,253)
        matrix = paris
        dijkstra = Dijkstra(matrix)
        result = dijkstra.find_distances(start, end)
        self.assertEqual(round((result["absoluteDistance"]), 1), (388.6))

    def test_shortest_path_complex_map_newyork(self):
        # Test scenario from moving AI: NewYork_2_256.map	256	256	245	254	72	32	321.33304443
        # route direction: bottom right corner -> upper left corner
        start, end = (254,245), (32,72)
        matrix = newyork
        dijkstra = Dijkstra(matrix)
        result = dijkstra.find_distances(start, end)
        self.assertEqual(round((result["absoluteDistance"]), 1), (321.3))

    def test_no_path_1(self):
        # Test no path with the test graph, start is isolated
        matrix = [
                [0,0,0],
                [1,1,0],
                [0,1,0]
                ]
        dijkstra = Dijkstra(matrix)
        result = dijkstra.find_distances((2,0), (0,0))
        self.assertEqual(result, False)

    def test_no_path_2(self):
        # Test no path with the test graph, end is isolated
        matrix = [
                [0,0,0],
                [1,1,0],
                [0,1,0]
                ]
        dijkstra = Dijkstra(matrix)
        result = dijkstra.find_distances((0,0), (2,0))
        self.assertEqual(result, False)

    def test_invalid_nodes(self):
        # Test when both nodes are not within the graph
        matrix = [
                [0,0,0],
                [1,1,0],
                [0,1,0]
                ]
        dijkstra = Dijkstra(matrix)
        result = dijkstra.find_distances((1,0), (2,1))
        self.assertEqual(result, False)

    def test_reconstruct_path(self):
        # Test the path reconstruction function
        matrix = [
                [0,0,1,1,1,0,0,0],
                [0,0,1,1,1,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
                ]
        start = (1, 1)
        end = (1, 5)
        dijkstra = Dijkstra(matrix)
        result = dijkstra.find_distances(start, end)
        came_from = result["cameFrom"]
        test_path = dijkstra.reconstruct_path(came_from, end)
        expected_path = [(1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (1,5)]
        self.assertEqual(test_path, expected_path)

if __name__ == '__main__':
    unittest.main()
