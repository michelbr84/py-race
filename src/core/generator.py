
import random
from src.data import maps

def generate_map(seed):
    """
    Generates a procedural map based on the given seed.
    Updates maps.map_1 and maps.map_1_rot in place.
    """
    try:
        random.seed(int(seed))
    except ValueError:
        # If seed is not an integer (e.g. text), use hash
        random.seed(seed)
    
    # 1. Initialize grid with "Grass"/Null (5)
    # 5 is null/grass in maps.py
    grid_size = 10
    new_map = [[5 for _ in range(grid_size)] for _ in range(grid_size)]
    new_rot = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    # 2. Random Walk Algorithm to build a connected track
    # Start in the middle
    x, y = 5, 5
    
    # 0=crossing, 1=straight, 2=turn, 3=split, 4=deadend, 5=null
    # To simplify, we will essentially place random valid road pieces.
    # A true coherent racing track is hard to generate perfectly with simple random walk blocks.
    # Strategy: Place a lot of road tiles (1, 2, 3, 0) randomly but connected.
    
    max_steps = 60
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    # Ensure start point is a crossing or split to allow options
    new_map[y][x] = 0 # Crossing
    
    current_x, current_y = x, y
    
    for _ in range(max_steps):
        # Pick a random direction
        dx, dy = random.choice(directions)
        
        # Move
        next_x, next_y = current_x + dx, current_y + dy
        
        # Check bounds
        if 0 <= next_x < grid_size and 0 <= next_y < grid_size:
            current_x, current_y = next_x, next_y
            
            # If empty, pick a random road type (0-4)
            # biased towards straight (1) and turns (2)
            if new_map[current_y][current_x] == 5:
                tile_type = random.choices([0, 1, 2, 3, 4], weights=[5, 40, 40, 5, 10], k=1)[0]
                rot = random.randint(0, 3)
                
                new_map[current_y][current_x] = tile_type
                new_rot[current_y][current_x] = rot
    
    # Update the global maps data
    maps.map_1 = new_map
    maps.map_1_rot = new_rot
    
    # Ensure traffic is reset or aware of new map?
    # Traffic spawns using road_tile() which reads maps.map_1, so it should be fine.
    
    print(f"Map generated with seed: {seed}")
