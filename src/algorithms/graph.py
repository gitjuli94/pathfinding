"""
Create a network of nodes and edges for the JPS algorithm using a map (matrix) with 1/0 syntax as an input.
"""

import math

class Graph:
    def __init__(self, input_matrix, directed=False):
        self._outgoing = {}
        #self._incoming = {} if directed else self._outgoing
        self._incoming = self._outgoing
        self.matrix = input_matrix

    #def is_directed(self):
        #return self._incoming is not self._outgoing

    def adjacent_edges(self, vertex, outgoing=True):
        adj_edges = self._outgoing# if outgoing else self._incoming
        for edge in adj_edges[vertex].values():
            yield edge #iterate over each of the edges for the vertex

    def add_vertex(self, entity=None, h=None, cost=None):
        vertex = self.Vertex(entity, h, cost)
        self._outgoing[vertex] = {}
        #if self.is_directed():
            #self._incoming[vertex] = {}
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
        m, n = len(self.matrix), len(self.matrix[0])
        vertices = {}

        # Add vertices
        for i in range(m):
            for j in range(n):
                vertex = self.add_vertex((i, j))
                vertex.obstacle = self.matrix[i][j] == 1  # Mark as obstacle if the matrix entry is 1
                vertices[(i, j)] = vertex
                #print(f"Added vertex: {vertex.entity}")

        # Add edges in form add_edge(origin, destination, weight, direction)
        for i in range(m):  # rows
            for j in range(n):  # columns
                if not vertices[(i, j)].obstacle:  # Only consider non-obstacle vertices
                    current_vertex = vertices[(i, j)]
                    #four directions added. the opposite directions (rotation with 180deg)
                    #are handled within JPS.change_dir (by adding 4 in the direction)
                    if j < n - 1:  # horizontal
                        self.add_edge(current_vertex, vertices[(i, j + 1)], weight=cost_hv, direction=0)

                    if i < m - 1:  # vertical
                        self.add_edge(current_vertex, vertices[(i + 1, j)], weight=cost_hv, direction=6)

                    if i < m - 1 and j < n - 1:  # left Diagonal
                        self.add_edge(current_vertex, vertices[(i + 1, j + 1)], weight=cost_di, direction=7)

                    if i < m - 1 and j > 0 and self.matrix[i + 1][j - 1] == 0:  # right Diagonal
                        self.add_edge(current_vertex, vertices[(i + 1, j - 1)], weight=cost_di, direction=5)


    def print_graph(self):
        for vertex in self._outgoing:
            print(f"Vertex {vertex.entity}:")
            for edge in self.adjacent_edges(vertex):
                origin, destination = edge.endpoints()
                print(f"  connects to {destination.entity} with weight {edge.weight} and direction {edge.direction}")

    class Vertex:
        __slots__ = '_entity', '_h', '_cost', '_obstacle', '_direction'

        def __init__(self, entity, h=None, cost=None):
            self.entity = entity
            self.h = h
            self.cost = cost
            self.obstacle = False
            self.direction = None

        @property
        def entity(self):
            return self._entity

        @entity.setter
        def entity(self, entity):
            self._entity = entity

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
            return hash(id(self))

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


"""g=Graph(input_matrix)
g.create_graph()
g.print_graph()"""
