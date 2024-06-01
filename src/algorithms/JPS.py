"""
Jump point search algorithm for shortest path finding.
"""
import time
from graph import Graph
from queue import PriorityQueue # = a standard library in python, instead of heapq
from collections import namedtuple
import sys
from pathlib import Path


#get the map matrices from a separate directory
base_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir))

from data.maps.simple import input_matrix


# Just a dummy object attached with a dummy function...
class Object:
    pass

def prune(graph, vertex, direction=None):
    neighbours = {}
    forced_neighbours_exist = False
    if direction is None:
        direction = vertex.direction

    # Enables us to return both the neighbouring vertices and the
    # indicator of forced neighbours existence
    pruned = namedtuple('pruned', 'vertices forced')

    # ...right here :-) We use it to ensure availability of the property
    # when the None object gets returned from the 'neighbours' dictionary.
    o = Object()
    o.obstacle = lambda: True

    # Collects all the surrounding vertices in a dictionary and
    # marks them with the search direction
    for edge in graph.adjacent_edges(vertex):
        neighbours[edge.direction] = edge.opposite(vertex)

    # Applies exclusively to the non-starting vertices
    if direction is not None:
        # Determines if the movement direction is horizontal/vertical (0) or diagonal (1)
        is_diagonal = direction % 2

        leftmost_dir = change_dir(direction, 2 + is_diagonal)
        rightmost_dir = change_dir(direction, -2 - is_diagonal)

        # Parent is never a neighbour candidate
        neighbours.pop(change_dir(direction, 4), None)

        # Trivial case - check if some of natural neighbours are obstacles
        for idx in range(-is_diagonal, is_diagonal + 1):
            if neighbours.get(change_dir(direction, idx), o).obstacle:
                neighbours.pop(change_dir(direction, idx), None)

        # Non-trivial case of potentially forced neighbours (left)
        if neighbours.get(change_dir(leftmost_dir, -1), o).obstacle \
                or not neighbours.get(leftmost_dir, o).obstacle:
            # Discards the forced neighbour candidate
            neighbours.pop(change_dir(leftmost_dir, -1), None)
        else:
            forced_neighbours_exist = True
        neighbours.pop(leftmost_dir, None)

        # Non-trivial case of potentially forced neighbours (right)
        if neighbours.get(change_dir(rightmost_dir, 1), o).obstacle \
                or not neighbours.get(rightmost_dir, o).obstacle:
            # Discards the forced neighbour candidate
            neighbours.pop(change_dir(rightmost_dir, 1), None)
        else:
            forced_neighbours_exist = True
        neighbours.pop(rightmost_dir, None)

        # Back vertices are never neighbour candidates
        neighbours.pop(change_dir(direction, 4 + 1), None)
        neighbours.pop(change_dir(direction, 4 - 1), None)

    return pruned(neighbours, forced_neighbours_exist)


def step(graph, vertex, direction, cost_so_far):
    # Defines a fail-safe result.
    next_vertex = None
    cost = 0

    # Searches among the available edges and follows the right one.
    for edge in graph.adjacent_edges(vertex):
        if edge.direction == direction and not edge.opposite(vertex).obstacle:
            next_vertex = edge.opposite(vertex)
            cost = cost_so_far + edge.weight
            break
        else:
            continue

    # If the edge is not found, the equivalent of "nothing" is returned.
    return next_vertex, cost


# Changes the direction within the defined eight directions
def change_dir(direction, amount):
    return (direction + amount) % 8


def jump(graph, vertex, direction, cost_so_far, goal_vertex):
    jump_point, cost = step(graph, vertex, direction, cost_so_far)

    if jump_point is None:
        return None, None

    # If a vertex is the goal vertex:
    if jump_point.entity == goal_vertex:
        return jump_point, cost

    # Checks if forced neighbours exist
    if prune(graph, jump_point, direction).forced:
        return jump_point, cost

    # Activates if the direction is diagonal.
    if direction % 2:
        for direction_l_r in (change_dir(direction, 1), change_dir(direction, -1)):
            # Tests if the next jump point exists (its cost is irrelevant in the context of the check alone).
            next_jump_point, _ = jump(graph, jump_point, direction_l_r, 0, goal_vertex)
            if next_jump_point is not None:
                return jump_point, cost

    # Proceed in the same direction.
    jump_point, cost = jump(graph, jump_point, direction, cost, goal_vertex)
    return jump_point, cost


