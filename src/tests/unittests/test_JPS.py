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

from algorithms.JPS import *
from algorithms.dijkstra import Dijkstra
from data.maps.milan import input_matrix as milan
from data.maps.paris import input_matrix as paris

class TestJPS(unittest.TestCase):
    def setUp(self):
        # Initialize the JPS with a test matrix
        pass

    def test_shortest_path_milan(self):
        # Test shortest distance with the test graph milan
        matrix=milan
        start = (45, 74)
        end = (2, 23)

        neighbor_list, start_position, end_position, cols, field_status = \
            initialize_graph(matrix, start, end)
        result = jump_point_search(neighbor_list, start_position, end_position, cols, field_status)
        #print(result)
        self.assertEqual(result["absolute_distance"], (111)) #pitäis olla 111
        #self.assertEqual(result["jpoints"], expected_jpoints)
    """def test_shortest_path_paris(self):
        # Test shortest distance with the test graph paris
        # 242	243	6	18	390.30360718
        matrix = paris
        start = (242, 243)
        end = (6, 18)
        neighbor_list, start_position, end_position, cols, field_status = \
            initialize_graph(matrix, start, end)
        result = jump_point_search(neighbor_list, start_position, end_position, cols, field_status)
        #print(result)
        #self.assertEqual(result["absolute_distance"], (390.3))
        #self.assertEqual(result["jpoints"], expected_jpoints)

    def test_against_dijkstra_milan_1(self): #doesnt work
        matrix=milan
        start = (45, 74) #
        end = (2, 23)
        dijkstra = Dijkstra(matrix)
        result_D = dijkstra.find_distances(start, end)
        neighbor_list, start_position, end_position, cols, field_status = \
            initialize_graph(matrix, start, end)
        result_JPS = jump_point_search(neighbor_list, start_position, end_position, cols, field_status)
        #self.assertEqual(result_D["absoluteDistance"], result_JPS["absolute_distance"])

    def test_against_dijkstra_milan_2(self): #works
        matrix=milan
        start = (29, 54)
        end = (68, 120)
        dijkstra = Dijkstra(matrix)
        result_D = dijkstra.find_distances(start, end)
        neighbor_list, start_position, end_position, cols, field_status = \
            initialize_graph(matrix, start, end)
        result_JPS = jump_point_search(neighbor_list, start_position, end_position, cols, field_status)
        self.assertEqual(result_D["absoluteDistance"], result_JPS["absolute_distance"])

    def test_no_path_1(self):
        # Test no path with the test graph, start is isolated
        #jps = JPS(self.test_matrix)
        #result = self.jps.jps((6, 3), (11, 13))
        #self.assertEqual(result, False)

    def test_invalid_nodes(self):
        # Test when both nodes are not within the graph
        result = self.jps.jps((0,0), (0,8))
        self.assertFalse(result)
        # Test when start node is not within the graph
        result = self.jps.jps((11,6), (4,13))
        self.assertFalse(result)
        # Test when end node is not within the graph
        result = self.jps.jps((5,8), (10,13))
        self.assertFalse(result)"""

if __name__ == '__main__':
    unittest.main()
