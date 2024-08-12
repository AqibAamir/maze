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
    print(f"Maze saved to {filename}")

# Function to export the maze as CSV
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
