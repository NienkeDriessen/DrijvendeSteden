from cell_finder import find_cells, show_results

if __name__== "__main__" :
    extracted_cells, img = find_cells('resources/grid_with_buildings.png')
    show_results(img, extracted_cells)