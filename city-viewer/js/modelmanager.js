import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export class ModelManager {
    constructor() {
        this.models = {};
        this.loader = new GLTFLoader();
        this.colors = ["BLUE", "BROWN", "GREEN", "ORANGE", "RED", "WHITE", "YELLOW"]
    }

    async loadModels() {
        for (const color of this.colors) {
            const gltf = await this.loadModel(color);
            const model = gltf.scene;
            this.setModelProperties(model, color)
            this.models[color] = model;
        }
    }

    async loadModel(color) {
        return new Promise((resolve, reject) => {
            this.loader.load(`buildings/${color}.gltf`, data => resolve(data), null, reject)
        });
    }

    getModel(color) {
        return this.models[color].clone();
    }

    setModelProperties(model, color) {
        switch (color) {
            case "RED":
                this.configRed(model)
                break;
            case "GREEN":
                this.configGreen(model)
                break;
            case "BLUE":
                this.configBlue(model)
                break;
            case "YELLOW":
                this.configYellow(model)
                break;
            case "ORANGE":
                this.configOrange(model)
                break;
            case "BROWN":
                this.configBrown(model)
                break;
            case "WHITE":
                this.configWhite(model)
                break;
            default:
                break;
        }
    }

    setMaterial(model, material) {
        model.traverse((child) => {
            if (child.isMesh) {
                child.material = material;
            }
        });
    }

    configRed(model) {
        const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
        this.setMaterial(model, material)

        model.scale.set(100, 100, 100);

        model.position.y += 0.19
    }

    configGreen(model) {
        const material = new THREE.MeshStandardMaterial({ color: 0x1a8f35 });
        this.setMaterial(model, material)

        model.scale.set(100, 100, 100);

        model.position.y += 0.85
    }

    configBlue(model) {
        const material = new THREE.MeshStandardMaterial({ color: 0x4287f5 });
        this.setMaterial(model, material)

        model.scale.set(100, 100, 100);

        model.position.y += 0.19
    }

    configYellow(model) {
        const material = new THREE.MeshStandardMaterial({ color: 0xffff00 });
        this.setMaterial(model, material)

        model.scale.set(100, 100, 100);

        model.position.y += 0.19
    }

    configOrange(model) {
        const material = new THREE.MeshStandardMaterial({ color: 0xff7d00 });
        this.setMaterial(model, material)

        model.scale.set(75, 75, 75);

        model.position.y += 0.3
    }

    configBrown(model) {
        const material = new THREE.MeshStandardMaterial({ color: 0x7b3f00 });
        this.setMaterial(model, material)

        model.scale.set(125, 125, 125);

        model.position.y += 0.1
    }

    configWhite(model) {
        const material = new THREE.MeshStandardMaterial({ color: 0xffffff });
        this.setMaterial(model, material)

        model.scale.set(75, 75, 75);

        model.position.y += 0.5
    }




}

