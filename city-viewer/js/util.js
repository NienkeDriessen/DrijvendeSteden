import data from '/public/building_grid.json';

export function load_city_definition() {
    let city_definition = {};
    let numCols = -1;
    let numRows = -1;
    for (let key in data) {
        const coords = parseCoords(key);
        if (coords[0] > numRows)
            numRows = coords[0]
        if (coords[1] > numCols)
            numCols = coords[1]

        city_definition[coords] = data[key];
    }
    return { city_definition, numCols, numRows }
}

function parseCoords(key) {
    let parts = key.slice(1, -1).split(',');
    let coord = parts.map(part => parseInt(part.trim()));
    return coord;
}