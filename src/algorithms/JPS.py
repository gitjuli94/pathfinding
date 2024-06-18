"""
Jump point search algorithm for shortest path finding.
sources:
https://blog.finxter.com/jump-search-algorithm-in-python-a-helpful-guide-with-video/
"""

import math
from algorithms.graph import Graph
import heapq
from collections import namedtuple


# A dummy object with the obstable attribute
# Used as a placeholder for missing neighbors
class DummyObject:
    def __init__(self):
        self.obstacle = True



class JPS:
    def __init__(self, input_matrix):
        # Initializes an empty self.graph (object).
        # Creating a self.graph from the input matrix
        self.graph = Graph(input_matrix)
        #self.graph.create_graph()
                # construct the 'vertices' dictionary

        #print(self.graph.vertices.coords)


        self.vertices = {k.coords: k for k in self.graph.vertices()}

    def prune(self, vertex, direction=None):
        # identify which neighbors of a given vertex should be considered for further exploration
        neighbours = {}
        forced_neighbours_exist = False # in the start node, no forced neighbors

        if direction is None:
            direction = vertex.direction

        # enables us to return both the neighbouring vertices and the
        # indicator of forced neighbours existence
        pruned = namedtuple('pruned', 'vertices forced')

        # if a direction is not present in the neighbors dictionary, return dummy,
        # an instance set as an obstacle
        dummy = DummyObject()

        # collects all the surrounding vertices in a dictionary and
        # marks them with the search direction
        for edge in self.graph.adjacent_edges(vertex):
            neighbours[edge.direction] = edge.opposite(vertex)

        # pruning to the non-starting vertices
        if direction is not None:
            # determines if the movement direction is diagonal
            is_diagonal = direction % 2

            # forced neighbors: the presence of obstacles can cause the path
            # to be rerouted around the obstacle

            # calculate directions for forced neighbors
            leftmost_dir = self.change_dir(direction, 2 + is_diagonal)
            rightmost_dir = self.change_dir(direction, -2 - is_diagonal)

            # removes the parent direction from neighbors
            neighbours.pop(self.change_dir(direction, 4), None)

            # check natural neighbours (directly reachable nodes) obstacles
            for idx in range(-is_diagonal, is_diagonal + 1):
                if neighbours.get(self.change_dir(direction, idx), dummy).obstacle:
                    neighbours.pop(self.change_dir(direction, idx), None)

            # check for forced neighbors on the left and right sides relative to the
            # current movement direction

            # check forced neighbours (left)
            # (forced neighbors are those that must be considered due to the presence of obstacles)
            if neighbours.get(self.change_dir(leftmost_dir, -1), dummy).obstacle or not neighbours.get(leftmost_dir, dummy).obstacle:
            #  ^ check if there is an obstacle at one step left                         ^ check if the leftmost direction itself does not have an obstacle
                neighbours.pop(self.change_dir(leftmost_dir, -1), None) # discards the forced neighbour candidate
            else:
              #  print("forced!")
                forced_neighbours_exist = True
            neighbours.pop(leftmost_dir, None) # remove the leftmost direction itself from neighbors as it is not a valid candidate

            # check forced neighbours (right)
            # (forced neighbors are those that must be considered due to the presence of obstacles)
            if neighbours.get(self.change_dir(rightmost_dir, 1), dummy).obstacle or not neighbours.get(rightmost_dir, dummy).obstacle:
            #  ^ check if there is an obstacle at one step right                         ^ check if the rightmost direction itself does not have an obstacle
                neighbours.pop(self.change_dir(rightmost_dir, 1), None) # discards the forced neighbour candidate
            else:
                forced_neighbours_exist = True
            neighbours.pop(rightmost_dir, None)

            # remove neighbors that would lead backwards
            neighbours.pop(self.change_dir(direction, 4 + 1), None)
            neighbours.pop(self.change_dir(direction, 4 - 1), None)

        return pruned(neighbours, forced_neighbours_exist)

    def prune_full_route_without_jumps(self, vertex, direction=None):
        # identify which neighbors of a given vertex should be considered for further exploration
        neighbours = {}
        forced_neighbours_exist = True # in the start node, no forced neighbors

        if direction is None:
            direction = vertex.direction

        # enables us to return both the neighbouring vertices and the
        # indicator of forced neighbours existence
        pruned = namedtuple('pruned', 'vertices forced')

        # if a direction is not present in the neighbors dictionary, return dummy,
        # an instance set as an obstacle
        dummy = DummyObject()

        # collects all the surrounding vertices in a dictionary and
        # marks them with the search direction
        for edge in self.graph.adjacent_edges(vertex):
            neighbours[edge.direction] = edge.opposite(vertex)

        # pruning to the non-starting vertices
        if direction is not None:
            # determines if the movement direction is diagonal
            is_diagonal = direction % 2

            # forced neighbors: the presence of obstacles can cause the path
            # to be rerouted around the obstacle

            # calculate directions for forced neighbors
            leftmost_dir = self.change_dir(direction, 2 + is_diagonal)
            rightmost_dir = self.change_dir(direction, -2 - is_diagonal)

            # removes the parent direction from neighbors
            neighbours.pop(self.change_dir(direction, 4), None)

            # check natural neighbours (directly reachable nodes) obstacles
            for idx in range(-is_diagonal, is_diagonal + 1):
                if neighbours.get(self.change_dir(direction, idx), dummy).obstacle:
                    neighbours.pop(self.change_dir(direction, idx), None)

            # check for forced neighbors on the left and right sides relative to the
            # current movement direction

            # check forced neighbours (left)
            # (forced neighbors are those that must be considered due to the presence of obstacles)
            if neighbours.get(self.change_dir(leftmost_dir, -1), dummy).obstacle or not neighbours.get(leftmost_dir, dummy).obstacle:
            #  ^ check if there is an obstacle at one step left                         ^ check if the leftmost direction itself does not have an obstacle
                neighbours.pop(self.change_dir(leftmost_dir, -1), None) # discards the forced neighbour candidate

            neighbours.pop(leftmost_dir, None) # remove the leftmost direction itself from neighbors as it is not a valid candidate

            # check forced neighbours (right)
            # (forced neighbors are those that must be considered due to the presence of obstacles)
            if neighbours.get(self.change_dir(rightmost_dir, 1), dummy).obstacle or not neighbours.get(rightmost_dir, dummy).obstacle:
            #  ^ check if there is an obstacle at one step right                         ^ check if the rightmost direction itself does not have an obstacle
                neighbours.pop(self.change_dir(rightmost_dir, 1), None) # discards the forced neighbour candidate

            neighbours.pop(rightmost_dir, None)

            # remove neighbors that would lead backwards
            neighbours.pop(self.change_dir(direction, 4 + 1), None)
            neighbours.pop(self.change_dir(direction, 4 - 1), None)

        return pruned(neighbours, forced_neighbours_exist)


    def step(self, vertex, direction, cost_so_far):
        # determine the next vertex to move to from a given vertex in a specified direction


        next_vertex = None # initially there is no determined next vertex
        cost = 0

        # searches among the available edges
        for edge in self.graph.adjacent_edges(vertex):
            if edge.direction == direction and not edge.opposite(vertex).obstacle:
                # ensure that the edge aligns with the desired direction of movement
                # and check that the opposite vertex of the edge is not an obstacle
                next_vertex = edge.opposite(vertex)
                cost = cost_so_far + edge.weight
                break # when a suitable edge is found
            else:
                continue

        return next_vertex, cost

    def change_dir(self, direction, amount):
        # changes the direction within the defined eight directions
        return (direction + amount) % 8


    def jump(self, vertex, direction, cost_so_far, goal_vertex):
        # looks for jump points in the grid

        # attempt to take a step from the current vertex in the specified direction
        jump_point, cost = self.step(vertex, direction, cost_so_far)

        if jump_point is None: # if no jump point is found in the specified direction
            return None, None

        if jump_point.coords == goal_vertex: # if a vertex is the goal:
            return jump_point, cost

        if self.prune(jump_point, direction).forced: # check if there are forced neighbors
            self.jump_points.append(jump_point.coords) # save the jump point
            return jump_point, cost

        if direction % 2: # if the direction is diagonal
            for direction_l_r in (self.change_dir(direction, 1), self.change_dir(direction, -1)): # iterate over diagonal movement variations
                next_jump_point, _ = self.jump(jump_point, direction_l_r, 0, goal_vertex) # recursive exploration, aims to find additional jump points in diagonal directions
                if next_jump_point is not None:
                    #self.jump_points.append(jump_point.coords) # save the jump point
                    return jump_point, cost

        jump_point, cost = self.jump(jump_point, direction, cost, goal_vertex) # continue in the same direction

        return jump_point, cost

    def jps(self, start_vertex, goal_vertex):


        # list of jump points:
        self.jump_points = []

        # data structures for nodes
        explored = [] # for vertices that have been fully explored and dequed from the priority queue
        visited = {} # the predecessors of each vertex in the path, not necessarily fully explored/processed

        # costs of directions
        cost_hv = 1
        cost_di = math.sqrt(2)



        #print("nodet:", vertices.keys())

        # create the priority queue for open vertices
        jump_points_pq = []
        #print(vertices)
        if start_vertex not in self.vertices or goal_vertex not in self.vertices:
            print("Check that start and end nodes are correctly specified.")
            return None
        start_vertex = self.vertices[start_vertex]
        start_vertex.cost = 0

        start_vertex.h = 0

        # Adds the start vertex to the priority queue.
      #  print(f'Visiting/queueing vertex {start_vertex.coords}')

        heapq.heappush(jump_points_pq, start_vertex)
      #  print('Prioritized vertices (v, cost, dir):',
      #      *((vert.coords, vert.cost, vert.direction) for vert in jump_points_pq.queue),
       #     end=2 * '\n')

        # The starting vertex is visited first and has no leading edges.
        visited[start_vertex.coords] = None

        # Loops until the priority list gets empty.
        while jump_points_pq:


            # Gets the previously calculated jump_point with the lowest cost.
            jpoint_prev = heapq.heappop(jump_points_pq)


         #   print(f'Exploring vertex {jpoint_prev.coords}')

            # If goal vertex reached, the algorithm ends.
            if jpoint_prev.coords == goal_vertex:
                distance = jpoint_prev.cost
                # The search path ends with the found vertex (coords).
                # Initializes the search path and a dictionary of visited vertices.

    #########kommentoi nämä pois? reitti muulla tapaa?
           #     path = []
           #     path_vertex = jpoint_prev.coords
                # Constructs the rest of the search path
           #     while path_vertex is not None:
                    # The coords is added to the 'path'.
           #         path.append(path_vertex)
            #        path_vertex = visited[path_vertex]

            #    path.reverse()

                #jpoints_final = [jpoint for jpoint in self.jump_points if jpoint.coords in path]
            #    print("self.jpoints: ", self.jump_points)
                return {
             #       "shortestPath": path,
                    "explored": explored,
                    "absoluteDistance": round(distance, 1),
                    "jpoints": self.jump_points
                }




            # Finds the vertex neighbours (natural and forced).
            neighbours = self.prune(jpoint_prev)

            for direction in neighbours.vertices:
                jpoint, cost = self.jump(jpoint_prev, direction, jpoint_prev.cost, goal_vertex)

                if jpoint is None or self.vertices.get(jpoint, None) in explored:
                    continue

                # Calculates the jump point's heuristic value.
                if jpoint.h is None:
                    # calculate the manhattan distance
                    jpoint.h = tuple(map(lambda x, y: abs(x - y), jpoint.coords, goal_vertex))
                    jpoint.h = abs(jpoint.h[0] - jpoint.h[1]) * cost_hv \
                        + min(jpoint.h[0], jpoint.h[1]) * cost_di

                # Prevents reinsertion to the priority queue. The endpoint distance value will be updated.
                if jpoint.coords not in visited:
                #    print(f'Visiting/queueing vertex {jpoint.coords}.')
                    visited[jpoint.coords] = jpoint_prev.coords
                    heapq.heappush(jump_points_pq, jpoint)


                if jpoint.cost is None or jpoint.cost - jpoint.h > cost - jpoint_prev.h:

                    jpoint.cost = cost - jpoint_prev.h + jpoint.h
                    jpoint.direction = direction

                # Forces the priority queue to recalculate in case of an
                # inner vertex update resulting with the highest priority.

                if jump_points_pq:
                    first = heapq.heappop(jump_points_pq)
                    heapq.heappush(jump_points_pq, first)



         #   print('Prioritized vertices (v, cost, dir):',
         #       *((vert.coords, vert.cost, vert.direction) for vert in jump_points_pq.queue), end=2 * '\n')
            # The vertex is used for update and put aside.
            explored.append(jpoint_prev)

        return False # returns false if no path found





