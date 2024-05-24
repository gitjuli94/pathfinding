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
        # Test with a simple graph
        shortest_path = self.dijkstra.find_distances((0,1), (2,1))["absoluteDistance"]
        print("polku:",shortest_path)
        self.assertEqual(shortest_path, (2.0))
