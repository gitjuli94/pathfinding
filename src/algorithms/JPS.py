"""
Jump point search algorithm for shortest path finding.
"""

from math import sqrt, inf
from heapq import heappush, heappop

class JPS:

    def __init__(self, matrix):
        self._map = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.sqrt2 = sqrt(2)
        self._end = None
        self._parents = None
        self.distances = None

    def heuristic_octile(self, start, end):
        """
        Calculates the heuristic octile distance from the jump point to the goal node
        """

        row_diff = abs(start[0] - end[0]) # y
        col_diff = abs(start[1] - end[1]) # x
        heuristic = min(row_diff, col_diff) * self.sqrt2 \
        + max(row_diff, col_diff) - min(row_diff, col_diff)

        return heuristic

    def _prune(self, current_pos, move):
        """
        Pruning rules to determine whether a node should be considered or skipped.
        """
        node = list(current_pos)
        distance = self.distances[node[0]][node[1]]
        diagonal = move[0] != 0 and move[1] != 0  # check whether moving diagonally

        while True:
            # update the coordinates
            node[0] += move[0]
            node[1] += move[1]
            distance += self.sqrt2 if diagonal else 1

            if self._is_unreachable(node):
                return None

            if diagonal:
                if self._is_diagonal_obstacle(node, move, distance):
                    return None
            else:
                if self._is_processed(node, distance):
                    return None

            self._update_parent_distance(node, move, distance)

            # if the end node is reached, skip pruning and return
            if tuple(node) == self._end:
                return node

            if self._has_forced_neighbors(node, move, diagonal):
                return node

    def _is_unreachable(self, node):
        # if unreachable node (outside matrix or is an obstacle)
        return (node[0] >= self.rows or node[1] >= self.cols or
                node[0] < 0 or node[1] < 0 or
                self._map[node[0]][node[1]] == 1)
                # --> skip the node (prune)

    def _is_diagonal_obstacle(self, node, move, distance):
                # if move leads into an obstacle horizontally or vertically
                # this forces going around corners orthogonally and not diagonally
        return (self._map[node[0] - move[0]][node[1]] == 1 or
                self._map[node[0]][node[1] - move[1]] == 1 or
                # if a distance has already been processed
                self.distances[node[0]][node[1]] != float('inf') and
                # and the new distance is bigger than the previous calculation
                # this >= is important when processing diagonal direction!
                distance >= self.distances[node[0]][node[1]])
                # --> skip the node (prune)

    def _is_processed(self, node, distance):
                # if a distance has already been processed
        return (self.distances[node[0]][node[1]] != float('inf') and
                # and the new distance is bigger than the previous calculation
                distance > self.distances[node[0]][node[1]])
                # --> skip the node (prune)

    def _update_parent_distance(self, node, move, distance):
        # update the parent nodes distance
        self._parents[node[0]][node[1]] = (node[0] - move[0], node[1] - move[1])
        self.distances[node[0]][node[1]] = distance

    def _has_forced_neighbors(self, node, move, diagonal):
        # look for forced neighbors
        # = nodes that must be considered due to the presence of obstacles
        if diagonal:
             # check in both components of diagonal movement
            return (self._prune(node, (0, move[1])) or self._prune(node, (move[0], 0)))
        return (self._has_horizontal_forced_neighbors(node, move) or
                self._has_vertical_forced_neighbors(node, move))

    def _has_vertical_forced_neighbors(self, node, move):
        if move[0] == 0:  # searching horizontally
            if (node[0] + 1 < self.rows and
                node[1] - move[1] >= 0 and
                node[1] - move[1] < self.cols and
                self._map[node[0] + 1][node[1] - move[1]] == 1):
                # presence of obstacle, down
                return True
            if (node[0] - 1 >= 0 and
                node[1] - move[1] >= 0 and
                node[1] - move[1] < self.cols and
                self._map[node[0] - 1][node[1] - move[1]] == 1):
                # presence of obstacle, up
                return True
        return False

    def _has_horizontal_forced_neighbors(self, node, move):
        if move[1] == 0:  # searching vertically
            if (node[1] + 1 < self.cols and
                node[0] - move[0] >= 0 and
                node[0] - move[0] < self.rows and
                self._map[node[0] - move[0]][node[1] + 1] == 1):
                # presence of obstacle, right
                return True
            if (node[1] - 1 >= 0 and
                node[0] - move[0] >= 0 and
                node[0] - move[0] < self.rows and
                self._map[node[0] - move[0]][node[1] - 1] == 1):
                # presence of obstacle, left
                return True
        return False


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

        while minheap:
            node = heappop(minheap)

            if (node[1],node[2]) == end: # when end node is reached
                # construct path, initialize with goal vertex
                path = self.reconstruct_path(end, start, [end])
                return {
                    "absoluteDistance": self.distances[end[0]][end[1]],
                    "path": path[::-1],
                    "visited": visited
                }

            # tuple representing the node with smallest heuristic value
            current_pos = (node[1], node[2])

            for move in straight_moves + diagonal_moves:
                # check if a move possible (not None)
                if pos := self._prune(current_pos, move):
                    f_score = self.distances[pos[0]][pos[1]] + self.heuristic_octile(pos, end)
                    visited.append((pos[0],pos[1]))
                    # add to priority queue
                    heappush(minheap, (f_score, pos[0], pos[1])) # add to priority queue

        return False


    def reconstruct_path(self, end, start, path):
        """
        Construct path for the shortest route, starting from the end node
        """

        while start != end:
            path.append(self._parents[end[0]][end[1]])
            end = self._parents[end[0]][end[1]]

        return path
