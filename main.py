from cell_finder import find_cells, show_results
from building_matcher import match_buildings

if __name__== "__main__" :
    extracted_cells, img = find_cells('resources/grid_with_buildings.png')
    # show_results(img, extracted_cells)

    for cell in extracted_cells.values():
        match_buildings(cell)
    