def jps(graph, start_vertex, goal_vertex):
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
    print('Prioritized vertices (v, cost, dir):',
          *((vert.entity, vert.cost, vert.direction) for vert in jump_points_pq.queue),
          end=2 * '\n')

    # The starting vertex is visited first and has no leading edges.
    visited[start_vertex.entity] = None

    # Loops until the priority list gets empty.
    while not jump_points_pq.empty():
        # Gets the previously calculated jump_point with the lowest cost.
        jpoint_prev = jump_points_pq.get()
        print(f'Exploring vertex {jpoint_prev.entity}')

        # If the vertex being explored is a goal vertex, the algorithm ends.
        if jpoint_prev.entity == goal_vertex:
            return jpoint_prev

        # Finds the vertex neighbours (natural and forced).
        neighbours = prune(graph, jpoint_prev)

        for direction in neighbours.vertices:
            jpoint, cost = jump(graph, jpoint_prev, direction, jpoint_prev.cost, goal_vertex)

            if jpoint is None or vertices.get(jpoint, None) in explored:
                continue

            # Calculates the jump point's heuristic value.
            if jpoint.h is None:
                jpoint.h = tuple(map(lambda x, y: abs(x - y), jpoint.entity, goal_vertex))
                jpoint.h = abs(jpoint.h[0] - jpoint.h[1]) * cost_hv \
                    + min(jpoint.h[0], jpoint.h[1]) * cost_di

            # Prevents reinsertion to the priority queue. The endpoint distance value will be updated.
            if jpoint.entity not in visited:
                print(f'Visiting/queueing vertex {jpoint.entity}.')
                visited[jpoint.entity] = jpoint_prev.entity
                jump_points_pq.put(jpoint)

            if jpoint.cost is None or jpoint.cost - jpoint.h > cost - jpoint_prev.h:
                jpoint.cost = cost - jpoint_prev.h + jpoint.h
                jpoint.direction = direction

            # Forces the priority queue to recalculate in case of an
            # inner vertex update resulting with the highest priority.
            if not jump_points_pq.empty():
                jump_points_pq.put(jump_points_pq.get())

        print('Prioritized vertices (v, cost, dir):',
              *((vert.entity, vert.cost, vert.direction) for vert in jump_points_pq.queue), end=2 * '\n')
        # The vertex is used for update and put aside.
        explored.append(jpoint_prev)

if __name__ == '__main__':
    # Initializes an empty graph (object).
    # Creating a graph from the input matrix
    g = Graph(input_matrix, directed=False)
    g.create_graph()


    cost_hv = 5
    cost_di = 7
    # Constructs the 'vertices' dictionary for a more
    # convenient access during the graph construction.
    vertices = {k.entity: k for k in g.vertices()}
    #vertices = vertices.keys()
    #print("nodet:", vertices)


    # Initializes the search path and a dictionary of visited vertices.
    path = []
    explored = []
    visited = {}


    #measure path finding time
    start_time = time.time()
    # Starts the search.
    result = jps(g, (3, 2), (0, 1))
    end_time = time.time()


    # If the entity is found...
    if result is not None:
        print(f"Path finding execution, JPS: {round((end_time - start_time), 6):.6f} s")
        # The search path ends with the found vertex (entity).
        # Each vertex is a container for its real-world entity.
        path_vertex = result.entity
        # Constructs the rest of the search path (if it exists)...
        while path_vertex is not None:
            # The entity is added to the 'path'.
            path.append(path_vertex)
            path_vertex = visited[path_vertex]
        print('Search path found:', end=' ')
        # The path is reversed and starts with the root vertex.
        print(*reversed(path), sep=' -> ')
    # Otherwise...
    else:
        print('\nEntity is not found')

"""
sources:
https://blog.finxter.com/jump-search-algorithm-in-python-a-helpful-guide-with-video/
"""
