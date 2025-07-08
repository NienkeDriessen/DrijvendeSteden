// ← add your API_USER/API_PASS here (or import from a config module)
const API_USER = 'admin';
const API_PASS = 'secret';
const API_BASE = 'http://127.0.0.1:5000';
const AUTH_HEADER = 'Basic ' + btoa(`${API_USER}:${API_PASS}`);

async function loadCityData(cityId) {
    console.log(`→ fetching city ${cityId} from ${API_BASE}/api/city/${cityId}`);
    const res = await fetch(`${API_BASE}/api/city/${cityId}`, {
        headers: { 'Authorization': AUTH_HEADER }
    });
    console.log('← status', res.status);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const body = await res.json();
    console.log('← payload', body);
    return body;
}

export async function load_city_definition() {
    // normalize the hash into a pure numeric ID
    const raw = window.location.hash.slice(1); // e.g. "2" or "?id=2"
    let id = '1';                               // default

    if (raw.startsWith('?')) {
        // parse "?id=2"
        const params = new URLSearchParams(raw.slice(1));
        id = params.get('id') || id;
    } else if (raw) {
        // parse "2"
        id = raw;
    }

    const cityData = await loadCityData(id);
    console.log('💾 raw cityData.grid_data:', cityData.grid_data);

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
    // strip parentheses if present
    const raw = key.startsWith('(') && key.endsWith(')') 
      ? key.slice(1, -1) 
      : key;
    const parts = raw.split(',');
    return parts.map(p => parseInt(p.trim(), 10));
}

export async function getCityIDs() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/ids', {
            headers: { 'Authorization': AUTH_HEADER }
        });
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