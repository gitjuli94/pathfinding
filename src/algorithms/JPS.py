"""
Jump point search algorithm for shortest path finding.
"""

import math
from heapq import heappush, heappop
#from network import Generate_Network
from algorithms.graph_array import generate_graph, get_coordinates
import math
#from newyork import input_matrix
#import time



def heuristic_octile(node: int, end_node: int, width: int) -> float:
    row0, col0 = divmod(node, width)
    row1, col1 = divmod(end_node, width)
    row_diff = abs(row1 - row0)
    col_diff = abs(col1 - col0)
    return min(row_diff, col_diff) * math.sqrt(2) + max(row_diff, col_diff) - min(row_diff, col_diff)

    """# calculates the heuristic octile distance from the jump point to the goal node
    row0 = node // width
    col0 = node % width
    row1 = end_node // width
    col1 = end_node % width

    row_diff = row1 - row0 # y
    col_diff = col1 - col0 # x
    heuristic = min(abs(row_diff), abs(col_diff)) * math.sqrt(2) \
    + max(abs(row_diff), abs(col_diff)) - min(abs(row_diff), abs(col_diff))"""

    return heuristic

"""class PriorityQueue:
    def __init__(self):
        self.elements = []

    def enqueue(self, item, priority):
        heappush(self.elements, (priority, item))

    def dequeue(self):
        return heappop(self.elements)[1]

    def is_empty(self):
        return not self.elements

    def contains(self, item):
        return any(element[1] == item for element in self.elements)

    def decrease_priority(self, item, priority):
        for i, (p, element) in enumerate(self.elements):
            if element == item:
                if p > priority:
                    del self.elements[i]
                    heappush(self.elements, (priority, item))
                break"""

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def enqueue(self, element, priority):
        self.heap.append({'element': element, 'priority': priority})
        self.bubble_up()

    def dequeue(self):
        if not self.is_empty():
            top = self.heap[0]
            last = self.heap.pop()

            if len(self.heap) > 0:
                self.heap[0] = last
                self.bubble_down()

            return top['element']
        return None

    def bubble_up(self, start_index=None):
        index = start_index if start_index is not None else len(self.heap) - 1

        while index > 0:
            parent_index = (index - 1) // 2

            if self.heap[index]['priority'] < self.heap[parent_index]['priority']:
                self.swap(index, parent_index)
                index = parent_index
            else:
                break

    def bubble_down(self):
        index = 0

        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            smallest_child_index = index

            if (left_child_index < len(self.heap) and
                self.heap[left_child_index]['priority'] < self.heap[smallest_child_index]['priority']):
                smallest_child_index = left_child_index

            if (right_child_index < len(self.heap) and
                self.heap[right_child_index]['priority'] < self.heap[smallest_child_index]['priority']):
                smallest_child_index = right_child_index

            if smallest_child_index != index:
                self.swap(index, smallest_child_index)
                index = smallest_child_index
            else:
                break

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def decrease_priority(self, element, new_priority):
        index = self.find_index(element)

        if index != -1 and new_priority < self.heap[index]['priority']:
            self.heap[index]['priority'] = new_priority
            self.bubble_up(index)

    def find_index(self, element):
        for i, item in enumerate(self.heap):
            if item['element'] == element:
                return i
        return -1

    def is_empty(self):
        return len(self.heap) == 0

    def contains(self, element):
        return any(item['element'] == element for item in self.heap)


