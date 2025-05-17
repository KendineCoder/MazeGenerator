#!/usr/bin/env python3
import random
import json
import math


def generate_maze_json(grid_size=20, cell_size=12, base_x=100, base_y=100, wall_start_height=20, wall_scale_factor=1.5, wall_spacing=0.8):

    maze = [[[1, 1, 1, 1] for _ in range(grid_size)] for _ in range(grid_size)]

    visited = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    stack = []

    start_x, start_y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
    stack.append((start_x, start_y))
    visited[start_y][start_x] = True

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    while stack:
        x, y = stack[-1]

        neighbors = []
        for i, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[ny][nx]:
                neighbors.append((nx, ny, i))

        if neighbors:
            nx, ny, direction = random.choice(neighbors)

            if direction == 0:
                maze[y][x][0] = 0
                maze[ny][nx][2] = 0
            elif direction == 1:
                maze[y][x][1] = 0
                maze[ny][nx][3] = 0
            elif direction == 2:
                maze[y][x][2] = 0
                maze[ny][nx][0] = 0
            elif direction == 3:
                maze[y][x][3] = 0
                maze[ny][nx][1] = 0

            visited[ny][nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()

    entrance_x = random.randint(0, grid_size - 1)
    maze[0][entrance_x][0] = 0

    exit_x = random.randint(0, grid_size - 1)
    maze[grid_size - 1][exit_x][2] = 0

    json_objects = []

    adjusted_wall_length = cell_size * wall_spacing

    for y in range(grid_size):
        for x in range(grid_size):
            current_x = base_x + (x * cell_size)
            current_y = base_y + (y * cell_size)
            end_x = current_x + cell_size
            end_y = current_y + cell_size

            offset_x = (cell_size - adjusted_wall_length) / 2
            offset_y = (cell_size - adjusted_wall_length) / 2

            # North wall
            if maze[y][x][0] == 1:
                wall_obj = create_wall_object(
                    current_x + offset_x,
                    current_y,
                    wall_start_height,
                    90,
                    [wall_spacing, 1.0, wall_scale_factor]
                )
                json_objects.append(wall_obj)

            # East wall
            if maze[y][x][1] == 1:
                wall_obj = create_wall_object(
                    end_x,
                    current_y + offset_y,
                    wall_start_height,
                    0,
                    [1.0, wall_spacing, wall_scale_factor]
                )
                json_objects.append(wall_obj)

            # South wall
            if maze[y][x][2] == 1:
                wall_obj = create_wall_object(
                    current_x + offset_x,
                    end_y,
                    wall_start_height,
                    90,
                    [wall_spacing, 1.0, wall_scale_factor]
                )
                json_objects.append(wall_obj)

            # West wall
            if maze[y][x][3] == 1:
                wall_obj = create_wall_object(
                    current_x,
                    current_y + offset_y,
                    wall_start_height,
                    0,
                    [1.0, wall_spacing, wall_scale_factor]
                )
                json_objects.append(wall_obj)

    perimeter_objects = create_perimeter_battlements(base_x, base_y, grid_size, cell_size, wall_start_height, entrance_x,
                                                     exit_x, wall_scale_factor)
    json_objects.extend(perimeter_objects)

    return json_objects


def create_wall_object(x, y, z, rotation, scale=[1.0, 1.0, 1.0]):
    angle_rad = math.radians(rotation)
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)

    return {
        "type": "prop",
        "id": 611,
        "garbage": "0x433f4bc",
        "rotation_matrix": [
            [cos_val, -sin_val, 0.0],
            [sin_val, cos_val, 0.0],
            [0.0, 0.0, 1.0]
        ],
        "pos": [x, y, z],
        "str": "spr_arabian_wall_a",
        "entry_no": 0,
        "menu_entry_no": 0,
        "scale": scale
    }


def create_battlement_object(x, y, z, rotation_degrees, scale_factor=1.0):
    angle_rad = math.radians(rotation_degrees)
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)

    return {
        "type": "prop",
        "id": 611,
        "garbage": "0x433f4bc",
        "rotation_matrix": [
            [cos_val, -sin_val, 0.0],
            [sin_val, cos_val, 0.0],
            [0.0, 0.0, 1.0]
        ],
        "pos": [x, y, z],
        "str": "spr_castle_e_battlement_a",
        "entry_no": 0,
        "menu_entry_no": 0,
        "scale": [1.0, 1.0, scale_factor]
    }


