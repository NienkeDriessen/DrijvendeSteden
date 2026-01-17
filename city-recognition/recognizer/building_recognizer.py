from .color_recognizer import get_color
from .util import debug_show
# TODO: recognize a building based on its color
def recognize_building(building):
    color = get_color(building)
    building = color 
    return building


def recognize_buildings(buildings, show_debug=False):
    recognized_buildings = {}
    for coords, building in buildings.items():      
        recognized_building = recognize_building(building)
        recognized_buildings[coords] = recognized_building
    
    # recognized buildings is a dict with coordinates as keys and values as recognized building (currently just color)
    return recognized_buildings


