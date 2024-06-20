import cv2
from building_finder import find_buildings
from building_recognizer import recognize_buildings
from grid_builder import build_grid

if __name__== "__main__" :
    img = cv2.imread('resources/stad1.png')
    buildings = find_buildings(img)
    recognized_buildings = recognize_buildings(buildings)
    building_grid = build_grid(recognized_buildings)
    
