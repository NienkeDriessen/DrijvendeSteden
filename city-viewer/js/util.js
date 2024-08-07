import { initializeApp } from 'firebase/app';
import { getDatabase, ref, get } from "firebase/database";

const firebaseConfig = {
    databaseURL: "https://drijvendesteden-default-rtdb.europe-west1.firebasedatabase.app/",
};

const app = initializeApp(firebaseConfig);

export async function load_city_definition() {
    
    let data = await retrieveData()
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

async function retrieveData() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id = urlParams.get('id')

    const database = getDatabase(app);

    const dataRef = ref(database, 'data/' + id);

    try {
        // Fetch the data
        const snapshot = await get(dataRef);

        if (snapshot.exists()) {
            return snapshot.val();
        } else {
            console.log("Key was not found")
            return null;
        }
    } catch (error) {
        // Handle any errors
        console.error('Error retrieving data:', error);
        return null;
    }
    
}

function parseCoords(key) {
    let parts = key.slice(1, -1).split(',');
    let coord = parts.map(part => parseInt(part.trim()));
    return coord;
}