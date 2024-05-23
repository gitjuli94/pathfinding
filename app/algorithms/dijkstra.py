"""
Dijkstra algorithm for shortest path finding.
"""

import heapq
import sys
import os

"""get the map matrices from a separate directory"""
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from network import Generate_Network
from maps.milan import input_matrix

class Dijkstra:
    def __init__(self, matrix):
        network = Generate_Network(matrix)
        self.nodes = network.graph.keys()
        self.graph = network.graph
        #print(self.graph)
        #print(self.nodes)

    def find_distances(self, start_node, end_node):
        result = True
        distances = {}
        for node in self.nodes:
            distances[node] = float("inf")
        distances[start_node] = 0
        #print(distances)
        came_from = {}  # Dictionary to store predecessors
        queue = []
        heapq.heappush(queue, (0, start_node))

        visited = set()
        if end_node not in self.nodes or start_node not in self.nodes:
            result = False
            return result

        while queue:
            node_a = heapq.heappop(queue)[1]
            if node_a == end_node:
                return {
                    "shortestPath": reconstruct_path(came_from, end_node),
                    "visited": visited,
                    "absoluteDistance": round(distances[end_node] + 1e-9, 1)  # Using round to handle floating point precision issues
                }
            if node_a in visited:
                continue
            visited.add(node_a)

            for node_b, weight in self.graph[node_a]:
                new_distance = distances[node_a] + weight
                if new_distance < distances[node_b]:
                    distances[node_b] = new_distance
                    new_pair = (new_distance, node_b)
                    heapq.heappush(queue, new_pair)
                    came_from[node_b] = node_a  # Update predecessor

        if distances[end_node] == float("inf"):
            return -1

        #return distances
        #return distances[end_node]#, came_from

def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.insert(0, current)

    return path

# Example usage
dijkstra = Dijkstra(input_matrix)
start_node = (0, 0)
end_node = (7, 0)
result = dijkstra.find_distances(start_node, end_node)

if result:
    shortest_path = result["shortestPath"]
    absolute_distance = result["absoluteDistance"]
    print("Shortest path:", shortest_path)
    print("Absolute Distance:", absolute_distance)
else:
    print("No path found.")
