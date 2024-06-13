"""
Unit testing for graph algorithm which is used for network creation for the JPS algorithm.
"""
import unittest
import sys
from pathlib import Path

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.graph import Graph
from data.maps.simple1 import input_matrix

class TestGraph(unittest.TestCase):
    def setUp(self):
        # Initialize the graph with a test matrix
        self.test_matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
        self.graph = Graph(self.test_matrix)
        self.nodes = list(self.graph.vertices())

    def test_create_graph_n_of_nodes(self):
        # Test if graph is correctly created
        # Compare number of nodes created to number of items in the matrix
        expected = 9
        self.assertEqual(len(self.nodes), expected)


    def test_create_graph_n_of_obstacles(self):
        # test if number of obstacles is according to the matrix
        expected = 4
        obstacles = 0
        for node in self.nodes:
            if node.obstacle == True:
                obstacles += 1
            #print(node.obstacle)

        self.assertEqual(obstacles, expected)

    def test_adjacent_multiple_edges(self):
        # test the adjacent edges generator function
        vertex = next(node for node in self.nodes if node.entity == (1, 1)) #The checked node (1,1) is inserted here
        gen_edges = self.graph.adjacent_edges(vertex)
        edges = list(gen_edges)
        expected_endpoints = [(0, 0), (0, 2), (2, 0), (2, 2)] # Accessible nodes from the middle node (1,1)
        actual_endpoints = [(edge.endpoints()[1].entity) for edge in edges]
        self.assertEqual(sorted(actual_endpoints), sorted(expected_endpoints))





if __name__ == '__main__':
    unittest.main()