def jump_point_search(adjacency_list, start_node, end_node, width, field_status):
    open_set = PriorityQueue()
    came_from = {}
    cost_until_now = {} # cheapest cost until now
    tot_cost_estimate = {} # estimate of the total cost
    directions = {}
    visited = {}

    open_set.enqueue(start_node, 0)

    directions[start_node] = set(["1,0", "-1,0", "0,1", "0,-1", "1,-1", "1,1", "-1,1", "-1,-1"])

    cost_until_now[start_node] = 0
    tot_cost_estimate[start_node] = heuristic_octile(start_node, end_node, width)

    while not open_set.is_empty():
        current = open_set.dequeue()

        if current == end_node:

            return {
                "jpoints": reconstruct_path(came_from, end_node, width),
                "visited": visited_into_coords(visited, width),
                "absolute_distance": round(tot_cost_estimate[end_node], 1),
                "came_from": came_from,
                "end": end_node,
                "width": width
            }

        neighbors = get_neighbors_with_jump_points(current, adjacency_list, width, field_status, directions)

        for neighbor in neighbors:
            # calculate the Euclidean distance between the current node and a neighbor
            step_cost = math.sqrt((current % width - neighbor % width) ** 2 + (current // width - neighbor // width) ** 2)

            tentative_cost_until_now = cost_until_now[current] + step_cost

            if neighbor not in cost_until_now or tentative_cost_until_now < cost_until_now[neighbor]:
                came_from[neighbor] = current
                cost_until_now[neighbor] = tentative_cost_until_now
                tot_cost_estimate[neighbor] = tentative_cost_until_now + round(heuristic_octile(neighbor, end_node, width), 10)

                if open_set.contains(neighbor):
                    open_set.decrease_priority(neighbor, tot_cost_estimate[neighbor])
                else:
                    open_set.enqueue(neighbor, tot_cost_estimate[neighbor])

        visited[current] = True

    return {"visited": visited}

def visited_into_coords(visited, width):
    visited_coordinates = {}
    for key in visited.keys():
        visited_coordinates[get_coordinates(key, width)]=None
    return visited_coordinates


def reconstruct_path(came_from, current, width):
    path = [get_coordinates(current, width)]
    while current in came_from:
        current = came_from[current]
        coordinate = get_coordinates(current, width)
        path.insert(0, coordinate)
    return path


def reconstruct_full_path(came_from, current, width):
    path = [get_coordinates(current, width)]
    while current in came_from:
        previous = came_from[current]
        intermediate_path = interpolate_path(previous, current, width)
        path = intermediate_path + path[1:]
        current = previous
    return path

def interpolate_path(start, end, width):
    path = []
    row0, col0 = divmod(start, width)
    row1, col1 = divmod(end, width)

    d_row = row1 - row0
    d_col = col1 - col0

    n_steps = max(abs(d_row), abs(d_col))
    for step in range(n_steps + 1):
        r = row0 + step * d_row // n_steps
        c = col0 + step * d_col // n_steps
        path.append((r, c))

    return path

def prune_straight_direction_neighbors(target, dx, dy, adjacency_list, width, field_status, directions):
    if field_status[target] == 3:
        return target

    forced_neighbors = []

    if dy == 0:
        north = target - width
        south = target + width

        if north > 0 and north not in adjacency_list[target]:
            if north + dx in adjacency_list[target]:
                forced_neighbors.append(f"{dx},-1")

        if south < len(field_status) and south not in adjacency_list[target]:
            if south + dx in adjacency_list[target]:
                forced_neighbors.append(f"{dx},1")

        if forced_neighbors:
            forced_neighbors.append(f"{dx},{dy}")
            directions[target] = directions.get(target, set()).union(forced_neighbors)
            return target

        next_target = target + dx
        if next_target not in adjacency_list[target]:
            return None

        return jump(target, dx, dy, adjacency_list, width, field_status, directions)

    west = target - 1
    east = target + 1

    if west // width == target // width and west not in adjacency_list[target]:
        if west + dy * width in adjacency_list[target]:
            forced_neighbors.append(f"-1,{dy}")

    if east // width == target // width and east not in adjacency_list[target]:
        if east + dy * width in adjacency_list[target]:
            forced_neighbors.append(f"1,{dy}")

    if forced_neighbors:
        forced_neighbors.append(f"{dx},{dy}")
        directions[target] = directions.get(target, set()).union(forced_neighbors)
        return target

    next_target = target + dy * width
    if next_target not in adjacency_list[target]:
        return None

    return jump(target, dx, dy, adjacency_list, width, field_status, directions)

def prune_diagonal_neighbors(target, dx, dy, adjacency_list, width, field_status, directions):
    if field_status[target] == 3:
        return target

    x_blocker = target - dx
    y_blocker = target - dy * width

    if x_blocker // width == target // width and x_blocker not in adjacency_list[target]:
        if x_blocker + dy * width in adjacency_list[target]:
            forced_neighbors = [f"{dx},{dy}", f"{-dx},{dy}", f"0,{dy}", f"{dx},0"]
            directions[target] = directions.get(target, set()).union(forced_neighbors)
            return target

    if 0 < y_blocker < len(field_status) and y_blocker not in adjacency_list[target]:
        if y_blocker + dx in adjacency_list[target]:
            forced_neighbors = [f"{dx},{dy}", f"{dx},{-dy}", f"0,{dy}", f"{dx},0"]
            directions[target] = directions.get(target, set()).union(forced_neighbors)
            return target

    x_neighbor = target + dx
    y_neighbor = target + dy * width

    scans = []

    if x_neighbor in adjacency_list[target]:
        result_x = prune_straight_direction_neighbors(x_neighbor, dx, 0, adjacency_list, width, field_status, directions)
        if result_x is not None:
            scans.append(f"{dx},0")

    if y_neighbor in adjacency_list[target]:
        result_y = prune_straight_direction_neighbors(y_neighbor, 0, dy, adjacency_list, width, field_status, directions)
        if result_y is not None:
            scans.append(f"0,{dy}")

    if scans:
        scans.append(f"{dx},{dy}")
        directions[target] = directions.get(target, set()).union(scans)
        return target

    next_target = target + dx + dy * width
    if next_target not in adjacency_list[target]:
        return None

    return jump(target, dx, dy, adjacency_list, width, field_status, directions)

def jump(parent, dx, dy, adjacency_list, width, field_status, directions):
    target = parent + dx + dy * width

    if target not in adjacency_list[parent]:
        return None

    if field_status[target] == 3:
        return target

    if dx != 0 and dy != 0:
        return prune_diagonal_neighbors(target, dx, dy, adjacency_list, width, field_status, directions)

    return prune_straight_direction_neighbors(target, dx, dy, adjacency_list, width, field_status, directions)

def get_neighbors_with_jump_points(parent, adjacency_list, width, field_status, directions):
    neighbors = []

    if parent not in directions:
        directions[parent] = set(["1,0", "-1,0", "0,1", "0,-1", "1,-1", "1,1", "-1,1", "-1,-1"])

    for direction in directions[parent]:
        dx, dy = map(int, direction.split(","))
        neighbor = jump(parent, dx, dy, adjacency_list, width, field_status, directions)
        if neighbor is not None:
            neighbors.append(neighbor)

    return neighbors

def initialize_graph(matrix, start, goal):
    return generate_graph(matrix, start, goal)








"""field_status = []

rows = len(matrix)
cols = len(matrix[0])

for i in range(rows):
    row_status = []
    for j in range(cols):
        cell_value = matrix[i][j]
        row_status.append(cell_value)

    field_status.extend(row_status)

#print(len(field_status))
# coords: (row,column)
start=(30, 18)
end=(53, 64)


start_index = cols*start[0]+start[1]

#end = (1,8)
end_index = cols*end[0]+end[1]

field_status[start_index] = 2
field_status[end_index] = 3
#print(field_status)


expected_jpoints = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (4, 4), (3, 5), (2, 5), (1, 6), (1, 8)]
#print("expected:", expected_jpoints)

graph = generate_graph(field_status, cols)
start_timer = time.time()
result = jump_point_search(graph, start_index, end_index, cols, field_status)
end_timer = time.time()

print("absolute_distance", result["absolute_distance"])
print("time", round((end_timer-start_timer), 6))"""


