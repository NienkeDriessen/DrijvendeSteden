import * as THREE from 'three';

export function createSun(parameters, sky, water, pmremGenerator, sceneEnv) {
    const sun = new THREE.Vector3();

    function updateSun() {
        const phi = THREE.MathUtils.degToRad(90 - parameters.elevation);
        const theta = THREE.MathUtils.degToRad(parameters.azimuth);

        sun.setFromSphericalCoords(1, phi, theta);

        sky.material.uniforms['sunPosition'].value.copy(sun);
        water.material.uniforms['sunDirection'].value.copy(sun).normalize();

        if (renderTarget !== undefined) renderTarget.dispose();

        sceneEnv.add(sky);
        renderTarget = pmremGenerator.fromScene(sceneEnv);
        sceneEnv.remove(sky); // Remove sky from the scene after generating the environment map
        scene.environment = renderTarget.texture;
    }

    updateSun();
}