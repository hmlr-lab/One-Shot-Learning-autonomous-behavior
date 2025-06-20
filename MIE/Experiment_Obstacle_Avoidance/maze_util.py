from collections import deque
import os
import string

def hash_fn(number):
    # Return "A" for 0 to match the initial implementation
    # Consider adjusting if "A" should represent 1 instead of 0
    if number==0:
        alpha="A"
    else:
        alpha=""
        while (number >0):  
            # Adjust remainder to be 1-based index for letters
            remainder = number % 26
            alpha_temp=string.ascii_uppercase[remainder]
            # Prepend the character to alpha to construct the string correctly
            alpha=alpha+alpha_temp
            number = number // 26
    return alpha
move_directions = {
         #'move_up': (-1, 0),          # Moving up increases the y-coordinate
         #'move_down': (1, 0),       # Moving down decreases the y-coordinate
         #'move_left': (0, -1),       # Moving left decreases the x-coordinate
         #'move_right': (0, 1),       # Moving right increases the x-coordinate
         'move_north': (-10, 0),       # Same as move_up
         'move_south': (10, 0),      # Same as move_down
         'move_east': (0, 10),        # Same as move_right
         'move_west': (0, -10),       # Same as move_left
       'move_north_east': (-10, 10),  # Moving northeast increases both x and y coordinates
        'move_south_east': (10, 10), # Moving southeast increases x and decreases y
       'move_north_west': (-10, -10), # Moving northwest decreases x and increases y
       'move_south_west': (10, -10) # Moving southwest decreases both x and y coordinates
    }


def compute_directions(path, move_mapping= move_directions):
    # Use the exact move_directions dictionary provided
    

    # Invert the dictionary to map coordinates to moves
    move_mapping_reverse = {v: k for k, v in move_mapping.items()}
    
    directions = []
    
    for i in range(len(path) - 1):
        # Calculate the difference between consecutive points
        dx = path[i+1][0] - path[i][0]
        dy = path[i+1][1] - path[i][1]
        # Find the corresponding direction
        if (dx, dy) in move_mapping_reverse:
            directions.append(move_mapping_reverse[(dx, dy)])
        else:
            raise ValueError(f"Unknown move from {path[i]} to {path[i+1]}")

    return directions

def get_move_coordinates(start_x = 0, start_y = 0, moves =[], move_mapping={}):
    # Define the basic movements
    

    # Initialize the starting coordinates
    x, y = start_x, start_y

    # Handle each move in the list of moves
    for move in moves:
        if move in move_mapping:
            dx, dy = move_mapping[move]
            x += dx
            y += dy

    return x, y


def is_valid_move(x, y, grid):
    # Check if the position (x, y) is within the grid boundaries and not an obstacle.
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1

def apply_move(direction, position,move_mapping=move_directions):
    #Applies a move based on the direction to the given position.
    x, y = position
    set_1 = get_move_coordinates(moves=[direction], move_mapping=move_directions)
    new_x, new_y = x+ set_1[0],  y+set_1[1]
    
    return (new_x, new_y)

def pathfinding(start, end, grid, basic_moves, recursive_rules):
    # Perform BFS to find the shortest path considering the rules provided.
    queue = deque([(start, [start], set())])  # Adding a set to track used basic moves
    visited = set()
    visited.add(start)
    total_steps = 0  # Count all steps including backtracking
    
    while queue:
        current, path, used_basic_moves = queue.popleft()
        total_steps += 1  # Count each step processed

        if current == end:
            
            return path, int(total_steps)
        
        if not recursive_rules:
            # If no recursive rules are provided, apply each basic move exactly once
            apply_basic_moves_once(current, path, grid, visited, queue, basic_moves, used_basic_moves)
            
        else:
            # Apply recursive moves based on the user-provided rules
            apply_recursive_moves(current, path, grid, visited, queue, recursive_rules)
            
    
    return None, int(total_steps)  # No path found

def apply_basic_moves_once(start, path, grid, visited, queue, basic_moves, used_basic_moves):
    # Apply each basic move exactly once.
    for move in basic_moves:
        next_position = apply_move(move, start)
        if is_valid_move(*next_position, grid) and next_position not in visited and move not in used_basic_moves:
            visited.add(next_position)
            new_used_basic_moves = used_basic_moves | {move}
            queue.append((next_position, path + [next_position], new_used_basic_moves))

def apply_recursive_moves(start, path, grid, visited, queue, recursive_rules):
    # Apply recursive moves starting from a given move.
    for rule in recursive_rules:
        first_move = rule
        second_move = rule

        # Apply the first move
        intermediate = apply_move(first_move, start)
        
        if is_valid_move(*intermediate, grid) and intermediate not in visited:
            new_path = path + [intermediate]
            visited.add(intermediate)
            queue.append((intermediate,new_path, set()))

            # Apply the second move recursively from the intermediate position
            if second_move == first_move:  # If the rule allows the same move repeatedly
                current = intermediate
                while True:
                    next_position = apply_move(second_move, current)
                    if is_valid_move(*next_position, grid) and next_position not in visited:
                        new_path = new_path + [next_position]
                        visited.add(next_position)
                        queue.append((next_position,new_path, set()))
                        current = next_position
                    else:
                        break
            else:
                # Apply a different second move (if allowed by the rules)
                next_position = apply_move(second_move, intermediate)
                if is_valid_move(*next_position, grid) and next_position not in visited:
                    new_path = new_path + [next_position]
                    visited.add(next_position)
                    queue.append((next_position, new_path, set()))

