import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { load_city_definition } from './util';


export async function createCity(scene) {
    const padding = 0.2;
    const hex_size = 3;

    const horizontal_distance = (hex_size + padding) * 1.5;
    const vertical_distance = (hex_size + padding) * Math.sqrt(3);
    const vertical_offset = (hex_size + padding) * (Math.sqrt(3) / 2); 

    

    const { city_definition, numRows, numCols } = await load_city_definition()

    const city = new THREE.Group();

    // const loader = new GLTFLoader();
    //     loader.load( 'buildings/a5.gltf', function ( gltf ) {
            
    //         for (let row = 0; row < 5; row++) {
    //             for (let col = 0; col < 2; col++) {
    //                 const model = gltf.scene.clone();
    //                 let x = row * horizontal_distance;
    //                 let z = col * vertical_distance;
                    
    //                 if (row % 2 !== 0) {
    //                     z += vertical_offset;
    //                 }


    //                 const hexagon = createHexagon(hex_size, model, "WHITE")
    //                 hexagon.position.set(x, 0, z);
    //                 city.add(hexagon)

    //                 // if (col % 2 !== 0) {
    //                 //     z += horizontal_offset;
    //                 // }

    //                 // if ([row,col] in city_definition){
    //                 //     const model = gltf.scene.clone();

    //                 //     let x = col * vertical_distance;
    //                 //     let z = row * horizontal_distance;

    //                 //     if (col % 2 !== 0) {
    //                 //         z += horizontal_offset;
    //                 //     }

    //                 //     const hexagon = createHexagon(hex_size, model, "WHITE")
    //                 //     hexagon.position.set(x, 0, z);
    //                 //     city.add(hexagon)
    //                 // }
                    
    //             }
    //         }

    //     }, undefined, function ( error ) {
    //     console.error( error );
    // } );

    // TODO: Find a better way to load each model and then pass a clone to the createHexagon
    const loader = new GLTFLoader();
        loader.load( 'buildings/a5.gltf', function ( gltf ) {
            
            for (let row = 0; row < numRows; row++) {
                for (let col = 0; col < numCols; col++) {

                    if ([row,col] in city_definition){
                        const model = gltf.scene.clone();

                        let x = row * horizontal_distance;
                        let z = col * vertical_distance;

                        if (row % 2 !== 0) {
                            z += vertical_offset;
                        }

                        const hexagon = createHexagon(hex_size, model, city_definition[[row, col]])
                        hexagon.position.set(x, 0, z);
                        city.add(hexagon)
                    }
                    
                }
            }

        }, undefined, function ( error ) {
        console.error( error );
    } );

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
    model.scale.set(50, 50, 50);

    let material = null;
    switch (color) {
        case "RED":
            material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
            break;
        case "GREEN":
            material = new THREE.MeshStandardMaterial({ color: 0x143c14 });
            break;
        case "BLUE":
            material = new THREE.MeshStandardMaterial({ color: 0x0000ff });
            break;
        case "YELLOW":
            material = new THREE.MeshStandardMaterial({ color: 0xffff00 });
            break;
        case "ORANGE":
            material = new THREE.MeshStandardMaterial({ color: 0xff7d00 });
            break;
        case "BROWN":
            material = new THREE.MeshStandardMaterial({ color: 0x50281e });
            break;
        case "WHITE":
            material = new THREE.MeshStandardMaterial({ color: 0xffffff });
            break;
        default:
            material = new THREE.MeshStandardMaterial({ color: 0x000000 });
            break;
    }

    model.traverse((child) => {
        if (child.isMesh) {
            child.material = material;
        }
    });

    hexagon.add(model)

    return hexagon;
}


// import * as THREE from 'three';
// import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
// import { createHexagonPlatform } from './hexagon';

// function loadBuilding(path) {
//     const loader = new GLTFLoader();
//     loader.load( path, function ( gltf ) {
//         const model = gltf.scene;
//         return model
//     }, undefined, function ( error ) {
//         console.error( error );
//     } );
// }

// export function createCity(scene) {
//     const city = new THREE.Group();
    
//     // Create Platform
//     const platform = createHexagonPlatform();
//     // const platformGeometry = createHexagonPlatform()
//     // // const platformGeometry = new THREE.BoxGeometry(100, 1, 60);
//     // const platformMaterial = new THREE.MeshStandardMaterial({ color: 0x888888 });
//     // const platform = new THREE.Mesh(platformGeometry, platformMaterial);
//     city.add(platform)
//     // scene.add(platform);

//     const buildingModel = loadBuilding('buildings/building_02/scene.gltf');

//     // Create Buildings
//     // const cubeGeometry = new THREE.BoxGeometry(0.8, 4, 0.8);
//     // const cubeMaterial = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
    
//     // const rows = 10;
//     // const cols = 15;
//     // const spacing = 5; // Spacing between cubes
    
//     // const loader = new GLTFLoader();
//     // loader.load( 'buildings/a5.gltf', function ( gltf ) {
//     //     for (let row = 0; row < rows; row++) {
//     //         for (let col = 0; col < cols; col++) {
//     //             const model = gltf.scene.clone();
//     //             model.scale.set(50, 50, 50);

//     //             const blueMaterial = new THREE.MeshStandardMaterial({ color: 0x0000ff });
//     //             model.traverse((child) => {
//     //                 if (child.isMesh) {
//     //                   child.material = blueMaterial;
//     //                 }
//     //               });
    
//     //             model.position.set(
//     //                 col * spacing - (cols * spacing) / 2, 
//     //                 0.3,
//     //                 row * spacing - (rows * spacing) / 2);
                
//     //             city.add(model)
    
//     //             // // const building = new THREE.Mesh(cubeGeometry, cubeMaterial);
//     //             // cube.position.set(
//     //             //     col * spacing - (cols * spacing) / 2, 
//     //             //     2.5,
//     //             //     row * spacing - (rows * spacing) / 2);
//     //             // city.add(cube)
//     //             // // scene.add(cube);
//     //         }
//     //     }

//     // }, undefined, function ( error ) {
//     //     console.error( error );
//     // } );

    
//     scene.add(city)
//     return city
// }
