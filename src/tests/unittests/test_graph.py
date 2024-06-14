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
        # test the adjacent edges generator function when node has multiple adjacent edges
        vertex = next(node for node in self.nodes if node.entity == (1, 1)) #The checked node (1,1) is inserted here
        gen_edges = self.graph.adjacent_edges(vertex)
        edges = list(gen_edges)
        expected_endpoints = [(0, 0), (0, 2), (2, 0), (2, 2)] # Accessible nodes from the middle node (1,1)
        actual_endpoints = [(edge.endpoints()[1].entity) for edge in edges]
        self.assertEqual(sorted(actual_endpoints), sorted(expected_endpoints))

    def test_adjacent_one_edge(self):
        # test the adjacent edges generator function when node has one adjacent edge
        vertex = next(node for node in self.nodes if node.entity == (0, 0)) #The checked node (0,0) is inserted here
        gen_edges = self.graph.adjacent_edges(vertex)
        edges = list(gen_edges)
        expected_endpoints = [(1, 1)] # Accessible node from the corner node (0,0)
        actual_endpoints = [(edge.endpoints()[1].entity) for edge in edges]
        self.assertEqual(sorted(actual_endpoints), sorted(expected_endpoints))

    def test_no_adjacent_edges(self):
        # test the adjacent edges generator function when node has no adjacent edges
        test_matrix = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]
        graph = Graph(test_matrix)
        nodes = list(graph.vertices())
        vertex = next(node for node in nodes if node.entity == (2, 2)) #The checked node (0,0) is inserted here
        gen_edges = graph.adjacent_edges(vertex)
        edges = list(gen_edges)
        expected_endpoints = [] # no accessible nodes from the corner
        actual_endpoints = [(edge.endpoints()[1].entity) for edge in edges]
        self.assertEqual(sorted(actual_endpoints), sorted(expected_endpoints))

    def test_create_simple_graph(self):
        # test graph creation for a small matrix with 3 open vertices
        test_matrix = [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 1]
        ]
        graph = Graph(test_matrix)
        nodes = list(graph.vertices())
        nodelist = []
        for node in nodes:
            if not node.obstacle:
                nodelist.append(node.entity)
        # open vertice list correct
        self.assertEqual(nodelist, [(0, 2), (1, 1), (2, 0)])
        # number of edges correct
        self.assertEqual(len(graph.edges()), 4) #4 edges because connected to both directions
        #graph.print_graph()

    def test_create_complex_graph(self):
        # test graph creation for a complex matrix
        graph = Graph(input_matrix)
        nodes = list(graph.vertices())
        nodelist = []
        for node in nodes:
            if not node.obstacle:
                nodelist.append(node.entity)
        #print(nodelist)
        expected_vertices = [(0, 1), (0, 4), (0, 7), (0, 9), (0, 12), (1, 1), (1, 5), (1, 8), (1, 9), (1, 13), (2, 1), (2, 5), (2, 7), (2, 8), (2, 10), (2, 13),\
                    (3, 2), (3, 3), (3, 4), (3, 6), (3, 9), (3, 12), (4, 1), (4, 5), (4, 7), (4, 8), (4, 9), (4, 13), (5, 1), (5, 5), (5, 8), (5, 9), (5, 12),\
                    (6, 1), (6, 3), (6, 5), (6, 7), (6, 8), (6, 9), (6, 12), (7, 1), (7, 5), (7, 7), (7, 8), (7, 10), (7, 11), (7, 13), (8, 1), (8, 5), (8, 8), \
                    (8, 9), (8, 12), (9, 1), (9, 5), (9, 8), (9, 9), (9, 12), (10, 1), (10, 4), (10, 7), (10, 9), (10, 12), (11, 1), (11, 5), (11, 7), (11, 8), (11, 9), (11, 12), (11, 13)]
        # open vertice list correct
        self.assertEqual(nodelist, expected_vertices)

if __name__ == '__main__':
    unittest.main()
