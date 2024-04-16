from hexagon_finder import find_hexagons
from building_matcher import match_buildings
from digital_grid_builder import build_hexagon_grid

if __name__== "__main__" :
    hexagons, img = find_hexagons('resources/city2_greenscreen.png', show_results=False)

    # for cell in extracted_cells.values():
    #     match_buildings(cell)

    hexagon_grid = build_hexagon_grid(hexagons.keys(), img)
    
