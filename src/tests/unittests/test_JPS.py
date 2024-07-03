"""
Unit testing for JPS algorithm.
"""
import unittest
import sys
from pathlib import Path
import random


# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.jps import JPS
from algorithms.dijkstra import Dijkstra
from data.maps.newyork import input_matrix as newyork
from data.maps.boston_2_256 import input_matrix as boston

class TestJPS(unittest.TestCase):
    def setUp(self):
        pass

    def test_shortest_path_complex_map_paris(self):
        # Test scenario from moving AI:
        # NewYork_2_256.map	256	256	236	236	19	25	337.78888855
        # route direction: bottom right corner -> upper left corner
        matrix = newyork
        start = (236, 236)
        end = (25, 19)
        jps = JPS(matrix)
        result = jps.jump_point_search(start, end)
        self.assertEqual(round((result["absoluteDistance"]), 1), (337.8))

    def test_shortest_path_complex_map_newyork(self):
        # Test scenario from moving AI: 95
        # NewYork_2_256.map	256	256	36	14	232	253	341.27416992
        # route direction: upper left corner -> bottom right corner
        matrix = newyork
        start = (14,36)
        end = (253,232)
        jps = JPS(matrix)
        result = jps.jump_point_search(start, end)
        self.assertEqual(round((result["absoluteDistance"]), 1), (341.3))

    def test_no_path_1(self):
        # Test no path with the test graph, start is isolated
        matrix = [
                [0,0,0],
                [1,1,0],
                [0,1,0]
                ]
        jps = JPS(matrix)
        result = jps.jump_point_search((2,0), (0,0))
        self.assertEqual(result, False)

    def test_no_path_2(self):
        # Test no path with the test graph, end is isolated
        matrix = [
                [0,0,0],
                [1,1,0],
                [0,1,0]
                ]
        jps = JPS(matrix)
        result = jps.jump_point_search((0,0), (2,0))
        self.assertEqual(result, False)

    def test_invalid_nodes(self):
        # Test when both nodes are not within the graph
        matrix = [
                [0,0,0],
                [1,1,0],
                [0,1,0]
                ]
        jps = JPS(matrix)
        result = jps.jump_point_search((1,0), (2,1))
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
        jps = JPS(matrix)
        result = jps.jump_point_search(start, end)
        test_path = result["path"]
        expected_path = [(1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (1,5)]
        self.assertEqual(test_path, expected_path)

    def test_JPS_against_Dijsktra_with_random_inputs(self):

        # test map without big isolated areas
        matrix = boston

        free_space=[]

        dijkstra = Dijkstra(matrix)
        graph = dijkstra.graph


        # choose suitable points from the nodes in the graph
        for node in dijkstra.nodes:
            # if a node has enough edges, it's not isolated (e.g. inside a building)
            if len(graph[node]) > 1:
                free_space.append(node)

        jps = JPS(matrix)

        # test both algorithms with 10 random start and end nodes
        for i in range(10):
            start = random.choice(free_space)
            end = random.choice(free_space)

            result_Dijkstra = dijkstra.find_distances(start, end)
            result_JPS = jps.jump_point_search(start, end)
            self.assertEqual(round((result_Dijkstra["absoluteDistance"]), 1),
                             round((result_JPS["absoluteDistance"]), 1))


if __name__ == '__main__':
    unittest.main()
