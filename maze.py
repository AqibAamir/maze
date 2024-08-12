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
def print_maze(maze, style='Default', colored_output=False):
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
            file.write(''.joining(row) + '\n')
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
        return "hard"
    elif difficulty_score > 0.1:
        return "medium"
    else:
        return "Easy."


# Function to let the user define a custom pattern for the maze
def custom_maze_theme():
    wall = input("Enter a symbol for walls: ") or WALL
    passage = input("Enter a symbol for passages: ") or PASSAGE
    start = input("Enter a symbol from the start: ") or START
    exit = input("Enter a symbol for the exit: ") or EXIT
    return {WALL: wall, PASSAGE: passage, START: start, EXIT: exit, VISITED: VISITED, PLAYER: PLAYER}

# Function to allow the user to interactively solve the maze
def interactive_maze_solver(maze):
    x, y = 1, 1
    maze[x][y] = PLAYER
    print_maze(maze)

    while (x, y) != (len(maze) - 2, len(maze[0]) - 2):
        move = input("move (WASD): ").lower()
        if move in ['w', 'a', 's', 'd']:
            dx, dy = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}[move]
            nx, ny = x + dx, y + dy
            if maze[nx][ny] == PASSAGE or maze[nx][ny] == EXIT:
                maze[x][y] = PASSAGE
                x, y = nx, ny
                maze[x][y] = PLAYER
            print_maze(maze)
        else:
            print("Invalid move. Use 'W' for up, 'A' for left, 'S' for down, and 'D' for right.")

    print("Congratulations! You solved the maze!")

# Function to calculate the complexity of the maze based on the solution path length
def maze_complexity(solution):
    return len(solution) if solution else 0

# Function to reset the maze for a new attempt
def reset_maze(maze):
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] in [PLAYER, VISITED]:
                maze[x][y] = PASSAGE
    print("Maze reset successfully.")

# Function to display the solution path
def display_solution_path(solution):
    for step in solution:
        print(f"Step: {step}")


# Function to log events with detailed timestamps
def log_event(event_message):
    with open('maze_log.txt', 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event_message}\n")

# Function to save user preferences to a configuration file
def save_user_preferences(preferences):
    with open('user_preferences.json', 'w') as file:
        json.dump(preferences, file)
    print("User preferences saved.")

