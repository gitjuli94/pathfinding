"""
Create a network of nodes and edges for the Dijkstra algorithm using
a map with 1/0 syntax as an input. Returns a dictionary with the node
as the key and the list of adjacent available nodes as the value.
"""

class GenerateNetwork:
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

    def add_edges(self, y: int, x: int):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.rows and 0 <= nx < self.cols and self.matrix[ny][nx] == 0:

                weight = 1 if abs(dx) + abs(dy) == 1 else 2**0.5
                if weight > 1: # diagonal edge
                    # don't add edges to diagonally pass corners
                    # (only orthogonal movement around corners)
                    if self.matrix[ny][x] == 0 and self.matrix[y][nx] == 0:
                        self.graph[(y, x)].append(((ny, nx), weight))
                else:
                    self.graph[(y, x)].append(((ny, nx), weight))
