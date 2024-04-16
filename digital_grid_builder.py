import math
import cv2 

def build_hexagon_grid(coordinates, img):
    adjacent_hexagon = find_adjacent_hexagon(coordinates)

    for coord_pair in adjacent_hexagon:
        cv2.line(img, coord_pair[0], coord_pair[1], (0, 255, 0), 2)

    show_image(img)
    
def find_adjacent_hexagon(coordinates, filter_threshold = 0.1):
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

def calculate_distance(coord1, coord2):
    return math.sqrt(pow((coord1[0] - coord2[0]), 2) + pow((coord1[1] - coord2[1]), 2))

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