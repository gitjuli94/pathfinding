from math import sqrt, inf
from heapq import heappush, heappop
from paris import input_matrix as paris
from newyork import input_matrix as newyork
from simple1 import input_matrix as simple1


class JPS:

    def __init__(self, map):
        self._map = map
        self.rows = len(map)
        self.cols = len(map[0])

    def heuristic_octile(self, start, end):
        """
        calculates the heuristic octile distance from the jump point to the goal node
        """

        row_diff = start[0] - end[0] # y
        col_diff = start[1] - end[1] # x
        heuristic = min(abs(row_diff), abs(col_diff)) * sqrt(2) \
        + max(abs(row_diff), abs(col_diff)) - min(abs(row_diff), abs(col_diff))

        return heuristic

    def prune_straight(self, current_pos, move):
        """
        Straight pruning rules to determine whether a node should be generated or skipped
        """
        node = list(current_pos)
        distance = self.distances[node[0]][node[1]]

        while True:
            # update the coordinates
            node[0] += move[0]
            node[1] += move[1]
            distance += 1

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
                return None

            # update the parent nodes distance
            self._parents[node[0]][node[1]] = (node[0] - move[0], node[1] - move[1])

            self.distances[node[0]][node[1]] = distance

            if tuple(node) == self._end: # if the end node is reached, skip pruning and return
                return node

            # pruning horizontally, look for forced neighbors
            # (forced neighbors = nodes that must be considered due to the presence of obstacles)
            if move[0] == 0:
                if (((node[0] + 1) < self.rows) and
                    (node[1] - move[1] >= 0) and
                        (node[1] - move[1] < self.cols)):
                    if (self._map[node[0]+1][node[1]-move[1]] == 1): # presence of obstacle, down
                        print("alapuolella, mennään vaakaan", node)
                        return node

                if ((node[0] - 1 >= 0) and
                        (node[1] - move[1] >= 0) and
                        (node[1] - move[1] < self.cols)):
                    if (self._map[node[0]-1][node[1]-move[1]] == 1): # presence of obstacle, up
                        print("yläpuolella, mennään vaakaan", node)
                        return node

            # pruning vertically, look for forced neighbors
            # (forced neighbors = nodes that must be considered due to the presence of obstacles)
            else:
                if ((node[1] + 1) < self.cols and
                        (node[0] - move[0] >= 0) and
                        (node[0] - move[0] < self.rows)):
                    if (self._map[node[0]-move[0]][node[1]+1] == 1): # presence of obstacle, right
                        print("oikealla, mennään pystysuuntaan", node)
                        return node

                if ((node[1] - 1 >= 0) and
                        (node[0] - move[0] >= 0) and
                        (node[0] - move[0] < self.rows)):
                    if (self._map[node[0]-move[0]][node[1]-1] == 1): # presence of obstacle, left
                        print("vasemmalla, mennään pystysuuntaan", node)
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
            distance += sqrt(2) # diagonal movement weight
            if (node[0] >= self.rows or node[1] >= self.cols or
                    node[0] < 0 or node[1] < 0 or
                    self._map[node[0]][node[1]] == 1):
                # if unreachable node (outside matrix or is an obstacle)
                # --> skip the node (prune)
                return None

            if (self._map[node[0]-move[0]][node[1]] == 1 or
                    self._map[node[0]][node[1]-move[1]] == 1):
                # if move leads into an obstacle horizontally or vertically
                # (have been pruned already in prune_straight)
                return None

            if (self.distances[node[0]][node[1]] != inf and
                    distance >= self.distances[node[0]][node[1]]):
                # if a distance has already been processed
                # and the new distance is bigger than the previous calculation
                # --> skip the node (prune)
                return None

            # update the parent nodes distance
            self._parents[node[0]][node[1]] = (node[0] - move[0], node[1] - move[1])

            self.distances[node[0]][node[1]] = distance

            if tuple(node) == self._end: # if the end node is reached, skip pruning and return
                return node
            # diagonal_moves = [(-1, -1), (1, 1), (1, -1), (-1, 1)] # (y, x)

            if self.prune_straight(node, (move[0], 0)): # diagonal pruning, vertical component
                return node
            if self.prune_straight(node, (0, move[1])):  # diagonal pruning, horizontal component
                return node

    def jump_point_search(self, start, end):
        """
        Run the jump point search
        """
        visited = []
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

        while minheap:
            node = heappop(minheap)

            if self.distances[end[0]][end[1]] != inf: # when end node is reached
                path = self.reconstruct_path(end, start, [end]) # construct path, initialize with goal vertex

                for x, row in enumerate(self.distances):
                    for y, val in enumerate(row):
                        if val != inf:
                            visited.append((x, y)) # append if visited during the execution

                return self.distances[end[0]][end[1]], path, visited

            current_pos = (node[1], node[2]) # tuple representing the node with smallest heuristic value

            for move in straight_moves:
                # check if straight move possible (not None)
                if pos := self.prune_straight(current_pos, move):
                    f_score = self.distances[pos[0]][pos[1]] + self.heuristic_octile(pos, end)
                    # add to priority queue
                    heappush(minheap, (f_score, pos[0], pos[1])) # add to priority queue

            for move in diagonal_moves:
                # check if diagonal move possible (not None)
                if pos := self.prune_diagonal(current_pos, move):
                    # update the estimated travel cost with current distance + heuristic estimation until goal
                    f_score = self.distances[pos[0]][pos[1]] + self.heuristic_octile(pos, end)
                    # add to priority queue
                    heappush(minheap, (f_score, pos[0], pos[1]))

        return -1, [], []

    def reconstruct_path(self, end, start, path):
        """
        Construct path for the shortest route, starting from the end node
        """

        while start != end:
            path.append(self._parents[end[0]][end[1]])
            end = self._parents[end[0]][end[1]]

        return path

start = (0, 1)
end = (6, 3)

# paris: 239	253	7	10	389.47518005

#start = (253, 239)
#end = (10, 7)

map = simple1

#new york:  38	15	237	195	292.30360718
#start = (15, 38)
#end = (195, 237)
#new york:  239	30	11	228	345.58787842
#start = (30, 239)
#end = (228, 11)

jps = JPS(map)
distance, path, visited = jps.jump_point_search(start, end)

if distance == -1:
    print("No path found.")
else:
    print(f"Distance of the shortest path: {distance}")
    #print(f"Path from start to end: {path[::-1]}")
    #print(f"Total time taken: {total_time:.6f} seconds")
    #print(f"Visited nodes: {visited}")
