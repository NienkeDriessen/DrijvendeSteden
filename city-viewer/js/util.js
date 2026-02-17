const DEFAULT_DEV_API_BASE = 'http://localhost:5050/DrijvendeSteden/recognition';
const DEFAULT_PROD_API_BASE = '/DrijvendeSteden/recognition';

const configuredApiBase = import.meta.env?.VITE_API_BASE_URL
  || (import.meta.env?.PROD ? DEFAULT_PROD_API_BASE : DEFAULT_DEV_API_BASE);

const normalizedBase = configuredApiBase.endsWith('/')
  ? configuredApiBase.slice(0, -1)
  : configuredApiBase;

const apiBase = normalizedBase.startsWith('http://') || normalizedBase.startsWith('https://')
  ? normalizedBase
  : `${window.location.origin}${normalizedBase}`;

const API_URL = `${apiBase}/api`;

export async function getCityIDs() {
  const res = await fetch(`${API_URL}/viewer/ids`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function loadCityData(slotId) {
  const res = await fetch(`${API_URL}/viewer/city/${slotId}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function load_city_definition() {
  const raw = window.location.hash.slice(1);
  const slotId = raw || '1';

  const cityData = await loadCityData(slotId);
  if (!cityData || !cityData.grid_data) {
    console.warn(`No city data found for slot: ${slotId}`);
    return { city_definition: {}, numCols: -1, numRows: -1 };
  }

  const city_definition = {};
  let numCols = -1;
  let numRows = -1;

  const data = cityData.grid_data;
  for (const key in data) {
    const coords = parseCoords(key);
    if (coords[0] > numRows) numRows = coords[0];
    if (coords[1] > numCols) numCols = coords[1];
    city_definition[coords] = data[key];
  }

  return { city_definition, numCols, numRows };
}

function parseCoords(key) {
  const raw = key.startsWith('(') && key.endsWith(')')
    ? key.slice(1, -1)
    : key;
  return raw.split(',').map((part) => parseInt(part.trim(), 10));
}
