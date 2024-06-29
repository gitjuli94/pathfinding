"""
Integration testing for the JPS and Dijkstra algorithms.
"""
import unittest
import sys
from pathlib import Path
import time
import random

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.JPS import JPS
from algorithms.dijkstra import Dijkstra
from data.maps.simple1 import input_matrix as matrix1
from data.maps.newyork import input_matrix as newyork

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass
        # Initialize the algorithms with a test matrix
        #self.test_matrix = matrix1
       # self.jps = JPS(self.test_matrix)
       # self.dijkstra = Dijkstra(self.test_matrix)

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
                self.assertEqual(str(result_JPS["shortestPath"]), str(route_dijkstra))

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
        # route: 0,2 -> 0,4 -> 1,5
        expected_jpoints = [(1, 1), (2, 2), (2, 4), (1, 5)]
        print("expected:", expected_jpoints)
        jps = JPS(test_matrix)
        result = jps.jps(start, end)
     #   print("explored:", result["explored"])
        print("shortestPath", result["shortestPath"])
      #  print("absoluteDistance", result["absoluteDistance"])
      #  print("jpoints", sorted(result["jpoints"]))

    def test_jump_points_within_the_route_2(self):
        # Test if the jump points are correctly found
        # example case from https://blog.finxter.com/jump-search-algorithm-in-python-a-helpful-guide-with-video/

        test_matrix = [
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        start = (0,0)
        end = (1,8)
        # route: 0,2 -> 0,4 -> 1,5
        expected_jpoints = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (4, 4), (3, 5), (2, 5), (1, 6), (1, 8)]
        print("expected:", expected_jpoints)
        jps = JPS(test_matrix)
        result = jps.jps(start, end)

        print("shortestPath", result["shortestPath"])"""

    def test_jump_points_within_the_route_x(self):

        matrix = newyork

        y=len(matrix) #rows
        x=len(matrix[0]) #cols

        free_space=[]

        # choose points from the free area within the map
        for i in range(y):
            for j in range(x):
                if matrix[i][j] == 0:
                    free_space.append((i,j))


        dijkstra = Dijkstra(matrix)
        jps = JPS(matrix)

        # test both algorithms with 10 random start and end vertices
        for i in range(10):
            start = random.choice(free_space)
            end = random.choice(free_space)

            result_Dijkstra = dijkstra.find_distances(start, end)
            rounded_Dijkstra = round(result_Dijkstra["absoluteDistance"])/2
            #print("D: ", round(result_Dijkstra["absoluteDistance"])/2)
            result_JPS = jps.jump_point_search(start, end)
            #print("JPS: ", round(result_JPS["absoluteDistance"])/2)
            rounded_JPS = round(result_JPS["absoluteDistance"])/2

            self.assertEqual(rounded_Dijkstra, rounded_JPS)

            #print("JPS:", result_JPS["absolute_distance"])
            #print("dijkstra:", result_Dijkstra["absoluteDistance"])"""

    """def test_both_random_route(self):
        matrix = milan
        start = (41, 75)
        end = (32, 10)
        dijkstra = Dijkstra(matrix)
        result_Dijkstra = dijkstra.find_distances(start, end)

        neighbor_list, start_position, end_position, cols, field_status = \
            JPS.initialize_graph(matrix, start, end)

        result_JPS = JPS.jump_point_search(neighbor_list, start_position, end_position, cols, field_status)
        self.assertEqual(result_JPS["absolute_distance"], result_Dijkstra["absoluteDistance"])
        #print("expeted:97,5")
       # print("jps:", result_JPS["absolute_distance"]) """


if __name__ == '__main__':
    unittest.main()