def print_grid(grid, start=None, end=None, path=None):
    #Print the grid with obstacles, start, end, and path (if provided) 
    #using colored cells.
    RESET = '\033[0m'
    START_COLOR = '\033[92m'  # Green
    END_COLOR = '\033[91m'  # Red
    PATH_COLOR = '\033[94m'  # Blue
    BLOCK_COLOR = '\033[90m'  # Gray
    FREE_COLOR = '\033[0m'  # Default
    
    # Initialize the grid with path
    grid_with_path = [['-' for _ in row] for row in grid]
    
    # Mark start and end positions
    if start:
        start_x, start_y = start
        grid_with_path[start_x][start_y] = 'S'  # Start position
    if end:
        end_x, end_y = end
        grid_with_path[end_x][end_y] = 'E'  # End position

    if path:
        # Mark the path
        for (x, y) in path:
            if (x, y) != path[0] and (x, y) != path[-1]:
                grid_with_path[x][y] = 'X'  # Path
    
    # Print the grid
    for i, row in enumerate(grid_with_path):
        for j, cell in enumerate(row):
            if (i, j) == start:
                print(f"{START_COLOR}S{RESET}", end=" ")
            elif (i, j) == end:
                print(f"{END_COLOR}E{RESET}", end=" ")
            elif (i, j) in path if path else False:
                print(f"{PATH_COLOR}X{RESET}", end=" ")
            elif grid[i][j] == 1:
                print(f"{BLOCK_COLOR}1{RESET}", end=" ")
            else:
                print(f"{FREE_COLOR}-{RESET}", end=" ")
        print()
        

def generate_moves(start, grid, grid_size):
    x_start, y_start = start
    one_step_moves = []
    two_step_moves = []

    for move_name_1, (dx1, dy1) in move_directions.items():
        new_x1, new_y1 = x_start + dx1, y_start + dy1
        if 0 <= new_x1 < grid_size and 0 <= new_y1 < grid_size and grid[new_x1][new_y1] != 1:
            one_step_moves.append(((x_start, y_start), (new_x1, new_y1), move_name_1))
            
            for move_name_2, (dx2, dy2) in move_directions.items():
                new_x2, new_y2 = new_x1 + dx2, new_y1 + dy2
                if 0 <= new_x2 < grid_size and 0 <= new_y2 < grid_size and grid[new_x2][new_y2] != 1:
                    two_step_moves.append(((x_start, y_start), (new_x2, new_y2), move_name_1, move_name_2))
    
    return one_step_moves, two_step_moves
        
        
"""
def print_path_and_steps(path, total_steps):
    #Print the path in a visually presentable way and the number of steps.
    if path is None:
        print("No path found.")
    else:
        print("Path:")
        for step in path:
            print(f"({step[0]}, {step[1]})", end=" -> ")
        print("End")
        print(f"Number of steps in the path: {len(path) - 1}")
        print(f"Total number of steps considered (including backtracking): {total_steps}")
"""


# =============================================================================
# Example usage
# =============================================================================
"""
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)
end = (4, 4)
# Define basic moves
basic_moves = ['move_right', 'move_down', 'move_left', 'move_up']
# Define recursive rules
recursive_rules = ['move_right', 'move_down', 'move_left', 'move_up']  # Can be populated with moves if needed
# Print the initial grid with obstacles, start, and end positions
print("Initial Grid:")
print_grid(grid, start=start, end=end)
# Find the path using pathfinding
path, total_steps = pathfinding(start, end, grid, basic_moves, recursive_rules)
# Print the path and the final grid with the path marked
print("Final Grid with Path:")
print_grid(grid, start=start, end=end, path=path)
print(*path, sep='->')
directions = compute_directions(path,move_mapping= move_directions)
print(*directions, sep='->')
"""

def parse_range(rng):
    """
    Parses a range string (like '1-2') into a list of numbers.
    If the input is a single number (like '1'), it returns a list containing that number.
    """
    if '-' in rng:
        start, end = map(int, rng.split('-'))
        return list(range(start, end + 1))
    else:
        return [int(rng)]

def convert_to_coordinates(grid_list):
    """
    Converts a list of lists, where each sublist can contain ranges and numbers,
    into a list of (x, y) coordinate tuples.
    """
    coordinates = []

    for x, row in enumerate(grid_list):
        for item in row:
            if isinstance(item, str) and '-' in item:
                # If the item is a range (e.g., '1-2'), parse it into individual numbers
                for y in parse_range(item):
                    coordinates.append((x, y))
            else:
                # If the item is a single number, add it as a coordinate
                coordinates.append((x, int(item)))

    return coordinates


