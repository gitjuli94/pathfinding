"""
Unit testing for network algorithm which is used for network creation for the Dijkstra algorithm.
"""
import unittest
import sys
from pathlib import Path

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.network import Generate_Network

class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_network_only_obstacles(self):
        # Test network generation of a matrix with only obstacles
        matrix = [[1 for _ in range(6)] for _ in range(6)]
        network_obstacles = Generate_Network(matrix)
        result = network_obstacles.create_graph()
        self.assertEqual(result, {})

    def test_generate_network_big_open_matrix(self):
        # Test network generation of a big open matrix
        matrix = [[0 for _ in range(100)] for _ in range(100)]
        network_obstacles = Generate_Network(matrix)
        result = network_obstacles.create_graph()
        self.assertEqual(len(result.keys()), 10000)

    def test_generate_network_pattern_matrix(self):
        # Test network generation of a matrix with a pattern
        matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
        network = Generate_Network(matrix)
        rounded_network = {} # Network with rounded weights to 3 digits
        for key, value in network.graph.items():
            rounded_network[key] = [((x, y), round(weight, 3)) for (x, y), weight in value]
        expected_graph = {
            (0, 0): [((1, 1), 1.414)],
            (0, 2): [((1, 1), 1.414)],
            (1, 1): [((0, 0), 1.414), ((0, 2), 1.414), ((2, 0), 1.414), ((2, 2), 1.414)],
            (2, 0): [((1, 1), 1.414)],
            (2, 2): [((1, 1), 1.414)]
        }
        self.assertEqual(rounded_network, expected_graph)

    def test_add_edges(self):
        # Test adding edges method by adding edges manually for a node
        matrix = [
            [0, 0],
            [0, 1]
        ]
        network = Generate_Network(matrix)
        network.graph = {(0, 0): []}  # Reset graph for the node (0, 0)
        network.add_edges(0, 0)
        expected_network = {(0, 0): [((1, 0), 1), ((0, 1), 1)]} # edges added down and right
        self.assertEqual(network.graph, expected_network)


if __name__ == '__main__':
    unittest.main()
