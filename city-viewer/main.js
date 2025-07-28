import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { createOcean } from './js/ocean';
import { createSky } from './js/sky';
import { createSun } from './js/sun';
import { createCity } from './js/city';
import { getCityIDs } from './js/util';

let scene, camera, renderer, controls, water, sky, city;

function getCurrentCityId() {
  return window.location.hash ? window.location.hash.slice(1) : '1';
}

function setCityTitle(cityId, cities) {
  console.log("CITY LIST = ", cities, " and city id = ", cityId)
  const city = cities.find(c => c.id === cityId);
  const titleEl = document.getElementById('cityNameTitle');
  titleEl.textContent = cities[cityId].name;
}

async function initScene() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.25;
  controls.minDistance = 20;
  controls.maxDistance = 160;
  controls.maxPolarAngle = Math.PI / 2 - 0.2;
  controls.target.set(40, 0, 40);
  camera.position.set(0, 120, 150);

  water = createOcean(scene);
  sky = createSky(scene);
  createSun(scene, renderer, sky, water);
  city = await createCity(scene);

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  animate();
}

function animate() {
  requestAnimationFrame(animate);
  if (water?.material?.uniforms?.time) {
    water.material.uniforms.time.value += 1 / 180;
  }
  if (city) {
    city.position.y = Math.sin(performance.now() * 0.001) * 0.3;
  }
  controls.update();
  renderer.render(scene, camera);
}

function createCityButton(city, index) {
  const button = document.createElement('div');
  button.className = 'city_button';
  button.innerHTML = `
    <div class="city_layout">
      <div class="city_number">${index + 1}</div>
      <div class="city_info">
        <div class="city_name">${city.name}</div>
        <div class="city_date">${new Date(city.upload_date).toLocaleDateString()}</div>
      </div>
    </div>
  `;
  button.onclick = () => {
    window.location.hash = `#${city.id -1}`;
    updateUI(); 
    //HERE THE CITY ONLY CHANGES IF I DO RELOAD? 
    // location.reload();
  };
  return button;
}

async function populateMenuButtons(cities) {
  const container = document.querySelector('.container');
  container.innerHTML = '';
  cities.forEach((city, index) => {
    const btn = createCityButton(city, index);
    container.appendChild(btn);
  });
}

function setupMenuToggle() {
  document.getElementById('menuIcon').addEventListener('click', () => {
    document.getElementById('menuOverlay').classList.toggle('active');
  });
}

async function updateUI() {
  const cities = await getCityIDs();
  const currentId = getCurrentCityId();
  setCityTitle(currentId, cities);
  populateMenuButtons(cities);

  // Don't update city if scene isn't ready yet
  if (!scene) {
    console.warn("Scene not initialized yet, skipping city update.");
    return;
  }

  // Remove existing city from scene
  if (city) {
    scene.remove(city);
    city.traverse(child => {
      if (child.geometry) child.geometry.dispose();
      if (child.material) {
        if (Array.isArray(child.material)) {
          child.material.forEach(m => m.dispose());
        } else {
          child.material.dispose();
        }
      }
    });
  } else {
    console.log("city is undefined?")
  }

  // Add new city to scene
  city = await createCity(scene);
}

async function main() {
  setupMenuToggle();
  await updateUI();
  await initScene();
  // window.addEventListener('hashchange', updateUI);
}

main();
