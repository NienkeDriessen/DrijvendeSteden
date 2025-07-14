// ← add your API_USER/API_PASS here (or import from a config module)
const API_USER = 'admin';
const API_PASS = 'secret';
const API_BASE = 'http://127.0.0.1:5000';
const AUTH_HEADER = 'Basic ' + btoa(`${API_USER}:${API_PASS}`);

// 1) fetch only the latest‐20 viewer slots
export async function getCityIDs() {
    const res = await fetch(`${API_BASE}/api/viewer/ids`, {
        headers: { 'Authorization': AUTH_HEADER }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    console.log(res);
    return res.json();  // -> [{slot_id, name, upload_date},…]
}


// 2) load a single slot’s full data
async function loadCityData(slotId) {
    const res = await fetch(`${API_BASE}/api/viewer/city/${slotId}`, {
        headers: { 'Authorization': AUTH_HEADER }
    });
    console.log(res);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();  // -> {slot_id,main_id,name,upload_date,grid_data}
}

export async function load_city_definition() {
    // normalize the hash into a pure numeric slot ID
    const raw = window.location.hash.slice(1); // e.g., "1", "15", etc.
    let slotId = raw || '1'; // Use the hash value, or default to '1'

    const cityData = await loadCityData(slotId);
    console.log('💾 raw cityData.grid_data:', cityData.grid_data);

    if (!cityData || !cityData.grid_data) {
        console.warn(`No city data found for slot: ${slotId}`);
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