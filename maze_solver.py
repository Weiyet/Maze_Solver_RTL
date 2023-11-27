def solve_maze_matrix(maze, start, end):
    rows = len(maze)
    cols = len(maze[0])
    path_matrix = [[0] * cols for _ in range(rows)]

    def dfs(x, y):
        if x < 0 or x >= rows or y < 0 or y >= cols or maze[x][y] == 0:
            return False

        # Mark the current cell as part of the path
        path_matrix[x][y] = 1
        maze[x][y] = 0  # Mark the cell as visited

        if (x, y) == end:
            return True  # Reached the end of the maze

        # Explore neighbors
        if dfs(x + 1, y) or dfs(x - 1, y) or dfs(x, y + 1) or dfs(x, y - 1):
            return True

        # If none of the neighbors lead to the end, backtrack
        path_matrix[x][y] = 0
        return False

    dfs(start[0], start[1])
    return path_matrix

# # Example usage
# start_point = (0, 0)
# end_point = (8, 8)

# maze = [[1, 1, 1, 1, 1, 0, 1, 1, 1],
#         [0, 0, 0, 0, 1, 0, 1, 0, 1],
#         [1, 1, 1, 0, 1, 1, 1, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 0, 1],
#         [1, 1, 1, 1, 1, 0, 1, 1, 1],
#         [1, 0, 0, 0, 1, 0, 1, 0, 0],
#         [1, 1, 1, 0, 1, 1, 1, 0, 1],
#         [0, 0, 1, 0, 0, 0, 0, 0, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1]]
# solution_matrix = solve_maze_matrix(maze, start_point, end_point)

# if solution_matrix:
#     print("Solution Matrix:")
#     for row in solution_matrix:
#         print(row)
# else:
#     print("No solution found.")
