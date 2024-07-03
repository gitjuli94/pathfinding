"""
Dijkstra algorithm for shortest path finding.
references:
https://tira.mooc.fi/kevat-2024/osa14/
"""

from math import inf
import heapq
from algorithms.network import GenerateNetwork

class Dijkstra:
    def __init__(self, matrix):
        network = GenerateNetwork(matrix)
        self.nodes = network.graph.keys()
        self.graph = network.graph

    def find_distances(self, start_node, end_node):

        distances = {}
        for node in self.nodes:
            distances[node] = inf
        distances[start_node] = 0
        came_from = {}

        queue = []
        heapq.heappush(queue, (0, start_node))
        visited = set()

        if end_node not in self.graph or start_node not in self.graph:
            return False

        while queue:
            node_a = heapq.heappop(queue)[1]
            if node_a == end_node:

                return {
                    "shortestPath": self.reconstruct_path(came_from, end_node),
                    "visited": visited,
                    "cameFrom": came_from,
                    "absoluteDistance": distances[end_node]
                }
            if node_a in visited:
                continue
            visited.add(node_a)

            # go through all node a's neighbors and distances
            for node_b, weight in self.graph[node_a]:
                new_distance = distances[node_a] + weight
                if new_distance < distances[node_b]:
                    distances[node_b] = new_distance
                    new_pair = (new_distance, node_b)
                    heapq.heappush(queue, new_pair)
                    # update predecessor
                    came_from[node_b] = node_a
        return False

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)

        return path
