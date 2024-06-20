"""
Create a network of nodes and edges for the JPS algorithm using a map (matrix) with 1/0 syntax as an input.
"""

def generate_graph(matrix, start, end):
    # create field status array
    # field status: 0 = free, 1 = obstacle, 2 = start, 3 = target
    field_status = []

    rows = len(matrix)
    cols = len(matrix[0]) # = width

    for i in range(rows):
        row_status = []
        for j in range(cols):
            cell_value = matrix[i][j]
            row_status.append(cell_value)

        field_status.extend(row_status)

    # coordinates in this form: (row,column)
    start_index = cols*start[0]+start[1]
    end_index = cols*end[0]+end[1]

    if field_status[start_index] != 0 or field_status[end_index] != 0:
        print("start and goal nodes can't be within obstacles")
    else:
        field_status[start_index] = 2
        field_status[end_index] = 3

    # initialize neighbor list for map vertices
    neighbor_list = {}

    def get_index(row, col):
        return row * cols + col



    for row in range(rows):
        for col in range(cols):
            current_index = get_index(row, col)

            if field_status[current_index] == 1:
                continue

            neighbors = []

            # cardinal directions
            if row > 0 and field_status[get_index(row - 1, col)] != 1:
                neighbors.append(get_index(row - 1, col))

            if row < rows - 1 and field_status[get_index(row + 1, col)] != 1:
                neighbors.append(get_index(row + 1, col))

            if col > 0 and field_status[get_index(row, col - 1)] != 1:
                neighbors.append(get_index(row, col - 1))

            if col < cols - 1 and field_status[get_index(row, col + 1)] != 1:
                neighbors.append(get_index(row, col + 1))

            # diagonals (8-way traversal)
            if row > 0 and col < cols - 1 and field_status[get_index(row - 1, col + 1)] != 1:
                if get_index(row - 1, col) in neighbors or get_index(row, col + 1) in neighbors:
                    neighbors.append(get_index(row - 1, col + 1))

            if row < rows - 1 and col < cols - 1 and field_status[get_index(row + 1, col + 1)] != 1:
                if get_index(row, col + 1) in neighbors or get_index(row + 1, col) in neighbors:
                    neighbors.append(get_index(row + 1, col + 1))

            if row < rows - 1 and col > 0 and field_status[get_index(row + 1, col - 1)] != 1:
                if get_index(row, col - 1) in neighbors or get_index(row + 1, col) in neighbors:
                    neighbors.append(get_index(row + 1, col - 1))

            if row > 0 and col > 0 and field_status[get_index(row - 1, col - 1)] != 1:
                if get_index(row, col - 1) in neighbors or get_index(row - 1, col) in neighbors:
                    neighbors.append(get_index(row - 1, col - 1))

            neighbor_list[current_index] = neighbors

    return neighbor_list, start_index, end_index, cols, field_status

def get_coordinates(node, rows):
        row = node // rows
        col = node % rows
        return (row,col)
