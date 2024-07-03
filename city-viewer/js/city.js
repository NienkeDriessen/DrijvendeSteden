import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

function loadBuilding(path) {
    const loader = new GLTFLoader();
    loader.load( path, function ( gltf ) {
        const model = gltf.scene;
        return model
    }, undefined, function ( error ) {
        console.error( error );
    } );
}

export function createCity(scene) {
    const city = new THREE.Group();

    // Create Platform
    const platformGeometry = new THREE.BoxGeometry(100, 1, 60);
    const platformMaterial = new THREE.MeshStandardMaterial({ color: 0x888888 });
    const platform = new THREE.Mesh(platformGeometry, platformMaterial);
    city.add(platform)
    // scene.add(platform);



    const buildingModel = loadBuilding('buildings/building_02/scene.gltf');

    // Create Buildings
    // const cubeGeometry = new THREE.BoxGeometry(0.8, 4, 0.8);
    // const cubeMaterial = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
    
    const rows = 10;
    const cols = 15;
    const spacing = 5; // Spacing between cubes
    
    const loader = new GLTFLoader();
    loader.load( 'buildings/a5.gltf', function ( gltf ) {
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const model = gltf.scene.clone();
                model.scale.set(50, 50, 50);

                const blueMaterial = new THREE.MeshStandardMaterial({ color: 0x0000ff });
                model.traverse((child) => {
                    if (child.isMesh) {
                      child.material = blueMaterial;
                    }
                  });
    
                model.position.set(
                    col * spacing - (cols * spacing) / 2, 
                    0.3,
                    row * spacing - (rows * spacing) / 2);
                
                city.add(model)
    
                // // const building = new THREE.Mesh(cubeGeometry, cubeMaterial);
                // cube.position.set(
                //     col * spacing - (cols * spacing) / 2, 
                //     2.5,
                //     row * spacing - (rows * spacing) / 2);
                // city.add(cube)
                // // scene.add(cube);
            }
        }



        
    }, undefined, function ( error ) {
        console.error( error );
    } );

    
    scene.add(city)
    return city
}
