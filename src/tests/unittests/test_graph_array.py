"""
Unit testing for graph algorithm which is used for network creation for the JPS algorithm.
"""
import unittest
import sys
from pathlib import Path

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.graph_array import generate_graph, get_coordinates
from data.maps.simple1 import input_matrix

class TestGraph(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_graph_big_input(self):
        matrix = [[0 for _ in range(90)] for _ in range(80)]
        graph = generate_graph(matrix, (0,0), (20,35))
        self.assertEqual(len(graph[0]), 7200)

    def test_generate_graph_big_input(self):
        matrix = [[1 for _ in range(10)] for _ in range(20)]
        graph = generate_graph(matrix, (0,0), (5,5))
        self.assertEqual(len(graph[0]), 0)

    def test_skip_wall_tiles(self):
        matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
        graph = generate_graph(matrix, (0,0), (2,2))
        self.assertEqual(len(graph[0]), 5)
        self.assertNotIn(1, graph[0])
        self.assertNotIn(3, graph[0])
        self.assertNotIn(5, graph[0])
        self.assertNotIn(7, graph[0])

    def test_edges_and_corners(self):
        matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        graph = generate_graph(matrix, (0,0), (2,1))
        self.assertEqual(graph[0][0], [3, 1, 4])
        self.assertEqual(graph[0][1], [4, 0, 2, 5, 3])
        self.assertEqual(graph[0][8], [5, 7, 4])
        self.assertEqual(graph[0][6], [3, 7, 4])


if __name__ == '__main__':
    unittest.main()
