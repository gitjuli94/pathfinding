from math import sqrt, inf
from heapq import heappush, heappop


import sys
from pathlib import Path
src_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(src_dir))

class JPS:

    def __init__(self, map):
        self._map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.sqrt2 = sqrt(2)

    def heuristic_octile(self, start, end):
        """
        calculates the heuristic octile distance from the jump point to the goal node
        """

        row_diff = abs(start[0] - end[0]) # y
        col_diff = abs(start[1] - end[1]) # x
        heuristic = min(row_diff, col_diff) * self.sqrt2 \
        + max(row_diff, col_diff) - min(row_diff, col_diff)

        return heuristic

    def prune_straight(self, current_pos, move):
        """
        Straight pruning rules to determine whether a node should be generated or skipped
        """
        node = list(current_pos)
        distance = self.distances[node[0]][node[1]]
        #print("node", node)

        while True:
            # update the coordinates
            node[0] += move[0]
            node[1] += move[1]
            distance += 1
            #print(distance)
            #print(node[0],node[1])

            if (node[0] >= self.rows or node[1] >= self.cols or
                    node[0] < 0 or node[1] < 0 or
                    self._map[node[0]][node[1]] == 1):
                # if unreachable node (outside matrix or is an obstacle)
                # --> skip the node (prune)

                return None

            if (self.distances[node[0]][node[1]] != inf and
                distance > self.distances[node[0]][node[1]]):
                # if a distance has already been processed
                # and the new distance is bigger than the previous calculation
                # --> skip the node (prune)
                #print("tää", node[0],node[1]) #täällä!
                return None

            # update the parent nodes distance
            self._parents[node[0]][node[1]] = (node[0] - move[0], node[1] - move[1])

            self.distances[node[0]][node[1]] = distance

            if tuple(node) == self._end: # if the end node is reached, skip pruning and return
                return node

            """# Allow diagonal movement past obstacles
            if move[0] != 0 and move[1] != 0:
                if self._map[node[0] - move[0]][node[1]] == 1 or self._map[node[0]][node[1] - move[1]] == 1:
                    return node"""
            # pruning horizontally, look for forced neighbors
            # (forced neighbors = nodes that must be considered due to the presence of obstacles)
        #else:
            if move[0] == 0:
                if (((node[0] + 1) < self.rows) and
                        (node[1] - move[1] >= 0) and
                        (node[1] - move[1] < self.cols)):
                    if (self._map[node[0]+1][node[1]-move[1]] == 1): # presence of obstacle, down
                        #print("obstacle below, go horizontal", node)
                        return node

                if ((node[0] - 1 >= 0) and
                        (node[1] - move[1] >= 0) and
                        (node[1] - move[1] < self.cols)):
                    if (self._map[node[0]-1][node[1]-move[1]] == 1): # presence of obstacle, up
                        #print("obstacle above, go horizontal", node)
                        #print(node[0]-1,node[1]-move[1])
                        return node

            # pruning vertically, look for forced neighbors
            # (forced neighbors = nodes that must be considered due to the presence of obstacles)
            else:
                if ((node[1] + 1) < self.cols and
                        (node[0] - move[0] >= 0) and
                        (node[0] - move[0] < self.rows)):
                    if (self._map[node[0]-move[0]][node[1]+1] == 1): # presence of obstacle, right
                        #print("obstacle right, go vertical", node)
                        return node

                if ((node[1] - 1 >= 0) and
                        (node[0] - move[0] >= 0) and
                        (node[0] - move[0] < self.rows)):
                    if (self._map[node[0]-move[0]][node[1]-1] == 1): # presence of obstacle, left
                        #print("obstacle right, go vertical", node)
                        return node



    def prune_diagonal(self, current_pos, move):
        """
        Diagonal pruning rules to determine whether a node should be generated or skipped
        """
        node = list(current_pos)
        distance = self.distances[node[0]][node[1]]

        while True:
            # update the coordinates
            node[0] += move[0]
            node[1] += move[1]
            distance += self.sqrt2 # diagonal movement weight

            if (node[0] >= self.rows or node[1] >= self.cols or
                    node[0] < 0 or node[1] < 0 or
                    self._map[node[0]][node[1]] == 1):
                # if unreachable node (outside matrix or is an obstacle)
                # --> skip the node (prune)
                return None

            if (self._map[node[0]-move[0]][node[1]] == 1 or
                    self._map[node[0]][node[1]-move[1]] == 1):
                # if move leads into an obstacle horizontally or vertically
                # --> force going around corners orthogonally and not diagonally
                return None

            if (self.distances[node[0]][node[1]] != inf and
                    distance > self.distances[node[0]][node[1]]):
                # if a distance has already been processed
                # and the new distance is bigger than the previous calculation
                # --> skip the node (prune)
                return None

            # update the parent nodes distance
            self._parents[node[0]][node[1]] = (node[0] - move[0], node[1] - move[1])

            self.distances[node[0]][node[1]] = distance

            if tuple(node) == self._end: # if the end node is reached, skip pruning and return
                return node


            if self.prune_straight(node, (0, move[1])):  # diagonal pruning, horizontal component
                    #print("node", node)

                    return node
            if self.prune_straight(node, (move[0], 0)):  # diagonal pruning, horizontal component
                    #print("node", node)
                    return node

    def jump_point_search(self, start, end):
        """
        Run the jump point search
        """
        visited = []
        #visited = {}
        self._end = end

        minheap = [] # binary minheap structure for priority queueing nodes

        # push the start node in the minheap, with its heuristic distance
        heappush(minheap, (self.heuristic_octile(start, end), start[0], start[1]))

        # initialize the parent nodes as None
        self._parents = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # initialize the distances as infinity
        self.distances = [[inf for _ in range(self.cols)] for _ in range(self.rows)]

        # mark start nodes distance as 0
        self.distances[start[0]][start[1]] = 0

        straight_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # (y, x)
        diagonal_moves = [(-1, -1), (1, 1), (1, -1), (-1, 1)] # (y, x)

        #visited[start] = None
        #current_pos = start

        while minheap:
            node = heappop(minheap)
            #print((node[1], node[2]))
            #visited[(node[1], node[2])] = current_pos

            if self.distances[end[0]][end[1]] != inf: # when end node is reached
            #if (node[1],node[2]) == end:
                path = self.reconstruct_path(end, start, [end]) # construct path, initialize with goal vertex
                """visited[tuple(end)] = current_pos
                jpoints = []
                print("path", path)
                print("visited", visited)
                jpoint_vertex = end#(node[1], node[2])#current_pos
                # Constructs the rest of the jps path
                path_dict = {t: None for t in path}

                while jpoint_vertex is not None:
                    # The coords is added to the 'jpoints'.
                    if jpoint_vertex in path_dict:
                        jpoints.append(jpoint_vertex)
                        jpoint_vertex = visited[jpoint_vertex]

                jpoints.reverse()"""

                return {
                    "absoluteDistance": self.distances[end[0]][end[1]],
                    "path": path[::-1],
                    "visited": visited
                    #"jpoints": "jpoints"
                }

            current_pos = (node[1], node[2]) # tuple representing the node with smallest heuristic value



            for move in straight_moves:
                # check if straight move possible (not None)
                if pos := self.prune_straight(current_pos, move):
                    f_score = self.distances[pos[0]][pos[1]] + self.heuristic_octile(pos, end)
                    visited.append((pos[0],pos[1]))
                    # add to priority queue
                    heappush(minheap, (f_score, pos[0], pos[1])) # add to priority queue

            for move in diagonal_moves:
                # check if diagonal move possible (not None)
                if pos := self.prune_diagonal(current_pos, move):
                    # update the estimated travel cost with current distance + heuristic estimation until goal
                    f_score = self.distances[pos[0]][pos[1]] + self.heuristic_octile(pos, end)
                    visited.append((pos[0],pos[1]))
                    # add to priority queue
                    heappush(minheap, (f_score, pos[0], pos[1]))




        return False
        #return -1, [], []


    def reconstruct_path(self, end, start, path):
        """
        Construct path for the shortest route, starting from the end node
        """

        while start != end:
            path.append(self._parents[end[0]][end[1]])
            end = self._parents[end[0]][end[1]]

        return path
