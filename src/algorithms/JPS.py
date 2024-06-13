"""
Jump point search algorithm for shortest path finding.
sources:
https://blog.finxter.com/jump-search-algorithm-in-python-a-helpful-guide-with-video/
"""

import math
from algorithms.graph import Graph
from queue import PriorityQueue # = a standard library in python, instead of heapq
from collections import namedtuple


# A dummy object with the obstable attribute
class DummyObject:
    def __init__(self):
        self.obstacle = True



class JPS:
    def __init__(self, input_matrix):
        # Initializes an empty self.graph (object).
        # Creating a self.graph from the input matrix
        self.graph = Graph(input_matrix)
        #self.graph.create_graph()
        #print(self.graph.vertices.entity)


    def prune(self, vertex, direction=None):
        # identify which neighbors of a given vertex should be considered for further exploration
        neighbours = {}
        forced_neighbours_exist = True
        if direction is None:
            direction = vertex.direction

        # Enables us to return both the neighbouring vertices and the
        # indicator of forced neighbours existence
        pruned = namedtuple('pruned', 'vertices forced')

        # ...right here :-) We use it to ensure availability of the property
        # when the None object gets returned from the 'neighbours' dictionary.
        dummy = DummyObject()
        #o.obstacle = lambda: True

        # Collects all the surrounding vertices in a dictionary and
        # marks them with the search direction
        for edge in self.graph.adjacent_edges(vertex):
            neighbours[edge.direction] = edge.opposite(vertex)

        # Applies exclusively to the non-starting vertices
        if direction is not None:
            # Determines if the movement direction is horizontal/vertical (0) or diagonal (1)
            is_diagonal = direction % 2

            leftmost_dir = self.change_dir(direction, 2 + is_diagonal)
            rightmost_dir = self.change_dir(direction, -2 - is_diagonal)

            # Parent is never a neighbour candidate
            neighbours.pop(self.change_dir(direction, 4), None)

            # Check natural neighbours (directly reachable nodes) obstacles
            for idx in range(-is_diagonal, is_diagonal + 1):
                if neighbours.get(self.change_dir(direction, idx), dummy).obstacle:
                    neighbours.pop(self.change_dir(direction, idx), None)

            # Check forced neighbours (left)
            # (forced neighbors are those that must be considered due to the presence of obstacles)
            if neighbours.get(self.change_dir(leftmost_dir, -1), dummy).obstacle \
                    or not neighbours.get(leftmost_dir, dummy).obstacle:
                # Discards the forced neighbour candidate
                neighbours.pop(self.change_dir(leftmost_dir, -1), None)
            else:
                forced_neighbours_exist = True
            neighbours.pop(leftmost_dir, None)

            # Check forced neighbours (right)
            # (forced neighbors are those that must be considered due to the presence of obstacles)
            if neighbours.get(self.change_dir(rightmost_dir, 1), dummy).obstacle \
                    or not neighbours.get(rightmost_dir, dummy).obstacle:
                # Discards the forced neighbour candidate
                neighbours.pop(self.change_dir(rightmost_dir, 1), None)
            else:
                forced_neighbours_exist = True
            neighbours.pop(rightmost_dir, None)

            # Back vertices are never neighbour candidates
            neighbours.pop(self.change_dir(direction, 4 + 1), None)
            neighbours.pop(self.change_dir(direction, 4 - 1), None)

        return pruned(neighbours, forced_neighbours_exist)


    def step(self, vertex, direction, cost_so_far):
        # Defines a fail-safe result.
        next_vertex = None
        cost = 0

        # Searches among the available edges and follows the right one.
        for edge in self.graph.adjacent_edges(vertex):
            if edge.direction == direction and not edge.opposite(vertex).obstacle:
                next_vertex = edge.opposite(vertex)
                cost = cost_so_far + edge.weight
                break
            else:
                continue

        # If the edge is not found, the equivalent of "nothing" is returned.
        return next_vertex, cost


    # Changes the direction within the defined eight directions
    def change_dir(self, direction, amount):
        return (direction + amount) % 8


    def jump(self, vertex, direction, cost_so_far, goal_vertex):

        jump_point, cost = self.step(vertex, direction, cost_so_far)

        if jump_point is None:
            return None, None

        # If a vertex is the goal vertex:
        if jump_point.entity == goal_vertex:
            return jump_point, cost

        # Checks if forced neighbours exist
        if self.prune(jump_point, direction).forced:
            return jump_point, cost

        # Activates if the direction is diagonal.
        if direction % 2:
            for direction_l_r in (self.change_dir(direction, 1), self.change_dir(direction, -1)):
                # Tests if the next jump point exists (its cost is irrelevant in the context of the check alone).
                next_jump_point, _ = self.jump(jump_point, direction_l_r, 0, goal_vertex)
                if next_jump_point is not None:
                    return jump_point, cost

        # Proceed in the same direction.
        jump_point, cost = self.jump(jump_point, direction, cost, goal_vertex)
        return jump_point, cost

    def jps(self, start_vertex, goal_vertex):
        # Initialize lists for node lists
        explored = []
        visited = {}

        # Costs of directions
        cost_hv = 1
        cost_di = math.sqrt(2)

        # Constructs the 'vertices' dictionary
        vertices = {k.entity: k for k in self.graph.vertices()}

        #print("nodet:", vertices.keys())

        # Create the priority queue for open vertices.
        jump_points_pq = PriorityQueue()
        if start_vertex not in vertices or goal_vertex not in vertices:
            return None
        start_vertex = vertices[start_vertex]
        start_vertex.cost = 0

        start_vertex.h = 0

        # Adds the start vertex to the priority queue.
        #print(f'Visiting/queueing vertex {start_vertex.entity}')

        jump_points_pq.put(start_vertex)
        #print('Prioritized vertices (v, cost, dir):',
            #*((vert.entity, vert.cost, vert.direction) for vert in jump_points_pq.queue),
            #end=2 * '\n')

        # The starting vertex is visited first and has no leading edges.
        visited[start_vertex.entity] = None

        # Loops until the priority list gets empty.
        while not jump_points_pq.empty():
            # Gets the previously calculated jump_point with the lowest cost.
            jpoint_prev = jump_points_pq.get()
            #print(f'Exploring vertex {jpoint_prev.entity}')

            # If goal vertex reached, the algorithm ends.
            if jpoint_prev.entity == goal_vertex:
                distance = jpoint_prev.cost
                # The search path ends with the found vertex (entity).
                # Initializes the search path and a dictionary of visited vertices.
                path = []
                path_vertex = jpoint_prev.entity
                # Constructs the rest of the search path
                while path_vertex is not None:
                    # The entity is added to the 'path'.
                    path.append(path_vertex)
                    path_vertex = visited[path_vertex]

                path.reverse()

                return {
                    "shortestPath": path,
                    "visited": explored,
                    "absoluteDistance": distance
                }

            # Finds the vertex neighbours (natural and forced).
            neighbours = self.prune(jpoint_prev)

            for direction in neighbours.vertices:
                jpoint, cost = self.jump(jpoint_prev, direction, jpoint_prev.cost, goal_vertex)

                if jpoint is None or vertices.get(jpoint, None) in explored:
                    continue

                # Calculates the jump point's heuristic value.
                if jpoint.h is None:
                    jpoint.h = tuple(map(lambda x, y: abs(x - y), jpoint.entity, goal_vertex))
                    jpoint.h = abs(jpoint.h[0] - jpoint.h[1]) * cost_hv \
                        + min(jpoint.h[0], jpoint.h[1]) * cost_di

                # Prevents reinsertion to the priority queue. The endpoint distance value will be updated.
                if jpoint.entity not in visited:
                    #print(f'Visiting/queueing vertex {jpoint.entity}.')
                    visited[jpoint.entity] = jpoint_prev.entity
                    jump_points_pq.put(jpoint)

                if jpoint.cost is None or jpoint.cost - jpoint.h > cost - jpoint_prev.h:
                    jpoint.cost = cost - jpoint_prev.h + jpoint.h
                    jpoint.direction = direction

                # Forces the priority queue to recalculate in case of an
                # inner vertex update resulting with the highest priority.
                if not jump_points_pq.empty():
                    jump_points_pq.put(jump_points_pq.get())

            #print('Prioritized vertices (v, cost, dir):',
                #*((vert.entity, vert.cost, vert.direction) for vert in jump_points_pq.queue), end=2 * '\n')
            # The vertex is used for update and put aside.
            explored.append(jpoint_prev)