# Function to load user preferences from a configuration file
def load_user_preferences():
    try:
        with open('user_preferences.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Main function to run the maze program
def main():
    print("Welcome to the Maze Generator!")

    # Load user preferences
    user_preferences = load_user_preferences()

    # Select difficulty and algorithm
    width, height = choose_difficulty()
    algorithm = choose_algorithm()
    
    start_time = time.time()

    # Generate the maze based on the selected algorithm
    if algorithm == 'dfs':
        maze = create_maze(width, height)
    elif algorithm == 'prim':
        maze = generate_prim_maze(width, height)
    elif algorithm == 'random':
        maze = random_maze(width, height)  # Implement a simple random maze generator
    else:
        print("Unknown algorithm. Using DFS by default.")
        maze = create_maze(width, height)

    generation_time = time.time() - start_time

    log_event(f"Maze generated using {algorithm} algorithm with dimensions {width}x{height}")

    print("\nGenerated Maze:")
    theme_option = input("Do you want to use a custom theme? (y/n): ").lower()
    if theme_option == 'y':
        theme = custom_maze_theme()
        print_maze(maze, style='default', colored_output=False)
    else:
        print_maze(maze, style='blocks')

    display_maze_stats(maze)

 save_option = input("\nDo you want to save the maze to a file? (y/n): ").lower()
    if save_option == 'y':
        filename = input("Enter the filename (with .txt extension): ")
        save_maze_to_file(maze, filename)
        export_option = input("Do you want to export the maze in CSV or JSON format? (csv/json/n): ").lower()
        if export_option == 'csv':
            export_maze_to_csv(maze, filename.replace('.txt', '.csv'))
        elif export_option == 'json':
            export_maze_to_json(maze, filename.replace('.txt', '.json'))
        log_event(f"Maze saved and exported to {filename}")

 solve_option = input("\nDo you want to solve the maze? (y/n): ").lower()
    if solve_option == 'y':
        interactive_option = input("Solve manually or automatically? (m/a): ").lower()
        if interactive_option == 'm':
            interactive_maze_solver(maze)
            log_event("User solved maze manually.")
        elif interactive_option == 'a':
            solution = []
            start_time = time.time()
            if solve_maze(maze, 1, 1, solution):
                solve_time = time.time() - start_time
                print("\nMaze Solved! Solution Path:")
                for step in solution:
                    print(step)
                print(f"Solution Length: {maze_complexity(solution)}")
                print(f"Solve Time: {solve_time:.2f} seconds")
                display_solution_path(solution)
                log_event(f"Maze solved automatically in {solve_time:.2f} seconds.")
            else:
                print("\nNo solution found.")
                log_event("Maze solving failed.")
        
        # Option to reset the maze and try again
        retry_option = input("\nDo you want to reset the maze and try again? (y/n): ").lower()
        if retry_option == 'y':
            reset_maze(maze)
            main()

    print(f"Maze Generation Time: {generation_time:.2f} seconds")

    # Save user preferences
    preferences = {
        'difficulty': choose_difficulty(),
        'algorithm': choose_algorithm()
    }
    save_user_preferences(preferences)


def generate_prim_maze(width, height):
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    walls = [(1, 1)]

    def add_walls(x, y):
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 < nx < height - 1 and 0 < ny < width - 1 and maze[nx][ny] == WALL:
                walls.append((nx, ny))
                maze[x + dx][y + dy] = PASSAGE

    maze[1][1] = PASSAGE
    add_walls(1, 1)

while walls:
        x, y = random.choice(walls)
        walls.remove((x, y))
        maze[x][y] = PASSAGE
        add_walls(x, y)
    
    maze[0][1] = START
    maze[height - 1][width - 2] = EXIT

    return maze

def random_maze(width, height):
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    for x in range(height):
        for y in range(width):
            maze[x][y] = PASSAGE if random.random() > 0.3 else WALL
    maze[0][1] = START
    maze[height - 1][width - 2] = EXIT
    return maze

# Enhanced configuration management
def save_configuration(config, filename='config.json'):
    with open(filename, 'w') as file:
        json.dump(config, file, indent=4)
    print(f"Configuration saved to {filename}")

def load_configuration(filename='config.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

# Advanced maze analysis
def analyze_maze_path_lengths(maze):
    path_lengths = []
    for x in range(1, len(maze) - 1):
        for y in range(1, len(maze[0]) - 1):
            if maze[x][y] == PASSAGE:
                length = bfs_path_length(maze, x, y)
                if length:
                    path_lengths.append(length)
    return path_lengths

def bfs_path_length(maze, start_x, start_y):
    queue = [(start_x, start_y, 0)]
    visited = set()
    visited.add((start_x, start_y))
    
    while queue:
        x, y, length = queue.pop(0)
        if maze[x][y] == EXIT:
            return length
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and (nx, ny) not in visited and maze[nx][ny] in [PASSAGE, EXIT]:
                queue.append((nx, ny, length + 1))
                visited.add((nx, ny))
    return None

def identify_bottlenecks(maze):
    bottlenecks = []
    for x in range(1, len(maze) - 1):
        for y in range(1, len(maze[0]) - 1):
            if maze[x][y] == PASSAGE:
                passages = sum(maze[x + dx][y + dy] == PASSAGE for dx, dy in DIRECTIONS)
                if passages == 1:  # Dead end
                    bottlenecks.append((x, y))
    return bottlenecks

# Improved logging with action tracking
def log_action(action_message, filename='maze_action_log.txt'):
    with open(filename, 'a') as file:
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action_message}\n")
    print(f"Action logged: {action_message}")

# Adding additional user preference options
def choose_difficulty():
    difficulties = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}
    print("Select maze difficulty:")
    for key, value in difficulties.items():
        print(f"{key}: {value}")
    choice = input("Enter choice (1/2/3): ").strip()
    return difficulties.get(choice, 'Easy')

def choose_algorithm():
    algorithms = {'1': 'DFS', '2': 'Prim', '3': 'Random'}
    print("Select maze generation algorithm:")
    for key, value in algorithms.items():
        print(f"{key}: {value}")
    choice = input("Enter choice (1/2/3): ").strip()
    return algorithms.get(choice, 'DFS')

# Function to display user manual
def display_user_manual():
    manual = """
    Maze Generator User Manual:

    1. Generating a Maze:
       - Select the maze width and height (must be odd and >= 7).
       - Choose the difficulty level and generation algorithm.

    2. Saving the Maze:
       - Save the maze to a text file.
       - Optionally export the maze as CSV or JSON.

    3. Solving the Maze:
       - Choose to solve the maze manually or automatically.
       - For manual solving, use 'W', 'A', 'S', 'D' to move.
       - For automatic solving, view the solution path and statistics.

    4. Analyzing the Maze:
       - View maze statistics including walls, passages, dead ends, and loops.
       - Export maze data in different formats.
       - Analyze path lengths and identify bottlenecks.

    5. Configuration and Preferences:
       - Save and load user preferences for difficulty and algorithm.
       - Customize maze themes and logging options.

    For additional help, consult the documentation or contact support.
    """
    print(manual)

