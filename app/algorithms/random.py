import heapq
from typing import Dict, List, Union

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return not self.elements

    def enqueue(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def dequeue(self):
        return heapq.heappop(self.elements)[1]

    def contains(self, item):
        return any(item == pair[1] for pair in self.elements)

    def decrease_priority(self, item, new_priority):
        for i, (priority, value) in enumerate(self.elements):
            if value == item:
                self.elements[i] = (new_priority, item)
                break

    def find_index(self, item):
        for i, (_, value) in enumerate(self.elements):
            if value == item:
                return i
        return -1

def is_diagonal(current, neighbor, width):
    return (current - neighbor) % (width + 1) == 0 or (current - neighbor) % (width - 1) == 0

def dijkstra(adjacency_list: Dict[int, List[int]], start_node: int, end_node: int, width: int) -> Dict[str, Union[Dict[int, bool], List[int], float]]:
    open_set = PriorityQueue()
    came_from = {}
    g_score = {}

    visited = {}

    open_set.enqueue(start_node, 0)

    g_score[start_node] = 0

    while not open_set.is_empty():
        current = open_set.dequeue()

        if current is None:
            break

        if current == end_node:
            return {
                "shortestPath": reconstruct_path(came_from, end_node),
                "visited": visited,
                "absoluteDistance": round(g_score[end_node] + 1e-9, 1)  # Using round to handle floating point precision issues
            }

        for neighbor in adjacency_list[current]:
            tentative_g_score = g_score[current] + 1

            if is_diagonal(current, neighbor, width):
                tentative_g_score = g_score[current] + 2 ** 0.5

            if neighbor not in g_score or tentative_g_score <= g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score

                if open_set.contains(neighbor):
                    open_set.decrease_priority(neighbor, g_score[neighbor])
                else:
                    open_set.enqueue(neighbor, g_score[neighbor])

        visited[current] = True

    return {"visited": visited}

def reconstruct_path(came_from: Dict[int, int], current: int) -> List[int]:
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.insert(0, current)

    return path
