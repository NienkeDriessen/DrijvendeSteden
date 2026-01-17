import cv2
from .building_finder import  find_buildings
from .building_recognizer import recognize_buildings
from .grid_builder import build_grid
from .util import debug_show

def recognize_city(file_path, show_debug=False):
    img = cv2.imread(file_path)
    
    buildings = find_buildings(img, show_debug)

    
    recognized_buildings = recognize_buildings(buildings, show_debug)
    if not recognized_buildings:
        return None
    building_grid = build_grid(recognized_buildings)
    return building_grid
