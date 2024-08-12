import random
import time
import csv
import json
from termcolor import colored
import os

# Constants for maze components
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
WALL = '#'
PASSAGE = ' '
START = 'S'
EXIT = 'E'
VISITED = '.'
PLAYER = 'P'

# Function to create a maze grid
def create_maze(width, height):
    maze = [[WALL for _ in range(width)] for _ in range(height)]

    def is_within_bounds(x, y):
        return 0 <= x < height and 0 <= y < width

    def carve_passage(x, y):
        maze[x][y] = PASSAGE
        random.shuffle(DIRECTIONS)
        for dx, dy in DIRECTIONS:
            nx, ny = x + 2 * dx, y + 2 * dy
            if is_within_bounds(nx, ny) and maze[nx][ny] == WALL:
                maze[x + dx][y + dy] = PASSAGE
                carve_passage(nx, ny)

    carve_passage(1, 1)  # Start carving from position (1, 1)
    maze[0][1] = START  # Entrance
    maze[height - 1][width - 2] = EXIT  # Exit

    return maze

# Function to print the maze with visualization options
def print_maze(maze, style='default', colored_output=False):
    styles = {
        'default': {WALL: '#', PASSAGE: ' ', START: 'S', EXIT: 'E', VISITED: '.', PLAYER: 'P'},
        'dots': {WALL: '•', PASSAGE: ' ', START: 'S', EXIT: 'E', VISITED: '.', PLAYER: 'P'},
        'blocks': {WALL: '█', PASSAGE: ' ', START: 'S', EXIT: 'E', VISITED: '.', PLAYER: 'P'},
        'binary': {WALL: '1', PASSAGE: '0', START: 'S', EXIT: 'E', VISITED: '.', PLAYER: 'P'},
    }
    selected_style = styles.get(style, styles['default'])

    for row in maze:
        line = ''.join(selected_style[cell] for cell in row)
        if colored_output:
            print(colored(line, 'green'))
        else:
            print(line)

# Function to save the generated maze to a file
def save_maze_to_file(maze, filename):
    with open(filename, 'w') as file:
        for row in maze:
            file.write(''.join(row) + '\n')
    print(f"Maze information saved  to {filename}")

# Function to export the maze as CSV file
def export_maze_to_csv(maze, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(maze)
    print(f"Maze exported to {filename}")

# Function to export the maze as JSON
def export_maze_to_json(maze, filename):
    with open(filename, 'w') as file:
        json.dump(maze, file)
    print(f"Maze exported to {filename}")


# Get maze dimensions from the user
def get_user_dimensions():
    while True:
        try:
            width = int(input("Please enter a maze width (odd number >= 7): "))
            height = int(input("Enter maze height (odd number >= 7): "))
            if width >= 7 and height >= 7 and width % 2 == 1 and height % 2 == 1:
                return width, height
            else:
                print("Both width and height must be odd numbers and at least 7.")
        except ValueError:
            print("Please enter valid integers for width and height.")


def solve_maze(maze, x, y, solution):
    if (x, y) == (len(maze) - 2, len(maze[0]) - 2):  # Check if the exit is reached
        solution.append((x, y))
        return True

    if maze[x][y] == PASSAGE or maze[x][y] == START:
        maze[x][y] = VISITED  # Mark as visited
        solution.append((x, y))

        for dx, dy in DIRECTIONS:
            if solve_maze(maze, x + dx, y + dy, solution):
                return True

        solution.pop()  # Backtrack if no path is found
        maze[x][y] = PASSAGE  # Unmark if backtracking

    return False

# Display statistics about the maze
def display_maze_stats(maze):
    wall_count = sum(row.count(WALL) for row in maze)
    passage_count = sum(row.count(PASSAGE) for row in maze)
    dead_ends = count_dead_ends(maze)
    loops = count_loops(maze)
    print(f"Maze Statistics:")
    print(f" - Walls: {wall_count}")
    print(f" - Passages: {passage_count}")
    print(f" - Total Cells: {len(maze) * len(maze[0])}")
    print(f" - Dead Ends/wall: {dead_ends}")
    print(f" - Loops: {loops}")
    print(f" - Start Position: (0, 1)")
    print(f" - Exit Position: ({len(maze) - 1}, {len(maze[0]) - 2})")
    print(f" - Maze Difficulty: {evaluate_difficulty(maze, dead_ends, loops)}")

# Count dead ends in the maze
def count_dead_ends(maze):
    dead_ends = 0
    for x in range(1, len(maze) - 1):
        for y in range(1, len(maze[0]) - 1):
            if maze[x][y] == PASSAGE:
                passages = sum(maze[x + dx][y + dy] == PASSAGE for dx, dy in DIRECTIONS)
                if passages == 1:
                    dead_ends += 1
    return dead_ends

# Count loops in the maze
def count_loops(maze):
    loops = 0
    for x in range(1, len(maze) - 1):
        for y in range(1, len(maze[0]) - 1):
            if maze[x][y] == PASSAGE:
                passages = sum(maze[x + dx][y + dy] == PASSAGE for dx, dy in DIRECTIONS)
                if passages > 2:
                    loops += 1
    return loops

# Function to evaluate the maze's difficulty based on dead ends and loops
def evaluate_difficulty(maze, dead_ends, loops):
    size_factor = len(maze) * len(maze[0])
    difficulty_score = (dead_ends + loops) / size_factor
    if difficulty_score > 0.2:
        return "Hard"
    elif difficulty_score > 0.1:
        return "Medium"
    else:
        return "Easy"
