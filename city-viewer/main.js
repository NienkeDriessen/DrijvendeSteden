import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { createOcean } from './js/ocean';
import { createSky } from './js/sky';
import { createSun } from './js/sun';
import { createCity } from './js/city';
import { getCityIDs } from './js/util';

let scene, camera, renderer, controls, water, sky, city; // Declare variables

async function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 1000 );

    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );


    controls = createControls()
    
    controls.target.set(40,0,40)
    camera.position.set(0, 120, 150);


    // Create environment
    water = createOcean(scene)
    sky = createSky(scene)
    createSun(scene, renderer, sky, water)

    // Create city
    city = await createCity(scene)

    function createControls() {
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.25;
        controls.screenSpacePanning = false;
        controls.minDistance = 20;
        controls.maxDistance = 160;
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
        if (water && water.material && water.material.uniforms && water.material.uniforms['time']) {
            water.material.uniforms['time'].value += 1.0 / 180.0;
        }
        if (city) {
            animateCity()
        }
        if (controls) {
            controls.update();
        }

        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }

    animate();
}

async function populateCitySelector() {
    const cityIDs = await getCityIDs();
    const citySelector = document.getElementById('citySelector');

    cityIDs.forEach(id => {
        const option = document.createElement('option');
        option.value = id;
        option.textContent = `City ID: ${id}`;
        citySelector.appendChild(option);
    });

    citySelector.addEventListener('change', () => {
        window.location.hash = citySelector.value;
        // Reload the scene when a new city is selected
        location.reload();
    });

    // Set initial city ID from URL hash
    if (window.location.hash) {
        citySelector.value = window.location.hash.slice(1);
    }

    // Initialize the scene after populating the selector
    await init();
}

populateCitySelector();