def create_perimeter_battlements(base_x, base_y, grid_size, cell_size, wall_height, entrance_x, exit_x,
                                 scale_factor=1.0):
    perimeter_objects = []

    maze_width = grid_size * cell_size
    maze_height = grid_size * cell_size

    battlement_height = wall_height + 2

    min_x = base_x
    min_y = base_y
    max_x = base_x + maze_width
    max_y = base_y + maze_height

    battlement_spacing = int(cell_size * 1.2)

    # North wall
    for x_pos in range(min_x, max_x + 1, battlement_spacing):
        entrance_pos_x = base_x + (entrance_x * cell_size)
        if not (x_pos >= entrance_pos_x - cell_size / 2 and x_pos <= entrance_pos_x + cell_size / 2):
            battlement = create_battlement_object(
                x_pos,
                min_y,
                battlement_height,
                180,

            )
            perimeter_objects.append(battlement)

    # South wall
    for x_pos in range(min_x, max_x + 1, battlement_spacing):
        exit_pos_x = base_x + (exit_x * cell_size)
        if not (x_pos >= exit_pos_x - cell_size / 2 and x_pos <= exit_pos_x + cell_size / 2):
            battlement = create_battlement_object(
                x_pos,
                max_y,
                battlement_height,
                0,

            )
            perimeter_objects.append(battlement)

    # West wall
    for y_pos in range(min_y, max_y + 1, battlement_spacing):
        battlement = create_battlement_object(
            min_x,
            y_pos,
            battlement_height,
            90,

        )
        perimeter_objects.append(battlement)

    # East wall
    for y_pos in range(min_y, max_y + 1, battlement_spacing):
        battlement = create_battlement_object(
            max_x,
            y_pos,
            battlement_height,
            270,

        )
        perimeter_objects.append(battlement)
    return perimeter_objects


def create_rotation_matrix(angle_degrees):
    angle_rad = math.radians(angle_degrees)
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)

    return [
        [cos_val, -sin_val, 0.0],
        [sin_val, cos_val, 0.0],
        [0.0, 0.0, 1.0]
    ]


def save_maze_to_json(filename, maze_json):
    with open(filename, 'w') as f:
        json.dump(maze_json, f, indent=2)
    print(f"Maze JSON saved to {filename}")


if __name__ == "__main__":

    try:
        grid_size = int(input("Enter maze grid size (default 30): ") or 40)
        cell_size = int(input("Enter cell size in game units (default 12): ") or 10)
        base_x = int(input("Enter base X coordinate (default 100): ") or 100)
        base_y = int(input("Enter base Y coordinate (default 100): ") or 100)
        wall_height = int(input("Enter wall height (default 0): ") or 0)
        wall_scale_factor = float(input("Enter wall scale factor (default 1.5): ") or 1.8)
        wall_spacing = float(input("Enter wall spacing factor (default 0.8): ") or 0.8)
        output_file = input("Enter output filename (default 'mission_objects.json'): ") or "mission_objects.json"

    except ValueError:
        print("Invalid input, using default values")
        grid_size = 20
        cell_size = 12
        base_x = 100
        base_y = 100
        wall_height = 20
        wall_scale_factor = 1.5
        wall_spacing = 0.8
        existing_file = ""
        output_file = "warband_maze.json"

    maze_json = generate_maze_json(grid_size, cell_size, base_x, base_y, wall_height, wall_scale_factor,
                                   wall_spacing)

    save_maze_to_json(output_file, maze_json)

    print("\nMaze generation complete!")
    print(f"Maze size: {grid_size}x{grid_size}, Total cells: {grid_size * grid_size}")
    print(f"Total objects: {len(maze_json)}")
    print(f"Wall height: {wall_height} units with scale factor: {wall_scale_factor}")
    print(f"Wall spacing factor: {wall_spacing} (lower = more space between walls)")
    print(f"Complete maze JSON saved to {output_file}")