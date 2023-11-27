import random

def generate_maze_matrix(rows, cols, start, end):
    maze = [[0] * cols for _ in range(rows)]
    stack = [start]
    
    while stack:
        current = stack[-1]
        x, y = current
        maze[x][y] = 1  # Mark the cell as part of the path
        
        neighbors = [
            (x + 2, y),
            (x - 2, y),
            (x, y + 2),
            (x, y - 2),
        ]
        random.shuffle(neighbors)
        
        found = False
        for nx, ny in neighbors:
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                maze[(x + nx) // 2][(y + ny) // 2] = 1  # Mark the cell between as part of the path
                stack.append((nx, ny))
                found = True
                break
        
        if not found:
            stack.pop()

    maze[start[0]][start[1]] = 1
    maze[end[0]][end[1]] = 1

    return maze

if __name__ == "__main__":
# # Example usage #randomized by x,y + 2 , make sure that end_point (x,y) = start_point(x+2n,y+2n)
    maze_rows = 17
    maze_cols = 17
    start_point = (0, 0)
    end_point = (maze_rows - 1, maze_cols - 1)

    generated_maze_dfs = generate_maze_matrix(maze_rows, maze_cols, start_point, end_point)

    print("Generated Maze using DFS:")
    for row in generated_maze_dfs:
        print(row)
