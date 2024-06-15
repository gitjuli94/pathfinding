"""
Dijkstra algorithm for shortest path finding.
sources:
https://tira.mooc.fi/kevat-2024/osa14/
"""

########

# only when testing the algorithm, remove/comment away when usin the main.py module:
import sys
from pathlib import Path
src_dir = Path(__file__).resolve().parent.parent
print("tää", src_dir)
sys.path.append(str(src_dir))
#########


import heapq
from algorithms.network import Generate_Network

class Dijkstra:
    def __init__(self, matrix):
        network = Generate_Network(matrix)
        self.nodes = network.graph.keys()
        self.graph = network.graph
       # print(self.graph)
       # print(self.nodes)

    def find_distances(self, start_node, end_node):
        routes = [] # list of different routes with same distance
        distances = {}
        for node in self.nodes:
            distances[node] = float("inf")
        distances[start_node] = 0
        #print(distances)
        #came_from = {node: [] for node in self.nodes}   # Dictionary to store all predecessors in a list (for all routes)
        came_from = {}

        queue = []
        heapq.heappush(queue, (0, start_node))
        visited = set()
        if end_node not in self.graph or start_node not in self.graph:
            print("Check that start and end nodes are correctly specified.")
            return False

        while queue:
            #choose 2nd (=[1]) item from the tuple (which is the node itself):
            #with a heap structure the first in the queue is always the one with the smallest distance
            #because the heap structure is saved as a tuple : (distance, node)
            node_a = heapq.heappop(queue)[1]
            if node_a == end_node:
                #routes.extend(self.reconstruct_paths(came_from, end_node)) # Add all routes to a list

                #print("n of routes: ", len(routes))
                #print("routes: ", routes)
                #print("from: ", came_from)
                #print("route1: ", sorted(routes)[0])

                return {
                    "cameFrom": came_from, #return dictionary of predecessor nodes
                    "shortestPath": self.reconstruct_path(came_from, end_node), # for visualizing the first found path
                    #"shortestPath": sorted(routes)[0], # for visualizing the first found path
                    #"Routes": routes, # list of shortest paths found
                    "visited": visited,
                    #using round to handle floating point precision issues
                    #"absoluteDistance": round(distances[end_node] + 1e-9, 1) -> unnecessary?
                    "absoluteDistance": round(distances[end_node], 1)
                }
            if node_a in visited:
                continue
            visited.add(node_a)

            for node_b, weight in self.graph[node_a]:#go through all node a's neighbors and distances
                new_distance = distances[node_a] + weight#calculate new distance
                if new_distance < distances[node_b]:
                    distances[node_b] = new_distance
                    new_pair = (new_distance, node_b)
                    heapq.heappush(queue, new_pair)
                    came_from[node_b] = node_a  # Update predecessor

                ### modify for multiple path saving:
                    #came_from[node_b].append(node_a)
                #elif new_distance == distances[node_b]: # If a route with same distance is found
                    #came_from[node_b].append(node_a)
                ###

        if distances[end_node] == float("inf"):
            return False

    def reconstruct_paths(self, came_from, current):
        # reconstruct multiple paths
        if not came_from[current]: # base case for recursion
            return [[current]] # if no predeccors, only returns the current node (start node)
        paths = []
        for prev in came_from[current]: # recursive function to find all the paths
            for path in self.reconstruct_paths(came_from, prev):
                paths.append(path + [current])
        #print("paths: ", paths)
        return paths

    def reconstruct_path(self, came_from, current):
        #for a single path
        path = [current]

        while current in came_from:
            current = came_from[current]
            path.insert(0, current)

        return path



from data.maps.newyork_test import input_matrix
import time

dijkstra = Dijkstra(input_matrix)
start = (16, 31)
end = (46, 74)

#measure path finding time
start_time = time.time()
result = dijkstra.find_distances(start, end)
end_time = time.time()

print(result["absoluteDistance"])
