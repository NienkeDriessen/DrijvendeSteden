import cv2
from .building_finder import find_buildings
from .building_recognizer import recognize_buildings
from .grid_builder import build_grid

def recognize_city(file_path):
    img = cv2.imread(file_path)
    buildings = find_buildings(img)
    recognized_buildings = recognize_buildings(buildings)
    building_grid = build_grid(recognized_buildings)
    return building_grid
