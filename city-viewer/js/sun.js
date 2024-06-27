import * as THREE from 'three';

export function createSun(scene, renderer, sky, water) {
    const parameters = {
        elevation: 2,
        azimuth: 180
    };
    
    const pmremGenerator = new THREE.PMREMGenerator( renderer );
    const sceneEnv = new THREE.Scene();
    
    let renderTarget;    
    const sun = new THREE.Vector3();

function updateSun() {
    const phi = THREE.MathUtils.degToRad( 90 - parameters.elevation );
    const theta = THREE.MathUtils.degToRad( parameters.azimuth );

    sun.setFromSphericalCoords( 1, phi, theta );

    sky.material.uniforms[ 'sunPosition' ].value.copy( sun );
    water.material.uniforms[ 'sunDirection' ].value.copy( sun ).normalize();

    if ( renderTarget !== undefined ) renderTarget.dispose();

    sceneEnv.add( sky );
    renderTarget = pmremGenerator.fromScene( sceneEnv );
    scene.add( sky );

    scene.environment = renderTarget.texture;
}
    updateSun();
}