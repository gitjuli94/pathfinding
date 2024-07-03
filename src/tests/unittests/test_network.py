"""
Unit testing for network algorithm which is used for network creation for the Dijkstra algorithm.
"""
import unittest
import sys
from pathlib import Path

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.network import GenerateNetwork

class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_network_only_obstacles(self):
        # Test network generation of a matrix with only obstacles
        matrix = [[1 for _ in range(6)] for _ in range(6)]
        network_obstacles = GenerateNetwork(matrix)
        result = network_obstacles.create_graph()
        self.assertEqual(result, {})

    def test_generate_network_big_open_matrix(self):
        # Test network generation of a big open matrix
        n= 100
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        network_obstacles = GenerateNetwork(matrix)
        result = network_obstacles.create_graph()

        # check amount of keys (nodes)
        self.assertEqual(len(result.keys()), (n*n))

        #check amount of items (edges):
        tot_edges = sum(len(value) for value in result.values())
        expected = 4*(n-1)*n+4*(n-1)**2
        self.assertEqual(tot_edges, expected)

    def test_generate_network_pattern_matrix(self):
        # Test network generation of a matrix,
        # check that goes around corners orthogonally
        matrix = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        network = GenerateNetwork(matrix)
        result = network.create_graph()
        expected_graph = {
            (0, 0): [((1, 0), 1), ((0, 1), 1)],
            (0, 1): [((0, 0), 1), ((0, 2), 1)],
            (0, 2): [((0, 1), 1), ((1, 2), 1)],
            (1, 2): [((0, 2), 1), ((2, 2), 1)],
            (2, 2): [((1, 2), 1), ((2, 1), 1)],
            (2, 1): [((2, 2), 1), ((2, 0), 1)],
            (2, 0): [((2, 1), 1), ((1, 0), 1)],
            (1, 0): [((2, 0), 1), ((0, 0), 1)]
        }
        # sort to put keys and items in same order
        result_sorted = sorted(result)
        expected_sorted = sorted(expected_graph)
        self.assertEqual(result_sorted, expected_sorted)

    def test_add_edges(self):
        # Test adding edges method by adding edges manually for a node
        matrix = [
            [0, 0],
            [0, 1]
        ]
        network = GenerateNetwork(matrix)
        network.graph = {(0, 0): []}  # reset graph for the node (0, 0)
        network.add_edges(0, 0)
        expected_network = {(0, 0): [((1, 0), 1), ((0, 1), 1)]} # edges added down and right
        self.assertEqual(network.graph, expected_network)


if __name__ == '__main__':
    unittest.main()