"""from data.maps.simple1 import input_matrix as simple1
from data.maps.paris import input_matrix as paris
from data.maps.newyork import input_matrix as newyork
from data.maps.moscow import input_matrix as moscow
from data.maps.shanghai import input_matrix as shanghai

import time
#start = (4, 1)
#end = (11, 4)

#vastaus 12,07
matrix = [
[0,0,1,0,0,0,0,0,0],
[0,0,1,0,1,0,0,0,0],
[0,0,1,0,1,0,1,0,0],
[0,0,0,0,1,0,1,0,0],
[0,0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0]
]

start = (1, 8)
end = (0, 0)

matrix = [
[0,0,0,0,0,0,0,0],
[0,0,0,0,1,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0]
]

start = (1, 5)
end = (1, 1)

#NewYork_2_256.map 17	209	253	40	344.58787842 (x,y)
start = (209, 17) # (y,x)
end = (40,253)

map = newyork

jps = JPS(map)

#start = (149, 4) #kokeily, yli 3s laskentaaika, shanghai
#end = (55, 153)


#measure path finding time
start_time = time.time()
result = jps.jump_point_search(start, end)
end_time = time.time()
print("time: ", end_time-start_time)

if result["absoluteDistance"] == -1:
    print("No path found.")
else:
    print(f"Distance of the shortest path: {result["absoluteDistance"]}")
    #print(f"Path from start to end: {result["path"]}")
    #print(f"Visited nodes: {result["visited"]}")
   # print(f"Visited nodes: {len(result["visited"])}")
  #  print(f"Visited nodes, set: {len(set(result["visited"]))}")
    #print(f"jpoints: {result["jpoints"]}")"""

