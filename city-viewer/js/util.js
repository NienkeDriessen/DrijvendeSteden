async function loadCityData(cityId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/city/${cityId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading city data:', error);
        return null;
    }
}

export async function load_city_definition() {
    const urlHash = window.location.hash;
    let id = urlHash ? urlHash.slice(1) : '1'; // Default to ID 1 if no hash

    // Remove any query parameters from the hash
    id = id.split('?')[0];

    // Convert id to string
    id = String(id);

    const cityData = await loadCityData(id);
    if (!cityData || !cityData.grid_data) {
        console.warn(`No city data found for ID: ${id}`);
        return { city_definition: {}, numCols: -1, numRows: -1 };
    }

    let city_definition = {};
    let numCols = -1;
    let numRows = -1;

    const data = cityData.grid_data;

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
    try {
        const response = await fetch('http://127.0.0.1:5000/api/ids');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const cities = await response.json();  // now an array of {id, name, upload_date}
        return cities;
    } catch (error) {
        console.error('Error loading city IDs:', error);
        return [];
    }
}