def load_map_data(module_name, cordinates=True):
    module = __import__(module_name)
    grid = module.map
    start = 0
    end = 0
    if cordinates:
        start = module.start
        end = module.end
    return grid, start, end

# Iterate through each file and load the data
"""
for file in input_files:
    grid, start, end = load_map_data(file)
    
    # Display the map, start, and end positions
    print(f"Data from {file}.py")
    print("Grid:")
    for row in grid:
        print(row)
    print(f"Start position: {start}")
    print(f"End position: {end}\n")
"""



def round_to_nearest_step(number,step):
    return round(number / step) * step

def find_actions_file(folder_path):
    """Generate the file name by concatenating folder name with 'ACTIONS' and find the file."""
    # Get the last component of the folder path as the folder name
    folder_name = os.path.basename(folder_path)
    # Concatenate the folder name with 'ACTIONS' to generate the file name
    actions_file_name = folder_name + "_ACTIONS"
    # Construct the full path to the actions file
    actions_file_path = os.path.join(folder_path, actions_file_name)
    
    # Check if the constructed file path exists
    if os.path.isfile(actions_file_path):
        return actions_file_path
    return None

def extract_start_end_coordinates(file_path,step):
    """Extract the coordinates from the start and end 'move' commands in the file."""
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()] 
        moves = [line.split() for line in lines if "move" in line]
        start_x = round_to_nearest_step(float(moves[0][-1]),step)
        start_y = round_to_nearest_step(float(moves[0][2]),step)
        end_x = round_to_nearest_step(float(moves[1][-1]),step)
        end_y = round_to_nearest_step(float(moves[1][2]),step)
        return (start_x,start_y), (end_x,end_y)
    




def pathgeneration(start, end, grid):
    """Perform BFS to find the shortest path and count all steps including backtracking."""
    queue = deque([(start, [start], [])])  # Queue now holds the current path and the directions
    visited = set()
    visited.add(start)
    total_steps = 0  # Count all steps including backtracking

    while queue:
        current, path, directions = queue.popleft()
        x, y = current
        total_steps += 1  # Count each step processed

        if current == end:
            return path, directions, total_steps
        
        # Define movement directions including diagonal moves
        moves = [
            (0, 1, 'move_east'),       # move_right
            (1, 0, 'move_south'),      # move_down
            (0, -1, 'move_west'),      # move_left
            (-1, 0, 'move_north'),     # move_up
            (1, 1, 'move_south_east'), # move_down_right
            (1, -1, 'move_south_west'),# move_down_left
            (-1, 1, 'move_north_east'),# move_up_right
            (-1, -1, 'move_north_west')# move_up_left
        ]
        
        for dx, dy, move_name in moves:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(new_x, new_y, grid) and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.append(((new_x, new_y), path + [(new_x, new_y)], directions + [move_name]))

    return None, None, total_steps  # No path found


def print_path_and_steps_example(path, total_steps, idx=None):
    """Print the path using directions and the number of steps."""
    #print(total_steps)
    example = "move(a_"+str(idx)+",b_"+str(idx)+")"
    facts = []
    directions_path = []
    if path is None:
        print("No path found.")
    else:
        #print("Path using directions:")
        count = 0
        
        for count_c, next_coord in enumerate(path[0:-1]):
            move_direction = get_direction(next_coord, path[count_c+1])
            if count==0:
                facts.append(f"{move_direction}({hash_fn(count).lower()}{"_"+str(idx)}, {hash_fn(count+2).lower()}{"_"+str(idx)})")
                directions_path.append(f"{move_direction}")
                count=2
            else:
                if count<total_steps-1:
                    facts.append(f"{move_direction}({hash_fn(count).lower()}{"_"+str(idx)}, {hash_fn(count+1).lower()}{"_"+str(idx)})")
                    directions_path.append(f"{move_direction}")
                    count=count+1
                else:
                    facts.append(f"{move_direction}({hash_fn(count).lower()}{"_"+str(idx)}, {hash_fn(1).lower()}{"_"+str(idx)})")
                    directions_path.append(f"{move_direction}")
    return facts, directions_path, example



def get_direction(start, end):
    """Determine the direction based on the start and end letters."""
    #start_idx = letter_to_index(start)
    #end_idx = letter_to_index(end)
    
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    if dx == 0 and dy == 1:
        return "move_east"
    elif dx == 0 and dy == -1:
        return "move_west"
    elif dx == -1 and dy == 0:
        return "move_north"
    elif dx == 1 and dy == 0:
        return "move_south"
    elif dx == -1 and dy == 1:
        return "move_north_east"
    elif dx == -1 and dy == -1:
        return "move_north_west"
    elif dx == 1 and dy == 1:
        return "move_south_east"
    elif dx == 1 and dy == -1:
        return "move_south_west"
    else:
        return "unknown"
    
    
