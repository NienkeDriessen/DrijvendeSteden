import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { createOcean } from './js/ocean';
import { createSky } from './js/sky';
import { createSun } from './js/sun';
import { createCity } from './js/city';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

camera.position.set(0, 50, 80);
const controls = createControls()

// Create environment
const water = createOcean(scene)
const sky = createSky(scene)
createSun(scene, renderer, sky, water)

// Create city
const city = createCity(scene)

function createControls() {
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    controls.screenSpacePanning = false;
    controls.minDistance = 20;
    controls.maxDistance = 80;
    controls.maxPolarAngle = (Math.PI / 2) - 0.2;
    
    return controls
}

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

function animateCity() {
    const time = performance.now() * 0.001;
    city.position.y = Math.sin( time ) * 0.3;
}

function animate() {
    water.material.uniforms[ 'time' ].value += 1.0 / 180.0;
    animateCity()
    controls.update();

    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

animate();