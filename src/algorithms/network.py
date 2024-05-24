"""
Create a network of nodes and edges for the Dijkstra algorithm using a map with 1/0 syntax as an input.
Returns a dictionary with the node as the key and the list of adjacent available nodes as the value.
"""

class Generate_Network:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.nodes=[]
        self.graph = {}
        self.graph = self.create_graph()

    def create_graph(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == 0:
                    self.graph[(i, j)] = []
                    self.add_edges(i, j)

        return self.graph

    def add_edges(self, x: int, y: int):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.matrix[nx][ny] == 0:
                weight = 1 if abs(dx) + abs(dy) == 1 else 2**0.5
                self.graph[(x, y)].append(((nx, ny), weight))
