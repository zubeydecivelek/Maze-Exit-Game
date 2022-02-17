import sys

health_board, board, passed_ways, health_time = [], [], [], int(sys.argv[3])
path_choice = [(0, 1), (0, -1), (1, 0), (-1, 0)]

with open(sys.argv[1], mode="r") as maze_file:
    for line in maze_file:
        inner = []
        for letter in line.strip("\n"):
            inner.append(letter)
        board.append(inner)

with open(sys.argv[2], mode="r") as maze_health_file:
    for line in maze_health_file:
        inner = []
        for letter in line.strip("\n"):
            inner.append(letter)
        health_board.append(inner)

[[start_row, start_column]] = [[board.index(i), i.index("S")] for i in board if "S" in i]
[[final_row, final_column]] = [[board.index(i), i.index("F")] for i in board if "F" in i]


def create_output(file_name, table1, table2):
    output = open(file_name, "w")
    for first in table1:
        output.write(', '.join(map(str, first)) + '\n')
    output.write("\n")
    for second in table2:
        output.write(', '.join(map(str, second)) + '\n')


def available_paths(table, row, column):
    available_ones = []
    for path in path_choice:
        is_available = (row + path[0], column + path[1])
        if (0 <= is_available[0] < len(table) and 0 <= is_available[1] < len(table[0])) and (
                table[is_available[0]][is_available[1]] == "P" or table[is_available[0]][is_available[1]] == "H"):
            available_ones.append(is_available)
    return available_ones


def find_final(table, row, column):
    for path in path_choice:
        is_available = (row + path[0], column + path[1])
        if (0 <= is_available[0] < len(table) and 0 <= is_available[1] < len(table[0])) and table[is_available[0]][
            is_available[1]] == "F":
            return True
    return False


def finish_game(table):
    for tup in passed_ways:
        if tup != (start_row, start_column) or tup != (final_row, final_column):
            table[tup[0]][tup[1]] = "1"
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] != "1":
                table[i][j] = "0"
    table[start_row][start_column] = "S"
    table[final_row][final_column] = "F"


def game(table, row, column, health_condition):
    global passed_ways, health_time
    available_paths_list = available_paths(table, row, column)
    if find_final(table, row, column):
        table[row][column] = "X"
        passed_ways.append((row, column))
        if health_condition:
            health_time -= 1
        finish_game(table)
        passed_ways = []
    elif len(available_paths_list) == 0:
        table[row][column] = "X"
        (new_row, new_column) = passed_ways[-1]
        if (row, column) not in passed_ways:
            passed_ways.append((row, column))
        elif (row, column) in passed_ways and health_condition:
            health_time -= 1
        passed_ways.remove((row, column))
        if health_condition:
            health_time += 1
        return game(table, new_row, new_column, health_condition)
    else:
        if table[row][column] == "H":
            health_time = int(sys.argv[3])
        table[row][column] = "X"
        passed_ways.append((row, column))
        if health_condition:
            health_time -= 1
        return game(table, available_paths_list[0][0], available_paths_list[0][1], health_condition)


game(board, start_row, start_column, False)
game(health_board, start_row, start_column, True)
create_output(sys.argv[4], board, health_board)