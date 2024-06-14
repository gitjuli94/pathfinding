"""
Create a network of nodes and edges for the JPS algorithm using a map (matrix) with 1/0 syntax as an input.
"""

import math

class Graph:
    def __init__(self, input_matrix):
        self._outgoing = {}
        self._incoming = self._outgoing
        self.matrix = input_matrix
        self.graph = self.create_graph()

    def adjacent_edges(self, vertex):
        # a method to iterate over the adjacent edges of a vertex
        adj_edges = self._outgoing
        for edge in adj_edges[vertex].values():
            yield edge #iterate over each of the edges for the vertex

    def add_vertex(self, coords=None, h=None, cost=None):
        # a method to add a vertex in the graph
        vertex = self.Vertex(coords, h, cost)
        self._outgoing[vertex] = {}
        return vertex


    def add_edge(self, origin, destination, weight=None, direction=None):
        edge = self.Edge(origin, destination, weight, direction)
        self._outgoing[origin][destination] = edge
        #add edges to both directions
        edge = self.Edge(destination, origin, weight, (direction + 4) % 8) # +4 means rotation of 180deg of the direction
        self._incoming[destination][origin] = edge

    def vertices(self):
        return self._outgoing.keys()

    def edges(self):
        result = set()
        for inner_dict in self._outgoing.values():
            result.update(inner_dict.values())
        return result

    def create_graph(self, cost_hv=1, cost_di=math.sqrt(2)):
        # creates a graph for nxm matrix
        m = len(self.matrix)
        vertices = {}

        # Add vertices
        for i in range(m):
            n = len(self.matrix[i])
            for j in range(n):
                vertex = self.add_vertex((i, j))
                vertex.obstacle = self.matrix[i][j] == 1  # Mark as obstacle if the matrix entry is 1
                vertices[(i, j)] = vertex
                #print(f"Added vertex: {vertex.coords}")

        # Add edges in form add_edge(origin, destination, weight, direction)
        for i in range(m):  # rows
            n = len(self.matrix[i])
            for j in range(n):  # columns
                if not vertices[(i, j)].obstacle:  # Only consider non-obstacle vertices
                    current_vertex = vertices[(i, j)]
                    #four directions added. the opposite directions (rotation with 180deg)
                    #are handled within JPS.change_dir (by adding 4 in the direction)
                    if j < n - 1 and  not vertices[(i, j + 1)].obstacle:  # horizontal
                        self.add_edge(current_vertex, vertices[(i, j + 1)], weight=cost_hv, direction=0)

                    if i < m - 1 and not vertices[(i + 1, j)].obstacle:  # vertical
                        self.add_edge(current_vertex, vertices[(i + 1, j)], weight=cost_hv, direction=6)

                    if i < m - 1 and j < n - 1:  # left Diagonal
                        if not vertices[(i + 1, j + 1)].obstacle:
                            self.add_edge(current_vertex, vertices[(i + 1, j + 1)], weight=cost_di, direction=7)

                    if i < m - 1 and j > 0 and self.matrix[i + 1][j - 1] == 0:  # right Diagonal
                        if not vertices[(i + 1, j - 1)].obstacle:
                            self.add_edge(current_vertex, vertices[(i + 1, j - 1)], weight=cost_di, direction=5)


    def print_graph(self):
        # a method to print the graph
        for vertex in self._outgoing:
            print(f"Vertex {vertex.coords}:")
            for edge in self.adjacent_edges(vertex):
                origin, destination = edge.endpoints()
                print(f"  connects to {destination.coords} with weight {edge.weight} and direction {edge.direction}")

    class Vertex:
        __slots__ = '_entity', '_h', '_cost', '_obstacle', '_direction'

        def __init__(self, coords, h=None, cost=None):
            self.coords = coords
            self.h = h
            self.cost = cost
            self.obstacle = False
            self.direction = None

        @property
        def coords(self):
            return self._entity

        @coords.setter
        def coords(self, coords):
            self._entity = coords

        @property
        def h(self):
            return self._h

        @h.setter
        def h(self, h):
            self._h = h

        @property
        def cost(self):
            return self._cost

        @cost.setter
        def cost(self, cost):
            self._cost = cost

        @property
        def obstacle(self):
            return self._obstacle

        @obstacle.setter
        def obstacle(self, obstacle):
            self._obstacle = obstacle

        @property
        def direction(self):
            return self._direction

        @direction.setter
        def direction(self, direction):
            self._direction = direction

        def __hash__(self):
            return hash(self._entity)
            return hash(id(self))

        def __eq__(self, other):
            return isinstance(other, Graph.Vertex) and self._entity == other._entity

        def __lt__(self, other):
            if self.cost is None:
                return False
            elif other.cost is None:
                return True
            else:
                return self.cost < other.cost

    class Edge:
        __slots__ = '_origin', '_destination', '_weight', '_direction'

        def __init__(self, origin, destination, weight=None, direction=None):
            self._origin = origin
            self._destination = destination
            self.weight = weight
            self.direction = direction

        def endpoints(self):
            return self._origin, self._destination

        def opposite(self, vertex):
            return self._destination if self._origin is vertex else self._origin

        @property
        def weight(self):
            return self._weight

        @weight.setter
        def weight(self, weight):
            self._weight = weight

        @property
        def direction(self):
            return self._direction

        @direction.setter
        def direction(self, direction):
            self._direction = direction

        def __hash__(self):
            return hash((self._origin, self._destination))


