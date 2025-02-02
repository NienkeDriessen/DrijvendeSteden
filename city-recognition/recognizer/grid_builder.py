import math
from collections import Counter
import numpy as np

def build_grid(recognized_buildings):
    coordinates = recognized_buildings.keys()

    # Find all the direct neighbours
    adjacent_hexagon, average_distance = find_adjacent_hexagon(coordinates)

    # Create an anchor to serve as a starting point
    anchor = find_anchor(adjacent_hexagon)

    # Find all direct neighbours of the anchor
    anchor_neighbours = find_neighbours(adjacent_hexagon, anchor)

    # Calculate a rotation angle which aligns the hexagons
    angle = find_rotation_angle(anchor, anchor_neighbours)

    # Rotate all the coordinates around the anchor
    new_coords = rotate_points_around_anchor(coordinates, anchor, angle)

    # Recursively create a grid starting at the anchor
    # The virtual coords are chosen in a way that we cannot get negative coordinates, they are later normalized
    virtual_coords = {anchor : (250, 250)}
    visited = [anchor]
    # Odd or even alternates per column of hexagon. This is because the x coordinate of certain neighbours (NW, NE, SW and SE) differs depending on the row.
    odd_or_even = {anchor : False}
    virtual_coords = create_hexagon_grid(anchor, new_coords, adjacent_hexagon, virtual_coords, visited, odd_or_even)

    # Although in theory there shouldn't be any disconnected parts, it can still happen that some hexagon are missed.
    # In case there are disconnected parts that are not found by the initial recursive pass, we try to approximate their location.
    while len(visited) < len(coordinates):
        unvisited = coordinates - visited
        sub_anchor = next(iter(unvisited))
        
        sa_coords, ooe = approximate_coords(sub_anchor, anchor, new_coords, average_distance)
        virtual_coords[sub_anchor] = sa_coords
        odd_or_even[sub_anchor] = ooe
        visited.append(sub_anchor)
        virtual_coords = create_hexagon_grid(sub_anchor, new_coords, adjacent_hexagon, virtual_coords, visited, odd_or_even)

    # This grid contains virtual coordinates pointing to original coordinates (which serve as keys)
    grid = normalize_virtual_coords(virtual_coords, anchor)

    final_grid = update_coords(recognized_buildings, grid)

    return final_grid

def create_hexagon_grid(current_hexagon, new_coords, adjacent_hexagon, virtual_coords, visited, odd_or_even):
    visited.append(current_hexagon)

    virtual_x, virtual_y = virtual_coords[current_hexagon]
    neighbours = find_neighbours(adjacent_hexagon, current_hexagon)

    # Calculate the virtual coordinates for each neighbour (that does not have coordinates yet)
    for nb in neighbours:
        if nb in virtual_coords.keys():
            continue

        angle = calculate_angle(new_coords[current_hexagon], new_coords[nb])
        odd = odd_or_even[current_hexagon]

        # South East Neighbour
        if angle > 0 and angle <= math.pi / 3:
            virtual_coords[nb] = (virtual_x + 1, virtual_y if odd else virtual_y + 1)
            odd_or_even[nb] = not odd
        # South Neighbour
        elif angle > (1/3) * math.pi and angle <= (2/3) * math.pi:
            virtual_coords[nb] = (virtual_x, virtual_y + 1)
            odd_or_even[nb] = odd
        # South West Neighbour
        elif angle > (2/3) * math.pi and angle <= math.pi:
            virtual_coords[nb] = (virtual_x - 1, virtual_y if odd else virtual_y + 1)
            odd_or_even[nb] = not odd
        # North East Neighbour
        elif angle < 0 and angle >= -math.pi / 3:
            virtual_coords[nb] = (virtual_x + 1, virtual_y - 1 if odd else virtual_y)
            odd_or_even[nb] = not odd
        # North Neighbour
        elif angle < -(1/3) * math.pi and angle >= -(2/3) * math.pi:
            virtual_coords[nb] = (virtual_x, virtual_y - 1)
            odd_or_even[nb] = odd
        # North West Neighbour
        elif angle < -(2/3) * math.pi and angle >= -math.pi:
            virtual_coords[nb] = (virtual_x - 1, virtual_y - 1 if odd else virtual_y)
            odd_or_even[nb] = not odd
        else:
            raise Exception("Angle is not within the boundaries of pi")
    
    # Recursively go through unvisited neighbours
    for nb in neighbours:
        if nb not in visited:
            virtual_coords = create_hexagon_grid(nb, new_coords, adjacent_hexagon, virtual_coords, visited, odd_or_even)

    return virtual_coords

