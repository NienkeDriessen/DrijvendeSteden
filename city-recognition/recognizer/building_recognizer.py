from .color_recognizer import get_color

# TODO: recognize a building based on its color
def recognize_building(building):
    color = get_color(building)
    building = color 
    return building


def recognize_buildings(buildings):
    recognized_buildings = {}
    for coords, building in buildings.items():      
        recognized_building = recognize_building(building)
        recognized_buildings[coords] = recognized_building
    
    return recognized_buildings


