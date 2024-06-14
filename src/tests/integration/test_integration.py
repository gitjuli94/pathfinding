"""
Integration testing for the JPS and Dijkstra algorithms.
"""
import unittest
import sys
from pathlib import Path

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.JPS import JPS
from algorithms.dijkstra import Dijkstra
from data.maps.simple1 import input_matrix

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Initialize the algorithms with a test matrix
        self.test_matrix = input_matrix
        self.jps = JPS(self.test_matrix)
        self.dijkstra = Dijkstra(self.test_matrix)

    """def test_same_path_length_found(self):
        # Test if the algorithms find the same path length
        result_JPS = self.jps.jps((4,7), (2,1))
        result_Dijkstra = self.dijkstra.find_distances((4,7), (2,1))
        self.assertEqual(result_JPS["absoluteDistance"], result_Dijkstra["absoluteDistance"])

    def test_same_path_found(self):
        # Test if the algorithms find the same path, here Dijkstra can find 4 different paths
        result_JPS = self.jps.jps((2,1), (7,13))
        result_Dijkstra = self.dijkstra.find_distances((2,1), (7,13))

        for route_dijkstra in result_Dijkstra["Routes"]:
            if str(result_JPS["shortestPath"]) == str(route_dijkstra):
                # test if the route found by JPS is same as one of the routes found by Dijkstra
                self.assertEqual(str(result_JPS["shortestPath"]), str(route_dijkstra))"""

    def test_jump_points_within_the_route(self):
        # Test if the jump points are correctly found
        # example case from https://blog.finxter.com/jump-search-algorithm-in-python-a-helpful-guide-with-video/

        test_matrix = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        start = (1,1)
        end = (1,5)
        expected_jpoints = [(0,2), (0,4)]
        jps = JPS(test_matrix)
        result = jps.jps(start, end)
        #print(result["jpoints"])
       # print("explored:", len(result_JPS["explored"]))
        print("shortestPath", result["shortestPath"])
        #print("jpoints", len(result_JPS["jpoints"]))


if __name__ == '__main__':
    unittest.main()
