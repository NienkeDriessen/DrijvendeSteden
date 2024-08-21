import * as THREE from 'three';
import { ModelManager } from './modelmanager';
import { load_city_definition } from './util';


export async function createCity(scene) {
    const padding = 0.2;
    const hex_size = 3;

    const horizontal_distance = (hex_size + padding) * 1.5;
    const vertical_distance = (hex_size + padding) * Math.sqrt(3);
    const vertical_offset = (hex_size + padding) * (Math.sqrt(3) / 2); 

    const { city_definition, numRows, numCols } = await load_city_definition()

    const city = new THREE.Group();

    const modelManager = new ModelManager();
    await modelManager.loadModels();

    for (let row = 0; row < numRows; row++) {
        for (let col = 0; col < numCols; col++) {

            if ([row,col] in city_definition){
                const color = city_definition[[row, col]];
                const model = modelManager.getModel(color);

                let x = row * horizontal_distance;
                let z = col * vertical_distance;

                if (row % 2 !== 0) {
                    z += vertical_offset;
                }

                const hexagon = createHexagon(hex_size, model, color)
                hexagon.position.set(x, 0, z);
                city.add(hexagon)
            }
            
        }
    }

    scene.add(city)
    return city
}



function createHexagon(hex_size, model, color) {
    const hexagon = new THREE.Group();

    // Create the platform:
    const height = 1;
    const radialSegments = 6;

    const geometry = new THREE.CylinderGeometry( hex_size, hex_size, height, radialSegments, 1, false, Math.PI / 2 );         
    const materialTop = new THREE.MeshBasicMaterial({ color: 0x888888 });
    const materialSide = new THREE.MeshBasicMaterial({ color: 0xaaaaaa });

    const materials = [
        materialSide,
        materialTop,
        materialTop
    ];
    const platform = new THREE.Mesh( geometry, materials );

    hexagon.add(platform)
    
    // Add the model on top of the platform:
    hexagon.add(model)

    return hexagon;
}
