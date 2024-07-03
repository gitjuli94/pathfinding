"""
Dijkstra algorithm for shortest path finding.
references:
https://tira.mooc.fi/kevat-2024/osa14/
"""

########

# only when testing the algorithm, remove/comment away when usin the main.py module:
import sys
from pathlib import Path
src_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(src_dir))
#########

from math import inf
import heapq
from algorithms.network import Generate_Network

class Dijkstra:
    def __init__(self, matrix):
        network = Generate_Network(matrix)
        self.nodes = network.graph.keys()
        self.graph = network.graph

    def find_distances(self, start_node, end_node):
        #routes = [] # list of different routes with same distance
        distances = {}
        for node in self.nodes:
            distances[node] = inf
        distances[start_node] = 0
        #print(distances)
        #came_from = {node: [] for node in self.nodes}   # Dictionary to store all predecessors in a list (for all routes)
        came_from = {}

        queue = []
        heapq.heappush(queue, (0, start_node))
        visited = set()
        if end_node not in self.graph or start_node not in self.graph:
            #print("Check that start and end nodes are correctly specified.")
            return False

        while queue:
            #choose 2nd (=[1]) item from the tuple (which is the node itself):
            #with a heap structure the first in the queue is always the one with the smallest distance
            #because the heap structure is saved as a tuple : (distance, node)
            node_a = heapq.heappop(queue)[1]
            #print(node_a, distances[node_a])
            if node_a == end_node:

                return {
                    "cameFrom": came_from, #return dictionary of predecessor nodes
                    "shortestPath": self.reconstruct_path(came_from, end_node), # for visualizing the first found path
                    #"shortestPath": sorted(routes)[0], # for visualizing the first found path
                    #"Routes": routes, # list of shortest paths found
                    "visited": visited,
                    #using round to handle floating point precision issues
                    #"absoluteDistance": round(distances[end_node] + 1e-9, 1) #-> unnecessary?
                    "absoluteDistance": distances[end_node]
                }
            if node_a in visited:
                continue
            visited.add(node_a)

            for node_b, weight in self.graph[node_a]:#go through all node a's neighbors and distances
                new_distance = distances[node_a] + weight #calculate new distance
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

        #if distances[end_node] == inf:
        return False

    """def reconstruct_paths(self, came_from, current):
        # reconstruct multiple paths (not used in this project)
        if not came_from[current]: # base case for recursion
            return [[current]] # if no predeccors, only returns the current node (start node)
        paths = []
        for prev in came_from[current]: # recursive function to find all the paths
            for path in self.reconstruct_paths(came_from, prev):
                paths.append(path + [current])
        #print("paths: ", paths)
        return paths"""

    def reconstruct_path(self, came_from, current):
        #for a single path
        path = [current]

        while current in came_from:
            current = came_from[current]
            path.insert(0, current)

        return path


"""from data.maps.paris import input_matrix as paris
from data.maps.simple1 import input_matrix as simple1
from data.maps.newyork import input_matrix as newyork
from data.maps.shanghai import input_matrix as shanghai
import time




matrix = [
[0,0,1,0,0,0,0,0,0],
[0,0,1,0,1,0,0,0,0],
[0,0,1,0,1,0,1,0,0],
[0,0,0,0,1,0,1,0,0],
[0,0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0]
]
start = (0, 0)
end = (1, 8)

matrix = [
[0,0,0,0,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0]
]
end = (1, 5)
start = (1, 1)

#NewYork_2_256.map 17	209	253	40	344.58787842 (x,y)
start = (209, 17) # (y,x)
end = (40,253)
start, end = (234, 242), (18,6)

#start = (149, 4) #kokeily, yli 3s laskentaaika, shanghai
#end = (55, 153)
dijkstra = Dijkstra(paris)

#paris 29	9	253	253	388.61731567
start, end = (9,29), (253,253)
print(start)



#measure path finding time
start_time = time.time()
result = dijkstra.find_distances(start, end)
end_time = time.time()
print("time: ", end_time-start_time)
print(result["absoluteDistance"])"""
