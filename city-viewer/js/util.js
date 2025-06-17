import Papa from 'papaparse';

async function loadCSVData() {
    try {
        const response = await fetch('city_data.csv');
        const csvText = await response.text();
        const result = Papa.parse(csvText, { header: true }); // Removed dynamicTyping
        return result.data;
    } catch (error) {
        console.error('Error reading CSV file:', error);
        return null;
    }
}

export async function load_city_definition() {
    const csvData = await loadCSVData();
    if (!csvData) {
        return { city_definition: {}, numCols: -1, numRows: -1 };
    }

    const urlHash = window.location.hash;
    let id = urlHash ? urlHash.slice(1) : '1'; // Default to ID 1 if no hash

    // Convert id to string
    id = String(id);

    let city_definition = {};
    let numCols = -1;
    let numRows = -1;

    // Find the correct row in the CSV data based on the ID
    let gridDataRow = csvData.find(row => row.id === id);

    if (!gridDataRow) {
        console.warn(`No city data found for ID: ${id}`);
        return { city_definition: {}, numCols: -1, numRows: -1 };
    }

    let gridDataString = gridDataRow.grid_data;

    // Parse the grid data string into an object
    const data = JSON.parse(gridDataString.replace(/'/g, "\""));

    for (let key in data) {
        const coords = parseCoords(key);
        if (coords[0] > numRows)
            numRows = coords[0]
        if (coords[1] > numCols)
            numCols = coords[1]

        city_definition[coords] = data[key];
    }
    return { city_definition, numCols, numRows };
}

function parseCoords(key) {
    let parts = key.slice(1, -1).split(',');
    let coord = parts.map(part => parseInt(part.trim()));
    return coord;
}

export async function getCityIDs() {
    const csvData = await loadCSVData();
    if (!csvData) {
        return [];
    }

    const ids = csvData.map(row => row.id);
    return ids;
}