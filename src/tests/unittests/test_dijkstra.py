"""
Unit testing for Dijkstra algorithm.
"""
import unittest
import sys
from pathlib import Path

"""get the tested algorithm from a separate directory"""
base_dir = Path(__file__).resolve().parent.parent.parent
src_dir = base_dir / 'algorithms'
sys.path.append(str(src_dir))
#print(src_dir)
from dijkstra import Dijkstra

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        # Initialize the Dijkstra with a test graph
        self.test_matrix = [
                        [1, 0, 1],
                        [1, 0, 1],
                        [1, 0, 1],
                        [1, 1, 1]
                    ]
        self.dijkstra = Dijkstra(self.test_matrix)

    def test_shortest_path_simple_graph(self):
        # Test shortest distance with the test graph
        result = self.dijkstra.find_distances((0,1), (2,1))
        #print("polku:",shortest_path)
        self.assertEqual(result["absoluteDistance"], (2.0))
        self.assertEqual(result["shortestPath"], [(0, 1), (1, 1), (2, 1)])

    def test_no_path(self):
        # Test no path with the test graph
        result = self.dijkstra.find_distances((0,1), (3,1))
        #print("result:",result)
        self.assertEqual(result, False)

    def test_invalid_nodes(self):
        # Test when the nodes are not within the graph
        result = self.dijkstra.find_distances((0,1), (4,1))
        #print("result:",result)
        self.assertEqual(result, False)
        result = self.dijkstra.find_distances((4,1), (3,1))
        #self.assertEqual(result, (-1))
        self.assertFalse(result)

    def test_reconstruct_path(self):
        # Test the path reconstruction function
        came_from = {(1, 1): (0, 0), (2, 2): (1, 1)}
        current = (2, 2)
        expected_path = [(0, 0), (1, 1), (2, 2)]
        self.assertEqual(self.dijkstra.reconstruct_path(came_from, current), expected_path)

if __name__ == '__main__':
    unittest.main()
