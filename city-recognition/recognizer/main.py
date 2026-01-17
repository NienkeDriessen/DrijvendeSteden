import cv2
from .building_finder import find_buildings
from .building_recognizer import recognize_buildings
from .grid_builder import build_grid
from .city_recognizer import recognize_city
from .util import debug_show

# This is only used for local debugging
if __name__== "__main__" :
    debug_image_path = 'recognizer/resources/test_dag_fotos/foto_3_witte_achtergrond.jpeg'
    # debug_image_path = 'recognizer/resources/stad1.png'
    print("Debugging city recognizer with image:", debug_image_path)
    show_debug = True

    grid = recognize_city(debug_image_path, show_debug)