def normalize_virtual_coords(virtual_coords, anchor):
    smallest_x = math.inf
    smallest_y = math.inf

    for coords in virtual_coords.values():
        x, y = coords
        if x < smallest_x:
            smallest_x = x
        if y < smallest_y:
            smallest_y = y

    # This makes sure that the anchor is in an "odd" row
    if (virtual_coords[anchor][1] - smallest_y) % 2 == 1:
        smallest_y-=1

    result = {}
    for key, v_coords in virtual_coords.items():
        x, y = v_coords
        result[x - smallest_x, y - smallest_y] = key

    return result

def update_coords(recognized_buildings, grid):
    final_grid = {}
    for new_coords, old_coords in grid.items():
        # print(new_coords)
        # print(old_coords)
        final_grid[str(new_coords)] = recognized_buildings[old_coords]

    return final_grid

# Adjacent hexagon are found based on the distance between the coordinates.
# We first look at the smallest distance between any coordinates and then determine neighbours based on this distance.
# The filter_threshold determines how much the distance is allowed to be different as opposed to the smallest distance
def find_adjacent_hexagon(coordinates, filter_threshold = 0.6):
    smallest_distance = math.inf
    distances = {}

    for i, coord1 in enumerate(coordinates):
        for coord2 in list(coordinates)[i+1:]:
            dist = calculate_distance(coord1, coord2)
            distances[(coord1, coord2)] = dist
            if dist < smallest_distance:
                smallest_distance = dist
    
    threshold = filter_threshold * smallest_distance
    adjacent_hexagon = [key for key, value in distances.items() if abs(value - smallest_distance) <= threshold]

    distance_sum = 0
    for key in adjacent_hexagon:
        distance_sum += distances[key]
    average_distance = distance_sum / len(adjacent_hexagon)

    return adjacent_hexagon, average_distance

def find_anchor(adjacent_hexagon):
    flat_list = [item for sublist in adjacent_hexagon for item in sublist]
    counter = Counter(flat_list)
    start,_ = counter.most_common(1)[0]
    return start

def find_neighbours(adjacent_hexagon, hex):
    neighbours = []
    for coord_pair in adjacent_hexagon:
        if coord_pair[0] == hex:
            neighbours.append(coord_pair[1])
        if coord_pair[1] == hex:
            neighbours.append(coord_pair[0])
        
    return neighbours

def calculate_distance(coord1, coord2):
    return math.sqrt(pow((coord1[0] - coord2[0]), 2) + pow((coord1[1] - coord2[1]), 2))

# Many functions that are used to rotate the image to make the recognition algorithm possible
# I think this approach brings some difficulties with it, especially because a small error can
# lead to much bigger errors on further hexagon.
#
# It is maybe better to scrap this and make sure that all pictures are correctly rotated before submitting it.
def rotate_point(coord, angle):
    x, y = coord
    rotated_x = x * np.cos(-angle) - y * np.sin(-angle)
    rotated_y = x * np.sin(-angle) + y * np.cos(-angle)
    return rotated_x, rotated_y

def rotate_points_around_anchor(coordinates, anchor, angle):
    translated_coords = [(x - anchor[0], y - anchor[1]) for x, y in coordinates]
    rotated_coords = [rotate_point(coord, angle) for coord in translated_coords]
    new_coords = [(int(x + anchor[0]), int(y + anchor[1])) for x,y in rotated_coords]
    result = {original: rotated for original, rotated in zip(coordinates, new_coords)}
    result[anchor] = anchor
    return result
        
def calculate_angle(anchor, point):
    dx = point[0] - anchor[0]
    dy = point[1] - anchor[1]
    return math.atan2(dy, dx)

def find_rotation_angle(anchor, neighbours):
    min_angle = float('inf')
    for nb in neighbours:
        angle = calculate_angle(anchor, nb)
        angle += math.pi/2
        if angle < 0:
            angle = -angle
        if angle > math.pi:
            angle -= math.pi

        if (angle < min_angle):
            min_angle = angle

    return min_angle

# Approximation function for disconnected parts.
def approximate_coords(sub_anchor, anchor, new_coords, average_distance):
    odd_or_even = False
    coords_a = new_coords[anchor]
    coords_b = new_coords[sub_anchor]
    distance_x = coords_b[0] - coords_a[0]
    distance_y = coords_b[1] - coords_a[1]

    dh = average_distance
    do = average_distance / 2
    dw = math.sqrt(pow(dh, 2) - pow(do, 2))

    width_shift = round(distance_x / dw)
    if width_shift % 2 != 0:
        odd_or_even = True
        if distance_y < 0:
            distance_y += do
        else:
            distance_y -= do

    height_shift = round(distance_y / dh)
    new_coords = (250 + width_shift, 250 + height_shift)

    return new_coords, odd_or_even
 