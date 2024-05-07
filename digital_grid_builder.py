import math
import cv2 
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def build_hexagon_grid(coordinates, img):
    # Find all the direct neighbours
    adjacent_hexagon = find_adjacent_hexagon(coordinates)
    print(adjacent_hexagon)

    # Create an anchor to serve as a starting point
    anchor = find_anchor(adjacent_hexagon)

    # Find all direct neighbours of the anchor
    anchor_neighbours = find_neighbours(adjacent_hexagon, anchor)

    # Calculate a rotation angle which aligns the hexagons
    angle = find_rotation_angle(anchor, anchor_neighbours)

    # Rotate all the coordinates around the anchor
    new_coords = rotate_points_around_anchor(coordinates, anchor, angle, img)

    # Recursively create a grid starting at the anchor
    virtual_coords = {anchor : (250, 250)}
    visited = [anchor]
    odd_or_even = {anchor : False}
    virtual_coords = create_hexagon_grid(anchor, new_coords, adjacent_hexagon, virtual_coords, visited, odd_or_even)

    # This grid contains virtual coordinates pointing to original coordinates (which serve as keys)
    grid = normalize_virtual_coords(virtual_coords, anchor)

    # Replace this with the code to generate 3d models:
    draw_grid(grid)

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
            virtual_coords[nb] = (virtual_x if odd else virtual_x - 1, virtual_y + 1)
            odd_or_even[nb] = not odd
        # South Neighbour
        elif angle > (1/3) * math.pi and angle <= (2/3) * math.pi:
            virtual_coords[nb] = (virtual_x - 1, virtual_y)
            odd_or_even[nb] = odd
        # South West Neighbour
        elif angle > (2/3) * math.pi and angle <= math.pi:
            virtual_coords[nb] = (virtual_x if odd else virtual_x - 1, virtual_y - 1)
            odd_or_even[nb] = not odd
        # North East Neighbour
        elif angle < 0 and angle >= -math.pi / 3:
            virtual_coords[nb] = (virtual_x + 1 if odd else virtual_x, virtual_y + 1)
            odd_or_even[nb] = not odd
        # North Neighbour
        elif angle < -(1/3) * math.pi and angle >= -(2/3) * math.pi:
            virtual_coords[nb] = (virtual_x + 1, virtual_y)
            odd_or_even[nb] = odd
        # North West Neighbour
        elif angle < -(2/3) * math.pi and angle >= -math.pi:
            virtual_coords[nb] = (virtual_x + 1 if odd else virtual_x, virtual_y - 1)
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
    return adjacent_hexagon

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

def rotate_point(coord, angle):
    x, y = coord
    rotated_x = x * np.cos(-angle) - y * np.sin(-angle)
    rotated_y = x * np.sin(-angle) + y * np.cos(-angle)
    return rotated_x, rotated_y

def rotate_points_around_anchor(coordinates, anchor, angle, img):
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



# Temporary code to display images:
def show_image(img):
    img_copy = img.copy()
    resized = resize_img(img_copy)
    cv2.imshow('shapes', resized) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize_img(raw_img, target_size = 800):
   h, w = raw_img.shape[:2]
   ratio = min(target_size / w, target_size / h)
   resized = cv2.resize(raw_img, (int(w * ratio), int(h * ratio)))
   return resized

# Temporary code to draw the hexagon:
def draw_hexagon(ax, center, size):
    angles = np.linspace(0, 2*np.pi, 7)
    x = center[0] + size * np.cos(angles)
    y = center[1] + size * np.sin(angles)
    ax.fill(x, y, edgecolor='black', linewidth=1, facecolor='lightgray')

def draw_grid(grid, hex_size = 1.0):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_axis_off()
    for row in range(50):
        for col in range(50):
            if (row, col) in grid.keys():
                x = col * 3/2 * hex_size
                y = row * np.sqrt(3) * hex_size
                if col % 2 != 0:
                    y += np.sqrt(3) / 2 * hex_size
                draw_hexagon(ax, (x, y), hex_size)
                # text = str(grid[(row, col)]) + "\n->\n" + str((row, col))
                # ax.text(x, y, text, ha='center', va='center', color='black')

            
    plt.show()